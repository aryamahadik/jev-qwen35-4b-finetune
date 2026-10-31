# T35 authoring task T35-author_freeform-19448c45-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_freeform-19448c45-000.json

Task kind: author_freeform; items: 24; outputs expected: 24.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write FREE-FORM NARRATIVES. Each item gives three facts: SITE (the name of a website), OPERATOR (the
organisation that runs a web crawler) and PURPOSE (what the crawler collects pages for). Write one short document in
the item's register that says who runs the crawler, what it collects pages for and which website it is about to
visit, and nothing more. A program later prints the website's crawl file, the request and the rules elsewhere on the
page, and may swap the three values for others: describe the website only by its name.

Hard rules (a document that breaks one is thrown away):
1. At most 60 words. Use each of the three fact values exactly once, copied verbatim (same spelling,
   capitals and spaces); never shorten, inflect or repeat them.
2. Outside the three values: no digits, number words or ordinals, no dates, times, months or weekdays, no currency or
   percent signs, no web addresses, e-mail addresses, domains or slashes, no codes that mix letters and digits.
3. No other names: no people, places, brands or products; a capital letter only at the start of a sentence, line or
   label (and in the word "URL").
4. No negation of any kind: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, refuse to, decline to, prevent ... from, rule out.
5. Say nothing about what the crawler gets to do: no word about access, permission, refusal, rules, robots files, crawl settings, status codes, errors, paths, sections or web addresses, and no hint about any outcome; no word that says whether something is let through or kept out.
6. No placeholders and no curly braces: the values are written out.
7. Avoid modal, hedge and quantity words: may, might, must, can, could, should, will, would, need, maybe, perhaps,
   probably, likely, seems, all, every, each, some, any, only, many, more, most.
Registers: email = a short e-mail: a greeting line, a few sentences and a sign-off line (no personal names); memo = an internal memo or work note in plain prose; chat = a chat message that starts with a speaker label such as 'crawl team:'; ticket = a work ticket with short labelled fields; faq = an FAQ-style entry: a 'Q:' line about the situation and an 'A:' line that answers it; pr_review = a code-review comment on a change to a crawler's configuration; transcript = a short call transcript: a few lines with speaker labels such as 'Caller:' and 'Agent:'; wiki = a wiki page snippet: a title line and a sentence or two.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the document>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qcc271f1ff8",
  "brief": "a note that names the crawl purpose before anything else",
  "register": "faq",
  "facts": {
   "SITE": "Pinecrest Boards",
   "OPERATOR": "Brightloom Prices",
   "PURPOSE": "accessibility checks"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q6fe38574ff",
  "brief": "a note written for a shared crawl queue",
  "register": "email",
  "facts": {
   "SITE": "Gallowhill Museum",
   "OPERATOR": "Maplewick Search",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qab6f656ef2",
  "brief": "a site administrator noting an incoming crawler",
  "register": "memo",
  "facts": {
   "SITE": "Millbrook Ledger",
   "OPERATOR": "Corvid Analytics",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qa6e7396b4c",
  "brief": "a handoff note between crawl team shifts",
  "register": "memo",
  "facts": {
   "SITE": "Fennel Row Nursery",
   "OPERATOR": "Saltmarsh Research",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q295a6beb19",
  "brief": "a structured note with labelled parts",
  "register": "pr_review",
  "facts": {
   "SITE": "Oatfield Table",
   "OPERATOR": "Kestrel Links",
   "PURPOSE": "academic research"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qbbee2b3367",
  "brief": "a summary written by a data team lead",
  "register": "ticket",
  "facts": {
   "SITE": "Brambleworth Kitchen",
   "OPERATOR": "Saltmarsh Research",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q39852e3dd0",
  "brief": "a formal, polite note",
  "register": "memo",
  "facts": {
   "SITE": "Westerby Art House",
   "OPERATOR": "Kestrel Links",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q1167205b86",
  "brief": "a support agent summarising who is asking and why",
  "register": "chat",
  "facts": {
   "SITE": "Larchmont Civic Office",
   "OPERATOR": "Brightloom Prices",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q504ffdf117",
  "brief": "a terse note from a busy crawl operator",
  "register": "ticket",
  "facts": {
   "SITE": "Riverlight Forum",
   "OPERATOR": "Ostrander Data",
   "PURPOSE": "accessibility checks"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q84e064f79c",
  "brief": "a friendly message that opens with a greeting",
  "register": "faq",
  "facts": {
   "SITE": "Harbor Lantern Books",
   "OPERATOR": "Pellucid Archive",
   "PURPOSE": "link checking"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qa8847ff4d1",
  "brief": "a message from the operator's partnerships desk",
  "register": "pr_review",
  "facts": {
   "SITE": "Ashgrove Booksellers",
   "OPERATOR": "Ostrander Data",
   "PURPOSE": "link checking"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qad9c5f205c",
  "brief": "a crawl engineer's routine work note",
  "register": "email",
  "facts": {
   "SITE": "Larkspur Gardens",
   "OPERATOR": "Fernhill Labs",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qcfb29994b2",
  "brief": "a site administrator noting an incoming crawler",
  "register": "ticket",
  "facts": {
   "SITE": "Quillmere Books",
   "OPERATOR": "Kestrel Links",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qb744aa2f58",
  "brief": "a support agent summarising who is asking and why",
  "register": "faq",
  "facts": {
   "SITE": "Saffron Lane Recipes",
   "OPERATOR": "Maplewick Search",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qcefc230fcf",
  "brief": "a terse note from a busy crawl operator",
  "register": "pr_review",
  "facts": {
   "SITE": "Fellside Wheels",
   "OPERATOR": "Saltmarsh Research",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q8123ac5890",
  "brief": "a note written from the crawler operator's point of view",
  "register": "memo",
  "facts": {
   "SITE": "Kingsford Town Hall",
   "OPERATOR": "Ostrander Data",
   "PURPOSE": "academic research"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q748b9b3a65",
  "brief": "a neutral, impersonal summary",
  "register": "chat",
  "facts": {
   "SITE": "Ridgeway Herald",
   "OPERATOR": "Fernhill Labs",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qa468cad2f1",
  "brief": "a crawl engineer's routine work note",
  "register": "chat",
  "facts": {
   "SITE": "Cobblestone Heritage Trust",
   "OPERATOR": "Pellucid Archive",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qbe9547e712",
  "brief": "a short update for a project channel",
  "register": "faq",
  "facts": {
   "SITE": "Spokewright Bikes",
   "OPERATOR": "Fernhill Labs",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q14b5a70c16",
  "brief": "a note that names the website before anything else",
  "register": "ticket",
  "facts": {
   "SITE": "Harrowgate Cycles",
   "OPERATOR": "Corvid Analytics",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qf331e2dbae",
  "brief": "a note from the web team of the website being visited",
  "register": "chat",
  "facts": {
   "SITE": "Copperbeech Growers",
   "OPERATOR": "Maplewick Search",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qa1b6a0a98f",
  "brief": "a note that thanks the website's web team",
  "register": "pr_review",
  "facts": {
   "SITE": "Lowmoor Community",
   "OPERATOR": "Corvid Analytics",
   "PURPOSE": "accessibility checks"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qd5bf19e289",
  "brief": "a casual message with a light touch of humour",
  "register": "email",
  "facts": {
   "SITE": "Eastmere City Portal",
   "OPERATOR": "Pellucid Archive",
   "PURPOSE": "academic research"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q1d4bf7f066",
  "brief": "a very short summary",
  "register": "email",
  "facts": {
   "SITE": "Tidewater Courier",
   "OPERATOR": "Brightloom Prices",
   "PURPOSE": "link checking"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 }
]
