# G3-H extraction T25-extract_g3h-923adfc4-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g3h/answers/T25-extract_g3h-923adfc4-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 47. Answers expected: 47 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "asker": <value or null>, "attr": <value or null>, "org": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q2a55e866dd",
  "text": "Hello there,\nMy name is Hana Watanabe and I am planning ahead. I would like to look into the league start date at Rookery Commons, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
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
  "qid": "q8afad07bf5",
  "text": "This internal memo records that Layla Haddad, a support agent, is handling a request about the padlock price at Harbourside Ferry Lines. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "q9522961c5d",
  "text": "Ximena Ferreira: Need to check the account opening fee at Fennel Hollow Gardens, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.",
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
  "qid": "qfb0eb37a32",
  "text": "Hey, I am Farid Azizi and I am a student who has been looking into the rural route price at Cobbler's Workshop. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
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
  "qid": "q7968d718f0",
  "text": "Ilinca Dobre: Sorry to rush you, this will be brief. I'm trying to get the registration fee at Meadowbank Dental Practice sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "qa56d25d590",
  "text": "Hana Watanabe: Need to check the guided tour charge at Quayside Lettings Office, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.",
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
  "qid": "q08eaace8c9",
  "text": "Lucia Carvalho: Hiya, I'm tidying the records and looking into the fitness orientation start date at Marrowdown Arts Festival. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.",
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
  "qid": "qe235ea701d",
  "text": "Dina Saleh: Hiya all, I'm tidying up the records and wanted to look into the fitness orientation start date at Hartwell Locksmiths. I've pasted what was found below, so have a look when you get a chance :)\ncolleague: Love that, thanks for doing it.\ncolleague: Happy to help with the tidy-up.",
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
  "qid": "q07e7febccb",
  "text": "Hi all, this memo comes from Lucia Carvalho, who is a team lead tidying records as usual. He wants the entry price at Bexwell Shuttle Lines and the extract is pasted in here for the team to see. Honestly it is a lovely little job to tidy up, so thanks for your help with it. Let's keep it in the usual place.",
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
  "qid": "q785694e8cc",
  "text": "Requester: Eleanor Farrant\nTopic: the race entry fee at Wexcombe Hospice\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
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
  "qid": "q5c493323f0",
  "text": "Yasmin Khoury handled a request by looking into the account opening fee at Ormsby Mart in a formal manner. The findings were pasted below in full. This entry sets out the steps taken.",
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
  "qid": "q6d33554db8",
  "text": "Requester: Amir Castellano\nTopic: the account opening fee at Harrowden Upholstery Services\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q203342ac1d",
  "text": "Hello,\nI am Oksana Bondar and I am preparing a reply on the parking charge at Stonechat Park, so I am a little pressed. The extract is pasted into this message for your reference. I will make the reply tidy and send it back as soon as I can.\nRegards,",
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
  "qid": "q596bf7f84a",
  "text": "Good day,\nI am writing in as a member and wish to set out how the document request deadline at Hadley Bike Works was examined. My name is Sigrid Lund and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "qa7a0e7d431",
  "text": "Memo for the team from Farhan Qureshi, a parent sorting out arrangements and stretched thin. The writer wants the electronics drop-off deadline at Lowmoor Heath Gardens and the extract is pasted in for reference. Please pass this on with the usual papers. Thanks for picking it up.",
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
  "qid": "qce8bdf7ed9",
  "text": "Memo for the team from Arjun Sethi, a parent sorting out arrangements and stretched thin. The writer wants the registration fee at Corrie Hall Institute and the extract is pasted in for reference. Please pass this on with the usual papers. Thanks for picking it up.",
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
  "qid": "qf15157f53e",
  "text": "Hello there,\nMy name is Mirek Hruska and I am planning ahead. I would like to look into the rural route price at Hawthorne Walk-In Clinic, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
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
  "qid": "q7184597dfa",
  "text": "Mirek Hruska: Hiya, I'm tidying the records and looking into the padlock price at Carrickmoor Sketch Club. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.",
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
  "qid": "q5f78db7718",
  "text": "Thandiwe Morrow is settling into the role at Wexcombe Hospice and needs to look at the race entry fee in a hurry. The extract is pasted in here for the team's use. Please pick this up when you get a moment.",
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
  "qid": "qc61f3e3225",
  "text": "Good day,\nI am writing in as a member and wish to set out how the document request deadline at Hadley Bike Works was examined. My name is Sigrid Lund and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "qca3bb7c918",
  "text": "Hi all, this memo comes from Maja Lindqvist, who is a team lead tidying records as usual. He wants the express surcharge at Wickerwood Theatre and the extract is pasted in here for the team to see. Honestly it is a lovely little job to tidy up, so thanks for your help with it. Let's keep it in the usual place.",
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
  "qid": "q8f4cd472a6",
  "text": "Thandiwe Morrow is settling into the role at Wexcombe Hospice and needs to look at the race entry fee in a hurry. The extract is pasted in here for the team's use. Please pick this up when you get a moment.",
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
  "qid": "q5b187ba887",
  "text": "Hey, I am Meera Joshi and I am a student who has been looking into the consultation fee at Cresswell Rail Company. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
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
  "qid": "q469217af93",
  "text": "Elena Marchetti: Sorry to rush you, this will be brief. I'm trying to get the entry price at Wrenwick Nature Reserve sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "q673706c231",
  "text": "Hi,\nMeera Joshi here, just helping out and keen to get on. I'm looking into the plant sale date at Larchwood Park and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "q257fdc6089",
  "text": "This internal memo records that Layla Haddad, a support agent, is handling a request about the padlock price at Harbourside Ferry Lines. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "qe72ed13e09",
  "text": "Ananya Iyer, writing in as a member, looked into the account opening fee at Linnet Savings Club. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.",
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
  "qid": "qd81faead21",
  "text": "Requester: Andreas Kallas\nTopic: the padlock price at Crestline Climbing Gym\nStage: preparing a reply\nI have pasted what was found below for the team to read.",
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
  "qid": "q999509e2c3",
  "text": "Internal memo: Meera Joshi, a visitor planning ahead, has asked about the late return fee at Hollowcastle Appliance Service. The extract is pasted in and the matter is calm and routine. Please keep it with the usual records.",
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
  "qid": "q75afa7b4b5",
  "text": "Yasmin Khoury handled a request by looking into the account opening fee at Ormsby Mart in a formal manner. The findings were pasted below in full. This entry sets out the steps taken.",
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
  "qid": "q65063f1ac7",
  "text": "Internal memo: Valentina Ochoa, a visitor planning ahead, has asked about the shoe hire charge at Cresswell Rail Company. The extract is pasted in and the matter is calm and routine. Please keep it with the usual records.",
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
  "qid": "q422f2c4c5f",
  "text": "Hello,\nI am Oksana Bondar and I am preparing a reply on the parking charge at Stonechat Park, so I am a little pressed. The extract is pasted into this message for your reference. I will make the reply tidy and send it back as soon as I can.\nRegards,",
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
  "qid": "qc5f9285d4c",
  "text": "Lucia Carvalho: Hiya, I'm tidying the records and looking into the fitness orientation start date at Marrowdown Arts Festival. I've pasted what was found below, nice and neat.\nteammate: Brilliant, thanks for tidying that up.\nteammate: Let's get it all filed.",
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
  "qid": "qb027c22573",
  "text": "Raised by: Yuki Hayashi\nOrganisation: Maplecroft Care Centre\nIssue: the entry price\nI am a student looking into this and have pasted the extract in for the desk.",
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
  "qid": "q9de8bb7f05",
  "text": "Dear colleague,\nMy name is Tunde Adeyemi and I am writing to look into the desk rental fee at Foxhollow Poetry Festival. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "q7d952d1498",
  "text": "Maja Lindqvist: Hi there. I'd like to look into the bicycle carriage charge at Thimble Lane Evening Classes and I've pasted what was found below.\ndesk: Thank you, I'll take it from here.\nsupervisor: Carry on, and send it back when you've finished.",
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
  "qid": "qe0a9d0e9c0",
  "text": "Requester: Omar Nasser\nTopic: the document request deadline at Hawthorne Walk-In Clinic\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
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
  "qid": "q6001562d9d",
  "text": "Thandiwe Morrow is settling into the role at Wexcombe Hospice and needs to look at the race entry fee in a hurry. The extract is pasted in here for the team's use. Please pick this up when you get a moment.",
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
  "qid": "q0cfeb85c72",
  "text": "Hello,\nI am Valentina Ochoa and I am preparing a reply on the camera hire price at Crestline Climbing Gym, so I am a little pressed. The extract is pasted into this message for your reference. I will make the reply tidy and send it back as soon as I can.\nRegards,",
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
  "qid": "qcf253b3bc1",
  "text": "Good day,\nI am writing in as a member and wish to set out how the entry price at Lowmoor Heath Gardens was examined. My name is Valentina Ochoa and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "q11db08b906",
  "text": "Hi,\nFelix Okonjo here, just helping out and keen to get on. I'm looking into the parking charge at Wrenwick Nature Reserve and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "qb8ef33c4bd",
  "text": "Elena Marchetti: Sorry to rush you, this will be brief. I'm trying to get the entry price at Wrenwick Nature Reserve sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "q789aeeae86",
  "text": "Hello,\nI am Ngozi Okonkwo and I am preparing a reply on the express surcharge at Morlande Rowing Club, so I am a little pressed. The extract is pasted into this message for your reference. I will make the reply tidy and send it back as soon as I can.\nRegards,",
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
  "qid": "q91e295fd25",
  "text": "Dear colleague,\nMy name is Farid Azizi and I am writing to look into the electronics drop-off deadline at Stanhope Sailing Club. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "q777460ca34",
  "text": "This write-up explains how Dina Saleh looked into the term start date at Brookhollow Folk Club. I am getting settled in the role, so I worked through the extract I pasted in as quickly as I could. Writing this down helps me keep track of the steps for whoever starts after me.",
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
  "qid": "qce2d1fe80d",
  "text": "Mateo Quiroga: Hi there. I'd like to look into the consultation fee at Winterdale Arcade and I've pasted what was found below.\ndesk: Thank you, I'll take it from here.\nsupervisor: Carry on, and send it back when you've finished.",
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
  "qid": "qdb49e646cb",
  "text": "Dear colleague,\nMy name is Tunde Adeyemi and I am writing to look into the desk rental fee at Foxhollow Poetry Festival. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
