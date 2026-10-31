# T35 authoring task T35-author_freeform-355d7a26-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_freeform-355d7a26-000.json

Task kind: author_freeform; items: 16; outputs expected: 16.

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
  "qid": "q377aa7b90f",
  "brief": "a casual message with a light touch of humour",
  "register": "transcript",
  "facts": {
   "SITE": "Harbor Lantern Books",
   "OPERATOR": "Pellucid Archive",
   "PURPOSE": "accessibility checks"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q0b40c50748",
  "brief": "a summary written by a data team lead",
  "register": "wiki",
  "facts": {
   "SITE": "Fennel Row Nursery",
   "OPERATOR": "Saltmarsh Research",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q5bc7f40e27",
  "brief": "a crawl engineer's routine work note",
  "register": "transcript",
  "facts": {
   "SITE": "Eastmere City Portal",
   "OPERATOR": "Pellucid Archive",
   "PURPOSE": "link checking"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q40523626d5",
  "brief": "a note that thanks the website's web team",
  "register": "wiki",
  "facts": {
   "SITE": "Harrowgate Cycles",
   "OPERATOR": "Corvid Analytics",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q8632ad1259",
  "brief": "a very short summary",
  "register": "transcript",
  "facts": {
   "SITE": "Pinecrest Boards",
   "OPERATOR": "Brightloom Prices",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qbf17c1ebd1",
  "brief": "a neutral, impersonal summary",
  "register": "transcript",
  "facts": {
   "SITE": "Larkspur Gardens",
   "OPERATOR": "Fernhill Labs",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qd372943580",
  "brief": "a message from the operator's partnerships desk",
  "register": "wiki",
  "facts": {
   "SITE": "Riverlight Forum",
   "OPERATOR": "Ostrander Data",
   "PURPOSE": "price comparison"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q7069496171",
  "brief": "a short update for a project channel",
  "register": "transcript",
  "facts": {
   "SITE": "Ridgeway Herald",
   "OPERATOR": "Fernhill Labs",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q7333c7c01b",
  "brief": "a site administrator noting an incoming crawler",
  "register": "wiki",
  "facts": {
   "SITE": "Westerby Art House",
   "OPERATOR": "Kestrel Links",
   "PURPOSE": "academic research"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q3e511104b1",
  "brief": "a support agent summarising who is asking and why",
  "register": "transcript",
  "facts": {
   "SITE": "Copperbeech Growers",
   "OPERATOR": "Maplewick Search",
   "PURPOSE": "link previews"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q7323779c49",
  "brief": "a note that names the website before anything else",
  "register": "wiki",
  "facts": {
   "SITE": "Millbrook Ledger",
   "OPERATOR": "Corvid Analytics",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qffaa16f9ad",
  "brief": "a note from the web team of the website being visited",
  "register": "transcript",
  "facts": {
   "SITE": "Gallowhill Museum",
   "OPERATOR": "Maplewick Search",
   "PURPOSE": "academic research"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q29fd89e7dd",
  "brief": "a note written from the crawler operator's point of view",
  "register": "wiki",
  "facts": {
   "SITE": "Ashgrove Booksellers",
   "OPERATOR": "Ostrander Data",
   "PURPOSE": "accessibility checks"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q03739a9b41",
  "brief": "a formal, polite note",
  "register": "wiki",
  "facts": {
   "SITE": "Oatfield Table",
   "OPERATOR": "Kestrel Links",
   "PURPOSE": "link checking"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "q6b8c1a2273",
  "brief": "a terse note from a busy crawl operator",
  "register": "wiki",
  "facts": {
   "SITE": "Brambleworth Kitchen",
   "OPERATOR": "Saltmarsh Research",
   "PURPOSE": "search indexing"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 },
 {
  "qid": "qcbd86a0e67",
  "brief": "a note that names the crawl purpose before anything else",
  "register": "transcript",
  "facts": {
   "SITE": "Larchmont Civic Office",
   "OPERATOR": "Brightloom Prices",
   "PURPOSE": "web archiving"
  },
  "rules": [
   "exactly one document",
   "each fact value exactly once, verbatim"
  ]
 }
]
