# Haiku authoring task T23-author_pack-bb2e38f6-003 (family T23, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T23/haiku/author/answers/T23-author_pack-bb2e38f6-003.json

The answer is one JSON list with exactly 10 objects, one per item below, each carrying that item's qid.

## Instructions

You invent "packs": the made-up setting of one everyday policy document of one invented organisation. A program later builds reading puzzles from your packs (it adds every date, number and rule itself); you never see the puzzles. Each item gives a domain, what value the document sets, the four dates a customer case has, and a setting. Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "doc": the document's name, 2-4 lower-case words (for example "returns policy", "leave policy").
- "term_label": the name of the one value the document sets, 2-5 lower-case words, fitting the kind of value the item names (for example "return window" for a number of days, "fee cap" for an amount of money).
- "qty_label": ONLY when the item says the case quantity is an input: its name, 2-6 lower-case words (for example "fee charged"). When the item says the program writes the quantity's label, write "" (an empty string).
- "date_labels": an object with the keys "purchase", "event", "filing" and "decision". Each value is a label of 2-4 lower-case words whose last word is "date" (for example "order date"), fitting the role the item describes. The four labels differ, none contains another, and none contains the word "to".
- "items": 5 different things or services a case can be about, 1-3 lower-case words each (for example "standing desk", "annual plan"); no brand names.
- "orgs": 3 invented organisation names, 2-3 capitalised words each (for example "Brightwell Supply"); never a real company, brand or famous name.
- "customers": 6 invented personal names "First Last", ordinary-sounding, never a famous person.
- "prefix": 2 capital letters for document codes (for example "RP").

Rules for every value: letters, spaces, hyphens and apostrophes only (no digits, no other symbols); no negative words (not, no, never, non, without, none, nothing, fail, lack); no words about time or change (new, old, latest, current, updated, effective). Names and labels must not reuse each other.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only.

## Answer format

[{"qid": "q...", "pack": {"doc": ..., "term_label": ..., "qty_label": ..., "date_labels": {"purchase": ..., "event": ..., "filing": ..., "decision": ...}, "items": [...], "orgs": [...], "customers": [...], "prefix": ...}}, ...]

## Items (10; one JSON object per line)

```json
[
{"qid": "q612266162f", "brief": "Domain: retention. Setting: a telecom support centre. The document sets one value per version: a number of days (example term label: \"retention period\"). The case quantity is a day count from the event-role date to the filing-role date; the program writes its label, so qty_label is \"\". Date roles (example labels, vary them): purchase = \"record creation date\", event = \"record closure date\", filing = \"deletion request date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "q9631cb16c1", "brief": "Domain: shipping. Setting: a garden centre that ships plants. The document sets one value per version: a number of days (example term label: \"delivery promise\"). The case quantity is a day count from the purchase-role date to the event-role date; the program writes its label, so qty_label is \"\". Date roles (example labels, vary them): purchase = \"order date\", event = \"delivery date\", filing = \"complaint date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "qc07b8bab16", "brief": "Domain: travel. Setting: a charity's field team. The document sets one value per version: an amount of money (example term label: \"nightly hotel cap\"). The case quantity is an input, an amount of money (example label: \"nightly rate claimed\"); write its qty_label. Date roles (example labels, vary them): purchase = \"booking date\", event = \"travel date\", filing = \"expense claim date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "q33b745ab83", "brief": "Domain: warranties. Setting: a bicycle and e-bike maker. The document sets one value per version: a number of days (example term label: \"warranty period\"). The case quantity is a day count from the purchase-role date to the event-role date; the program writes its label, so qty_label is \"\". Date roles (example labels, vary them): purchase = \"purchase date\", event = \"fault date\", filing = \"claim date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "qc06a598b65", "brief": "Domain: travel. Setting: a consulting firm's travel desk. The document sets one value per version: an amount of money (example term label: \"nightly hotel cap\"). The case quantity is an input, an amount of money (example label: \"nightly rate claimed\"); write its qty_label. Date roles (example labels, vary them): purchase = \"booking date\", event = \"travel date\", filing = \"expense claim date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "qa4c337bf4b", "brief": "Domain: pricing. Setting: a building materials yard. The document sets one value per version: an amount of money (example term label: \"price cap per unit\"). The case quantity is an input, an amount of money (example label: \"unit price charged\"); write its qty_label. Date roles (example labels, vary them): purchase = \"contract date\", event = \"delivery date\", filing = \"invoice date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "qabcbb6a8aa", "brief": "Domain: pricing. Setting: a school uniform supplier. The document sets one value per version: an amount of money (example term label: \"price cap per unit\"). The case quantity is an input, an amount of money (example label: \"unit price charged\"); write its qty_label. Date roles (example labels, vary them): purchase = \"contract date\", event = \"delivery date\", filing = \"invoice date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "q10be6dc330", "brief": "Domain: leave. Setting: a design studio. The document sets one value per version: a number of days (example term label: \"paid leave allowance\"). The case quantity is an input, a number of days (example label: \"number of leave days claimed\"); write its qty_label. Date roles (example labels, vary them): purchase = \"hire date\", event = \"leave start date\", filing = \"claim date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "qd9ccbc5fa7", "brief": "Domain: travel. Setting: a university research office. The document sets one value per version: an amount of money (example term label: \"nightly hotel cap\"). The case quantity is an input, an amount of money (example label: \"nightly rate claimed\"); write its qty_label. Date roles (example labels, vary them): purchase = \"booking date\", event = \"travel date\", filing = \"expense claim date\", decision = \"decision date\" (the day the organisation settles the case)."},
{"qid": "q0fe79c3819", "brief": "Domain: shipping. Setting: an online grocery store. The document sets one value per version: a number of days (example term label: \"delivery promise\"). The case quantity is a day count from the purchase-role date to the event-role date; the program writes its label, so qty_label is \"\". Date roles (example labels, vary them): purchase = \"order date\", event = \"delivery date\", filing = \"complaint date\", decision = \"decision date\" (the day the organisation settles the case)."}
]
```
