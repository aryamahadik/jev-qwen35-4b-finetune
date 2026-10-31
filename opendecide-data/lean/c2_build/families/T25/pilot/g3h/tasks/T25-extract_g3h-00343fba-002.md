# G3-H extraction T25-extract_g3h-00343fba-002 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/pilot/g3h/answers/T25-extract_g3h-00343fba-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 19. Answers expected: 19 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "asker": <value or null>, "attr": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q8836e05c5a",
  "text": "Idris Varga: I need to get a reply out on the private lesson price at Bramwell Market and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q0bf0e3208e",
  "text": "Requester: Lucia Carvalho\nTopic: the plant sale date at Marrowdown Arts Festival\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qbe167a9812",
  "text": "Requester: Abena Boateng\nTopic: the membership fee at Brightmoor College of Crafts\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q740b60a4e8",
  "text": "Hi there,\nRohan Kapoor here, a student looking into the rural route price at Haverley Lending Circle. I have pasted the extract straight into this message so you can see what I am working from. Thanks so much for taking the trouble to read it, I really appreciate it.\nCheers,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qbbe1422795",
  "text": "Sigrid Lund: Hello, I'm handling a request about the young driver fee at Wexcombe Hospice and I have pasted what was found below.\nclient: Thank you for that, it is appreciated.\nclient: I'll wait while you read through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qeb68d32a27",
  "text": "Good day,\nI am writing in as a member and wish to set out how the parking charge at Fennel Hollow Gardens was examined. My name is Kofi Mensah and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q523360388d",
  "text": "Hello there,\nMy name is Farhan Qureshi and I am planning ahead. I would like to look into the parking charge at Ormsby Mart, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q88a08f585b",
  "text": "Amir Castellano: I need to get a reply out on the account opening fee at Plumbridge Emporium and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qe9bf03077a",
  "text": "Ananya Iyer: Hello, I'm at the front desk looking into the padlock price at Ormsby Mart. I have pasted what was found below.\nclerk: Thanks for that, I'll have a look.\nclerk: Please keep going.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qad0f34e7e7",
  "text": "Sunil Dhawan: Hi! I'm looking into the shoe hire charge at Rookery Commons and I've pasted what was found below, hope that's ok.\nguide: Sure, that's a great thing to be checking.\nguide: Paste away and we'll go through it together.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q39a38919fe",
  "text": "Fionnuala Doyle: Quick query on the race entry fee at Morlande Rowing Club, I am in a rush.\ndesk clerk: Fine, I have the extract in front of me.\ndesk clerk: Read it out and we will go through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q8d77d246c0",
  "text": "Requester: Idris Varga\nTopic: the young driver fee at Linnet Savings Club\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q5c6ec8216d",
  "text": "Nikos Papadakis: Hi! I'm looking into the parking charge at Oakhaven Residents Association and I've pasted what was found below, hope that's ok.\nguide: Sure, that's a great thing to be checking.\nguide: Paste away and we'll go through it together.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q04af39d74b",
  "text": "Hi,\nFionnuala Doyle here, sorry for the rush. I need to look into the damage deposit at Stanhope Sailing Club and have pasted what was found below. Please take a quick look when you can.\nThanks,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qf85c7709ab",
  "text": "Hello there,\nMy name is Ximena Ferreira and I am planning ahead. I would like to look into the padlock price at Brightwater Physio Clinic, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q5792d7bb56",
  "text": "Dear colleague,\nMy name is Radu Calin and I am writing to look into the young driver fee at Thimble Lane Evening Classes. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "q55dc309667",
  "text": "Lucia Carvalho asked at the front desk about the late return fee at Hawthorne Walk-In Clinic in a calm, routine way. He looked into it by reading the extract pasted in and setting out the main points in plain words. Colleagues facing a similar matter can repeat these steps.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qe51a5dce09",
  "text": "Freja Nyberg: Quick query on the private lesson price at Larkfield Coach Tours, I am in a rush.\ndesk clerk: Fine, I have the extract in front of me.\ndesk clerk: Read it out and we will go through it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 },
 {
  "qid": "qe0d8e6cc0f",
  "text": "Hey, I am Mirek Hruska and I am a student who has been looking into the consultation fee at Wexcombe Hospice. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
  "schema": [
   {
    "field": "asker",
    "type": "name",
    "describe": "the person asking, as written"
   },
   {
    "field": "org",
    "type": "name",
    "describe": "the organisation the question is about, as written"
   },
   {
    "field": "attr",
    "type": "str",
    "describe": "the attribute being looked up, as written"
   }
  ]
 }
]
