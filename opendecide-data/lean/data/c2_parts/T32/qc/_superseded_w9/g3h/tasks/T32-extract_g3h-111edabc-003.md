# G3-H extraction T32-extract_g3h-111edabc-003 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g3h/answers/T32-extract_g3h-111edabc-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "owner": <value or null>, "topic": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qaad83f704f",
  "text": "Ravi shared this to pin down the garden makeover, housemates.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q81b056f7db",
  "text": "Here is the plan for the loft conversion, saved by Lena for the group.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q6a4200c008",
  "text": "Subject: Saved chat on the platform rewrite\nHere is the export from Ivo, for the record.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the data cleanup",
     "the mobile release",
     "the onboarding flow",
     "the platform rewrite"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q20cbe0c05d",
  "text": "Here is the quiet street fund, posted by Malik for the family to read.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qc98f94d724",
  "text": "Yuki shared this to pin down the quiet street fund, housemates.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qe94a3d3e7e",
  "text": "Subject: Chat about the documentary cut\nThe copy from Leila follows below as a plain record.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the campaign edit",
     "the documentary cut",
     "the showreel refresh",
     "the sound mix"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q10a920a928",
  "text": "Subject: Forwarded chat on the quiet street fund\nThe chat below comes from Bruno, copied as is for reference.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qbb2cad7f2f",
  "text": "Our flat chat about the loft conversion, saved by Ines for whoever lives here.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qae171ec0f5",
  "text": "Mo saved these replies from the agent on the flatmate contract terms.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the autumn term budget",
     "the flatmate contract terms",
     "the rent split plan",
     "the student house hunt"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qda24108ed2",
  "text": "Here is the plan for the loft conversion, saved by Lena for the group.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q2076ba3f50",
  "text": "Messages with the letting agent about the kitchen refit, forwarded by Dara for the rental file.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the balcony garden project",
     "the flat upgrade list",
     "the kitchen refit",
     "the tenancy renewal talks"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qae9d7c4f3d",
  "text": "Shared by Ravi, this is where the house rules debate gets planned.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the big house plan",
     "the cellar project",
     "the house rules debate",
     "the old house restoration"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qaa81282856",
  "text": "Our flat chat about the house rules debate, shared by Mo for whoever lives here.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the big house plan",
     "the cellar project",
     "the house rules debate",
     "the old house restoration"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q9b40d10195",
  "text": "Committee chat on the new kit design, shared by Hana with the volunteers.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the annual tour",
     "the new kit design",
     "the sponsor search",
     "the training plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q172363156d",
  "text": "Posted by Ines from the work channel, the grant renewal thread.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the field survey",
     "the grant renewal",
     "the lab move",
     "the peer review"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qbe8a484ccb",
  "text": "Forwarded by Dara: a help-desk thread covering the field survey.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the field survey",
     "the grant renewal",
     "the lab move",
     "the peer review"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q9aadc9d01c",
  "text": "Posted by Priya from the work channel: the office refit.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the desk plan",
     "the office refit",
     "the staff handbook",
     "the visitor policy"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q50b0755fa8",
  "text": "Saved by Oskar, this talk about the garden shed build is just for family.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the allotment expansion",
     "the garden shed build",
     "the kitchen garden project",
     "the vegetable plot plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qddc0aa9527",
  "text": "Forwarded by Oskar: a help-desk thread covering the choir tour.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the choir tour",
     "the music library",
     "the new repertoire",
     "the winter concert"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q0c651a25dc",
  "text": "Subject: Forwarded chat on the allotment expansion\nFrom Mo, the thread below is shared as it stands.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the allotment expansion",
     "the garden shed build",
     "the kitchen garden project",
     "the vegetable plot plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q71cf97a7a6",
  "text": "Forwarded by Oskar: a help-desk thread covering the website relaunch.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the social media plan",
     "the spring campaign",
     "the trade show push",
     "the website relaunch"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q0065bea368",
  "text": "Forwarded by Kofi, these tenant replies are about the student house hunt for the file.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the autumn term budget",
     "the flatmate contract terms",
     "the rent split plan",
     "the student house hunt"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q4ebe3f1528",
  "text": "Our flat chat about the street watch scheme, saved by Wren for whoever lives here.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qfdb79ed2d7",
  "text": "Our flat chat about the house refit, saved by Tess for whoever lives here.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q7ad4bf0f1c",
  "text": "Subject: Saved thread about the volunteer roster\nThis export from Mo is pasted in full for readers who want it.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the new term plans",
     "the playground project",
     "the school fundraiser",
     "the volunteer roster"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q94d762c416",
  "text": "Subject: Chat about the payment setup\nA plain copy from Yuki follows, exactly as exported.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the holiday catalogue",
     "the online store move",
     "the payment setup",
     "the shop rebuild"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q719f6d57c7",
  "text": "Forwarded by Kofi, these tenant replies are about the student house hunt for the file.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the autumn term budget",
     "the flatmate contract terms",
     "the rent split plan",
     "the student house hunt"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q2edc03ff88",
  "text": "Exported by Mo, this is the full back and forth on the wedding weekend.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the big day",
     "the guest list",
     "the honeymoon album",
     "the wedding weekend"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q2c2cc366d3",
  "text": "Subject: Forwarded chat on the loft conversion\nFrom Ravi, the thread below is shared as it stands.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qbc071c9e9d",
  "text": "Mo shared this so the family follows the street watch scheme.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q7207c0901a",
  "text": "Committee chat on the new term plans, shared by Lee with the volunteers.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the new term plans",
     "the playground project",
     "the school fundraiser",
     "the volunteer roster"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qf8427c48b1",
  "text": "Chat attached to a support case about the holiday catalogue, shared by Ivo.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the holiday catalogue",
     "the online store move",
     "the payment setup",
     "the shop rebuild"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qdd7087cb1e",
  "text": "Team channel: the spring campaign\nExported by Jonas.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the social media plan",
     "the spring campaign",
     "the trade show push",
     "the website relaunch"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q4b890df903",
  "text": "Casual chat for the flat, saved by Omar, and it covers the allotment expansion.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the allotment expansion",
     "the garden shed build",
     "the kitchen garden project",
     "the vegetable plot plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q60580030b5",
  "text": "Posted by Bruno from the work channel, the visitor policy thread.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the desk plan",
     "the office refit",
     "the staff handbook",
     "the visitor policy"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qefea49cbbe",
  "text": "Forwarded by Zara: a help-desk thread covering the summer getaway.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the packing plan",
     "the summer getaway",
     "the travel plans",
     "the trip itinerary"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q9b7520a5e0",
  "text": "Subject: Forwarded chat on the new kit design\nThe thread below comes from Zara and is passed on as it is.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the annual tour",
     "the new kit design",
     "the sponsor search",
     "the training plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q0aff069683",
  "text": "Casual chat for the flat, saved by Leila, and it covers the big house plan.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the big house plan",
     "the cellar project",
     "the house rules debate",
     "the old house restoration"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q9b441725eb",
  "text": "Here is the plan for the bathroom refit, saved by Sami for the group.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the bathroom refit",
     "the garden makeover",
     "the house refit",
     "the loft conversion"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q03f99dd818",
  "text": "Subject: Forwarded chat on the rebrand package\nFrom Mo, the thread below is passed on in its original form.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the gallery show",
     "the menu redesign",
     "the rebrand package",
     "the store makeover"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qe34ff73bb1",
  "text": "Attached chat: the new term plans\nShared by: Omar",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the new term plans",
     "the playground project",
     "the school fundraiser",
     "the volunteer roster"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qbe3744e79a",
  "text": "Read up on the summer lets season, flatmates, as Bruno exported it.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the cottage refresh",
     "the guest review drive",
     "the guest welcome plan",
     "the summer lets season"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qafa5dc7f98",
  "text": "Team channel: the office refit\nShared by: Zara.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the desk plan",
     "the office refit",
     "the staff handbook",
     "the visitor policy"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q1b9d12e225",
  "text": "Leila shared this channel export covering the onboarding flow for the team.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the data cleanup",
     "the mobile release",
     "the onboarding flow",
     "the platform rewrite"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q226a26f7aa",
  "text": "Kai shared this so the family follows the garden shed build.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the allotment expansion",
     "the garden shed build",
     "the kitchen garden project",
     "the vegetable plot plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qc83ce79a74",
  "text": "Exported by Mo, this is the full back and forth on the wedding weekend.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the big day",
     "the guest list",
     "the honeymoon album",
     "the wedding weekend"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q07b518a83e",
  "text": "Nadia saved this so we stay on the same page about the quiet street fund, mates.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the front garden scheme",
     "the quiet street fund",
     "the speed bump plan",
     "the street watch scheme"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "q4e43df8338",
  "text": "Subject: Forwarded chat on the attic conversion idea\nFrom Nadia, the thread below is shared as it stands.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the attic conversion idea",
     "the lodger house rules",
     "the shared kitchen scheme",
     "the spare room plan"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qd64689f0bb",
  "text": "Ravi shared this so the music library is easy to follow for the volunteers.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the choir tour",
     "the music library",
     "the new repertoire",
     "the winter concert"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 },
 {
  "qid": "qef35cd03da",
  "text": "Chat attached to a support case about the autumn term budget, shared by Oskar.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the autumn term budget",
     "the flatmate contract terms",
     "the rent split plan",
     "the student house hunt"
    ]
   },
   {
    "field": "owner",
    "type": "name",
    "describe": "the person who saved or shared the chat"
   }
  ]
 }
]
