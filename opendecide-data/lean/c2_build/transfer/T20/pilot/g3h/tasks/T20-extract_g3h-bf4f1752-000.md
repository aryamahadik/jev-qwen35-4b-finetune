# G3-H extraction T20-extract_g3h-bf4f1752-000 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot/g3h/answers/T20-extract_g3h-bf4f1752-000.json

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
  "qid": "q4aeedb8212",
  "text": "Hello Eskerline cell,\nYrsa Kerrigan raised this; assigning to you, record attached.\nRegards",
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
  "qid": "qb099de2bec",
  "text": "Dear Dunmarrow unit,\nCorentin Orellana raised it. Assigned to you, details attached.\nBest",
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
  "qid": "q30ab51e328",
  "text": "Quince guild, record routed\nWiebke Kaczmarek raised it, details below.",
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
  "qid": "q5c23752735",
  "text": "Hello Fardel watch,\nThis is yours; Zosia Lasko raised it, and details are attached.\nCheers",
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
  "qid": "q392ceb44f4",
  "text": "Subject: handover\nAssigned team: Mirelle guild, raised by Bronwen Ostrowski. Please see the incident details pasted below.",
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
  "qid": "qc6366ba02e",
  "text": "Brackenwold rota, message from Corentin Orellana: the incident record is attached.",
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
  "qid": "q931c831289",
  "text": "Runbook entry added by Jovana Waddington for Bluewren rota, with the incident record attached.",
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
  "qid": "qc0f54f4da0",
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
  "qid": "q30294713ef",
  "text": "Subject: handover\nFrom: Bruna Nemeth\nTeam: Dunmarrow unit, the incident record is attached",
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
  "qid": "q9b45723463",
  "text": "to: Brackenwold rota\nspotted by Corentin Orellana, details pasted below, cheers!",
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
  "qid": "qdce0cb9a45",
  "text": "Runbook entry added by Yrsa Kerrigan for Eskerline cell, with the incident record attached.",
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
  "qid": "q0d073ff51d",
  "text": "Chickweed desk, record routed\nJovana Waddington raised it, details below.",
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
  "qid": "qc2fb012f8e",
  "text": "Added to the team runbook by Maelys Zarnecki for Tinderwick unit.\nThe record is pasted below.",
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
  "qid": "q9d7e603cae",
  "text": "Ottilie Abbate is forwarding this to Penkeld guild, and the incident details are attached.",
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
  "qid": "q8f5dfafd42",
  "text": "Runbook note added by Ottavio Dressler for Lapwing unit. The incident record follows below.",
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
  "qid": "q2e2edd7ca4",
  "text": "To Valerian cell, from Vanya Halbrook: record filed, details follow.",
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
  "qid": "qc101a1eca8",
  "text": "Added to the team runbook by Zeljka Lindahl for Mattock squad.\nThe record is pasted below.",
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
  "qid": "q8901f161b5",
  "text": "Petra Chandrel: brisk filing for Dimmorrow cell, incident record pasted below.",
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
  "qid": "qb23601685b",
  "text": "Ospreth watch, a friendly alert from Ulric Ilyasova\ndetails attached, thank you kindly!",
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
  "qid": "qd5b5cf5e24",
  "text": "Dear Grenvary crew,\nYours to take: Bertil Nwosu raised it, details pasted below.\nKind regards",
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
  "qid": "q7be810dc28",
  "text": "to: Ospreth watch\nspotted by Svetla Gidney, details pasted below, cheers!",
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
  "qid": "q926b434800",
  "text": "to: Ulmarth squad\nfrom: Kasimir Wieczorek\nnote: lovely to flag this, record below",
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
  "qid": "q83e560a175",
  "text": "For Fyrnwood squad: entry added by Tadeusz Drumgold, with the incident details pasted below.",
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
  "qid": "q17d17745d7",
  "text": "For Cinderlane squad: a runbook entry, added by Rhys Ekwueme.\nSee the incident details below.",
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
  "qid": "q6c6b843756",
  "text": "Hello Rookery unit,\nThis is yours; Fenella Raskin raised it, and details are attached.\nCheers",
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
  "qid": "q2da14e1268",
  "text": "Courteously relaying the note of Zosia Lasko, written for Fardel watch, and the incident record is attached below.",
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
  "qid": "qc9b23cb36a",
  "text": "Katalin Xuereb: brisk filing for Chickweed desk, incident record pasted below.",
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
  "qid": "q39a2d3d2e0",
  "text": "Hi Redling desk,\nTaking this to you: Perpetua Baptista raised it, record below.\nRegards",
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
  "qid": "qa949f31bd3",
  "text": "Ospreth watch, message from Tamsin Haddow: the incident record is attached.",
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
  "qid": "qebae19cf1b",
  "text": "Sending this to Zinnia desk. Mairead Zelinsky raised it; the incident record is pasted below.",
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
  "qid": "q201fc7807d",
  "text": "Hello Eskerline cell,\nYrsa Kerrigan raised this; assigning to you, record attached.\nRegards",
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
  "qid": "q2f6128ffdc",
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
  "qid": "q074e46818c",
  "text": "to: Ospreth watch\nspotted by Svetla Gidney, details pasted below, cheers!",
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
  "qid": "q184b14abc9",
  "text": "Hi Eskerline cell,\nAssigned to you. Yrsa Kerrigan raised it, record below.\nThanks",
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
  "qid": "q00ed8b88d2",
  "text": "Routing the record to Yarnwood watch. Xiomara Jessop raised it, and the incident details follow below.",
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
  "qid": "q0449fe3d55",
  "text": "Hello Quillet rota,\nThis is yours; Perpetua Baptista raised it, and details are attached.\nCheers",
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
  "qid": "qc64fcfd98e",
  "text": "For Zinnia desk: entry added by Mairead Zelinsky, with the incident details pasted below.",
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
  "qid": "q15b827ade6",
  "text": "Hello Pewter rota,\nAbimbola Mendoza raised this; assigning to you, record attached.\nRegards",
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
  "qid": "qf334c7a25a",
  "text": "Sending this to Mattock squad. Zeljka Lindahl raised it; the incident record is pasted below.",
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
  "qid": "qa84bd80e73",
  "text": "Subject: handover\nAssigned team: Thistledew unit, raised by Brigid Ogunbiyi. Please see the incident details pasted below.",
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
  "qid": "q3d5d0a96a3",
  "text": "Rhodri Oduya: brisk filing for Elderun unit, incident record pasted below.",
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
  "qid": "qf31e6f4091",
  "text": "Routing the record to Sablevane squad. Jorunn Rennick raised it, and the incident details follow below.",
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
  "qid": "q2d1f077da2",
  "text": "Hi Brackenwold rota,\nAssigned to you. Ambrose Mahlangu raised it, record below.\nThanks",
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
  "qid": "qfd33e37366",
  "text": "Opening of the incident review draft.\nWritten by Vesna Ibarra for Halvard guild, with the record provided below.",
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
  "qid": "q08761ad666",
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
  "qid": "qff792988cd",
  "text": "Assigned team: Bluewren rota\nRaised by: Jovana Waddington. Kindly see the incident details pasted below.",
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
  "qid": "q5f253a245f",
  "text": "Routing this to Larkspur unit. Aurelio Mazur raised it, and the incident record is attached.",
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
  "qid": "q44e3592f9d",
  "text": "Hello Pewter rota,\nAbimbola Mendoza raised this; assigning to you, record attached.\nRegards",
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
  "qid": "q2abb6d7117",
  "text": "Sending this to Ferrule watch. Quenton Dombrowski raised it; the incident record is pasted below.",
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
  "qid": "q2e6ef2dde4",
  "text": "For Cinderlane squad: a runbook entry, added by Rhys Ekwueme.\nSee the incident details below.",
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
