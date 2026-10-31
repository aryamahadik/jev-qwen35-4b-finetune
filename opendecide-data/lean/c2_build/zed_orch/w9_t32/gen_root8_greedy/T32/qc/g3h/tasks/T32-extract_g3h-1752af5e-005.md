# G3-H extraction T32-extract_g3h-1752af5e-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t32/gen_root8/T32/qc/g3h/answers/T32-extract_g3h-1752af5e-005.json

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
  "qid": "q0218dec2aa",
  "text": "Exported by Hana, this is the back and forth on the honeymoon album.",
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
  "qid": "q6c5db33672",
  "text": "Subject: Chat about the autumn term budget\nBelow, with Zara named as the source, is the chat as exported.",
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
  "qid": "qbaf7f22c17",
  "text": "Subject: Saved thread about the balcony garden project\nThis export from Tomas is pasted in full for readers who want it.",
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
  "qid": "q549fd53c3d",
  "text": "Shared by Bruno, this is where the family history gets planned.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family history",
     "the guest travel plans",
     "the reunion planning",
     "the reunion weekend"
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
  "qid": "q6b49dbde9b",
  "text": "Here we plan the summer visits together, and Dara saved this for the family.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family day out",
     "the family photo book",
     "the holiday memories",
     "the summer visits"
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
  "qid": "q4af626077b",
  "text": "Subject: Saved thread about the guest welcome plan\nThis export came from Leila and is pasted in full below.",
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
  "qid": "q14a61e7c4d",
  "text": "Saved by Kofi, this talk about the packing plan is just for family.",
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
  "qid": "qd237f139d7",
  "text": "Subject: Saved thread about the mobile release\nThis export came from Mo and is pasted in full below.",
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
  "qid": "qb723a2b807",
  "text": "Tenant and landlord back-and-forth on the summer lets season, saved by Nadia.",
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
  "qid": "q36fd413340",
  "text": "Volunteers, Ana shared this with you about the kit sponsorship.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the ground upgrade",
     "the junior section",
     "the kit sponsorship",
     "the league run"
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
  "qid": "q055df6871b",
  "text": "We have been planning the reunion weekend here, shared by Leila.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family history",
     "the guest travel plans",
     "the reunion planning",
     "the reunion weekend"
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
  "qid": "q8700f953b0",
  "text": "Kofi shared this so the annual tour is easy to follow for the volunteers.",
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
  "qid": "qbcac144d54",
  "text": "We are getting ready for the summer getaway, and Sami shared this chat with us.",
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
  "qid": "q9b204d5ee6",
  "text": "Forwarded by Arlo, this thread on the music library stays attached to the ticket.",
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
  "qid": "q1129b3b921",
  "text": "Shared by Tomas, this back and forth with the client covers the campaign edit.",
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
  "qid": "q0771657936",
  "text": "Subject: Chat about the cottage refresh\nA plain copy from Ana follows, exactly as exported.",
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
  "qid": "q7fce2c8fc0",
  "text": "Ravi shared this channel export, covering the mobile release for the team.",
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
  "qid": "qe81a965a7e",
  "text": "Subject: Saved thread about the family photo book\nThis export came from Sami and is pasted in full below.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family day out",
     "the family photo book",
     "the holiday memories",
     "the summer visits"
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
  "qid": "q7b2f3bce74",
  "text": "We are getting ready for the reunion weekend, and Tomas shared this chat with us.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family history",
     "the guest travel plans",
     "the reunion planning",
     "the reunion weekend"
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
  "qid": "q96a0f0c30a",
  "text": "Femi saved this so we stay on the same page about the street watch scheme, mates.",
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
  "qid": "q1f49e39549",
  "text": "Subject: Saved thread about the mobile release\nThis export came from Mo and is pasted in full below.",
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
  "qid": "q732916c20d",
  "text": "Our flat chat about the house refit, shared by Nadia for whoever lives here.",
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
  "qid": "q825bb09099",
  "text": "Saved by Kai, this talk about the garden shed build is just for family.",
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
  "qid": "q67b962c05d",
  "text": "Hana saved this exchange with the client about the big day.",
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
  "qid": "q79bb723c9c",
  "text": "Shared by Lena, this is where the street watch scheme gets planned.",
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
  "qid": "q4450b671dc",
  "text": "Subject: Forwarded chat on the family history\nFrom Sami, the thread below is shared as it stands.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family history",
     "the guest travel plans",
     "the reunion planning",
     "the reunion weekend"
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
  "qid": "qfe2f27b711",
  "text": "Attached chat: the documentary cut\nShared by: Ana.",
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
  "qid": "qc6da7f980c",
  "text": "Greta forwarded this support chat, which is about the payment setup.",
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
  "qid": "qeafddc7177",
  "text": "Forwarded by Ravi, this thread on the shop rebuild stays attached to the ticket.",
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
  "qid": "qb61023e1ba",
  "text": "Shared by Elif for the committee, this is the group chat on the ground upgrade.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the ground upgrade",
     "the junior section",
     "the kit sponsorship",
     "the league run"
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
  "qid": "qe869f9764c",
  "text": "Shared by Greta, a help-desk thread covering the data cleanup.",
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
  "qid": "qba1dd8c215",
  "text": "Ravi shared this to pin down the street watch scheme, housemates.",
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
  "qid": "q46ca48e5f8",
  "text": "Lena exported this channel chat about the field survey for the team.",
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
  "qid": "q215b6034e4",
  "text": "Yo flatmates, Femi shared this chat about the street watch scheme, so chip in.",
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
  "qid": "q08eda6283a",
  "text": "Casual chat for the flat, saved by Priya, and it covers the lodger house rules.",
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
  "qid": "qcdd9c70198",
  "text": "Subject: Chat about the holiday memories\nBelow is a copy that came from Zara, pasted as found.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the family day out",
     "the family photo book",
     "the holiday memories",
     "the summer visits"
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
  "qid": "qee0b5e7ba5",
  "text": "Greta shared this to pin down the autumn term budget, housemates.",
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
  "qid": "qd47321cc8c",
  "text": "Yo flatmates, Ana shared this chat about the guest welcome plan, so chip in.",
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
  "qid": "qb751cc2c52",
  "text": "Greta forwarded this support chat, which is about the payment setup.",
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
  "qid": "q3aab3a7f24",
  "text": "Saved by Malik, this talk about the cellar project is just for family.",
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
  "qid": "q92db2c84b2",
  "text": "Subject: Chat about the house refit\nA plain copy from Zara follows, exactly as exported.",
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
  "qid": "q5814f275d7",
  "text": "Yuki forwarded these replies from the agent on the guest welcome plan for the file.",
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
  "qid": "qee52c82f26",
  "text": "Elif shared this family chat about the travel plans for the relatives.",
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
  "qid": "qa114e3b716",
  "text": "Saved by Dara, this talk about the care plan is just for family.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the care plan",
     "the caring rota",
     "the home adaptations"
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
  "qid": "q04f1eec97f",
  "text": "Here we plan the kitchen garden project together, and Ravi saved this for the family.",
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
  "qid": "q6431a3eeb1",
  "text": "Forwarded by Ravi, this thread on the league run stays attached to the ticket.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the ground upgrade",
     "the junior section",
     "the kit sponsorship",
     "the league run"
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
  "qid": "q0cc86d7426",
  "text": "Committee chat on the kit sponsorship, forwarded by Yuki to the volunteers.",
  "schema": [
   {
    "field": "topic",
    "type": "category",
    "describe": "what the chat is about, as written",
    "choices": [
     "the ground upgrade",
     "the junior section",
     "the kit sponsorship",
     "the league run"
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
  "qid": "qede2f62434",
  "text": "Subject: Saved chat on the old house restoration\nHere is the export from Sami, for the record.",
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
  "qid": "q90c3f08f65",
  "text": "Subject: Chat about the guest list\nBelow is a copy that came from Yuki, pasted as found.",
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
  "qid": "q75175d99d0",
  "text": "Volunteers, Jonas shared this with you about the playground project.",
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
 }
]
