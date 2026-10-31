# G3-H extraction T32-extract_g3h-ca3160b3-002 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/pilot_i1/g3h/answers/T32-extract_g3h-ca3160b3-002.json

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
  "qid": "q92241dbf96",
  "text": "Here is the thread on the student house hunt, posted by Jonas for the house.",
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
  "qid": "q383cbaee47",
  "text": "Subject: Chat about the playground project\nBelow, with Bruno named as the source, is the chat as exported.",
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
  "qid": "q2f77320127",
  "text": "Volunteers, here is the volunteer roster thread that Kofi forwarded for us.",
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
  "qid": "qb468466b7d",
  "text": "Attached chat: the ground upgrade\nShared by: Ivo.",
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
  "qid": "q4c80d15acb",
  "text": "Shared by Dara, this thread covers the big day as pasted from email.",
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
  "qid": "q9f56206279",
  "text": "Team channel: the field survey\nExported by Bruno.",
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
  "qid": "qdca90d9478",
  "text": "Shared by Ines, this thread covers the online store move as pasted from email.",
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
  "qid": "q54b260e2f7",
  "text": "Team channel: the lab move\nShared by: Arlo.",
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
  "qid": "q26031bef5c",
  "text": "Yuki shared this exchange with the client about the documentary cut.",
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
  "qid": "q093415aa36",
  "text": "Subject: Chat about the spare room plan\nA plain copy from Nadia follows, exactly as exported.",
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
  "qid": "q7e5a5306a1",
  "text": "Subject: Chat about the online store move\nBelow is a copy that came from Priya, pasted as found.",
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
  "qid": "q8ca4177f21",
  "text": "Subject: Chat about the loft conversion\nBelow is a copy that came from Wren, pasted as found.",
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
  "qid": "qee88886d65",
  "text": "Client thread on the big day, shared by Tomas for the project log.",
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
  "qid": "qd2fc5c4172",
  "text": "Shared by Ravi, a help-desk thread covering the spring campaign.",
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
  "qid": "qebd059e44e",
  "text": "Subject: Chat about the junior section\nBelow, with Jonas named as the source, is the chat as exported.",
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
  "qid": "q55c10752ee",
  "text": "Forwarded by Wren, this thread on the holiday catalogue stays attached to the ticket.",
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
  "qid": "q4b96f805c4",
  "text": "Ines shared this channel export, covering the grant renewal for the team.",
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
  "qid": "qfcda2c2cec",
  "text": "Messages with the letting agent about the student house hunt, forwarded by Jonas for the rental file.",
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
  "qid": "q9a03becc41",
  "text": "Tenant and agent back-and-forth on the spare room plan, forwarded by Ivo.",
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
  "qid": "qcb5c55c06d",
  "text": "Ana forwarded this for the committee, covering the winter concert.",
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
  "qid": "qd600b83c44",
  "text": "Lena shared this so the family follows the loft conversion.",
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
  "qid": "q0ae57ff55f",
  "text": "Subject: Saved thread about the quiet street fund\nThis export from Leila is pasted in full for readers who want it.",
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
  "qid": "q201d2e9504",
  "text": "Volunteers, this is the annual tour thread that Greta shared with the committee.",
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
  "qid": "q344630c8e4",
  "text": "Committee chat on the training plan, forwarded by Kofi to the volunteers.",
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
  "qid": "qf3b07bf430",
  "text": "Committee chat on the new term plans, shared by Mo with the volunteers.",
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
  "qid": "q4be9f1b92a",
  "text": "Shared by Leila, this is where the bathroom refit gets planned.",
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
  "qid": "q486f2989de",
  "text": "Shared by Priya, this thread covers the store makeover as pasted from email.",
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
  "qid": "qcae55bd0a6",
  "text": "Committee chat on the sponsor search, shared by Ravi with the volunteers.",
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
  "qid": "q30cb7c4eb9",
  "text": "Subject: Forwarded chat on the summer visits\nFrom Ana, the thread below is shared as it stands.",
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
  "qid": "q037e990dfb",
  "text": "Subject: Chat about the cottage refresh\nThe copy from Sami follows below as a plain record.",
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
  "qid": "q745fd91ae7",
  "text": "Casual chat for the flat, saved by Leila, and it covers the rent split plan.",
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
  "qid": "q22069a9a81",
  "text": "Subject: Forwarded chat on the menu redesign\nThe chat below comes from Rhea, copied as is for reference.",
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
  "qid": "q65f2cb3d42",
  "text": "Zara shared this so the rent split plan is easy to find, flatmates.",
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
  "qid": "q218c1d2fa6",
  "text": "Shared by Omar for the committee, this is the group chat on the sponsor search.",
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
  "qid": "q6948bb4428",
  "text": "Our flat chat about the autumn term budget, shared by Ivo for whoever lives here.",
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
  "qid": "q61d6562e6b",
  "text": "Messages with the letting agent about the balcony garden project, saved by Tomas for the rental file.",
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
  "qid": "qb69abf650c",
  "text": "Subject: Saved thread about the quiet street fund\nThis export from Leila is pasted in full for readers who want it.",
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
  "qid": "qdcfcc3dc3b",
  "text": "Subject: Saved thread about the lodger house rules\nThis export from Leila is pasted in full for readers who want it.",
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
  "qid": "q2a71478815",
  "text": "Committee chat on the new term plans, shared by Mo with the volunteers.",
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
  "qid": "q5548b9b443",
  "text": "Tenant and agent back-and-forth on the shared kitchen scheme, saved by Wren.",
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
  "qid": "q05b15afc1c",
  "text": "Casual chat for the flat, saved by Ines, and it covers the quiet street fund.",
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
  "qid": "q8a8fdee983",
  "text": "Kai shared this so the kit sponsorship is easy to follow for the volunteers.",
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
  "qid": "q1791ded177",
  "text": "Zara shared this so the rent split plan is easy to find, flatmates.",
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
  "qid": "qb644752ee8",
  "text": "Volunteers, here is the choir tour thread that Ana forwarded for us.",
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
  "qid": "q84f6cab4dd",
  "text": "Team channel: the platform rewrite\nShared by: Nadia.",
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
  "qid": "q0b2e8575e8",
  "text": "Messages with the letting agent about the tenancy renewal talks, forwarded by Tomas for the rental file.",
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
  "qid": "qb29086f6f6",
  "text": "Subject: Saved thread about the grant renewal\nThis export from Tomas is pasted in full for readers who want it.",
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
  "qid": "q7886b77c5d",
  "text": "Messages with the letting agent about the student house hunt, forwarded by Jonas for the rental file.",
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
  "qid": "q615ad2e5fb",
  "text": "Read up on the spare room plan, flatmates, as Priya exported it.",
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
  "qid": "q7d9e4ffe0a",
  "text": "Subject: Forwarded chat on the vegetable plot plan\nThe thread below comes from Omar and is passed on as it is.",
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
 }
]
