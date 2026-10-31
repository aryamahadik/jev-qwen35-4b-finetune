# G3-H extraction T32-extract_g3h-9e89a47e-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/pilot_i2/g3h/answers/T32-extract_g3h-9e89a47e-005.json

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
  "qid": "qb6f30bb42d",
  "text": "Our flat chat about the house refit, saved by Sami for whoever lives here.",
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
  "qid": "q7697db9fdb",
  "text": "Saved by Elif, this talk about the care plan is just for family.",
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
  "qid": "q02ff2f6c0c",
  "text": "Committee chat on the music library, forwarded by Sami to the volunteers.",
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
  "qid": "q6220fe5a88",
  "text": "Volunteers, this is the new kit design thread that Lena shared with the committee.",
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
  "qid": "qbf63a8f604",
  "text": "Sami shared this so the family follows the garden makeover.",
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
  "qid": "q66e702771d",
  "text": "Team channel: the mobile release\nExported by Kai.",
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
  "qid": "qd136b6da5c",
  "text": "Forwarded by Nadia, these tenant replies are about the rent split plan for the file.",
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
  "qid": "qe0c5203f93",
  "text": "Casual chat for the flat, saved by Arlo, and it covers the student house hunt.",
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
  "qid": "qd2bf2e1c89",
  "text": "Shared by Ana, this back and forth with the client covers the documentary cut.",
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
  "qid": "q03520e6523",
  "text": "Team channel: the data cleanup\nShared by Leila.",
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
  "qid": "q9a6036904f",
  "text": "Volunteers, here is the choir tour thread that Omar forwarded for us.",
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
  "qid": "q7eadcdad73",
  "text": "Committee chat on the music library, forwarded by Oskar to the volunteers.",
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
  "qid": "q36cd0500fd",
  "text": "Attached chat: the spare room plan\nForwarded by: Ravi",
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
  "qid": "q7e10dbdebb",
  "text": "Subject: Forwarded chat on the menu redesign\nThe chat below comes from Kofi, copied as is for reference.",
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
  "qid": "qe9451304b9",
  "text": "Posted by Mo from the work channel: the desk plan.",
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
  "qid": "q3982487227",
  "text": "Subject: Saved thread about the new kit design\nThis export came from Lee and is pasted in full below.",
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
  "qid": "qdf387dc415",
  "text": "Committee chat on the training plan, shared by Tess with the volunteers.",
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
  "qid": "q7e4483306e",
  "text": "Nadia shared this so the family follows the street watch scheme.",
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
  "qid": "q5ce450c881",
  "text": "Shared by Tess, this thread covers the menu redesign as pasted from email.",
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
  "qid": "q09133bb1c2",
  "text": "Attached chat: the music library\nShared by: Oskar",
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
  "qid": "qee325e4856",
  "text": "Subject: Chat about the summer getaway\nA plain copy from Omar follows, exactly as exported.",
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
  "qid": "qf981b600f8",
  "text": "Subject: Chat about the guest welcome plan\nThe copy from Sami follows below as a plain record.",
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
  "qid": "q70ed459147",
  "text": "Team channel: the trade show push\nExported by Oskar.",
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
  "qid": "qd24ea27ac1",
  "text": "Shared by Lee for the committee, this is the group chat on the music library.",
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
  "qid": "q01acdbe354",
  "text": "Shared by Femi, this is where the cellar project gets planned.",
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
  "qid": "qc7f1d6778d",
  "text": "Leila forwarded this support chat, which is about the trade show push.",
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
  "qid": "qa8aeb91548",
  "text": "Shared by Rhea, a help-desk thread covering the website relaunch.",
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
  "qid": "q19cd6cf243",
  "text": "Committee chat on the training plan, shared by Tess with the volunteers.",
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
  "qid": "q1f9edbd1a9",
  "text": "Client thread on the online store move, saved by Omar for the project log.",
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
  "qid": "q66c9147248",
  "text": "Subject: Forwarded chat on the training plan\nFrom Priya, the thread below is passed on in its original form.",
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
  "qid": "qa66be9825e",
  "text": "Yuki saved these replies from the agent on the guest welcome plan.",
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
  "qid": "q1f2bc1be8c",
  "text": "Client thread on the wedding weekend, shared by Bruno for the project log.",
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
  "qid": "q11e53f6283",
  "text": "Committee chat on the music library, forwarded by Sami to the volunteers.",
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
  "qid": "q8bc3cefa15",
  "text": "Volunteers, this is the choir tour thread that Nadia shared with the committee.",
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
  "qid": "qc615369590",
  "text": "Volunteers, here is the choir tour thread that Omar forwarded for us.",
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
  "qid": "q588f161b97",
  "text": "Team channel: the lab move\nShared by: Leila.",
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
  "qid": "q4568c0036e",
  "text": "Messages with the letting agent about the kitchen refit, saved by Omar for the rental file.",
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
  "qid": "qda03970a4e",
  "text": "Shared by Zara for the committee, this is the group chat on the annual tour.",
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
  "qid": "q43cdfd6909",
  "text": "Shared by Femi, this is where the cellar project gets planned.",
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
  "qid": "q0ebd2f1d22",
  "text": "Volunteers, Ivo shared this with you about the new kit design.",
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
  "qid": "q31b1542092",
  "text": "Shared by Arlo, this thread covers the gallery show as pasted from email.",
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
  "qid": "q65b9148de5",
  "text": "Volunteers, here is the playground project thread that Oskar forwarded for us.",
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
  "qid": "q1b8e454725",
  "text": "Client thread on the online store move, saved by Omar for the project log.",
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
  "qid": "q083b623c6a",
  "text": "Yo flatmates, Tomas shared this chat about the autumn term budget, so chip in.",
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
  "qid": "qdabb122768",
  "text": "Yo flatmates, Tomas shared this chat about the autumn term budget, so chip in.",
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
  "qid": "q39883b03c6",
  "text": "Rhea shared this exchange with the client about the documentary cut.",
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
  "qid": "q972a3fdd96",
  "text": "Priya shared this channel export covering the visitor policy for the team.",
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
  "qid": "qeec331f5f9",
  "text": "Subject: Chat about the grant renewal\nThe copy from Omar follows below as a plain record.",
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
  "qid": "qb75fe97f6b",
  "text": "Parents and cousins, this is where we sort out the care plan. Saved by Lena.",
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
  "qid": "q1400b36183",
  "text": "Here is the plan for the speed bump plan, saved by Elif for the group.",
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
 }
]
