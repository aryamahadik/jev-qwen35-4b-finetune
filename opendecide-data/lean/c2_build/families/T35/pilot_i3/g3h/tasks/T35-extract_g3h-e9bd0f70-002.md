# G3-H extraction T35-extract_g3h-e9bd0f70-002 (family T35)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/pilot_i3/g3h/answers/T35-extract_g3h-e9bd0f70-002.json

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
  "qid": "q134ada5113",
  "text": "Q: What is new in the project channel?\nA: Aldergrove Catalogue is sending a crawler that collects pages for academic research, and it is about to visit Ember Hollow Tutoring.",
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
  "qid": "q3887d77900",
  "text": "Q: What is new in the project channel?\nA: Anselm Corpus is sending a crawler that collects pages for search indexing, and it is about to visit Quillmere Harvest Yard.",
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
  "qid": "qd68584ff68",
  "text": "Review comment:\nThis setup change covers a crawler run by Strand Cohort, which collects pages for web archiving. It is about to visit Snowcrest Alpine Club. Thanks to the web team for their help.",
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
  "qid": "q313cc01a0a",
  "text": "Handoff comment on the change: Brindle Lantern runs the crawler that collects pages for link checking, and it is about to visit Ashgrove Booksellers. Please pick up the review from here.",
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
 },
 {
  "qid": "q536666f866",
  "text": "Web team: heads up, Crestwood Data Lab runs a crawler that collects pages for accessibility checks. It is about to visit Thornbrake Camp Rentals.",
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
  "qid": "qf1b3fe2348",
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
  "qid": "qd2ffdccc27",
  "text": "Review note:\nChange: crawler setup tweak.\nBy: Dolmen Cart.\nFor: web archiving.\nSite: Orchardwhistle Cider Bar.\nQuick note, crawler about to arrive. Thanks.",
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
  "qid": "q8b66091468",
  "text": "Memo: crawl operations\nWho: Carrow Stacks runs the crawler.\nWhy: it collects pages for link checking.\nWhat: it is about to visit Pawsworth Grooming Salon.",
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
  "qid": "qf75cd1b751",
  "text": "Ticket: crawl heads-up\nOperator: Holloway Probe\nPurpose: search indexing\nTarget: Saffron Lane Recipes\nType: planned visit",
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
  "qid": "q0e2d6642f9",
  "text": "Q: Who is behind the crawler visiting Isobarlane Weather Log, and what is it for?\nA: Halvorsen Watch runs it, and it collects pages for link previews.",
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
  "qid": "q193b5e3988",
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
  "qid": "qd6e11e7012",
  "text": "Review comment:\nChange: the crawler setup covers a new visit.\nNote: Halvorsen Watch runs this crawler, which collects pages for price comparison.\nScope: Kestwater Ferry Lines.\nComment: the wording reads clearly, thanks for the update.",
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
  "qid": "qe4de59b9be",
  "text": "Q: Who is behind the crawler visiting Ashgrove Booksellers, and what is it for?\nA: Halden Lark runs it, and it collects pages for academic research.",
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
  "qid": "q15b50d08b1",
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
  "qid": "qcad64566b5",
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
  "qid": "q7740fd53f7",
  "text": "Q: Who is behind the crawler visiting Ashgrove Booksellers, and what is it for?\nA: Halden Lark runs it, and it collects pages for academic research.",
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
  "qid": "q8874b24604",
  "text": "Support agent: Halvorsen Watch is behind this visit. Its crawler collects pages for web archiving, and it is about to visit Harrowgate Cycles. That is the whole story from my side.",
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
  "qid": "q0b94867757",
  "text": "Hi there,\nHope things are going well on your side. Silverlace Feed runs a crawler that collects pages for price comparison, and it is about to visit Kilnharbour Ceramics Hall. Thanks for helping us keep track of this.\nWarm regards,",
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
  "qid": "q0e811eb6f4",
  "text": "Notice for colleagues. Kindly be advised that Thessaly Manuscripts operates a crawler that collects pages for web archiving. The crawler is respectfully about to visit Windward Sailing Academy. We are grateful for your attention to this notice.",
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
  "qid": "q472b1c53fd",
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
  "qid": "q61f063fd54",
  "text": "Q: Which crawler is waiting in the shared queue, and what does it collect pages for?\nA: Bramblewick Cards runs it. It collects pages for search indexing and is about to visit Tidemoor Aquarium Emporium.",
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
  "qid": "qe612c83fa1",
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
  "qid": "q2b243d70f9",
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
  "qid": "qbd34c73f13",
  "text": "Summary: incoming crawler notice.\nOperator: Tallowick Wire.\nPurpose: price comparison.\nDetail: the crawler is about to visit Quarkhollow Podcast, and this summary comes from the data team lead.",
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
  "qid": "q656d430476",
  "text": "From the partnerships desk at Maplewick Search: we run a crawler that collects pages for price comparison. Our crawler is about to visit Hollinmere Parish Records, and we are glad to talk through the details.",
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
  "qid": "q06b45174c1",
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
  "qid": "qcee4263292",
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
  "qid": "q244c97d3d6",
  "text": "Summary for the review: Tallowick Wire runs the crawler that collects pages for link previews. It is about to visit Corrandale Animal Park, and the change to its code reads well to us.",
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
  "qid": "q452992f204",
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
  "qid": "q191ff17f16",
  "text": "Summary: incoming crawler notice.\nOperator: Ellery Contrast.\nPurpose: academic research.\nDetail: the crawler is about to visit Wrenfold Tea House, and this summary comes from the data team lead.",
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
  "qid": "qe4e163c440",
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
  "qid": "q8ee8b4c360",
  "text": "Q: Who runs this crawler, and what is it collecting pages for?\nA: Kestrel Panel runs it. It collects pages for link previews and is about to visit Larchfold Outfitters.",
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
  "qid": "qad0d97754e",
  "text": "Ops feed: Ruddock Metrics operates a crawler that collects pages for web archiving. The crawler is about to visit Millrace Loaf Shop. Logged for reference.",
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
  "qid": "qf0d22e050f",
  "text": "Crawl engineer: routine work, as usual. Fernhill Labs runs the crawler, which collects pages for link previews, and it is about to visit Rushdale Playhouse.",
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
  "qid": "qe042761865",
  "text": "Hello,\nThis crawl collects pages for accessibility checks. Saltmarsh Research runs the crawler, which is about to visit Spokeyard Cycle Cooperative. We wanted you to hear about it from us directly.\nKind regards,",
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
  "qid": "q0922e44c2a",
  "text": "Crawl engineer: routine work, as usual. Tallowick Wire runs the crawler, which collects pages for web archiving, and it is about to visit Plinth Gaming Lounge.",
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
  "qid": "qa69e5e0653",
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
 },
 {
  "qid": "q18bde637c3",
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
  "qid": "qea35b0347f",
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
  "qid": "q22153da33d",
  "text": "Memo: crawl operations\nWho: Carrow Stacks runs the crawler.\nWhy: it collects pages for link checking.\nWhat: it is about to visit Pawsworth Grooming Salon.",
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
  "qid": "qba96f1084f",
  "text": "Internal note for the operations desk.\nA crawler run by Marlowe Folio is about to visit Fernlea Botanic Grounds. It collects pages for academic research. Please share this note with the people on the desk.",
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
  "qid": "q08052f4edf",
  "text": "Partnerships desk, review comment:\nSilverlace Feed runs the crawler covered by this setup change, and it collects pages for academic research. The crawler is about to visit Whistlewood Botanical Gardens. Please reply on the thread with questions.",
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
  "qid": "qad081a2d35",
  "text": "Q: What is this routine crawl about, and who runs it?\nA: Ellery Contrast runs the crawler, which collects pages for search indexing. It is about to visit Windward Sailing Academy.",
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
  "qid": "q48801a95ac",
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
 }
]
