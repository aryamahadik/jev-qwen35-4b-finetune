# G3-H extraction T35-extract_g3h-e9bd0f70-000 (family T35)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/pilot_i3/g3h/answers/T35-extract_g3h-e9bd0f70-000.json

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
  "qid": "q1be6bb3ef0",
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
  "qid": "q64a8fb0047",
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
  "qid": "qb3074276ff",
  "text": "Internal note for the operations desk.\nA crawler run by Corrigan Pulse is about to visit Riverlight Forum. It collects pages for search indexing. Please share this note with the people on the desk.",
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
  "qid": "q7e22833c28",
  "text": "Hello team,\nPelham Insight runs the crawler at the front of the shared queue. It collects pages for accessibility checks and is about to visit Kilnharbour Ceramics Hall. Please note this as the queue moves on.\nThanks,\nCrawl queue",
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
  "qid": "q0a23af7aaf",
  "text": "Partnerships desk, review comment:\nRuddock Metrics runs the crawler covered by this setup change, and it collects pages for accessibility checks. The crawler is about to visit Eastmere City Portal. Please reply on the thread with questions.",
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
  "qid": "q0d1ec9813f",
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
  "qid": "q3380d062d8",
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
  "qid": "q081dbee52f",
  "text": "Handoff for the crawl team.\nSaltmarsh Research runs the crawler that is about to visit Larkstone Ramblers. It collects pages for link checking. Please pick up from here and reply on this thread with questions.",
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
  "qid": "qb984227f57",
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
  "qid": "q66fa767e57",
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
  "qid": "qe04bd626af",
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
  "qid": "q097d77e575",
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
  "qid": "q6c2e9bbbe9",
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
  "qid": "q6ae5a0271c",
  "text": "Hey team,\nKindred Trace has a crawler with a real taste for tea breaks, and it is off to visit Tidewater Courier. Its whole job is to collect pages for link previews, which is a very cozy task.\nCheers,\nCrawl team",
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
  "qid": "qd6a1216b85",
  "text": "Q: Which crawler is waiting in the shared queue, and what does it collect pages for?\nA: Jasper Snapwell runs it. It collects pages for link checking and is about to visit Chainwell Repair Collective.",
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
  "qid": "q99c07bc521",
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
  "qid": "q9d200cd4e2",
  "text": "Hello,\nA quick summary of who is asking. Saltmarsh Research runs a crawler that collects pages for link checking. It is about to visit Oatfield Table, so we wanted to mention that.\nThanks,",
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
  "qid": "q4fb8d4a587",
  "text": "Review note:\nChange: crawler setup tweak.\nBy: Silverlace Feed.\nFor: search indexing.\nSite: Fernlea Botanic Grounds.\nQuick note, crawler about to arrive. Thanks.",
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
  "qid": "qd80db8c7b9",
  "text": "Support agent: Corrigan Pulse is behind this visit. Its crawler collects pages for price comparison, and it is about to visit Harbor Lantern Books. That is the whole story from my side.",
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
  "qid": "q22283710f4",
  "text": "Ticket: courtesy message\nOperator: Mirelane Check\nPurpose: link checking\nTarget: Spokewright Bikes\nDetail: we kindly wish to inform you of this planned visit.",
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
  "qid": "q76082a382f",
  "text": "Q: Who runs this crawler, and what is it collecting pages for?\nA: Pelham Insight runs it. It collects pages for link previews and is about to visit Windward Sailing Academy.",
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
  "qid": "q747d38ad0c",
  "text": "Quick heads up. Aldergrove Catalogue runs the crawler that collects pages for link previews. It is about to visit Brightwire Science Audio.",
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
  "qid": "qcc6763c8a4",
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
  "qid": "q56022f9e8b",
  "text": "Q: Which crawler is waiting in the shared queue, and what does it collect pages for?\nA: Jasper Snapwell runs it. It collects pages for link checking and is about to visit Chainwell Repair Collective.",
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
  "qid": "qabcf2cb6e2",
  "text": "Internal note for the operations desk.\nA crawler run by Corrigan Pulse is about to visit Gambit Corner Club. It collects pages for search indexing. Please share this note with the people on the desk.",
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
  "qid": "q9364bcc332",
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
  "qid": "qeaf3615fcb",
  "text": "Ticket: courtesy message\nOperator: Wenlock Shelf\nPurpose: academic research\nTarget: Sablecorner Print Studio\nDetail: we kindly wish to inform you of this planned visit.",
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
  "qid": "q6bca4509b6",
  "text": "Review comment:\nChange: the crawler setup covers a new visit.\nNote: Corrigan Pulse runs this crawler, which collects pages for link checking.\nScope: Thornbrake Camp Rentals.\nComment: the wording reads clearly, thanks for the update.",
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
  "qid": "qd2f0ac2152",
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
  "qid": "qac586c38d9",
  "text": "crawl team: Amberline Archive runs a crawler that collects pages for link previews, and it is about to visit Spokeyard Cycle Cooperative.",
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
  "qid": "q5039a4ab80",
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
  "qid": "qfc0bd9b229",
  "text": "Work note from our side. Silverlace Feed is sending our crawler to Tandem Corner Forum. The crawler collects pages for web archiving, and we are writing this so the record is complete.",
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
  "qid": "q8c2970d28f",
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
  "qid": "q23c6d2fee7",
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
  "qid": "q1cc53a5d8d",
  "text": "Quick heads up. Aldergrove Catalogue runs the crawler that collects pages for link previews. It is about to visit Brightwire Science Audio.",
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
  "qid": "q868ab11202",
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
  "qid": "qb1b5b22b9d",
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
  "qid": "q60717a3f95",
  "text": "Review note:\nChange: crawler setup tweak.\nBy: Silverlace Feed.\nFor: search indexing.\nSite: Fernlea Botanic Grounds.\nQuick note, crawler about to arrive. Thanks.",
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
  "qid": "q01216cbbdf",
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
  "qid": "qc122133932",
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
  "qid": "qaf249dd98f",
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
  "qid": "q950e1e21e9",
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
  "qid": "q1034e09641",
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
  "qid": "qc33223449b",
  "text": "Hi there, thanks for getting in touch.\nQ: Why is a crawler about to visit Brightwire Science Audio?\nA: Kestrel Links runs it, and it collects pages for academic research.\nWarm wishes from the crawl team.",
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
  "qid": "q619b5c1fc6",
  "text": "Hello team,\nDolmen Cart runs a crawler that collects pages for price comparison, and it is about to visit Cumulus Corner Journal. Routine work, as usual.\nThanks,\nCrawl engineering",
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
  "qid": "qdea7072c06",
  "text": "Ticket: courtesy message\nOperator: Greywater Vault\nPurpose: search indexing\nTarget: Cumulus Corner Journal\nDetail: we kindly wish to inform you of this planned visit.",
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
  "qid": "q8f25a1000f",
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
  "qid": "q8a4827b208",
  "text": "Q: Why is a crawler collecting pages for academic research?\nA: Greywater Vault runs that crawler, and it is about to visit Lingua Brook Board.",
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
