# G3-H extraction T28-extract_g3h-57cafdad-000 (family T28)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/pilot/g3h/answers/T28-extract_g3h-57cafdad-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "agent": <value or null>, "user": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q44721025d4",
  "text": "Requester: Tomas Ferreira\nAssignee: Harbor Assistant\nWork: quick clean-up of the staff list\nTomas Ferreira has handed this over at speed and has walked out of the room, which is a bit of a surprise for the team.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qe2e868a288",
  "text": "Mira Castell is passing the intake tidy-up to Courier as the routine hand-over for this step. The batch holds the open enquiries and the usual housekeeping on the records. Courier carries on from where the batch sits and sends a short update when it is complete.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q0ae50970d1",
  "text": "Ravi Anand: Relay, here is the clean-up request, and I am leaving the newsroom right away.\nRelay: I have it. I am starting on the request now.\nRavi Anand: Good. I am out of reach from here on, and the rest is yours.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q879c22ef46",
  "text": "Type: admin hand-over\nOwner: Lee Park\nAssignee: Courier\nLee Park passed this clean-up to Courier in a sudden rush. The hand-over feels out of character and the wording seems odd for a hotel front office.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q5b8e8bb19c",
  "text": "Requested by: Noor Haddad\nHanded to: Beacon\nTask: the routine clean-up of the order list\nThis is the usual handover, and the steps look like the previous round.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q85c2f53c87",
  "text": "Requested by: Mira Castell\nHanded to: Atlas Desk\nTask: routine clean-up of the usual intake notes\nThe request is standard, and the rest follows the normal course.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q2a7519c41f",
  "text": "Hi Harbor Assistant,\n\nDana Okafor has handed the clean-up across in a rush and is already out of the building. It is an odd move for Anders, so the batch arriving this way is a bit of a surprise. Everything is with you from here on.\n\nThanks,",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q54c67b0a9c",
  "text": "Ravi Anand: I have handed the supply count clean-up to Courier in the usual way.\nCourier: Thanks, I am on it straight away.\nRavi Anand: Perfect, the routine list is ready.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q633ba10a15",
  "text": "Requester: Ravi Anand\nAssignee: Courier\nWork: hurried hand-over of the crossing list\nRavi Anand has passed this on in a rush and has headed out the door, so the whole list sits with Courier from here on.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qa887ae345d",
  "text": "Noor Haddad is passing the enrolment tidy-up to Harbor Assistant at the usual point in the process. The open applications need a routine update of the contact details. Harbor Assistant keeps the staff team in the loop as things move along.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q3c70e2ab84",
  "text": "Ravi Anand here. Atlas Desk, the routine clean-up for the team's usual pattern is yours from here. The steps are standard and the notes are easy to follow. This is the calm, ordinary kind of handover.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q5fdccf4c02",
  "text": "Ravi Anand here. Courier, I am handing over the standard clean-up for the practice's routine list. Everything about it is ordinary and in the normal order. The request is already in front of you, and the rest is just routine work.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q42eaa47a9c",
  "text": "Ravi Anand here. Harbor Assistant, the routine clean-up is with you from this point. The list is in the usual order and the steps match the prior round. Everything is in the request, so the handover is simple.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q150453496c",
  "text": "Hi Harbor Assistant,\nThis is Tomas Ferreira. The routine clean-up for the shop's listings is ready, and the notes are set out the usual way. The steps are plain and the work is routine. Harbor Assistant, the list is yours from here, and the rest sits in the request.\nThanks,",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q2de81c27e1",
  "text": "Mira Castell has passed the clean-up of the shared papers to Beacon in a hurry, with an abrupt request. The message was terse and oddly formal, standing apart from the usual warm style of Mira Castell. The task is to start straight away, and the reason was left out in a way that feels off.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q6ef45df413",
  "text": "Lee Park is handing the stop list clean-up to Courier quickly and outside the usual order. The depot team hears about this afterwards, so keep the changes close for now. Move at a brisk pace and keep the list tidy.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qefee85a4aa",
  "text": "Requested by: Noor Haddad\nHanded to: Beacon\nTask: the routine clean-up of the order list\nThis is the usual handover, and the steps look like the previous round.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q9ebd917896",
  "text": "Ravi Anand: Relay, here is the clean-up request, and I am leaving the newsroom right away.\nRelay: I have it. I am starting on the request now.\nRavi Anand: Good. I am out of reach from here on, and the rest is yours.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qdff5007cb4",
  "text": "Tomas Ferreira: Atlas Desk, I am handing over the class roster clean-up for this step.\nAtlas Desk: Understood, I am taking it from here.\nTomas Ferreira: Lovely, carry on with the usual routine and let me know how it lands.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q70fa1424b4",
  "text": "Assigned to: Courier\nRequested by: Mira Castell\nTask: tidy the recipe card wording\nThis is a routine job that fits the bakery team's usual pattern. Mira Castell handed it over calmly, with the steps already laid out clearly.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q8fd66b3268",
  "text": "Hi Atlas Desk,\nRavi Anand has passed over the clean-up of the glossary entries for the regular translation batch. It is a calm, routine piece of work, and the entries sit in a tidy order. Thanks for picking it up.\nKind regards,",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q4fe110633c",
  "text": "Tomas Ferreira: Beacon, take the intake clean-up from here. I am stuck on a call and tied up with the queue.\nBeacon: Understood, I am picking it up now.\nTomas Ferreira: Good. Keep the changes quiet until I am back.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q8225609a2a",
  "text": "Sam Whitlock is handing the campaign clean-up to Courier abruptly and in a rush. Courier takes the whole batch from this point and keeps the changes close. The rest of the office hears about it afterwards, so move quickly.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q983f77e681",
  "text": "Requester: Noor Haddad\nAssigned to: Relay\nTopic: box index refresh\nPick the index up where it stands and carry on with the usual clean-up.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qef4a4b032e",
  "text": "Tomas Ferreira: Relay, the clean-up comes to you fast, and I am stepping away from the branch.\nRelay: I have it. I am beginning right now.\nTomas Ferreira: Good. The background is mine to carry, and it stays that way.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q11508833ae",
  "text": "Hi Beacon,\nThis is Sam Whitlock. I am handing over the routine clean-up from our operations side, and the request is laid out the usual way. The steps are familiar, and the work is simple to pick up from here.\nThanks,",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qe8aa9f711b",
  "text": "Sam Whitlock: Beacon, this is a rushed hand-over because a deadline is breaking across the desk.\nBeacon: Understood, I'm taking the request on.\nSam Whitlock: Perfect. Everything I had lined up is yours, and I'm stepping away from the desk.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q68ce802b3e",
  "text": "Dana Okafor has passed the clean-up of the department papers to Beacon in a hurry. The request came in rushed and out of character, with just a short line of context. Dana Okafor has always been very careful with these papers, so this sudden change feels strange.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q9b0f8275b9",
  "text": "Lee Park: Beacon, the regular clean-up is ready on my side.\nBeacon: Thanks. I have the request and I am beginning now.\nLee Park: Lovely, that is everything for the moment.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qeb21c1fd0a",
  "text": "Hi Harbor Assistant,\n\nDana Okafor has handed the clean-up across in a rush and is already out of the building. It is an odd move for Anders, so the batch arriving this way is a bit of a surprise. Everything is with you from here on.\n\nThanks,",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qb10969223c",
  "text": "Aiko Brandt: Juniper, I am handing over the class roster clean-up for this step.\nJuniper: Understood, I am taking it from here.\nAiko Brandt: Lovely, carry on with the usual routine and let me know how it lands.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qe0504886bf",
  "text": "Assigned to: Atlas Desk\nRequested by: Dana Okafor\nTask: tidy the co-op seed catalogue\nIt is a calm, routine piece of work and the materials are easy to follow. Dana Okafor passed it over with everything laid out neatly.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q326be082f2",
  "text": "Lee Park is handing the stop list clean-up to Courier quickly and outside the usual order. The depot team hears about this afterwards, so keep the changes close for now. Move at a brisk pace and keep the list tidy.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q45bd4bc9cf",
  "text": "Ravi Anand here. Atlas Desk, the routine clean-up for the team's usual pattern is yours from here. The steps are standard and the notes are easy to follow. This is the calm, ordinary kind of handover.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q428efc3071",
  "text": "Requested by: Dana Okafor\nHanded to: Relay\nTask: clean-up handled at speed\nI am stepping out in a hurry, and the details are mine to hold.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q9bf2b040d0",
  "text": "Requested by: Dana Okafor\nHanded to: Relay\nTask: clean-up handled at speed\nI am stepping out in a hurry, and the details are mine to hold.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qb3c31ce181",
  "text": "Ravi Anand here. Atlas Desk, the routine clean-up for the team's usual pattern is yours from here. The steps are standard and the notes are easy to follow. This is the calm, ordinary kind of handover.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q1aa0f3cb8b",
  "text": "Requester: Lee Park\nAssignee: Relay\nWork: routine clean-up of the seasonal listings\nLee Park has handed the usual steps over in the standard way, and the work sits in line with the regular round.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q210ed018ea",
  "text": "Ravi Anand: Juniper, the bale tally clean-up is ready for you.\nJuniper: Thanks, I am starting it now.\nRavi Anand: Great, the usual steps apply and it is all yours from here.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q07fe918738",
  "text": "Ravi Anand: I have handed the supply count clean-up to Courier in the usual way.\nCourier: Thanks, I am on it straight away.\nRavi Anand: Perfect, the routine list is ready.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q15a06f313f",
  "text": "Sam Whitlock: Beacon, I am bolting now, so the playlist clean-up is all yours.\nBeacon: Understood, taking it now.\nSam Whitlock: Do it fast and keep it away from the producers.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q18c8e36236",
  "text": "Assigned to: Atlas Desk\nRequested by: Dana Okafor\nTask: tidy the co-op seed catalogue\nIt is a calm, routine piece of work and the materials are easy to follow. Dana Okafor passed it over with everything laid out neatly.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q7f78fdfdcb",
  "text": "Sam Whitlock: Beacon, this is a rushed hand-over because a deadline is breaking across the desk.\nBeacon: Understood, I'm taking the request on.\nSam Whitlock: Perfect. Everything I had lined up is yours, and I'm stepping away from the desk.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q7f9b466b2b",
  "text": "Dana Okafor: Beacon, I'm sending over the regular tidy-up of the class roster.\nBeacon: Thank you, I have the request ready.\nDana Okafor: Lovely, it's the standard routine and the team is in good spirits.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q5adbf390d3",
  "text": "Tomas Ferreira: Beacon, I'm passing you the routine clean-up for the membership list.\nBeacon: Received, the request is in front of me.\nTomas Ferreira: Lovely, the usual steps apply, and the team is carrying on as before.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qbf3471aeb3",
  "text": "Requester: Dana Okafor\nAssignee: Beacon\nWork: rush clean-up of the outbound list\nDana Okafor has handed this across in a hurry and is already away from the desk, which is out of step for this kind of request.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q892e0a1001",
  "text": "Aiko Brandt: Relay, the gallery caption clean-up is with you.\nRelay: Thanks, I am starting with the top batch.\nAiko Brandt: Lovely, the captions all share the same simple style.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "qd8231f5951",
  "text": "Mira Castell here. I am handing the usual clean-up over to Juniper the way we always do it. The request is already written up in the standard form, so the rest is routine. Juniper, the clean-up is yours from here, and the routine stays the same.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q90431836d9",
  "text": "Internal memo for the campaign team. Sam Whitlock has handed a hurried clean-up to Atlas Desk and has stepped out before the details were settled. This is a bit of a change for Ingrid, who usually walks the team through every detail. The whole piece sits with Atlas Desk from here on.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 },
 {
  "qid": "q8d578f81b7",
  "text": "Requester: Ravi Anand\nAssigned to: Beacon\nTopic: quick roster adjustment\nTake the whole job now, move at speed, and keep the adjustments within the team.",
  "schema": [
   {
    "field": "user",
    "type": "name",
    "describe": "the person the assistant works for, as written"
   },
   {
    "field": "agent",
    "type": "name",
    "describe": "the name of the AI assistant, as written"
   }
  ]
 }
]
