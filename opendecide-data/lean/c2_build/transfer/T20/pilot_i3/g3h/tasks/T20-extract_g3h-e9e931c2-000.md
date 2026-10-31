# G3-H extraction T20-extract_g3h-e9e931c2-000 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot_i3/g3h/answers/T20-extract_g3h-e9e931c2-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "reporter": <value or null>, "team": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q9caad09b6a",
  "text": "to: Mattock squad\nspotted by Yannick Kaminsky, details pasted below, cheers!",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q325b1af118",
  "text": "Dear Mirelle guild,\nDagny Adeyemi raised it. Assigned to you, details attached.\nBest",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q26c5d89a58",
  "text": "Leocadia Yellin: filing this for Dandrell unit, the incident record is below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q71344469d6",
  "text": "Raised by: Rasmus Dvorsky\nAssigned to: Quillet rota\nSubject: handover, kindly see the incident record below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qce6a570bea",
  "text": "heads-up: Ospreth watch\nfrom: Svetla Gidney\nnote: incident record attached, thank you",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q8850431ef1",
  "text": "Hello Ospreth watch,\nThis is yours; Svetla Gidney raised it, and details are attached.\nCheers",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qde0f83a1c0",
  "text": "Plinth crew, record handed on\nFionn Rasmussen raised it, details attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q96e0122755",
  "text": "Ferrule watch, record handed on\nRhys Ekwueme raised it, details attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q838b09cc38",
  "text": "Ngaio Abrahams: brisk filing for Brambleset unit, incident record pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q4d63ef5382",
  "text": "Orrery guild, record routed\nAbimbola Mendoza raised it, details below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q3e260a634e",
  "text": "Routing this to Cinderlane squad. Rhys Ekwueme raised it, and the incident record is attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q88dd837cf8",
  "text": "to: Mattock squad\nspotted by Yannick Kaminsky, details pasted below, cheers!",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q570cf72556",
  "text": "Dear Scrimshaw unit,\nShamus Engstrom raised it. Assigned to you, details attached.\nBest",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qc9d66bc405",
  "text": "to: Yarnwood watch\nfrom: Zorica Lemaire\nnote: lovely to flag this, record below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q5bf5d8057b",
  "text": "Hi Cinderlane squad,\nAssigned to you. Quenton Dombrowski raised it, record below.\nThanks",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qa335632c00",
  "text": "Handing this over to Jackdaw rota, from Lenka Yeboah; the incident details are pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qb66dd80505",
  "text": "Yrsa Kerrigan: filing this for Eskerline cell, the incident record is below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q4ac3ba70f3",
  "text": "Hi Puffery crew,\nTaking this to you: Ulric Ilyasova raised it, record below.\nRegards",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qace74f1136",
  "text": "to: Sablevane squad\nfrom: Kiran Pembrick\nnote: lovely to flag this, record below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q1a87d3f6a9",
  "text": "heads-up: Tarrock squad\nfrom: Vanya Halbrook\nnote: incident record attached, thank you",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q61a25fe85b",
  "text": "Raised by: Ruairi Rauscher\nAssigned to: Jaspernet rota\nSubject: handover, kindly see the incident record below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qa80f42aceb",
  "text": "Sending this to Obsidel watch. Fionn Rasmussen raised it; the incident record is pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q6dc7db6c14",
  "text": "Hi Puffery crew,\nTaking this to you: Ulric Ilyasova raised it, record below.\nRegards",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q916569c4a7",
  "text": "Routing this to Penkeld guild. Quirino Cruickshank raised it, and the incident record is attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q0f2967aaa1",
  "text": "Bruna Nemeth: brisk filing for Brackenwold rota, incident record pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qf84c0527a1",
  "text": "Subject: handover\nAssigned team: Whinmoor cell, raised by Adaeze Nieminen. Please see the incident details pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qccd0d4d049",
  "text": "Routing note: Ferrule watch\nQuenton Dombrowski raised this, see the incident record attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q6dd651df58",
  "text": "Hi Hedgerow crew,\nTaking this to you: Lenka Yeboah raised it, record below.\nRegards",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qb893dc46a0",
  "text": "To Dunlin unit, from Ilse Quintero: record filed, details follow.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q5ace17c4b9",
  "text": "Routing the record to Kelpie watch. Esmae Halvorsen raised it, and the incident details follow below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q0d20c78067",
  "text": "To Dunlin unit, from Ilse Quintero: record filed, details follow.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q690a73c144",
  "text": "Rookery unit, record routed\nGunnhild Strudwick raised it, details below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qe74052166d",
  "text": "Sending this to Penkeld guild. Perpetua Baptista raised it; the incident record is pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q9e5fb3cf36",
  "text": "Subject: handover\nAssigned team: Chickweed desk, raised by Katalin Xuereb. Please see the incident details pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q0cfa8c19b4",
  "text": "Dear Scrimshaw unit,\nShamus Engstrom raised it. Assigned to you, details attached.\nBest",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q34fab896c6",
  "text": "Routing this to Penkeld guild. Quirino Cruickshank raised it, and the incident record is attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q694d0ec2e8",
  "text": "Routing the record to Kelpie watch. Esmae Halvorsen raised it, and the incident details follow below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qfc54b338bc",
  "text": "to: Eskerline cell\nfrom: Ximena Jurado\nalert: thanks, the record is pasted below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q21c7975ded",
  "text": "to: Zorrel crew\nfrom: Zorica Lemaire\nalert: thanks, the record is pasted below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qce0259baf9",
  "text": "Routing the record to Kelpie watch. Esmae Halvorsen raised it, and the incident details follow below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "qb66a2d2e4f",
  "text": "Sending this to Obsidel watch. Fionn Rasmussen raised it; the incident record is pasted below.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q24a249b722",
  "text": "Hi Hedgerow crew,\nTaking this to you: Lenka Yeboah raised it, record below.\nRegards",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q7f01f2120e",
  "text": "heads-up: Corrowen desk\nfrom: Bruna Nemeth\nnote: incident record attached, thank you",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q6305374016",
  "text": "heads-up: Zabrine crew\nfrom: Hiroshi Upadhyay\nnote: incident record attached, thank you",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q283ce42383",
  "text": "Routing note: Ferrule watch\nQuenton Dombrowski raised this, see the incident record attached.",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q9698d71800",
  "text": "Quillet rota, a friendly alert from Ottilie Abbate\ndetails attached, thank you kindly!",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q8f984a23a0",
  "text": "to: Zorrel crew\nfrom: Zorica Lemaire\nalert: thanks, the record is pasted below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q6f596db230",
  "text": "to: Dimmorrow cell\nfrom: Quenton Dombrowski\nnote: lovely to flag this, record below",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q89d62ba708",
  "text": "heads-up: Ospreth watch\nfrom: Svetla Gidney\nnote: incident record attached, thank you",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 },
 {
  "qid": "q91a97d6b7b",
  "text": "Dear Brackenwold rota,\nBruna Nemeth raised it. Assigned to you, details attached.\nBest",
  "schema": [
   {
    "field": "team",
    "type": "name",
    "describe": "the team handling the incident, as written"
   },
   {
    "field": "reporter",
    "type": "name",
    "describe": "the person who reported it, as written"
   }
  ]
 }
]
