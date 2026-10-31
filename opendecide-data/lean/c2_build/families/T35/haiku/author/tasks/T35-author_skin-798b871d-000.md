# T35 authoring task T35-author_skin-798b871d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_skin-798b871d-000.json

Task kind: author_skin; items: 4; outputs expected: 24.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE TEMPLATES in the register "transcript": a short call or meeting transcript: two to four lines, each starting with a speaker label such as 'Caller:' and 'Agent:' or 'Crawl lead:' and 'Web admin:'.
A narrative only says which organisation runs a web crawler, what the crawler collects pages for and which website it
is about to visit. Elsewhere on the page a program prints the website's crawl file, the crawler's request and the rules
for reading them; your text must add no fact of its own and must give no hint about what those rules decide.
Example of the register (do not copy it): Caller: this is {OPERATOR}, calling about our crawler.\nAgent: which website is it about?\nCaller: {SITE}. We crawl it for {PURPOSE}.

Placeholders: each item lists the placeholders ("slots") to use. Use every listed placeholder EXACTLY ONCE, spelled
exactly as given with its curly braces (e.g. {SITE}), and never use any other placeholder or write a real value in
its place. A placeholder is a whole name or phrase: never add a word that changes it (no "the" before {SITE} unless
the sentence still reads well with any website name).

Hard rules (a text that breaks one is thrown away):
1. One block of text of at most 40 words (a placeholder counts as one word): no empty line, no leading or
   trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no currency
   or percent signs, no web addresses, e-mail addresses, domains, file names or slashes, no codes that mix letters and
   digits.
4. Outside the placeholders, none of these words (any letter case):
- number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal: able, can, cannot, could, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, prohibited, required, shall, should, shouldn, unable, will, would
- hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status: accept, accepted, active, approval, approve, approved, authorised, authorized, block, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- phrases: have to, has to, had to, got to, sort of, kind of
5. No negation of any kind: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, refuse to, decline to, prevent ... from, rule out.
6. No names: a capital letter only on the first word of a sentence, line, list item or label (the word "URL" may be
   capitalised anywhere). Names come only through the placeholders.
7. Say nothing about what the crawler gets to do: no word about access, permission, refusal, rules, robots files, crawl settings, status codes, errors, paths, sections or web addresses, and no hint about any outcome.
8. Vary the wording, the sentence structure and the order of the placeholders across all your texts.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q53249e9525",
  "brief": "a note that names the website before anything else; write 6 different texts",
  "register": "transcript",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'",
   "PURPOSE": "what the crawler collects pages for, a short lowercase noun phrase that reads well after 'for', such as 'search indexing', 'web archiving', 'price comparison', 'accessibility checks'",
   "UA": "the crawler's product token, a single CamelCase word such as 'MaplewickBot'"
  },
  "rules": [
   "write 6 different texts",
   "use {SITE}, {OPERATOR}, {PURPOSE}, {UA} each exactly once"
  ]
 },
 {
  "qid": "qcc8a4c558a",
  "brief": "a terse note from a busy crawl operator; write 6 different texts",
  "register": "transcript",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'",
   "PURPOSE": "what the crawler collects pages for, a short lowercase noun phrase that reads well after 'for', such as 'search indexing', 'web archiving', 'price comparison', 'accessibility checks'",
   "UA": "the crawler's product token, a single CamelCase word such as 'MaplewickBot'"
  },
  "rules": [
   "write 6 different texts",
   "use {SITE}, {OPERATOR}, {PURPOSE}, {UA} each exactly once"
  ]
 },
 {
  "qid": "qca0d47b3fc",
  "brief": "a note written for a shared crawl queue; write 6 different texts",
  "register": "transcript",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'",
   "PURPOSE": "what the crawler collects pages for, a short lowercase noun phrase that reads well after 'for', such as 'search indexing', 'web archiving', 'price comparison', 'accessibility checks'"
  },
  "rules": [
   "write 6 different texts",
   "use {SITE}, {OPERATOR}, {PURPOSE} each exactly once",
   "no {UA} placeholder"
  ]
 },
 {
  "qid": "q5dff56bda6",
  "brief": "a crawl engineer's routine work note; write 6 different texts",
  "register": "transcript",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'",
   "PURPOSE": "what the crawler collects pages for, a short lowercase noun phrase that reads well after 'for', such as 'search indexing', 'web archiving', 'price comparison', 'accessibility checks'"
  },
  "rules": [
   "write 6 different texts",
   "use {SITE}, {OPERATOR}, {PURPOSE} each exactly once",
   "no {UA} placeholder"
  ]
 }
]
