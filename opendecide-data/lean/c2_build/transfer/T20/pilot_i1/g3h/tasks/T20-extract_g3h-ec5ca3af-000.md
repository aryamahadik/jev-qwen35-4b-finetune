# G3-H extraction T20-extract_g3h-ec5ca3af-000 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot_i1/g3h/answers/T20-extract_g3h-ec5ca3af-000.json

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
  "qid": "qf8f1b49dac",
  "text": "Routing note: Plinth crew\nFionn Rasmussen raised this, see the incident record attached.",
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
  "qid": "qab24780b1b",
  "text": "Leocadia Yellin: filing this for Chickweed desk, the incident record is below.",
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
  "qid": "q3b4452c805",
  "text": "to: Dimmorrow cell\nfrom: Petra Chandrel\nnote: lovely to flag this, record below",
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
  "qid": "q2f9bc45de1",
  "text": "to: Kilnward unit\nspotted by Ignatius Ulmen, details pasted below, cheers!",
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
  "qid": "qf79fb49bb3",
  "text": "heads-up: Puffery crew\nfrom: Svetla Gidney\nnote: incident record attached, thank you",
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
  "qid": "q4c482f93c9",
  "text": "Hi Pewter rota,\nAssigned to you. Zaida Loveday raised it, record below.\nThanks",
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
  "qid": "qe9f540f8aa",
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
  "qid": "q00c02f6b84",
  "text": "Saoirse Feldmann: filing the record for Ferrule watch, see below.",
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
  "qid": "q24d1181956",
  "text": "Quillet rota, message from Ottilie Abbate: the incident record is attached.",
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
  "qid": "q4991247117",
  "text": "Dear Nettlewick cell,\nYours to take: Fionn Rasmussen raised it, details pasted below.\nKind regards",
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
  "qid": "q87500f7849",
  "text": "Chickweed desk, record handed on\nInes Valenti raised it, details attached.",
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
  "qid": "q0105bb9cb1",
  "text": "heads-up: Zabrine crew\nfrom: Fatou Szymanski\nnote: incident record attached, thank you",
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
  "qid": "qd84bd1f67e",
  "text": "to: Yarnwood watch\nfrom: Xiomara Jessop\nnote: lovely to flag this, record below",
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
  "qid": "q9881f771fe",
  "text": "Subject: handover\nAssigned team: Tamarisk cell, raised by Deepak Pruitt. Please see the incident details pasted below.",
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
  "qid": "q91a2448d12",
  "text": "Subject: handover\nFrom: Liesl Corvalan\nTeam: Wrenhald cell, the incident record is attached",
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
  "qid": "qa479ec287d",
  "text": "Bluewren rota, a friendly alert from Ines Valenti\ndetails attached, thank you kindly!",
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
  "qid": "q9af1020f3c",
  "text": "Redling desk, a friendly alert from Quirino Cruickshank\ndetails attached, thank you kindly!",
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
  "qid": "q0d3870c357",
  "text": "Subject: handover\nFrom: Yoana Lorimer\nTeam: Quince guild, the incident record is attached",
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
  "qid": "q3259e7d9da",
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
  "qid": "qbdfc54de23",
  "text": "Routing note: Redling desk\nOttilie Abbate raised this, see the incident record attached.",
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
  "qid": "q6ba9e97ea9",
  "text": "Dear Kelpie watch,\nYusra Tsang raised it. Assigned to you, details attached.\nBest",
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
  "qid": "q45af6ce1dc",
  "text": "Zorrel crew, a friendly alert from Wilhelmina Ismail\ndetails attached, thank you kindly!",
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
  "qid": "q4f88688a31",
  "text": "to: Alderwood guild\nspotted by Hiroshi Upadhyay, details pasted below, cheers!",
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
  "qid": "q44760e5f89",
  "text": "Hi Brackenwold rota,\nAssigned to you. Bruna Nemeth raised it, record below.\nThanks",
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
  "qid": "qf9a61074de",
  "text": "Alderwood guild, record handed on\nGulnara Tomczak raised it, details attached.",
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
  "qid": "q5a361adc11",
  "text": "Kelpie watch, message from Esmae Halvorsen: the incident record is attached.",
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
  "qid": "qe26990b783",
  "text": "Dmitry Pradhan: brisk filing for Corrowen desk, incident record pasted below.",
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
  "qid": "q3752c7acd2",
  "text": "heads-up: Corrowen desk\nfrom: Ambrose Mahlangu\nnote: incident record attached, thank you",
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
  "qid": "q03d52dca86",
  "text": "Subject: handover\nAssigned team: Tamarisk cell, raised by Deepak Pruitt. Please see the incident details pasted below.",
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
  "qid": "q719449d207",
  "text": "Kwabena Sorel: brisk filing for Ismere cell, incident record pasted below.",
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
  "qid": "q42dff8858a",
  "text": "Dear Tarrock squad,\nShamus Engstrom raised it. Assigned to you, details attached.\nBest",
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
  "qid": "q8fe4863c74",
  "text": "Subject: handover\nFrom: Liesl Corvalan\nTeam: Wrenhald cell, the incident record is attached",
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
  "qid": "q6fd1aabfd1",
  "text": "Message for Mistrel cell, from Kaveh Verhagen. Record attached, see below.",
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
  "qid": "q0a9eae0da7",
  "text": "to: Jessamy desk\nspotted by Benedykt Sundgren, details pasted below, cheers!",
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
  "qid": "q347975f1ab",
  "text": "Routing the record to Lantry crew. Dagny Adeyemi raised it, and the incident details follow below.",
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
  "qid": "q3bea9f507b",
  "text": "to: Yarnwood watch\nfrom: Xiomara Jessop\nnote: lovely to flag this, record below",
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
  "qid": "q5100952769",
  "text": "Fardel watch, message from Yrsa Kerrigan: the incident record is attached.",
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
  "qid": "q9c82a49029",
  "text": "Cinderlane squad, record handed on\nPetra Chandrel raised it, details attached.",
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
  "qid": "qd2761c9d03",
  "text": "to: Eskerline cell\nspotted by Yrsa Kerrigan, details pasted below, cheers!",
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
  "qid": "q9dd31d6ffc",
  "text": "Dear Yarrowen watch,\nYours to take: Liesl Corvalan raised it, details pasted below.\nKind regards",
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
  "qid": "q3d9dcdd1fc",
  "text": "Dear Fyrnwood squad,\nTadeusz Drumgold raised it. Assigned to you, details attached.\nBest",
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
  "qid": "qd81da64c1f",
  "text": "Subject: handover\nAssigned team: Thistledew unit, raised by Adaeze Nieminen. Please see the incident details pasted below.",
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
  "qid": "q42aa5d30e4",
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
  "qid": "q418f4a7652",
  "text": "To Galdra squad, from Ilse Quintero: record filed, details follow.",
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
  "qid": "q25787f707d",
  "text": "Routing this to Quillet rota. Perpetua Baptista raised it, and the incident record is attached.",
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
  "qid": "q81a32f1047",
  "text": "Idrel rota, message from Ulla Hovland: the incident record is attached.",
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
  "qid": "q83b4b02092",
  "text": "Dmitry Pradhan: brisk filing for Corrowen desk, incident record pasted below.",
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
  "qid": "q9a425f81d1",
  "text": "to: Kilnward unit\nspotted by Ignatius Ulmen, details pasted below, cheers!",
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
  "qid": "qf9420b202c",
  "text": "Message for Mistrel cell, from Kaveh Verhagen. Record attached, see below.",
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
  "qid": "q2c5d5c4584",
  "text": "heads-up: Puffery crew\nfrom: Svetla Gidney\nnote: incident record attached, thank you",
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
