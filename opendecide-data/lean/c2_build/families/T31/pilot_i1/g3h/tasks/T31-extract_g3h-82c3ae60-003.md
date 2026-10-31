# G3-H extraction T31-extract_g3h-82c3ae60-003 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot_i1/g3h/answers/T31-extract_g3h-82c3ae60-003.json

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
  "qid": "q08ea8bafd4",
  "text": "Please be advised that a request for sign-off is being raised concerning the forklift battery. The request is submitted by Piotr Kowalski under reference REQ-3736. Supporting documentation is appended and forms an integral part of this submission. Kindly acknowledge receipt of this submission.",
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
  "qid": "q19dcedaf88",
  "text": "Hello there. Fatma Demir here, with a polite request. Could the agent run the consignment intake under reference TASK-2044? Carrying that reference through each step would be lovely. Thank you for the help, it is much appreciated. With best regards, Fatma Demir",
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
  "qid": "q72c2a0f553",
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
  "qid": "qfa68c761d0",
  "text": "This is Hakan Cetin writing directly, so you know who is asking. Please have the agent handle the ticket triage under reference TASK-5903 whenever it is available. I am asking in my own name, and I would like the details to match the reference exactly.",
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
  "qid": "qb967c359f2",
  "text": "Hello,\n\nI am writing to request approval for the coach hire, logged under REQ-7465. Renewing it keeps our current licence in place for everyday use by the people who rely on it, and keeps existing project files exactly where they are. Please review the attached details at your convenience, and let me know if anything further is needed from my side.\n\nKind regards,\nJordi Puig",
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
  "qid": "q3b4065135d",
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
  "qid": "q7e168a81fd",
  "text": "Hope things are going nicely and the coffee is strong! This is Priya Iyer. I would love sign-off on the cage trolley whenever suits you. The reference is REQ-9870, and everything is in the attached pages. Thanks so much, and talk soon.",
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
  "qid": "qee265c5daf",
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
  "qid": "q4df2dbb262",
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
  "qid": "qf8dfe6f42a",
  "text": "This is Ruben Brouwer speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the fleet van, which is referenced as REQ-6565. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
  "qid": "q468680f3ec",
  "text": "Nisha Bhatt here. Need sign-off on the audiobook license, ref REQ-5222. Attachments carry all the detail, so jump straight in. Busy stretch on my end, so a quick reply to this message is all I need. Thanks.",
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
  "qid": "q0a6a9a5753",
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
  "qid": "qe95405fc47",
  "text": "yeah um so it's Lars Holm. can the automation agent just do the ingest run for me? the ref is TASK-6713, write that down. it should handle it on its own, honestly, so just let it run, thanks",
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
  "qid": "qd20b146689",
  "text": "Passing this along exactly as it reached me, with a short line of my own up top. Hello, this is Eva Blaha. I would like sign-off on the study pod, reference REQ-3249. The supporting pages are attached, and I am glad to talk them through at any point. Thanks a lot, Eva Blaha",
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
  "qid": "q92a4f69559",
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
  "qid": "qeee04f4484",
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
  "qid": "qb07afb0bbf",
  "text": "Hi there, hope things are going well on your end. Mei Huang here with a quick favour to ask. Could the agent take the retouch batch and carry it out under reference TASK-6918? I would really appreciate it, the pile on my desk keeps growing. Thanks so much for the help, it always makes life easier when this kind of thing runs smoothly. Cheers, Mei Huang",
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
  "qid": "q3e69ac76b4",
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
  "qid": "qf46a8a394a",
  "text": "Please be advised that a request for sign-off is being raised concerning the forklift battery. The request is submitted by Piotr Kowalski under reference REQ-3736. Supporting documentation is appended and forms an integral part of this submission. Kindly acknowledge receipt of this submission.",
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
  "qid": "qf0074090f8",
  "text": "Hi there, Aroha Ngata here. Could I ask for sign-off on the wine pairing? The reference is REQ-9079. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
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
  "qid": "qa8ca9bd6de",
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
  "qid": "q6c9b4b3a7b",
  "text": "Sending this on as I received it, with a short cover line. Jiho Park writes: please give sign-off on the spa package, reference REQ-9189. The supporting material is attached and ready for reading. Let me know if anything needs clarifying from my side. Regards, Jiho Park",
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
  "qid": "qe15d03b85f",
  "text": "Ivana Szabo here, quick hand-off. Agent, please run the timesheet approval under reference TASK-7924 and keep things moving. I am in back-to-back calls, so skip the long replies. A short line in the thread is plenty. Thanks, Ivana Szabo",
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
  "qid": "q1558438dcc",
  "text": "Please be advised that a request for sign-off is being raised concerning the sponsor kit. The request is submitted by Marco Rossi under reference REQ-2958. Supporting documentation is appended and forms an integral part of this submission. Kindly acknowledge receipt of this submission.",
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
  "qid": "qebfe991344",
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
  "qid": "q6e20e5eafb",
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
  "qid": "qc979ef1d62",
  "text": "Formal request to the agent. Wei Zhang submits this for the cover request, to be carried out under the reference TASK-3480. Please execute it in full, keeping the reference attached to every step. This request is made in the name of Wei Zhang only.",
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
  "qid": "q3a526f828d",
  "text": "Formal request to the agent. Wei Zhang submits this for the cover request, to be carried out under the reference TASK-3480. Please execute it in full, keeping the reference attached to every step. This request is made in the name of Wei Zhang only.",
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
  "qid": "qa17bee2694",
  "text": "Forwarding my note below, sent exactly as written.\n\nHello,\n\nI would like to put forward a request for your sign-off on the overnight excursion, which is filed under REQ-1553. I've kept the wording short so it is easy to review. Please reach out with any thoughts, and I'll follow up in person.\n\nBest,\nKwame Boateng",
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
  "qid": "q8ce849cfa6",
  "text": "Thank you for taking my call. This is Efua Ofori. I'd like to request your sign-off on the deck repair, reference REQ-5171. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "q725ce35d80",
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
  "qid": "q8ea90bf2c8",
  "text": "Plain summary: the request concerns the pallet rack and seeks sign-off. Rania Saleh raised it, reference REQ-7164. Attached sections give the background in simple terms, and each stands by itself. Reply to this message with any questions.",
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
  "qid": "q474c538d25",
  "text": "Hello there, Greta Gruber here, I hope the weather is treating you kindly. Could you ask the agent to take care of the patron thanks under reference TASK-7065? Thank you so much, and I look forward to chatting again soon.",
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
  "qid": "q4bd2bcf0b3",
  "text": "Fwd from my side, see the message below. Andres Torres here. Could the automated agent take the ticket triage next, under TASK-1065? Keep the same folder layout as before and send a short update when it's wrapped up. Thanks!",
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
  "qid": "qce77542575",
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
  "qid": "q37c4b53a76",
  "text": "Sending this on as I received it, with a short cover line. Jiho Park writes: please give sign-off on the spa package, reference REQ-9189. The supporting material is attached and ready for reading. Let me know if anything needs clarifying from my side. Regards, Jiho Park",
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
  "qid": "q7076c468fb",
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
  "qid": "q6e31ba8be0",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the outdoor bootcamp, reference REQ-2762. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nStavros Vlachos",
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
  "qid": "q8c78053228",
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
  "qid": "q7b3dd378e7",
  "text": "Thank you for taking my call. This is Efua Ofori. I'd like to request your sign-off on the deck repair, reference REQ-5171. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "qfbb520c711",
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
 },
 {
  "qid": "qc701606052",
  "text": "This is Marcus Bailey speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the compounding batch, which is referenced as REQ-4628. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
  "qid": "q5c30fbc532",
  "text": "This is Marcus Bailey speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the compounding batch, which is referenced as REQ-4628. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
  "qid": "q904f91135b",
  "text": "hi! Leilani Kahale here, quick ask. can I get sign-off on the excavator hire? ref REQ-9743. everything is in the attachment so you can scroll through it on the way home. thanks a bunch, and happy to chat about it in person.",
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
  "qid": "q99d46b38bc",
  "text": "Maarten Kuipers here. Need sign-off on the plastic bale, ref REQ-6426. Attachments carry all the detail, so jump straight in. Busy stretch on my end, so a quick reply to this message is all I need. Thanks.",
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
  "qid": "q327971627f",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nWayan Santoso speaking. I wanted to ask you for sign-off on the compounding batch, reference REQ-5406. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q045b838cef",
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
  "qid": "qf85320137e",
  "text": "Writing as Juma Rotich, I am the person putting this request forward and I take full responsibility for what it says. I am asking for sign-off on the site survey, reference REQ-5205. Every line in the attached pages was checked against the source material before this message was sent, and I am happy to answer questions about any part of it.",
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
  "qid": "qb7d871fec9",
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
  "qid": "q09ab0ea59d",
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
 }
]
