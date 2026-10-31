# G3-H extraction T25-extract_g3h-00343fba-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/pilot/g3h/answers/T25-extract_g3h-00343fba-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "asker": <value or null>, "attr": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qfbf63f0ea0",
  "text": "Dear colleague,\nMy name is Sofia Benitez and I am writing to look into the private lesson price at Garrow Cab Company. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "q9e63b65f1e",
  "text": "Jiho Kang, writing in as a member, looked into the electronics drop-off deadline at Ormsby Mart. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.",
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
  "qid": "qa16398db58",
  "text": "Hi there,\nHarriet Pemberton here, a student looking into the race entry fee at Fennel Hollow Gardens. I have pasted the extract straight into this message so you can see what I am working from. Thanks so much for taking the trouble to read it, I really appreciate it.\nCheers,",
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
  "qid": "q476e84a331",
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
  "qid": "q0c2e42ec44",
  "text": "Hi,\nAbena Boateng here, sorry for the rush. I need to look into the parking charge at Quarry Lane Debating Society and have pasted what was found below. Please take a quick look when you can.\nThanks,",
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
  "qid": "qa804bab841",
  "text": "Ximena Ferreira: Sorry to rush you, this will be brief. I'm trying to get the late return fee at Wrenwick Nature Reserve sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "q9b90404ea0",
  "text": "Kristoffer Dahl: Hello there, I would like to ask about the season registration fee at Bramwell Market.\nfront desk: Of course, the extract is here and I can go through it with you.",
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
  "qid": "q5d272c3f5e",
  "text": "Arjun Sethi: Hi there. I'd like to look into the express surcharge at Otterbourne Film Society and I've pasted what was found below.\ndesk: Thank you, I'll take it from here.\nsupervisor: Carry on, and send it back when you've finished.",
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
  "qid": "q6197ad1245",
  "text": "Hi,\nI'm Harriet Pemberton and I'm sorting out a booking, so this will be brief. I need to check the padlock price at Hartwell Locksmiths and I've pasted what was found below.\nBest,",
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
  "qid": "q0990abc597",
  "text": "Hi there,\nI'm Dina Saleh, and I'm tidying up our records and wanted to look into the race entry fee at Maplecroft Care Centre. I've pasted what was found below, so have a read whenever suits you! Thanks a bunch.\nCheers,",
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
  "qid": "q6bf999e2ac",
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
  "qid": "q15b67d7b7c",
  "text": "Felix Okonjo, a member, has been in touch about the season registration fee at Brightmoor College of Crafts. The findings are pasted below. Kindly keep this memo on file for the team.",
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
  "qid": "qff1327af93",
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
  "qid": "q36941b9473",
  "text": "Andreas Kallas: Need the express surcharge for Cresswell Rail Company, I am sorting things out fast.\nclerk: Got it, I have the extract ready to read to you.",
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
  "qid": "q5c57503c82",
  "text": "Kristoffer Dahl: Hello there, I would like to ask about the season registration fee at Bramwell Market.\nfront desk: Of course, the extract is here and I can go through it with you.",
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
  "qid": "q359b05caa4",
  "text": "This internal memo records that Lucia Carvalho, a support agent, is handling a request about the camera hire price at Thornmere Leisure Centre. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "qb262532bcb",
  "text": "Farid Azizi, a member, has been in touch about the consultation fee at Haverley Lending Circle. The findings are pasted below. Kindly keep this memo on file for the team.",
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
  "qid": "q7ec3056af9",
  "text": "Hi all, this memo comes from Harriet Pemberton, who is a team lead tidying records as usual. He wants the plant sale date at Foxhollow Poetry Festival and the extract is pasted in here for the team to see. Honestly it is a lovely little job to tidy up, so thanks for your help with it. Let's keep it in the usual place.",
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
  "qid": "q01a45f6195",
  "text": "Sigrid Lund is helping out and is looking into the damage deposit at Winterdale Arcade. The findings are pasted below for the wider team. Things are busy around here, so this memo keeps things short.",
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
  "qid": "q295d95ad68",
  "text": "Maja Lindqvist: Pleased to be here, I'm planning ahead and want the plant sale date at Lindenfield Music Hall. I've pasted what was found below.\nofficer: Lovely, thanks for sharing that.\nofficer: Take it at your own pace.",
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
  "qid": "q0fa2bfa196",
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
  "qid": "qfba2257189",
  "text": "Ilinca Dobre: Need the late return fee for Hollin Corner Bazaar, I am sorting things out fast.\nclerk: Got it, I have the extract ready to read to you.",
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
  "qid": "qfbdc1fb603",
  "text": "Logged by: Valentina Ochoa\nProvider: Winterdale Arcade\nSubject: the custom cake deposit\nI am a visitor planning ahead and the extract is pasted in for the desk.",
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
  "qid": "q34846169c7",
  "text": "Elena Marchetti looked into the camera hire price at Harrowden Upholstery Services in a hurry and pasted what was found below. Keeping the write-up short suits a busy desk. Whoever reads it can repeat the same steps.",
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
  "qid": "qb37cc99066",
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
  "qid": "q902316bb93",
  "text": "Requester: Meera Joshi\nTopic: the account opening fee at Linden Street Health Centre\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q628579f32c",
  "text": "Logged by: Farid Azizi\nOrganisation: Meadowbank Dental Practice\nTopic: the season registration fee\nI am a member writing in and have pasted the extract here for the desk to look at.",
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
  "qid": "qa88a927b17",
  "text": "Felix Okonjo, a parent sorting out arrangements in a rush, looked into the parking charge at Bexwell Shuttle Lines. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "qa39712a114",
  "text": "Radu Calin: Need the guided tour charge for Corrie Hall Institute, I am sorting things out fast.\nclerk: Got it, I have the extract ready to read to you.",
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
  "qid": "q7226e2983d",
  "text": "Hey, I am Yasmin Khoury and I am a student who has been looking into the registration fee at Starling Cinema. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
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
  "qid": "q063e9101fe",
  "text": "Hi,\nI'm Rohan Kapoor and I'm sorting out a booking, so this will be brief. I need to check the consultation fee at Quayside Lettings Office and I've pasted what was found below.\nBest,",
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
  "qid": "q848e3a3b62",
  "text": "Dragana Petrovic: I need to get a reply out on the table fee at Fennel Hollow Gardens and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
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
  "qid": "q6f1fafe249",
  "text": "This internal memo records that Ngozi Okonkwo, a support agent, is handling a request about the shoe hire charge at Quayside Lettings Office. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "qaea8ed773e",
  "text": "Camila Restrepo: Hi there. I'd like to look into the young driver fee at Otterbourne Film Society and I've pasted what was found below.\ndesk: Thank you, I'll take it from here.\nsupervisor: Carry on, and send it back when you've finished.",
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
  "qid": "q23a922fac0",
  "text": "Request from: Ananya Iyer\nRegarding: Brookhollow Folk Club\nTopic: the registration fee\nI am a volunteer helping out and have pasted the extract in underneath.",
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
  "qid": "qe8ef194031",
  "text": "Request from: Ananya Iyer\nRegarding: Brookhollow Folk Club\nTopic: the registration fee\nI am a volunteer helping out and have pasted the extract in underneath.",
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
  "qid": "qda0afb9b6a",
  "text": "Ananya Iyer: Hello, I'm a member writing in about the express surcharge at Larchwood Park and I've pasted what was found below.\nofficer: Thank you for writing in, I'll look into that straight away.",
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
  "qid": "qc6dcfecd11",
  "text": "Lakshmi Nair: Hiya, I'm tidying the records and looking into the bicycle carriage charge at Fennel Hollow Gardens. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.",
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
  "qid": "qf03b2ccab8",
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
  "qid": "qb127accd97",
  "text": "Hi,\nKofi Mensah here, sorry for the rush. I need to look into the season registration fee at Halsey Study Centre and have pasted what was found below. Please take a quick look when you can.\nThanks,",
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
  "qid": "qe7167d9f79",
  "text": "Hi there,\nHarriet Pemberton here, a student looking into the race entry fee at Fennel Hollow Gardens. I have pasted the extract straight into this message so you can see what I am working from. Thanks so much for taking the trouble to read it, I really appreciate it.\nCheers,",
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
  "qid": "q360e9f0052",
  "text": "Ilinca Dobre: Need the late return fee for Hollin Corner Bazaar, I am sorting things out fast.\nclerk: Got it, I have the extract ready to read to you.",
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
  "qid": "q5d429d223e",
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
  "qid": "q4aabee23fa",
  "text": "Hi there,\nI'm Freja Nyberg, and I'm tidying up our records and wanted to look into the race entry fee at Bramwell Market. I've pasted what was found below, so have a read whenever suits you! Thanks a bunch.\nCheers,",
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
  "qid": "q708a599d72",
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
  "qid": "q08326a4952",
  "text": "Logged by: Valentina Ochoa\nProvider: Winterdale Arcade\nSubject: the custom cake deposit\nI am a visitor planning ahead and the extract is pasted in for the desk.",
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
  "qid": "q65efa50971",
  "text": "Yasmin Khoury: Just running through the table fee at Garrow Cab Company, the extract is pasted in here.\nguide: Lovely, let us go through it together at your own pace.",
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
  "qid": "q676cfedb3c",
  "text": "Hi,\nAnanya Iyer here, just helping out and keen to get on. I'm looking into the custom cake deposit at Bramwell Market and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "qfdb4c30094",
  "text": "Hi all, this memo comes from Harriet Pemberton, who is a team lead tidying records as usual. He wants the plant sale date at Foxhollow Poetry Festival and the extract is pasted in here for the team to see. Honestly it is a lovely little job to tidy up, so thanks for your help with it. Let's keep it in the usual place.",
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
  "qid": "q8e90a802d9",
  "text": "This internal memo records that Lucia Carvalho, a support agent, is handling a request about the camera hire price at Thornmere Leisure Centre. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
