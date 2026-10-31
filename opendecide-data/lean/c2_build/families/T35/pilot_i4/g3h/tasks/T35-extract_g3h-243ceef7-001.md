# G3-H extraction T35-extract_g3h-243ceef7-001 (family T35)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/pilot_i4/g3h/answers/T35-extract_g3h-243ceef7-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "operator": <value or null>, "purpose": <value or null>, "site": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q6951f2b9f1",
  "text": "Quick heads up. Eastmarch Lab runs the crawler that collects pages for search indexing. It is about to visit Sablecorner Print Studio.",
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
  "qid": "q04794e5409",
  "text": "Handoff for the crawl team.\nSaltmarsh Research runs the crawler that is about to visit Larkstone Ramblers. It collects pages for web archiving. Please pick up from here and reply on this thread with questions.",
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
  "qid": "q035cd600e7",
  "text": "Q: What is new in the project channel?\nA: Ellery Contrast is sending a crawler that collects pages for link checking, and it is about to visit Redwater Clay Studio.",
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
  "qid": "qb263032fc8",
  "text": "Quillmere Books is at the top of this review comment. Jasper Snapwell runs the crawler that collects pages for price comparison, and it is about to visit it. The change reads well to us.",
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
  "qid": "q25822757fa",
  "text": "crawl team: Hi there! Zephyrine Bargain runs a crawler that collects pages for accessibility checks, and it is about to visit Lowmoor Community. Thanks a lot!",
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
  "qid": "q8c153bad7c",
  "text": "Crawl engineer: routine work, as usual. Ottoline Scriptorium runs the crawler, which collects pages for link previews, and it is about to visit Spindlewood Dance Academy.",
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
  "qid": "q14f4d33423",
  "text": "Hello,\nA quick summary of who is asking. Brindle Lantern runs a crawler that collects pages for web archiving. It is about to visit Wassailcourt Craft Cider, so we wanted to mention that.\nThanks,",
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
  "qid": "q19fc6c34ce",
  "text": "Handoff comment on the change: Ruddock Metrics runs the crawler that collects pages for accessibility checks, and it is about to visit Frostlight Ballet Hall. Please pick up the review from here.",
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
  "qid": "q000b3d1969",
  "text": "Hey team,\nKestrel Links has a crawler with a real taste for tea breaks, and it is off to visit Rushdale Playhouse. Its whole job is to collect pages for academic research, which is a very cozy task.\nCheers,\nCrawl team",
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
  "qid": "q98eb93d7f5",
  "text": "Q: Who is behind the crawler visiting Isobarlane Weather Log, and what is it for?\nA: Pellucid Archive runs it, and it collects pages for search indexing.",
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
  "qid": "qe3dd1d4716",
  "text": "Handoff for the crawl team.\nBrindle Lantern runs the crawler that is about to visit Lensgrade Science Hour. It collects pages for link previews. Please pick up from here and reply on this thread with questions.",
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
  "qid": "q067731b68b",
  "text": "Q: Who runs this crawler, and what is it collecting pages for?\nA: Pennyroyal Digest runs it. It collects pages for accessibility checks and is about to visit Hedgerow Wildlife Rescue.",
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
  "qid": "q91b3228b12",
  "text": "Notice for colleagues. Kindly be advised that Brisk Ledger operates a crawler that collects pages for accessibility checks. The crawler is respectfully about to visit Saltcliff Guest House. We are grateful for your attention to this notice.",
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
  "qid": "q9efd42f875",
  "text": "Quillmere Books is at the top of this review comment. Jasper Snapwell runs the crawler that collects pages for price comparison, and it is about to visit it. The change reads well to us.",
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
  "qid": "q3ca520eba9",
  "text": "Review comment:\nThis setup change covers a crawler run by Jasper Snapwell, which collects pages for link previews. It is about to visit Brindlegate Growers Market. Thanks to the web team for their help.",
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
  "qid": "qafd85ffc4c",
  "text": "Summary: incoming crawler notice.\nOperator: Brindle Lantern.\nPurpose: academic research.\nDetail: the crawler is about to visit Harrowgate Cycles, and this summary comes from the data team lead.",
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
  "qid": "q0f81ddcc40",
  "text": "Q: What is new in the project channel?\nA: Maplewick Search is sending a crawler that collects pages for link checking, and it is about to visit Quillmere Harvest Yard.",
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
  "qid": "qe4406947d8",
  "text": "Crawl engineer: routine work, as usual. Ottoline Scriptorium runs the crawler, which collects pages for link previews, and it is about to visit Spindlewood Dance Academy.",
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
  "qid": "q71446a0126",
  "text": "Support agent: Ottoline Scriptorium is behind this visit. Its crawler collects pages for link checking, and it is about to visit Wendle Vale Heritage Circle. That is the whole story from my side.",
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
  "qid": "q96bc538add",
  "text": "Q: Who runs this crawler, and what is it collecting pages for?\nA: Ruddock Metrics runs it. It collects pages for price comparison and is about to visit Tidewater Courier.",
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
  "qid": "q2c169bdeaa",
  "text": "Ticket: visit notice.\nRun by: Ellery Contrast.\nFor: accessibility checks.\nSite: Larchfold Outfitters.\nNote: short notice, crawler about to arrive.",
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
  "qid": "q5fe5ffacb2",
  "text": "Hello team,\nMarlowe Folio runs a crawler that collects pages for link checking, and it is about to visit Spokewright Bikes.\nThanks,\nCrawl team",
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
  "qid": "q7088403614",
  "text": "Q: What is new in the project channel?\nA: Maplewick Search is sending a crawler that collects pages for link checking, and it is about to visit Quillmere Harvest Yard.",
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
  "qid": "q997145a3c5",
  "text": "Internal note for the operations desk.\nA crawler run by Pennant Compare is about to visit Pawnhurst Chess Society. It collects pages for academic research. Please share this note with the people on the desk.",
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
  "qid": "qb2a6e651ab",
  "text": "Quick heads up. Eastmarch Lab runs the crawler that collects pages for search indexing. It is about to visit Sablecorner Print Studio.",
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
  "qid": "qefc1d945c8",
  "text": "Handoff comment on the change: Corrigan Pulse runs the crawler that collects pages for link previews, and it is about to visit Ashgrove Booksellers. Please pick up the review from here.",
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
  "qid": "qdf4241be86",
  "text": "Q: What is new in the project channel?\nA: Ellery Contrast is sending a crawler that collects pages for link checking, and it is about to visit Redwater Clay Studio.",
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
  "qid": "q8faf7a9150",
  "text": "Ticket: visit notice.\nRun by: Ellery Contrast.\nFor: accessibility checks.\nSite: Larchfold Outfitters.\nNote: short notice, crawler about to arrive.",
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
  "qid": "q9f51109b16",
  "text": "Quick heads up. Thornbeck Access runs the crawler that collects pages for web archiving. It is about to visit Quarkhollow Podcast.",
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
  "qid": "q3ffea6422c",
  "text": "Hello team,\nOstrander Data runs a crawler that collects pages for link checking, and it is about to visit Glenmere Community Radio. Routine work, as usual.\nThanks,\nCrawl engineering",
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
  "qid": "qe192b08c18",
  "text": "Review comment:\nThis setup change covers a crawler run by Quillbrook Audits, which collects pages for web archiving. It is about to visit Lowmoor Community. Thanks to the web team for their help.",
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
  "qid": "qb8fcde3597",
  "text": "Handoff for the crawl team.\nHalberd Analysis Group runs the crawler that is about to visit Gambit Corner Club. It collects pages for academic research. Please pick up from here and reply on this thread with questions.",
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
  "qid": "qb199cb7432",
  "text": "Review comment on this diff: Jasper Snapwell runs the crawler that collects pages for link checking, and it is about to visit Highmoor Walkers Club.\nThe change reads well to us. Please add a short comment on naming.",
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
  "qid": "q1a92a802fa",
  "text": "Hi there,\nHope things are going well on your side. Longhaven Trust runs a crawler that collects pages for search indexing, and it is about to visit Kilnharbour Ceramics Hall. Thanks for helping us keep track of this.\nWarm regards,",
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
  "qid": "q23c5737554",
  "text": "Handoff comment on the change: Ravensworth Monitor runs the crawler that collects pages for search indexing, and it is about to visit Pawnhurst Chess Society. Please pick up the review from here.",
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
  "qid": "q5450426a9a",
  "text": "Partnerships desk, review comment:\nThornbeck Access runs the crawler covered by this setup change, and it collects pages for accessibility checks. The crawler is about to visit Eastmere City Portal. Please reply on the thread with questions.",
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
  "qid": "q60aa52ab6b",
  "text": "Ticket: visit notice.\nRun by: Fernhill Labs.\nFor: accessibility checks.\nSite: Inkwell Poster Works.\nNote: short notice, crawler about to arrive.",
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
  "qid": "qbdcad7bec0",
  "text": "Ticket: crawl heads-up\nOperator: Jasper Snapwell\nPurpose: price comparison\nTarget: Quillmere Books\nType: planned visit",
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
  "qid": "q687efb612e",
  "text": "Memo: crawl operations\nWho: Pelham Insight runs the crawler.\nWhy: it collects pages for search indexing.\nWhat: it is about to visit Saffron Lane Recipes.",
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
  "qid": "qd935d8f760",
  "text": "Ticket: crawl visit planning\nOperator: Maplewick Search\nPurpose: collecting pages for accessibility checks\nTarget: Kilnharbour Ceramics Hall\nDetail: our crawler is about to start its visit as planned.",
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
  "qid": "q57310a6418",
  "text": "Handoff comment on the change: Ravensworth Monitor runs the crawler that collects pages for search indexing, and it is about to visit Pawnhurst Chess Society. Please pick up the review from here.",
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
  "qid": "q10f1251553",
  "text": "Internal note for the operations desk.\nA crawler run by Pennant Compare is about to visit Pawnhurst Chess Society. It collects pages for academic research. Please share this note with the people on the desk.",
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
  "qid": "qa76e121fbb",
  "text": "Q: Which crawler is waiting in the shared queue, and what does it collect pages for?\nA: Holloway Probe runs it. It collects pages for accessibility checks and is about to visit Ashgrove Booksellers.",
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
  "qid": "q77fdc0f389",
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
  "qid": "qf2fc07d91a",
  "text": "Support agent: Ottoline Scriptorium is behind this visit. Its crawler collects pages for link checking, and it is about to visit Wendle Vale Heritage Circle. That is the whole story from my side.",
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
  "qid": "qffa4e4c743",
  "text": "Thanks to the web team for their patience. Greywater Vault runs a crawler that collects pages for search indexing, and it is about to visit Kestwater Ferry Lines.",
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
  "qid": "qb7bc2e1d6f",
  "text": "Crawl engineer: routine work, as usual. Fernhill Labs runs the crawler, which collects pages for academic research, and it is about to visit Fallowmark Print House.",
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
  "qid": "q1d47083a87",
  "text": "From the partnerships desk at Corvane Index: we run a crawler that collects pages for search indexing. Our crawler is about to visit Starling Fen Rescue Centre, and we are glad to talk through the details.",
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
  "qid": "qc87877a395",
  "text": "Quick heads up. Eastmarch Lab runs the crawler that collects pages for search indexing. It is about to visit Sablecorner Print Studio.",
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
  "qid": "q01b11d89b8",
  "text": "Internal note for the operations desk.\nA crawler run by Oakhollow Preview is about to visit Cobblestone Heritage Trust. It collects pages for link previews. Please share this note with the people on the desk.",
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
