# G3-H extraction T25-extract_g3h-00343fba-000 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/pilot/g3h/answers/T25-extract_g3h-00343fba-000.json

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
  "qid": "qb474668543",
  "text": "Hana Watanabe: Hi! I'm looking into the plant sale date at Harrowden Upholstery Services and I've pasted what was found below, hope that's ok.\nguide: Sure, that's a great thing to be checking.\nguide: Paste away and we'll go through it together.",
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
  "qid": "qe396ea5951",
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
  "qid": "q382c2494d1",
  "text": "Hi there,\nI'm Dragana Petrovic, and I'm tidying up our records and wanted to look into the account opening fee at Morlande Rowing Club. I've pasted what was found below, so have a read whenever suits you! Thanks a bunch.\nCheers,",
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
  "qid": "qfa23743027",
  "text": "Yuki Hayashi: Hello, I'm at the front desk looking into the shoe hire charge at Corrie Hall Institute. I have pasted what was found below.\nclerk: Thanks for that, I'll have a look.\nclerk: Please keep going.",
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
  "qid": "qddbed5b32b",
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
  "qid": "q26137d7866",
  "text": "Fionnuala Doyle, a parent sorting out arrangements in a rush, looked into the registration fee at Marrowdown Arts Festival. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "qe3e2ac0458",
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
  "qid": "q9515d619f5",
  "text": "Hi there,\nI'm Dragana Petrovic, and I'm tidying up our records and wanted to look into the account opening fee at Morlande Rowing Club. I've pasted what was found below, so have a read whenever suits you! Thanks a bunch.\nCheers,",
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
  "qid": "q94e74c715f",
  "text": "Tunde Adeyemi, acting as a member, looked into the electronics drop-off deadline at Haldane Travel Express. The extract pasted in alongside it was read in a careful and orderly way. Readers who need the same check can use this route. Thank you for your attention.",
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
  "qid": "q263783bfb9",
  "text": "Nikos Papadakis: Just to say, I am handling a request about the express surcharge at Saltmarsh Exchange and I have pasted what was found below.\nsupervisor: Thank you for handling it so neatly.\nagent: Happy to proceed on that basis.",
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
  "qid": "qd773d296d4",
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
  "qid": "q74a54cded2",
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
  "qid": "q9f31607cb0",
  "text": "Good day,\nI am writing in as a member and wish to set out how the custom cake deposit at Hadley Bike Works was examined. My name is Sigrid Lund and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "qfa4157a626",
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
  "qid": "q25c6466d20",
  "text": "Farid Azizi, a parent sorting out arrangements in a rush, looked into the damage deposit at Wrenwick Nature Reserve. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "q6ae19b109a",
  "text": "Hello there,\nMy name is Meera Joshi and I am planning ahead. I would like to look into the shoe hire charge at Wickerwood Theatre, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
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
  "qid": "q59d08a35d4",
  "text": "Abena Boateng, a parent sorting out arrangements in a rush, looked into the bicycle carriage charge at Harrowden Upholstery Services. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "q9792d0b7b6",
  "text": "This internal memo records that Fionnuala Doyle, a support agent, is handling a request about the consultation fee at Ormsby Mart. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "q3804383c1d",
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
  "qid": "q77f3a66e6d",
  "text": "Requester: Valentina Ochoa\nTopic: the padlock price at Cobbler's Workshop\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
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
  "qid": "qa39f5d365c",
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
  "qid": "q02af71a58f",
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
  "qid": "q80f71bbb13",
  "text": "Hello there,\nMy name is Ananya Iyer and I am planning ahead. I would like to look into the parking charge at Crestline Climbing Gym, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
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
  "qid": "q3a7efe8220",
  "text": "Contact: Omar Nasser\nOrganisation: Oldbridge Language School\nIssue: the bicycle carriage charge\nI am a student who is looking into this and the extract is pasted here for the team.",
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
  "qid": "q81257aac0b",
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
  "qid": "q3454cdfe5d",
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
 },
 {
  "qid": "qa47a5324c6",
  "text": "Hi,\nOksana Bondar here, sorry for the rush. I need to look into the camera hire price at Quarry Lane Debating Society and have pasted what was found below. Please take a quick look when you can.\nThanks,",
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
  "qid": "qb953062663",
  "text": "Raised by: Mirek Hruska\nOrganisation: Fernhill Housing Co-operative\nIssue: the plant sale date\nI am a student looking into this and have pasted the extract in for the desk.",
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
  "qid": "qf51ecf2b43",
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
  "qid": "qfd343e4231",
  "text": "Requester: Lucia Carvalho\nTopic: the guided tour charge at Winterdale Arcade\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
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
  "qid": "qd75beef511",
  "text": "Requester: Farhan Qureshi\nTopic: the account opening fee at Harrowden Upholstery Services\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
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
  "qid": "q96c821b7fb",
  "text": "Requester: Farhan Qureshi\nTopic: the account opening fee at Harrowden Upholstery Services\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
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
  "qid": "q9da2940935",
  "text": "Oksana Bondar: Just to say, I am handling a request about the damage deposit at Cobbler's Workshop and I have pasted what was found below.\nsupervisor: Thank you for handling it so neatly.\nagent: Happy to proceed on that basis.",
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
  "qid": "q2dfaf62745",
  "text": "Farid Azizi, a parent sorting out arrangements in a rush, looked into the damage deposit at Wrenwick Nature Reserve. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "q16fe446965",
  "text": "Felix Okonjo is helping out and is looking into the guided tour charge at Thistledown Gallery. The findings are pasted below for the wider team. Things are busy around here, so this memo keeps things short.",
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
  "qid": "q49fabeb62e",
  "text": "Thandiwe Morrow is a student who has been poking around the registration fee at Saltmarsh Exchange and is enjoying the work. The extract is pasted in here so the team can have a look. Lovely bit of research, and thanks to whoever reads this.",
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
  "qid": "q22349d43b9",
  "text": "Tariq Mansour asked at the front desk about the camera hire price at Hollin Corner Bazaar in a calm, routine way. He looked into it by reading the extract pasted in and setting out the main points in plain words. Colleagues facing a similar matter can repeat these steps.",
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
  "qid": "q5059cb3b65",
  "text": "Hi there,\nAdaeze Nwosu here, a student looking into the parking charge at Hollinwood Tennis Centre. I have pasted the extract straight into this message so you can see what I am working from. Thanks so much for taking the trouble to read it, I really appreciate it.\nCheers,",
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
  "qid": "qda32de9a59",
  "text": "Requester: Declan Murphy\nTopic: the electronics drop-off deadline at Starling Cinema\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q90f56bd9d2",
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
  "qid": "qf240c4674a",
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
  "qid": "q3d753cad37",
  "text": "Camila Restrepo: Pleased to be here, I'm planning ahead and want the membership fee at Hawthorne Walk-In Clinic. I've pasted what was found below.\nofficer: Lovely, thanks for sharing that.\nofficer: Take it at your own pace.",
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
  "qid": "q610e4f74dc",
  "text": "Oksana Bondar: Just to say, I am handling a request about the damage deposit at Cobbler's Workshop and I have pasted what was found below.\nsupervisor: Thank you for handling it so neatly.\nagent: Happy to proceed on that basis.",
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
  "qid": "q9283f03e59",
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
  "qid": "q12c602d3fe",
  "text": "Requester: Declan Murphy\nTopic: the electronics drop-off deadline at Starling Cinema\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q692d854aaf",
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
  "qid": "q8782739766",
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
  "qid": "q9fff0a3642",
  "text": "Ngozi Okonkwo: Hello, I'm at the front desk looking into the entry price at Lantern Hill Rowing Club. I have pasted what was found below.\nclerk: Thanks for that, I'll have a look.\nclerk: Please keep going.",
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
  "qid": "qadf47dce14",
  "text": "This write-up explains how Tunde Adeyemi looked into the consultation fee at Stonechat Park. I am getting settled in the role, so I worked through the extract I pasted in as quickly as I could. Writing this down helps me keep track of the steps for whoever starts after me.",
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
  "qid": "qa04b7453fb",
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
 }
]
