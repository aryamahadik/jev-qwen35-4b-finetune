# G3-H extraction T20-extract_g3h-bf4f1752-001 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot/g3h/answers/T20-extract_g3h-bf4f1752-001.json

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
  "qid": "q0518441b76",
  "text": "Halvard guild, message from Vesna Ibarra: the incident record is attached.",
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
  "qid": "q15824eda54",
  "text": "Mirelle guild, message from Yusra Tsang: the incident record is attached.",
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
  "qid": "qf9e172c2dd",
  "text": "Ines Valenti is forwarding this to Bluewren rota, and the incident details are attached.",
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
  "qid": "q780ddc8892",
  "text": "Added to the team runbook by Ilse Quintero for Galdra squad.\nThe record is pasted below.",
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
  "qid": "q0df4d4d44a",
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
  "qid": "q6454717063",
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
  "qid": "q363275e4af",
  "text": "Runbook entry added by Zaida Loveday for Quarry desk, with the incident record attached.",
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
  "qid": "q1492f199a3",
  "text": "Cinderlane squad, record handed on\nRhys Ekwueme raised it, details attached.",
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
  "qid": "q477359ef23",
  "text": "Opening of the incident review draft.\nWritten by Ayesha Mottram for Eskerline cell, with the record provided below.",
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
  "qid": "q5152d3872e",
  "text": "Hello Dunlin unit,\nThis is yours; Kwabena Sorel raised it, and details are attached.\nCheers",
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
  "qid": "q6fdadbde29",
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
  "qid": "q03112c67c2",
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
  "qid": "qa62c1ad2a9",
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
  "qid": "q9f9fc6e25d",
  "text": "heads-up for Dunlin unit from Ilse Quintero\ndetails: see the incident record attached, cheers",
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
  "qid": "q5a2ba2ac59",
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
  "qid": "q71d2b6fe75",
  "text": "Sending this to Corvane desk. Sunniva Teague raised it; the incident record is pasted below.",
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
  "qid": "q9f851ad3d9",
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
  "qid": "q7c318e9830",
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
  "qid": "qd3b1e810dd",
  "text": "Raised by: Rasmus Dvorsky\nAssigned to: Redling desk\nSubject: handover, kindly see the incident record below",
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
  "qid": "qb539fa0713",
  "text": "Subject: handover\nRaised by: Lorcan Yakubu, for Tinderwick unit. Kindly see the incident details pasted below.",
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
  "qid": "q719a2824aa",
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
  "qid": "q9f0e939c4f",
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
  "qid": "qbb5257253f",
  "text": "Opening lines of the incident review being drafted: written by Eudora Rydberg for Yardarm watch, record provided below.",
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
  "qid": "qe7e32550ba",
  "text": "Opening of the incident review draft.\nWritten by Tamsin Haddow for Nutmeg cell, with the record provided below.",
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
  "qid": "q8f4615ef4b",
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
  "qid": "qf3004b8e56",
  "text": "Opening of the incident review draft.\nWritten by Ayesha Mottram for Eskerline cell, with the record provided below.",
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
  "qid": "qd309dfc4f7",
  "text": "Added to the team runbook by Ruairi Rauscher for Ironwick guild.\nThe record is pasted below.",
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
  "qid": "qda375d197b",
  "text": "Ines Valenti is forwarding this to Bluewren rota, and the incident details are attached.",
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
  "qid": "q19be88b28c",
  "text": "Penkeld guild, message from Quirino Cruickshank: the incident record is attached.",
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
  "qid": "q7d35414bf5",
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
  "qid": "qe3eda332b9",
  "text": "For Yarrowen watch: entry added by Jorunn Rennick, with the incident details pasted below.",
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
  "qid": "q45f5649ff3",
  "text": "For Yarrowen watch: entry added by Jorunn Rennick, with the incident details pasted below.",
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
  "qid": "q0eeaef5b39",
  "text": "Dear Jessamy desk,\nBenedykt Sundgren raised it. Assigned to you, details attached.\nBest",
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
  "qid": "qe5e21c6585",
  "text": "Opening of the incident review draft.\nWritten by Quirino Cruickshank for Penkeld guild, with the record provided below.",
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
  "qid": "q7d292f02bc",
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
  "qid": "qde8e2efb04",
  "text": "From: Zeljka Lindahl\nTo: Mattock squad\nRecord: see below",
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
  "qid": "qa6ab3d5e3d",
  "text": "Assigned team: Valerian cell\nRaised by: Thora Farrimond. Kindly see the incident details pasted below.",
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
  "qid": "q0a78c272e9",
  "text": "Hi Jessamy desk,\nAssigned to you. Aurelio Mazur raised it, record below.\nThanks",
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
  "qid": "q655617db79",
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
  "qid": "qb40537d70c",
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
  "qid": "q7c4feb87e4",
  "text": "From: Lazar Yoshida\nTo: Brambleset unit\nRecord: see below",
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
  "qid": "qc7c4c59131",
  "text": "Added to the team runbook by Ruairi Rauscher for Ironwick guild.\nThe record is pasted below.",
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
  "qid": "q37408de953",
  "text": "Runbook note by Rafaela Dumont for Galdra squad, with the incident record attached.",
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
  "qid": "qf3d1469508",
  "text": "Cinderlane squad, record handed on\nRhys Ekwueme raised it, details attached.",
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
  "qid": "q3e9e4339dc",
  "text": "Dimmorrow cell, record routed\nQuenton Dombrowski raised it, details below.",
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
  "qid": "q7627c056f7",
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
  "qid": "q7347d1bdba",
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
  "qid": "q910709e2aa",
  "text": "Arkwold rota, message from Ursel Gorczyca: the incident record is attached.",
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
  "qid": "q35001fad88",
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
  "qid": "q12aaab6d4d",
  "text": "Ospreth watch, message from Rudi Fairhurst: the incident record is attached.",
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
