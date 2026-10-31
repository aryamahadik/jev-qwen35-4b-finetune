# G3-H extraction T20-extract_g3h-bf4f1752-003 (family T20)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/pilot/g3h/answers/T20-extract_g3h-bf4f1752-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 20. Answers expected: 20 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "reporter": <value or null>, "team": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q3d1a0f4ebf",
  "text": "to: Ambergris guild\nfrom: Zorica Lemaire\nalert: thanks, the record is pasted below",
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
  "qid": "q913aec0c40",
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
  "qid": "qe0205cc38e",
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
  "qid": "q40cdf8a3dd",
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
  "qid": "qc69477964a",
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
  "qid": "q2d7df843a2",
  "text": "For Hasterell guild: a runbook entry, added by Cathal Ostergaard.\nSee the incident details below.",
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
  "qid": "q5ad79f0811",
  "text": "For Obsidel watch: a runbook entry, added by Fionn Rasmussen.\nSee the incident details below.",
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
  "qid": "q4f60038fe7",
  "text": "Added to the team runbook by Dmitry Pradhan for Corrowen desk.\nThe record is pasted below.",
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
  "qid": "q3b1a71aa39",
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
  "qid": "qe93b89e4ad",
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
  "qid": "q27321253ac",
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
  "qid": "q35d75655a3",
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
  "qid": "q32c6a7c539",
  "text": "Assigned team: Penkeld guild\nRaised by: Ottilie Abbate. Kindly see the incident details pasted below.",
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
  "qid": "qc3219fb053",
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
  "qid": "q88dafef57a",
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
  "qid": "q55f63568f6",
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
  "qid": "q57a4ccbb57",
  "text": "Corentin Orellana: brisk filing for Dunmarrow unit, incident record pasted below.",
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
  "qid": "q58dcb82522",
  "text": "From: Bruna Nemeth\nTo: Brackenwold rota\nRecord: see below",
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
  "qid": "q6e55e61170",
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
  "qid": "q913b66cdaf",
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
 }
]
