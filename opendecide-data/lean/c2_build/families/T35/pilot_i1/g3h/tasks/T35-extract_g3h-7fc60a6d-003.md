# G3-H extraction T35-extract_g3h-7fc60a6d-003 (family T35)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/pilot_i1/g3h/answers/T35-extract_g3h-7fc60a6d-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 14. Answers expected: 14 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "operator": <value or null>, "purpose": <value or null>, "site": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qeec02319d6",
  "text": "Review comment:\nThis setup change covers a crawler run by Aldergrove Catalogue, which collects pages for web archiving. It is about to visit Oatfield Table. Thanks to the web team for their help.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q7f162491f1",
  "text": "Q: Why is this crawler arriving, and who runs it?\nA: Wenlock Shelf runs it to collect pages for search indexing. Our web team has been told it is about to visit Quillbright Tutors.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "qa2e5ea3c8d",
  "text": "Ops feed: Ruddock Metrics operates a crawler that collects pages for academic research. The crawler is about to visit Ridgeway Herald. Logged for reference.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "qff263715ee",
  "text": "Thanks to the web team for their patience. Greywater Vault runs a crawler that collects pages for accessibility checks, and it is about to visit Ridgeholm Trail Society.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q7e9f424f64",
  "text": "Hello team,\nEllery Contrast runs a crawler that collects pages for academic research, and it is about to visit Quillmere Books.\nThanks,\nCrawl team",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q57b9fc8509",
  "text": "Crawl engineer: routine work, as usual. Halvorsen Watch runs the crawler, which collects pages for academic research, and it is about to visit Caldermere Theatre Company.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q593f856083",
  "text": "Q: Why is a crawler collecting pages for price comparison?\nA: Kestrel Panel runs that crawler, and it is about to visit Lensgrade Science Hour.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q7ca3049b15",
  "text": "Q: What is this routine crawl about, and who runs it?\nA: Gantry Relay runs the crawler, which collects pages for web archiving. It is about to visit Saltcliff Guest House.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q50e460e70c",
  "text": "Hey team,\nEllery Contrast has a crawler with a real taste for tea breaks, and it is off to visit Spinewell Craft Bindery. Its whole job is to collect pages for search indexing, which is a very cozy task.\nCheers,\nCrawl team",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q1e58e7bd8f",
  "text": "Handoff for the crawl team.\nKestrel Panel runs the crawler that is about to visit Rookdale Chess Club. It collects pages for link previews. Please pick up from here and reply on this thread with questions.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q731e3f1d39",
  "text": "Q: Who is behind the crawler visiting Barometer Hill Notes, and what is it for?\nA: Longhaven Trust runs it, and it collects pages for accessibility checks.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "q2a96729eb1",
  "text": "Q: Why is this crawler arriving, and who runs it?\nA: Brightloom Prices runs it to collect pages for link checking. Our web team has been told it is about to visit Greywheel Pottery Depot.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "qd8bae8c7c4",
  "text": "Internal note for the operations desk.\nA crawler run by Silverlace Feed is about to visit Whistlewood Botanical Gardens. It collects pages for link previews. Please share this note with the people on the desk.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 },
 {
  "qid": "qe9e3718bac",
  "text": "Summary for the review: Quarry Hollow runs the crawler that collects pages for link checking. It is about to visit Sablecorner Print Studio, and the change to its code reads well to us.",
  "schema": [
   {
    "field": "site",
    "type": "name",
    "describe": "the website the crawler wants to visit, as written"
   },
   {
    "field": "operator",
    "type": "name",
    "describe": "the organisation that runs the crawler, as written"
   },
   {
    "field": "purpose",
    "type": "category",
    "describe": "what the crawler collects pages for",
    "choices": [
     "academic research",
     "accessibility checks",
     "link checking",
     "link previews",
     "price comparison",
     "search indexing",
     "web archiving"
    ]
   }
  ]
 }
]
