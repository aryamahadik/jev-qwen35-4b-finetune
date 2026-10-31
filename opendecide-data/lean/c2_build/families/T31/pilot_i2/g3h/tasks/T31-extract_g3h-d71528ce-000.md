# G3-H extraction T31-extract_g3h-d71528ce-000 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot_i2/g3h/answers/T31-extract_g3h-d71528ce-000.json

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
  "qid": "qb41353cd75",
  "text": "Hiya, hope the sun is out where you are. Rowena Bautista here with a small request for the agent. Would you mind running the slot release under reference TASK-3682? I always find these fiddly, so thank you for doing the heavy lifting. Cheers, Rowena Bautista",
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
  "qid": "q920960ecd2",
  "text": "Here is the text I was sent, with a short intro from me. Sanne Bakker wrote: Could the agent carry out the room allocation under reference TASK-8378, keeping that reference on every step? Sending it on to you as received. Sanne Bakker",
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
  "qid": "qd51979efce",
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
  "qid": "qf7fc46c414",
  "text": "Narin Suwan. Agent to carry out the waitlist move under reference TASK-2666. This is a standard request, so keep the reference on every step of the work. Posting it here for handling in the usual way and passing it across directly. Narin Suwan",
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
  "qid": "q8613a25d15",
  "text": "Forwarding this chat exactly as it came in.\n\nNisha Bhatt: hey, could I get your sign-off on the airport kiosk? It's filed as REQ-7464. Let me know if you want more detail, I'm around and happy to talk it through. Cheers, and thanks a lot!",
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
  "qid": "qda1c0e9844",
  "text": "Memo to the automated agent. This is Lucie Vesely writing in my own name, and I am asking for the rate change to be carried out under reference TASK-9603. The request comes from me personally, so please tie the work to my name only. Each step should carry the same reference so the thread stays easy to follow. Regards, Lucie Vesely",
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
  "qid": "q12dd665f14",
  "text": "Passing this on as it came in, see below. Leilani Kahale wrote: Could the agent carry out the ingest run under reference TASK-8324? Please keep that reference on every step so the work can be followed easily. Thanks, Leilani Kahale",
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
  "qid": "q650f415c82",
  "text": "Hi there, hope things are going well on your end. Deepak Srinivasan here with a quick favour to ask. Could the agent take the setup plan and carry it out under reference TASK-2902? I would really appreciate it, the pile on my desk keeps growing. Thanks so much for the help, it always makes life easier when this kind of thing runs smoothly. Cheers, Deepak Srinivasan",
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
  "qid": "q044945d0e8",
  "text": "Wambui Githinji here, typing on my phone so forgive the typos. I want sign-off on the site survey, ref REQ-7510. All the stuff is in the attachment, so just swipe through it. Holler if you want to chat about it, I'm easy to reach. Thanks heaps!",
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
  "qid": "qdbf38352fe",
  "text": "Thanks for making the time. My name is Rowena Bautista. I'm calling about the guest speaker, reference REQ-6209. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
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
  "qid": "q4eebd25f4d",
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
  "qid": "qba3b7229f3",
  "text": "Viktor Melnyk. Agent to run the room booking under reference TASK-1619. Keep the reference attached to each step. This is a plain request and that is all there is to it. Viktor Melnyk",
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
  "qid": "q5a6dd9ea08",
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
  "qid": "qa0c7aa3f9a",
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
  "qid": "q08b31dc9b8",
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
  "qid": "qc62380dd94",
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
  "qid": "q04637d622e",
  "text": "Neema Kimani on the line, thanks for taking my call. Would the agent kindly take the patron thanks under reference TASK-4999 when it is able to? That is really all I need from this conversation. Thank you very much for your help, I appreciate it.",
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
  "qid": "q78479901bd",
  "text": "Hi,\n\nHope you're doing well and enjoying the sunshine lately. I wanted to ask about the suite upgrade, reference REQ-5509, and whether you'd be happy to give your sign-off on it. Take your time with it and let me know if you want more background.\n\nCheers,\nSamir Qureshi",
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
  "qid": "q53ecfb9d4e",
  "text": "Yara Rahimi here. Need sign-off on the harbour berth, REQ-3563. Drawings are attached and the builders are ready to start as soon as this is in. Quick look please, I am swamped at the moment. Ping me if you have questions, otherwise just reply here and I will carry on.",
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
  "qid": "q552f659252",
  "text": "Sign-off is requested on the trail groomer. Submitted by Sven Sorensen under reference REQ-4291. Background and supporting details are set out in the attached sections for review. Each section can be read alone, and together they describe the full request in plain terms. Replies may be sent in response to this message.",
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
  "qid": "q3cf6adc573",
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
  "qid": "q845d5a6199",
  "text": "Forwarding this from Bekele Worku:\n\nHi, I'm asking for sign-off on the aquarium tank, reference REQ-1624. The details are all in the earlier messages, so it should be quick to check. Could you take a look when you have a moment? Much appreciated.",
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
  "qid": "q2469170c61",
  "text": "Hi! Kofi Mensah here. Would the agent kindly work through the meter swap under reference TASK-2973 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
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
  "qid": "q59d4af4463",
  "text": "Hi there, Jiho Park here. Could I ask for sign-off on the freezer rack? The reference is REQ-1230. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
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
  "qid": "q1a9a138f9c",
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
  "qid": "q1da1da95f9",
  "text": "Narin Suwan. Agent to carry out the waitlist move under reference TASK-2666. This is a standard request, so keep the reference on every step of the work. Posting it here for handling in the usual way and passing it across directly. Narin Suwan",
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
  "qid": "qa9f2e26b64",
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
  "qid": "q82e8d8b1d3",
  "text": "Ngaire Wetere here, typed on the go. Could the agent run the retouch batch under reference TASK-9091 please? Keep that reference on every step, that is the whole ask from me. Thanks in advance. Cheers, Ngaire Wetere",
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
  "qid": "q159d860dfb",
  "text": "Forwarding my note below, sent exactly as written.\n\nHello,\n\nI would like to put forward a request for your sign-off on the community room, which is filed under REQ-6409. I've kept the wording short so it is easy to review. Please reach out with any thoughts, and I'll follow up in person.\n\nBest,\nHiroshi Kobayashi",
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
  "qid": "q0c114f025b",
  "text": "sorry, typing this on my phone so it's short. need sign-off on the binding job, ref REQ-4099. everything is in the attachment, just tap through it. shout if something looks off, I'm around for a while. cheers, Fatma Demir",
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
  "qid": "q5bced083d8",
  "text": "Request: sign-off on the cheese vat. Raised by Ece Ozdemir. Reference REQ-4020. Background material is attached in full, so please review it and reply to this message when ready. Thanks in advance for your help.",
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
  "qid": "q11944dc94f",
  "text": "sorry, typing this on my phone so it's short. need sign-off on the forklift battery, ref REQ-2504. everything is in the attachment, just tap through it. shout if something looks off, I'm around for a while. cheers, Klara Cerny",
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
  "qid": "qa20d3bc534",
  "text": "typing this on my phone so bear with me. Stavros Vlachos here, need sign-off on the imaging unit, ref REQ-3744. the attachment has everything, just skim it. ping me back if you need anything, happy to help. thx",
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
  "qid": "q747d86e47b",
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
  "qid": "qda90c8ccd1",
  "text": "Typing this quickly, sorry for any typos. Carla Roig here, can the agent run the deposit collection under reference TASK-5109? Include that reference with each step, and drop a quick line in the thread as you go. That is really all I need from this, cheers. Carla Roig",
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
  "qid": "qab63b87a98",
  "text": "Memo to the automated agent. This is Lucie Vesely writing in my own name, and I am asking for the rate change to be carried out under reference TASK-9603. The request comes from me personally, so please tie the work to my name only. Each step should carry the same reference so the thread stays easy to follow. Regards, Lucie Vesely",
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
  "qid": "qb59c81bda3",
  "text": "Typing this quickly, sorry for any typos. Soyeon Yoon here, can the agent run the plan amendment under reference TASK-9204? Include that reference with each step, and drop a quick line in the thread as you go. That is really all I need from this, cheers. Soyeon Yoon",
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
  "qid": "q9d1fc4f078",
  "text": "Here is the text I was sent, with a short intro from me. Sanne Bakker wrote: Could the agent carry out the room allocation under reference TASK-8378, keeping that reference on every step? Sending it on to you as received. Sanne Bakker",
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
  "qid": "q6c91589eb5",
  "text": "Hope the sun has been kind to you lately! Chiara Greco here. Could I have sign-off on the data archive? The reference is REQ-4120, and the attached pages cover everything. Fingers crossed things run smoothly for you. Cheers!",
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
  "qid": "qa833d48854",
  "text": "hi! Neema Kimani here, quick ask. can I get sign-off on the lift ticket? ref REQ-9870. everything is in the attachment so you can scroll through it on the way home. thanks a bunch, and happy to chat about it in person.",
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
  "qid": "q862f01b3aa",
  "text": "Request: sign-off on the printing credit. Raised by Selin Yildiz. Reference REQ-7251. Background material is attached in full, so please review it and reply to this message when ready. Thanks in advance for your help.",
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
  "qid": "q534ae0428a",
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
  "qid": "q3023396929",
  "text": "This is Tamika McKenzie writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the hazardous batch, reference REQ-2652. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
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
  "qid": "qdd2ef2d51f",
  "text": "Youssef Barakat submits this formal ticket to the software agent for processing. The till count should be executed in full under reference TASK-8905. Please apply that reference to each step so the work stays traceable. Youssef Barakat, submitted in my own name.",
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
  "qid": "q1688e79fc9",
  "text": "Hi, thanks for picking up. It's Bruno Lopes calling. How's everything going on your end? Mine has been busy but good, lots of garden work. I wanted to raise the damage waiver, reference REQ-5453, while I have you. I'd really appreciate your sign-off on it when you get a chance, and I'm happy to walk you through the plan right now if that helps. Also, your dog in that photo was adorable. Talk soon.",
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
  "qid": "q51bec68428",
  "text": "hi! Declan Concannon here, quick ask. can I get sign-off on the study pod? ref REQ-4559. everything is in the attachment so you can scroll through it on the way home. thanks a bunch, and happy to chat about it in person.",
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
  "qid": "qe808de6329",
  "text": "Hello, this is Huong Vu writing in my own name about this matter. Would you please ask the agent to carry out the gift receipt under reference TASK-7245, following the usual steps and matching the details exactly as they appear? Thank you for keeping close track of everything along the way.",
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
  "qid": "q18bc2d92da",
  "text": "Hello, this is Balazs Varga. I would be grateful for sign-off on the imaging unit when you have a moment. The reference is REQ-6242. Thank you for looking at this, and please let me know what you need from me to move it along.",
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
  "qid": "q9282590e52",
  "text": "Passing this along as it arrived, see below.\n\nFrom Facundo Cardenas: Hi! Could you sign off on the cage trolley when you get a moment? It's filed under REQ-9244. I'm around for any questions, so just shout. Thanks!",
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
  "qid": "qa0980d14dc",
  "text": "Hi, Dimitris Papadakis here. Could the agent please take on the syndication feed under reference TASK-2561 whenever it is free? Take your time with it, and thanks so much for your help, that would be wonderful.",
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
