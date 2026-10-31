# G3-H extraction T25-extract_g3h-7ad5ec37-001 (family T25)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T25/qc/g3h/answers/T25-extract_g3h-7ad5ec37-001.json

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
  "qid": "q3ebea341f6",
  "text": "Requester: Tariq Mansour\nTopic: the membership fee at Foxhollow Poetry Festival\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
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
  "qid": "q00232ddb19",
  "text": "Yaw Ofori: I need to get a reply out on the late return fee at Quayside Lettings Office and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
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
  "qid": "q633847d7da",
  "text": "Sofia Benitez, writing in as a member, looked into the consultation fee at Linnet Savings Club. The extract is pasted in with this write-up and the wording has been kept intact. The approach is recorded here so that colleagues can repeat it. Thank you for reading.",
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
  "qid": "q4a7f14e3ad",
  "text": "Sunil Dhawan is settling into the role at Fernhill Housing Co-operative and needs to look at the account opening fee in a hurry. The extract is pasted in here for the team's use. Please pick this up when you get a moment.",
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
  "qid": "q78954363dc",
  "text": "Hi,\nMirek Hruska here, just helping out and keen to get on. I'm looking into the league start date at Garrow Cab Company and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "qa2984b6ab5",
  "text": "Yuki Hayashi: Hiya all, I'm tidying up the records and wanted to look into the membership fee at Brightmoor College of Crafts. I've pasted what was found below, so have a look when you get a chance :)\ncolleague: Love that, thanks for doing it.\ncolleague: Happy to help with the tidy-up.",
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
  "qid": "q8d1c8e1c19",
  "text": "Dear colleague,\nMy name is Fionnuala Doyle and I am writing to look into the padlock price at Starling Cinema. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "qa4ba6facb5",
  "text": "Ximena Ferreira: Hello, I'm handling a request about the damage deposit at Wickerwood Theatre and I have pasted what was found below.\nclient: Thank you for that, it is appreciated.\nclient: I'll wait while you read through it.",
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
  "qid": "q1edd90ccd8",
  "text": "Dear colleague,\nMy name is Fionnuala Doyle and I am writing to look into the padlock price at Starling Cinema. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "qe0c4e0ad82",
  "text": "Logged by: Omar Nasser\nOrganisation: Cobbler's Workshop\nTopic: the shoe hire charge\nI am a member writing in and have pasted the extract here for the desk to look at.",
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
  "qid": "q8448671ba6",
  "text": "Raised by: Ansgar Holm\nOrganisation: Linnet Savings Club\nIssue: the season registration fee\nI am a student looking into this and have pasted the extract in for the desk.",
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
  "qid": "q11ee75d75d",
  "text": "Arjun Sethi: Kind greetings. I'm a member and would like to look into the fitness orientation start date at Ormsby Mart. I have pasted the findings below.\nofficer: Thank you, that is much appreciated.\nadmin: Please carry on from here.",
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
  "qid": "q99ba16bc59",
  "text": "Requester: Declan Murphy\nTopic: the membership fee at Foxhollow Poetry Festival\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q3e19a5dd70",
  "text": "Requester: Tariq Mansour\nTopic: the term start date at Stanhope Sailing Club\nQueue: volunteer desk\nI'm helping out and have pasted what was found below.",
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
  "qid": "q2e27f99f03",
  "text": "Sunil Dhawan, acting as a member, looked into the entry price at Hallam Chess Club. The extract pasted in alongside it was read in a careful and orderly way. Readers who need the same check can use this route. Thank you for your attention.",
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
  "qid": "q626454ebfc",
  "text": "Maja Lindqvist: I need to get a reply out on the shoe hire charge at Halsey Study Centre and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
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
  "qid": "qfaa6d148a6",
  "text": "Requester: Freja Nyberg\nTopic: the padlock price at Maplecroft Care Centre\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
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
  "qid": "q2010c6b86b",
  "text": "Camila Restrepo, a member, has been in touch about the desk rental fee at Lowmoor Heath Gardens. The findings are pasted below. Kindly keep this memo on file for the team.",
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
  "qid": "q08daf5b78c",
  "text": "Kristoffer Dahl: Hello, I'm handling a request about the bicycle carriage charge at Brookhollow Folk Club and I have pasted what was found below.\nclient: Thank you for that, it is appreciated.\nclient: I'll wait while you read through it.",
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
  "qid": "q10dcccdd08",
  "text": "Fionnuala Doyle: Just to say, I am handling a request about the consultation fee at Hollin Corner Bazaar and I have pasted what was found below.\nsupervisor: Thank you for handling it so neatly.\nagent: Happy to proceed on that basis.",
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
  "qid": "q403a1604a0",
  "text": "Hello,\nI am Sunil Dhawan and I am preparing a reply on the electronics drop-off deadline at Stanhope Sailing Club, so I am a little pressed. The extract is pasted into this message for your reference. I will make the reply tidy and send it back as soon as I can.\nRegards,",
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
  "qid": "q43d304fae0",
  "text": "Requester: Adaeze Nwosu\nTopic: the race entry fee at Crestline Climbing Gym\nQueue: support handling\nI'm working through the request and have pasted what was found below.",
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
  "qid": "qb2403defb0",
  "text": "Kristoffer Dahl, a customer at the front desk, has asked about the entry price at Crestline Climbing Gym. The extract pasted in for this request is kept with the memo for reference. It is a routine matter and it is being handled in the usual way. Please keep this with the regular records.",
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
  "qid": "q61b605080e",
  "text": "Oksana Bondar: Sorry to rush you, this will be brief. I'm trying to get the young driver fee at Lowmoor Heath Gardens sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "q9b92273378",
  "text": "Dear colleague,\nMy name is Abena Boateng and I am writing to look into the padlock price at Quarry Lane Debating Society. I have pasted what was found below for your reference. Thank you for your help on this matter.\nKind regards,",
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
  "qid": "q38d1c82d22",
  "text": "Hi,\nMirek Hruska here, just helping out and keen to get on. I'm looking into the league start date at Garrow Cab Company and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "q5096504d0a",
  "text": "Hey, I am Ximena Ferreira and I am a student who has been looking into the express surcharge at Thimble Lane Evening Classes. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
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
  "qid": "q1b4ac485ec",
  "text": "Hey, I am Ximena Ferreira and I am a student who has been looking into the express surcharge at Thimble Lane Evening Classes. I pasted the extract in and worked through it step by step, which was really good fun. It was a friendly bit of digging and I came away with a much better feel for the process. Happy to help others who want to try it.",
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
  "qid": "q95f7f11c59",
  "text": "Hi,\nYaw Ofori here, just helping out and keen to get on. I'm looking into the parking charge at Hadley Bike Works and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "q21c9100a92",
  "text": "Mei Huang: Need a hand with the fitness orientation start date at Stonechat Park, I am on it but flat out.\ncoordinator: Fine, paste the extract over and I will help you read it.\ncoordinator: Stay with it, we are close to finishing.",
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
  "qid": "q3624ee7fa0",
  "text": "Yuki Hayashi, acting as a member, looked into the fitness orientation start date at Fernhill Housing Co-operative. The extract pasted in alongside it was read in a careful and orderly way. Readers who need the same check can use this route. Thank you for your attention.",
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
  "qid": "qa0b41dd60a",
  "text": "Good day,\nI am writing in as a member and wish to set out how the late return fee at Larkfield Coach Tours was examined. My name is Yuki Hayashi and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "qd81cda01e8",
  "text": "Requester: Mateo Quiroga\nTopic: the plant sale date at Oldbridge Language School\nContext: sorting out a booking\nI have pasted what was found below so the team can see it.",
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
  "qid": "q4415236432",
  "text": "Arjun Sethi: Kind greetings. I'm a member and would like to look into the fitness orientation start date at Ormsby Mart. I have pasted the findings below.\nofficer: Thank you, that is much appreciated.\nadmin: Please carry on from here.",
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
  "qid": "q21489e17a2",
  "text": "Ilinca Dobre handled a request by looking into the damage deposit at Foxhollow Poetry Festival in a formal manner. The findings were pasted below in full. This entry sets out the steps taken.",
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
  "qid": "q2a2c6a5e2d",
  "text": "Arjun Sethi: Need to check the damage deposit at Corrie Hall Institute, I am juggling a busy list at the moment.\ncolleague: Send the extract over and I will look at it with you.\ncolleague: Happy to help you work through it.",
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
  "qid": "qfbe9541717",
  "text": "Joaquin Lozano, a customer at the front desk, has asked about the league start date at Oakhaven Residents Association. The extract pasted in for this request is kept with the memo for reference. It is a routine matter and it is being handled in the usual way. Please keep this with the regular records.",
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
  "qid": "q779b3f1c7e",
  "text": "Raised by: Ansgar Holm\nOrganisation: Linnet Savings Club\nIssue: the season registration fee\nI am a student looking into this and have pasted the extract in for the desk.",
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
  "qid": "q6a9c886cb1",
  "text": "Kofi Mensah: Hiya all, I'm tidying up the records and wanted to look into the plant sale date at Wrenwick Nature Reserve. I've pasted what was found below, so have a look when you get a chance :)\ncolleague: Love that, thanks for doing it.\ncolleague: Happy to help with the tidy-up.",
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
  "qid": "q14a6202615",
  "text": "This internal memo records that Rohan Kapoor, a support agent, is handling a request about the desk rental fee at Tinkerwell Repairs. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "q3ed98161a2",
  "text": "Contact: Kristoffer Dahl\nOrganisation: Plumbridge Emporium\nIssue: the term start date\nI am a student who is looking into this and the extract is pasted here for the team.",
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
  "qid": "q14c3e8c7fd",
  "text": "Hi,\nFionnuala Doyle here, just helping out and keen to get on. I'm looking into the entry price at Meadowbank Dental Practice and I've pasted what was found below. Shout if you need anything else.\nCheers,",
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
  "qid": "q79ff524036",
  "text": "Dragana Petrovic: Sorry to rush you, this will be brief. I'm trying to get the plant sale date at Saltmarsh Exchange sorted and I've pasted what was found below.\nmanager: Sure, send it over.\nclerk: Got it, reading through it.",
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
  "qid": "q6595e735e6",
  "text": "Yaw Ofori: I need to get a reply out on the late return fee at Quayside Lettings Office and I am a bit rushed.\ncolleague: Pass me the extract and I will help you draft it.\ncolleague: Keep going, we are nearly through it.",
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
  "qid": "qe742e2d058",
  "text": "Camila Restrepo, a member, has been in touch about the desk rental fee at Lowmoor Heath Gardens. The findings are pasted below. Kindly keep this memo on file for the team.",
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
  "qid": "q8363286b90",
  "text": "Amir Castellano, a parent sorting out arrangements in a rush, looked into the electronics drop-off deadline at Haldane Travel Express. The extract was pasted in so that the details could be checked all together. Others in the same position may find this route useful.",
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
  "qid": "qaab81bbd8b",
  "text": "Good day,\nI am writing in as a member and wish to set out how the shoe hire charge at Wexcombe Hospice was examined. My name is Thandiwe Morrow and the extract is pasted in here for your records. I would be grateful for a tidy reply.\nYours faithfully,",
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
  "qid": "q54a51bcd4c",
  "text": "Arjun Sethi: Kind greetings. I'm a member and would like to look into the fitness orientation start date at Ormsby Mart. I have pasted the findings below.\nofficer: Thank you, that is much appreciated.\nadmin: Please carry on from here.",
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
  "qid": "qcba0d33b5a",
  "text": "This internal memo records that Rohan Kapoor, a support agent, is handling a request about the desk rental fee at Tinkerwell Repairs. The extract supplied for that request has been pasted in for reference. The matter is being dealt with in a formal and orderly manner. Please keep this with the usual support papers.",
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
  "qid": "q9338d43f50",
  "text": "Hello there,\nMy name is Arjun Sethi and I am planning ahead. I would like to look into the entry price at Crestline Climbing Gym, and I have pasted the findings below. Thanks for your help with this.\nWarm regards,",
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
