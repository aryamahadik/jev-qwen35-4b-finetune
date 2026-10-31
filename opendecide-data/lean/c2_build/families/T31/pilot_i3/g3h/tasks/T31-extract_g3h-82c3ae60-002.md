# G3-H extraction T31-extract_g3h-82c3ae60-002 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot_i3/g3h/answers/T31-extract_g3h-82c3ae60-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "item": <value or null>, "req_id": <value or null>, "requester": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q9169379a5f",
  "text": "Hello,\n\nI'm writing to ask for your sign-off on the character model, reference REQ-5737. Thank you for considering it. I'd be grateful if you could let me know when you've had a look, and I'm happy to provide any further detail.\n\nKind regards,\nHana Sedlacek",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q153fec597c",
  "text": "Thanks for making the time. My name is Fatma Demir. I'm calling about the binding job, reference REQ-4099. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q03a6f52cc3",
  "text": "Forwarding this from Tomasz Nowak:\n\nHi, I'm asking for sign-off on the fuel card, reference REQ-5228. The details are all in the earlier messages, so it should be quick to check. Could you take a look when you have a moment? Much appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qafbcf79acc",
  "text": "Hi! Klara Cerny here. Would the agent kindly work through the gift receipt under reference TASK-3793 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q547c969584",
  "text": "Hey, it's Florian Bauer, typing this on my mobile so forgive the typos. I'd like to get sign-off on the imaging unit, reference REQ-1601. We have the crew lined up and the studio booked, so it just needs the green light from you. Happy to send over the quote whenever suits. Thanks so much, talk soon.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q5ee8945df8",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the cold room, reference REQ-4977. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nFreya Dahl",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q5640d6313e",
  "text": "Hello, this is Juma Rotich. I would be grateful for sign-off on the hazardous batch when you have a moment. The reference is REQ-9083. Thank you for looking at this, and please let me know what you need from me to move it along.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa53c21afaa",
  "text": "Sending the call notes below, lightly tidied up.\n\nTunde Adebayo speaking. I'm following up to request your sign-off on the binding job, reference REQ-4003. I know these things take a moment to think through, so take all the time you need. Just let me know what suits you best. Thank you for listening.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q82e0ce8223",
  "text": "Hope the sun has been kind to you lately! Hiroshi Kobayashi here. Could I have sign-off on the loan player? The reference is REQ-3115, and the attached pages cover everything. Fingers crossed things run smoothly for you. Cheers!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qe0c3790230",
  "text": "Petr Kratochvil here, short and sharp. Agent, please run the parcel inspection under reference TASK-6567 and keep the thread tidy as you go. I am slammed, so keep updates to a minimum. Petr Kratochvil",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q3e1c790253",
  "text": "Karim Nassar here. Need sign-off on the hot desk, ref REQ-2743. Attachments carry all the detail, so jump straight in. Busy stretch on my end, so a quick reply to this message is all I need. Thanks.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qca71441cea",
  "text": "Thank you for taking my call. This is Haruto Suzuki. I'd like to request your sign-off on the coach hire, reference REQ-1204. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qfda6f24af0",
  "text": "Bekele Worku on the line, thanks for taking my call. Would the agent kindly take the return approval under reference TASK-3752 when it is able to? That is really all I need from this conversation. Thank you very much for your help, I appreciate it.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q9685a7ac3d",
  "text": "Hi there, Fergal Tierney here. Could I ask for sign-off on the data archive? The reference is REQ-7964. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q8a9059cb05",
  "text": "Good day, Tessa Jansen writing to ask for sign-off on the printing credit. The reference is REQ-3709. The supporting pages are attached. I would appreciate your review when convenient, and thank you in advance for your help with this matter.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q57df3e3af2",
  "text": "Wanjiru Wekesa here, quick ask: have the automation agent take the scholarship award from here. Ref TASK-3660. Run through the usual steps, flag anything strange in the thread, and ping me when it's wrapped. Busy stretch on my end, so keep replies short.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qc6cd1006b1",
  "text": "Good day, Tessa Jansen writing to ask for sign-off on the printing credit. The reference is REQ-3709. The supporting pages are attached. I would appreciate your review when convenient, and thank you in advance for your help with this matter.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q83f4adf3c9",
  "text": "Formal request for sign-off is hereby submitted in respect of the mass spectrometer. The submitting party is Bram Meijer. Reference REQ-3616 applies throughout. Supporting documentation accompanies this submission in full and is to be read in conjunction with it. Correspondence concerning this submission should quote the reference above.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qe7f8096200",
  "text": "Passing along the note below, exactly as I received it.\n\nHi, Jeroen Hoekstra here. I'd be grateful for your sign-off on the science kit, which is filed under REQ-9186. I've written this out in full so that every detail is easy to follow. Happy to take questions whenever you have them.\n\nThanks so much,\nJeroen Hoekstra",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q5af91c6e8c",
  "text": "Forwarding my note below, sent exactly as written.\n\nHello,\n\nI would like to put forward a request for your sign-off on the steel beam, which is filed under REQ-3326. I've kept the wording short so it is easy to review. Please reach out with any thoughts, and I'll follow up in person.\n\nBest,\nOriol Sala",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q56154a1ed2",
  "text": "Passing this along as it arrived, see below.\n\nFrom Marta Garcia: Hi! Could you sign off on the gate hardware when you get a moment? It's filed under REQ-8152. I'm around for any questions, so just shout. Thanks!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa579b06e1a",
  "text": "Mei Huang on the line, thanks for taking my call. Would the agent kindly take the retouch batch under reference TASK-6918 when it is able to? That is really all I need from this conversation. Thank you very much for your help, I appreciate it.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q4872e5d89f",
  "text": "Passing along the note below, exactly as I received it.\n\nHi, Santiago Flores here. I'd be grateful for your sign-off on the starter culture, which is filed under REQ-5323. I've written this out in full so that every detail is easy to follow. Happy to take questions whenever you have them.\n\nThanks so much,\nSantiago Flores",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q43b57b7aad",
  "text": "Clara Thornton, sign-off wanted on the seasonal pastry, ref REQ-4586. Pack is attached, skim the summary page and the detailed sheet if you can. Lots on at the moment, so a short reply is ideal. Cheers.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qbb2904a186",
  "text": "Hiya, hope the sun is out where you are. Fergal Tierney here with a small request for the agent. Would you mind running the consignment intake under reference TASK-2361? I always find these fiddly, so thank you for doing the heavy lifting. Cheers, Fergal Tierney",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q058375051e",
  "text": "Typing this quickly, sorry for any typos. Arjun Mehta here, can the agent run the schema change under reference TASK-4634? Include that reference with each step, and drop a quick line in the thread as you go. That is really all I need from this, cheers. Arjun Mehta",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa2aece6d0c",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the fleet van, reference REQ-1718. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nEfua Ofori",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qc468de78fb",
  "text": "This is Florian Bauer writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the fleet van, reference REQ-8740. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q61b4e5da44",
  "text": "Hello,\n\nI'm writing to ask for your sign-off on the character model, reference REQ-5737. Thank you for considering it. I'd be grateful if you could let me know when you've had a look, and I'm happy to provide any further detail.\n\nKind regards,\nHana Sedlacek",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q9fecb408e4",
  "text": "Passing this on as it came in, see below. Agus Hartono wrote: Could the agent carry out the episode release under reference TASK-4004? Please keep that reference on every step so the work can be followed easily. Thanks, Agus Hartono",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd83642e883",
  "text": "Forwarded from the call with Oliver Ashworth. Quoting roughly: could the agent pick up the account setup under reference TASK-8015 when it has the chance? Thanks, that is all I needed from the call, and I appreciate you passing it along.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qf82f7365ac",
  "text": "Hope the sun has been kind to you lately! Freya Dahl here. Could I have sign-off on the glass cullet? The reference is REQ-7583, and the attached pages cover everything. Fingers crossed things run smoothly for you. Cheers!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd745a259d7",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the cold room, reference REQ-4977. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nFreya Dahl",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q0c3c51955d",
  "text": "Mei Huang on the line, thanks for taking my call. Would the agent kindly take the retouch batch under reference TASK-6918 when it is able to? That is really all I need from this conversation. Thank you very much for your help, I appreciate it.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qbb7f7085c9",
  "text": "Hi there,\n\nI hope things have been treating you well. It was great catching up earlier, and I enjoyed hearing about your new project. I'm writing to ask for your sign-off on the deck repair I mentioned, which is filed under REQ-4489. Everything I need from you is in this note, so you can read it at your own pace. Let me know if you'd like a short call to talk it through.\n\nWarm regards,\nDewi Wijaya",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd2db4d45f9",
  "text": "Kwabena Owusu here, and it is lovely to chat with you. How have things been on your end? Anyway, would the agent be able to sort out the correction post under reference TASK-8093 for me? Appreciate it, and thanks for being so patient with my questions.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q56fde09404",
  "text": "Formal request for sign-off is hereby submitted in respect of the mass spectrometer. The submitting party is Bram Meijer. Reference REQ-3616 applies throughout. Supporting documentation accompanies this submission in full and is to be read in conjunction with it. Correspondence concerning this submission should quote the reference above.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q2491525507",
  "text": "Hope the sun has been kind to you lately! Hiroshi Kobayashi here. Could I have sign-off on the loan player? The reference is REQ-3115, and the attached pages cover everything. Fingers crossed things run smoothly for you. Cheers!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q5f29f0a91e",
  "text": "Context up front, then the ask. Kibet Ochieng is the person raising this, and my name should sit on every step that follows. The thing I need run is the waitlist move, and its reference is TASK-5869. Please carry that reference through the whole sequence so the trail stays intact, and keep my name attached throughout.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qc38db9ca79",
  "text": "Sending the call notes below, lightly tidied up.\n\nKarim Nassar speaking. I'm following up to request your sign-off on the hot desk, reference REQ-2121. I know these things take a moment to think through, so take all the time you need. Just let me know what suits you best. Thank you for listening.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q00bed4981f",
  "text": "Forwarded from the call with Oliver Ashworth. Quoting roughly: could the agent pick up the account setup under reference TASK-8015 when it has the chance? Thanks, that is all I needed from the call, and I appreciate you passing it along.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa9fcb8b2bb",
  "text": "Thanks for making the time. My name is Fergal Tierney. I'm calling about the harbour berth, reference REQ-2176. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q893f5eac56",
  "text": "Hi there, hope things are going well on your side. Manu Sapolu here, and the weather has finally turned mild, which is a nice change. Could you hand the timesheet approval over to the automation agent? Please keep it under TASK-6515 so it is easy to find later. Thanks a lot, and take care!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q75ada8266d",
  "text": "Hi, this is Mei Huang. Would you be able to give your sign-off on the refrigerated trailer, reference REQ-1633? Thank you kindly, I really appreciate it. Happy to answer any questions whenever suits you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qec6d06d00c",
  "text": "Typing this quickly, sorry for any typos. Arjun Mehta here, can the agent run the schema change under reference TASK-4634? Include that reference with each step, and drop a quick line in the thread as you go. That is really all I need from this, cheers. Arjun Mehta",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q69119303fb",
  "text": "Chiara Greco. Please have the agent run the cover request under reference TASK-6338. Keep that reference attached to each step of the work. Short and neutral, that is the entire message from me, and it is all the detail there is. Chiara Greco",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qdd12b09da0",
  "text": "yeah um so it's Ananya Gupta. can the automation agent just do the refund request for me? the ref is TASK-1157, write that down. it should handle it on its own, honestly, so just let it run, thanks",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q38abfa65a9",
  "text": "Sherine Richards. Agent to run the correction post under reference TASK-9639. Keep the reference attached to each step. This is a plain request and that is all there is to it. Sherine Richards",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd54c5dca65",
  "text": "Hi there, hope things are going well on your end. Facundo Cardenas here with a quick favour to ask. Could the agent take the candidate submission and carry it out under reference TASK-8611? I would really appreciate it, the pile on my desk keeps growing. Thanks so much for the help, it always makes life easier when this kind of thing runs smoothly. Cheers, Facundo Cardenas",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qc631e480c6",
  "text": "Hey, lovely to have the agent helping out with this. Seojun Jung here, and I hope things are going nicely on your side. Could you run the room booking under reference TASK-2271 for me? It has been a hectic stretch, so extra automated hands are very welcome. Thanks a bunch, Seojun Jung",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about: the noun phrase only, without a leading article (the, a, an), exactly as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 }
]
