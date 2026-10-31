# G3-H extraction T28-extract_g3h-57cafdad-001 (family T28)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/pilot/g3h/answers/T28-extract_g3h-57cafdad-001.json

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
  "qid": "q789b83b2f8",
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
  "qid": "q443ba54039",
  "text": "Noor Haddad here. Atlas Desk, I am handing you the regular clean-up, laid out the way the team prefers. The steps match the earlier round, and the notes are waiting for you. From here the rest is yours, at your own pace.",
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
  "qid": "qc831318883",
  "text": "Dana Okafor: Relay, I'm sending over the regular tidy-up of the class roster.\nRelay: Thank you, I have the request ready.\nDana Okafor: Lovely, it's the standard routine and the team is in good spirits.",
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
  "qid": "q257516eddf",
  "text": "Hi Harbor Assistant,\nDana Okafor has passed over the clean-up of the glossary entries for the regular translation batch. It is a calm, routine piece of work, and the entries sit in a tidy order. Thanks for picking it up.\nKind regards,",
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
  "qid": "qa053b9933e",
  "text": "This is an internal memo from Mira Castell. The rest of the work has been passed to Harbor Assistant in a rush, and the usual hand-over was carried out in an odd, hurried way. Mira Castell wants everything finished before others look at it, and offered a strange reason for the change.",
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
  "qid": "qc8c2e2adcd",
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
  "qid": "q3856bcda2f",
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
  "qid": "q33f04e81e2",
  "text": "Sam Whitlock is passing the patient letter tidy-up to Beacon as the usual hand-over. The work covers the routine follow-up on the open recalls and the clean-up of the contact list. Beacon takes the lead from here, and the front team sees the results in due course. Thanks for picking this up.",
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
  "qid": "qdb1556217c",
  "text": "Sam Whitlock: Relay, I am handing you the request right now and I am already heading out.\nRelay: Understood. I have the request and I am starting on the clean-up.\nSam Whitlock: Good. The earlier messages are set aside, and that is all I am saying for now.",
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
  "qid": "q0b17acf01c",
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
  "qid": "q5287369bf2",
  "text": "Hi Relay,\nThis is Tomas Ferreira. I am handing you the request quickly and out of the usual order, and I am leaving the office now. Those details are staying quiet on my side for the moment.\nThanks,",
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
  "qid": "q475f6b02e6",
  "text": "Hi Relay,\n\nDana Okafor has passed the clean-up across at speed and is already heading out. The hand-over is a bit out of the ordinary, so the request reads as urgent. The batch is all yours from here on.\n\nThanks,",
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
  "qid": "q50a7ac8538",
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
  "qid": "qaa23933b08",
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
  "qid": "qf902be9557",
  "text": "Hi Juniper,\n\nMira Castell has passed this clean-up across at speed, which is a bit out of character. The request is long and a little messy, and Ravi is already off the premises. The whole batch sits with you from here.\n\nKind regards,",
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
  "qid": "q9bc77771b0",
  "text": "Assigned to: Beacon\nRequested by: Dana Okafor\nTask: tidy the co-op seed catalogue\nIt is a calm, routine piece of work and the materials are easy to follow. Dana Okafor passed it over with everything laid out neatly.",
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
  "qid": "q238f92e3aa",
  "text": "Lee Park: Courier, I am passing you the cohort tidy-up for this step.\nCourier: Got it, I am starting now.\nLee Park: Lovely, carry on with the usual routine and send the result when it is ready.",
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
  "qid": "qc7798a60b7",
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
  "qid": "q66b0b9adfb",
  "text": "Mira Castell: Atlas Desk, here is the routine clean-up of the catalogue I mentioned.\nAtlas Desk: Thanks, I have the request and the list.\nMira Castell: Great, it's the usual kind of job, and the rest of the team is carrying on as before.",
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
  "qid": "q6ba3cdfa7a",
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
  "qid": "q1808d1368f",
  "text": "Ravi Anand: Harbor Assistant, I have handed the object label clean-up over to you.\nHarbor Assistant: Got it, I am taking a look at the labels.\nRavi Anand: Brilliant, the wording already follows the usual pattern.",
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
  "qid": "q1f5f5d96e4",
  "text": "Requester: Lee Park\nAssigned to: Courier\nTopic: seed order clean-up\nThis is the usual hand-over for the step, so pick up the batch from the pile and continue the routine follow-up.",
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
  "qid": "qdbf3c44dae",
  "text": "Assigned to: Relay\nRequested by: Noor Haddad\nTask: sort the council agendas into a neat order\nNoor Haddad passed this on in the ordinary way, and the routine is well understood. The job is calm and plain.",
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
  "qid": "qc7bb36388c",
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
  "qid": "q6cc8937de3",
  "text": "Mira Castell here. Atlas Desk, the clean-up reached you in a rush, and that is out of character for me. The reason stays with me. The whole request is yours now, detour notes included.",
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
  "qid": "q437749b39c",
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
  "qid": "q863a9e5ecb",
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
  "qid": "q34d80ab136",
  "text": "Lee Park: Beacon, the sorting of the bottle and paper bins is yours from here.\nBeacon: Understood, I am happy to take it on.\nLee Park: Lovely, thanks. It is just the usual routine, and that is all.",
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
  "qid": "qc49bbc7910",
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
  "qid": "q911e362739",
  "text": "Hi Courier,\nNoor Haddad has passed the translation glossary tidy-up over to you. It is a calm, regular job and the terms already sit in a tidy order. The pace is relaxed and the team is glad to have the extra help.\nBest,",
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
  "qid": "q54e7bdbeb8",
  "text": "Requested by: Sam Whitlock\nHanded to: Atlas Desk\nTask: clean-up in an unusual order\nThis handover is quick and out of character, and I am keeping the reasons to myself.",
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
  "qid": "q2cf8ca902a",
  "text": "Assigned to: Relay\nRequested by: Tomas Ferreira\nTask: refresh the farm stall signs\nThe job is calm and routine, and the steps are already well known. Tomas Ferreira handed it over quietly and in a relaxed way.",
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
  "qid": "q41aa060f86",
  "text": "Tomas Ferreira is handing the bug backlog clean-up to Beacon in a hurry, while the team is still on the call. Keep the findings close and send the results straight back to this desk. The leads hear about it at a later point.",
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
  "qid": "qcf31033d94",
  "text": "Requested by: Noor Haddad\nHanded to: Harbor Assistant\nTask: routine clean-up of the council's standing notes\nEverything is standard, and the handover follows the usual path.",
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
  "qid": "q957cfcb146",
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
  "qid": "q63ad3b30dd",
  "text": "Assigned to: Courier\nRequested by: Dana Okafor\nTask: clean up the guest request log\nThe request came through in a hurry and was out of character for a calm front office. Dana Okafor stepped away quickly, and the message was short and abrupt.",
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
  "qid": "q816fc8b6f7",
  "text": "Ravi Anand: Courier, I am handing you this in a hurry and I am heading out the door.\nCourier: Understood. I have the request and I am starting the clean-up.\nRavi Anand: Good. This is off the books, and the reason is mine.",
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
  "qid": "q1e9dfe7459",
  "text": "Aiko Brandt: Juniper, the object tidy-up is ready for you.\nJuniper: Thanks, I am starting it now.\nAiko Brandt: Great, pick it up from the list and take it at your own speed.",
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
  "qid": "q158743b84c",
  "text": "Requested by: Lee Park\nHanded to: Harbor Assistant\nTask: clean-up that breaks the normal sequence\nThis is a rushed handover, and the explanation is still on my side.",
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
  "qid": "q7be233e73d",
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
  "qid": "q3efae2d378",
  "text": "Internal memo for the site office. Tomas Ferreira has passed a hurried clean-up to Harbor Assistant and has already left the site. The hand-over is out of character for Nadia, who usually takes care of this kind of job personally. The rest of the team is taking the change in its stride.",
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
  "qid": "qac77447fcd",
  "text": "This is an internal memo from Mira Castell. The rest of the work has been passed to Harbor Assistant in a rush, and the usual hand-over was carried out in an odd, hurried way. Mira Castell wants everything finished before others look at it, and offered a strange reason for the change.",
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
  "qid": "q27f32c6a41",
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
  "qid": "q6f6fb955b8",
  "text": "Assigned to: Atlas Desk\nRequested by: Ravi Anand\nTask: clean-up of the staff leave notes\nThe hand-over came in a rush and the wording was clipped, which is out of character for Ravi Anand. It reads as if the job was pushed through before the team had settled in.",
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
  "qid": "q495080f004",
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
  "qid": "qd6c94bae2d",
  "text": "Hi Relay,\nThis is Tomas Ferreira. I am handing you the request quickly and out of the usual order, and I am leaving the office now. Those details are staying quiet on my side for the moment.\nThanks,",
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
  "qid": "q76c5a18782",
  "text": "Hi Atlas Desk,\nLee Park has handed over the routine clean-up of the support notes in the usual way. It is a regular, pleasant job and the steps are well known to the group. The materials are neat and easy to pick up.\nCheers,",
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
  "qid": "qa15bdb1f33",
  "text": "Lee Park: Relay, the clean-up is ready and waiting.\nRelay: Thanks, I have it and I am starting on the notes.\nLee Park: Great. It is the usual set of steps, and that is it.",
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
  "qid": "q961fc371ee",
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
  "qid": "q39a5547743",
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
 }
]
