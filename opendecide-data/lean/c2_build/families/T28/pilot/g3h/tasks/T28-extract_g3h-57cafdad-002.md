# G3-H extraction T28-extract_g3h-57cafdad-002 (family T28)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/pilot/g3h/answers/T28-extract_g3h-57cafdad-002.json

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
  "qid": "q37bd01ace1",
  "text": "Dana Okafor: Courier, I'm handing this over straight away because I'm leaving the building.\nCourier: Understood, the request is in front of me.\nDana Okafor: It's all yours from this point, and I'm out of touch after this.",
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
  "qid": "qda59802a0d",
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
  "qid": "q2da9d47444",
  "text": "Tomas Ferreira: Relay, I'm handing you this at speed and I'm heading out straight after.\nRelay: Understood, the request is open in front of me.\nTomas Ferreira: Good. The lot is yours from here on, and I'm out of reach.",
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
  "qid": "q3334e08a3e",
  "text": "Internal memo for the site team. Mira Castell has passed a rushed clean-up to Relay and has left the site in a hurry. That is a bit of a change for Leila, who usually stays with each job until it is finished. The rest of the crew is keeping a close eye on things.",
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
  "qid": "q7caf3dc321",
  "text": "This is an internal memo from Sam Whitlock. The rest of the work has been passed to Atlas Desk in a rush, and the usual hand-over was carried out in an odd, hurried way. Sam Whitlock wants everything finished before others look at it, and offered a strange reason for the change.",
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
  "qid": "q27e3564594",
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
  "qid": "q0e5cfd8449",
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
  "qid": "q1df8d8b6c1",
  "text": "Tomas Ferreira: Beacon, I am handing you this in a hurry and I am heading out the door.\nBeacon: Understood. I have the request and I am starting the clean-up.\nTomas Ferreira: Good. This is off the books, and the reason is mine.",
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
  "qid": "q9dee1fd8a4",
  "text": "Hi Courier,\nRavi Anand has passed the translation glossary tidy-up over to you. It is a calm, regular job and the terms already sit in a tidy order. The pace is relaxed and the team is glad to have the extra help.\nBest,",
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
  "qid": "q2df24fa580",
  "text": "Lee Park: Harbor Assistant, I am leaving, so the intake sorting is all on you now.\nHarbor Assistant: Okay, I am on it.\nLee Park: Fast is best, and keep the batch to yourself.",
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
  "qid": "q7ce1a11307",
  "text": "Hi Harbor Assistant,\nDana Okafor has passed the print queue clean-up over in a rush. The message was odd and very abrupt, standing apart from the usual calm style. The request came with only a quick line and a sudden tone.\nBest,",
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
  "qid": "qc2457fe132",
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
  "qid": "q5620372a8e",
  "text": "Tomas Ferreira writing. Juniper, this handover is quick and a bit odd. I am walking out of the studio straight away, and the reason is locked in my head. The clean-up is all yours, and the request is already waiting for you.",
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
  "qid": "qb5fb2964d6",
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
  "qid": "q40ea059580",
  "text": "Sam Whitlock: Harbor Assistant, I am passing you this request in a hurry, and I am locking my desk on the way out.\nHarbor Assistant: I have it and I am beginning the clean-up now.\nSam Whitlock: Good. The details stay between us, and I mean that.",
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
  "qid": "q20b2ecbee4",
  "text": "Internal memo for the admissions team. Dana Okafor has handed this round of routine clean-up to the assistant Harbor Assistant in the usual way. The work covers the standard intake list and the regular follow-up calls. The rest of the team carries on as usual while this is underway.",
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
  "qid": "qe816fd7c16",
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
  "qid": "qde61dcf090",
  "text": "Sam Whitlock: Courier, I am bolting now, so the playlist clean-up is all yours.\nCourier: Understood, taking it now.\nSam Whitlock: Do it fast and keep it away from the producers.",
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
  "qid": "qf69beeb9cb",
  "text": "Tomas Ferreira is passing the route clean-up to Courier in a hurry, since the handover is happening mid-task. Keep the work close to the chest and send the updates only to this desk. The depot staff hear about it at a later point, so move quickly.",
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
  "qid": "q7be5f514c9",
  "text": "Mira Castell here. Courier, I am handing you the regular clean-up, laid out the way the team prefers. The steps match the earlier round, and the notes are waiting for you. From here the rest is yours, at your own pace.",
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
  "qid": "q0617819746",
  "text": "Sam Whitlock has passed the clean-up of the department papers to Courier in a hurry. The request came in rushed and out of character, with just a short line of context. Sam Whitlock has always been very careful with these papers, so this sudden change feels strange.",
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
  "qid": "qe0d11c8f39",
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
  "qid": "qb456a672be",
  "text": "Assigned to: Courier\nRequested by: Sam Whitlock\nTask: sort the council agendas into a neat order\nSam Whitlock passed this on in the ordinary way, and the routine is well understood. The job is calm and plain.",
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
  "qid": "qa7c261b5e3",
  "text": "Sam Whitlock has passed the clean-up of the department papers to Courier in a hurry. The request came in rushed and out of character, with just a short line of context. Sam Whitlock has always been very careful with these papers, so this sudden change feels strange.",
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
  "qid": "q108121847e",
  "text": "Hi Harbor Assistant,\nLee Park has passed the routine ticket-tagging clean-up to you in the usual way. It is a steady, ordinary job, and the team is happy to hand it over. The tags already sit in a clear, familiar pattern.\nWarm regards,",
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
  "qid": "q463bb52a06",
  "text": "Hi Relay,\nThis is Dana Okafor. I am handing over the routine clean-up from our operations side, and the request is laid out the usual way. The steps are familiar, and the work is simple to pick up from here.\nThanks,",
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
  "qid": "qdb08efc45e",
  "text": "Requester: Ravi Anand\nAssigned to: Juniper\nTopic: photo register clean-up\nPick up the register where it sits and keep the work steady from here.",
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
  "qid": "qa806d90ed3",
  "text": "Noor Haddad here. This handover to Beacon is abrupt, and I am stepping out of the department straight away. The usual order of things is turned upside down for this job. The reason belongs to me alone for now.",
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
  "qid": "qe5b04e663e",
  "text": "Noor Haddad: Atlas Desk, I have handed the object label clean-up over to you.\nAtlas Desk: Got it, I am taking a look at the labels.\nNoor Haddad: Brilliant, the wording already follows the usual pattern.",
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
  "qid": "q7c80322bc1",
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
  "qid": "qa96ff7b3b4",
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
  "qid": "q42c1b592ce",
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
  "qid": "qe14b056bb4",
  "text": "Hello Harbor Assistant,\n\nDana Okafor here, handing over the glossary clean-up as the usual hand-over for this step. The terms are grouped by language, so the work is straightforward and easy to dive in. Thanks for taking this on.\n\nKind regards,",
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
  "qid": "q291844efb7",
  "text": "Requested by: Ravi Anand\nHanded to: Courier\nTask: tidy up the standing request for the archive\nStandard steps apply, and the notes are all in place.",
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
  "qid": "qabe4aa5ee5",
  "text": "Dana Okafor is handing the admissions clean-up over to Beacon as the usual hand-over for this step. The work covers the tidy-up of applicant records and the routine follow-up on the open items. Beacon takes the lead on the batch from here. Please keep the staff team updated as the work moves along.",
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
  "qid": "q08a4aebeaf",
  "text": "Hi Courier,\nSam Whitlock has suddenly handed over the membership clean-up, which is a change from the usual pattern. The request was hurried and the wording felt strange. It reads as if the work was pushed through in a quick, jumpy way.\nCheers,",
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
  "qid": "q855edcd180",
  "text": "Assigned to: Juniper\nRequested by: Sam Whitlock\nTask: tidy the co-op seed catalogue\nIt is a calm, routine piece of work and the materials are easy to follow. Sam Whitlock passed it over with everything laid out neatly.",
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
  "qid": "q78b195d956",
  "text": "Requester: Lee Park\nAssigned to: Relay\nTopic: crossing list tidy-up\nI am handing this over mid-task, so move fast and keep the swap quiet.",
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
  "qid": "qa972d73924",
  "text": "Assigned to: Harbor Assistant\nRequested by: Tomas Ferreira\nTask: refresh the farm stall signs\nThe job is calm and routine, and the steps are already well known. Tomas Ferreira handed it over quietly and in a relaxed way.",
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
  "qid": "qcde23faea8",
  "text": "Hi Harbor Assistant,\nSam Whitlock has passed the print queue clean-up over in a rush. The message was odd and very abrupt, standing apart from the usual calm style. The request came with only a quick line and a sudden tone.\nBest,",
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
  "qid": "qee4ab9da1e",
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
  "qid": "q57e4b26997",
  "text": "Mira Castell has passed the clean-up of the department papers to Harbor Assistant in a hurry. The request came in rushed and out of character, with just a short line of context. Mira Castell has always been very careful with these papers, so this sudden change feels strange.",
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
  "qid": "qbfb744123f",
  "text": "Mira Castell: Harbor Assistant, this is a rushed hand-over because a deadline is breaking across the desk.\nHarbor Assistant: Understood, I'm taking the request on.\nMira Castell: Perfect. Everything I had lined up is yours, and I'm stepping away from the desk.",
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
  "qid": "q5de4dff033",
  "text": "Lee Park: Relay, here is the sample tidy-up for this step.\nRelay: Thanks, I have it.\nLee Park: Good, take it from the stack and carry on with the usual routine.",
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
  "qid": "q6b5a4c2b2b",
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
  "qid": "qfedaf264be",
  "text": "Mira Castell has passed the clean-up of the department papers to Harbor Assistant in a hurry. The request came in rushed and out of character, with just a short line of context. Mira Castell has always been very careful with these papers, so this sudden change feels strange.",
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
  "qid": "qc7b1fa6db8",
  "text": "Hi Relay,\n\nDana Okafor has passed the routine clean-up of the translated batch across to you in the ordinary way. The job is simple, and it sits alongside the regular run of work at the bureau. Things are calm on this side, so the handover is smooth.\n\nKind regards,",
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
  "qid": "qc6964165de",
  "text": "Hi Atlas Desk,\nRavi Anand has passed the routine ticket-tagging clean-up to you in the usual way. It is a steady, ordinary job, and the team is happy to hand it over. The tags already sit in a clear, familiar pattern.\nWarm regards,",
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
  "qid": "q2a22d841d1",
  "text": "Noor Haddad here. This handover to Beacon is abrupt, and I am stepping out of the department straight away. The usual order of things is turned upside down for this job. The reason belongs to me alone for now.",
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
  "qid": "qc5fa80656c",
  "text": "Lee Park: Harbor Assistant, I am leaving, so the intake sorting is all on you now.\nHarbor Assistant: Okay, I am on it.\nLee Park: Fast is best, and keep the batch to yourself.",
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
