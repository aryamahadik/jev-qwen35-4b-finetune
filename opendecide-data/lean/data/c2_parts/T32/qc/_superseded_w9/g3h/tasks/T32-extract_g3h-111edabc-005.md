# G3-H extraction T32-extract_g3h-111edabc-005 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T32/qc/g3h/answers/T32-extract_g3h-111edabc-005.json

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
  "qid": "qfbda656ab1",
  "text": "Subject: Forwarded chat on the junior section\nThe thread below comes from Zara and is passed on as it is.",
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
  "qid": "q8e72621d1f",
  "text": "Arlo saved this so we stay on the same page about the garden shed build, mates.",
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
  "qid": "q1b7fb3c64a",
  "text": "Yo flatmates, Arlo shared this chat about the house rules debate, so chip in.",
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
  "qid": "qadf24a001b",
  "text": "Subject: Saved thread about the summer getaway\nThis export from Zara is pasted in full for readers who want it.",
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
  "qid": "qd25442cf22",
  "text": "Arlo saved this so we stay on the same page about the garden shed build, mates.",
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
  "qid": "q927da923c5",
  "text": "Yo flatmates, Rhea shared this chat about the flatmate contract terms, so chip in.",
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
  "qid": "q32767fd598",
  "text": "Team channel export, shared by Bruno, which is about the social media plan.",
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
  "qid": "q207826c8c7",
  "text": "Subject: Saved thread about the online store move\nThis export came from Ana and is pasted in full below.",
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
  "qid": "q7c2b8a09d0",
  "text": "Our flat chat about the house refit, shared by Ana for whoever lives here.",
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
  "qid": "q37fb8773f6",
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
  "qid": "q61a1fc4078",
  "text": "Team channel: the website relaunch\nShared by Ana.",
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
  "qid": "q31e7e864d9",
  "text": "Arlo forwarded this support chat, which is about the spring campaign.",
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
  "qid": "q56b5d73c96",
  "text": "Subject: Forwarded chat on the platform rewrite\nThe thread below comes from Lena and is passed on as it is.",
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
  "qid": "qa1d9620fb3",
  "text": "Oskar forwarded this exchange with the landlord on the student house hunt.",
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
  "qid": "qd671f725a9",
  "text": "Attached chat: the choir tour\nShared by: Ivo",
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
  "qid": "q6c107cf411",
  "text": "Subject: Saved thread about the care plan\nThis export came from Jonas and is pasted in full below.",
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
  "qid": "q74353cb75c",
  "text": "Our flat chat about the house refit, shared by Ana for whoever lives here.",
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
  "qid": "q24d02513c7",
  "text": "Volunteers, Leila shared this with you about the playground project.",
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
  "qid": "q06371ab103",
  "text": "Oskar shared this so the family follows the care plan.",
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
  "qid": "q1521883556",
  "text": "Volunteers, here is the ground upgrade chat that Arlo forwarded to us.",
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
  "qid": "qee9d3bad0a",
  "text": "Greta saved this so we stay on the same page about the quiet street fund, mates.",
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
  "qid": "qbcb34ec9e8",
  "text": "Parents and cousins, this is where we sort out the house rules debate. Saved by Yuki.",
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
  "qid": "qed48515257",
  "text": "Shared by Sami for the committee, this is the group chat on the volunteer roster.",
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
  "qid": "q28cb93efb0",
  "text": "Subject: Saved thread about the garden shed build\nThis export from Kofi is pasted in full for readers who want it.",
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
  "qid": "q16d89640f7",
  "text": "Bruno forwarded this for the committee as we dig in on the training plan.",
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
  "qid": "qe78a23533a",
  "text": "Bruno shared this channel export, covering the onboarding flow for the team.",
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
  "qid": "q0f5ca70d75",
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
  "qid": "q45ac5aa446",
  "text": "Read up on the speed bump plan, flatmates, as Lee exported it.",
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
  "qid": "q6dee446165",
  "text": "Arlo forwarded this support chat, which is about the spring campaign.",
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
  "qid": "q29a01b7d2d",
  "text": "Zara forwarded this exchange with the landlord on the rent split plan.",
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
  "qid": "q2288f0c6c1",
  "text": "Yo flatmates, Wren shared this chat about the bathroom refit, so chip in.",
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
  "qid": "qe8187bcc22",
  "text": "We have been planning the family history here, shared by Mo.",
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
  "qid": "q6b99b698f0",
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
  "qid": "q9b289e4133",
  "text": "Shared by Dara, a help-desk thread covering the payment setup.",
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
  "qid": "qf7116d2163",
  "text": "Parents and cousins, this is where we sort out the house refit. Saved by Greta.",
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
  "qid": "q585f3760e3",
  "text": "Our flat chat about the cottage refresh, shared by Kai for whoever lives here.",
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
  "qid": "q2869ed470e",
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
  "qid": "q453e434058",
  "text": "Priya shared this family chat about the packing plan for the relatives.",
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
  "qid": "qd309227b5a",
  "text": "Subject: Chat about the online store move\nThe copy from Priya follows below as a plain record.",
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
  "qid": "q8a3ec40bfa",
  "text": "Attached chat: the platform rewrite\nForwarded by: Arlo",
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
  "qid": "q2ddf7969b1",
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
  "qid": "qd8cdbb8ec1",
  "text": "Subject: Saved thread about the junior section\nThis export from Ravi is pasted in full for readers who want it.",
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
  "qid": "q44df99eb1c",
  "text": "Parents and cousins, this is where we sort out the care plan. Saved by Rhea.",
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
  "qid": "q02b99757d5",
  "text": "We are getting ready for the home adaptations, and Ivo shared this chat with us.",
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
  "qid": "qc0259703a1",
  "text": "Leila forwarded this exchange with the landlord on the guest welcome plan.",
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
  "qid": "qfd105e706c",
  "text": "We are getting ready for the house rules debate, and Yuki shared this chat with us.",
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
  "qid": "q00272985a6",
  "text": "Parents and cousins, this is where we sort out the garden shed build. Saved by Dara.",
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
  "qid": "q421aa78a96",
  "text": "We are getting ready for the family photo book, and Lena shared this chat with us.",
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
  "qid": "q7af63c61c3",
  "text": "Subject: Chat about the family day out\nBelow is a copy that came from Omar, pasted as found.",
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
  "qid": "q36e194921c",
  "text": "Here is the thread on the old house restoration, posted by Dara for the house.",
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
 }
]
