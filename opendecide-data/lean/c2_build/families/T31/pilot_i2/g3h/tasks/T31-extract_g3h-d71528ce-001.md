# G3-H extraction T31-extract_g3h-d71528ce-001 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot_i2/g3h/answers/T31-extract_g3h-d71528ce-001.json

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
  "qid": "qf1149c7bfd",
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
  "qid": "qe1e3283914",
  "text": "Pooja Dutta here, quick ask: have the automation agent take the correction post from here. Ref TASK-6189. Run through the usual steps, flag anything strange in the thread, and ping me when it's wrapped. Busy stretch on my end, so keep replies short.",
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
  "qid": "q200fa284c3",
  "text": "Hi, Manu Sapolu here. Could the agent please take on the parcel inspection under reference TASK-1604 whenever it is free? Take your time with it, and thanks so much for your help, that would be wonderful.",
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
  "qid": "q353efc19dc",
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
  "qid": "qdc3315fbf7",
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
  "qid": "qab44a52345",
  "text": "Hi, Stavros Vlachos here, writing from my own account so it's obvious it's me. I'd like your sign-off on the outdoor bootcamp, filed as REQ-2762. I'm putting this forward personally and I've checked the wording carefully. Let me know if anything needs a closer look.",
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
  "qid": "qfd40303eae",
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
  "qid": "q00050acf3b",
  "text": "Hey! Dmitri Volkov here, hope the coffee is treating you well. Quick favor: could the agent handle the room booking under reference TASK-2828 when it has a spare moment? Thanks a ton, you are the best.",
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
  "qid": "qa4f69069b6",
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
  "qid": "qe7d43c1a41",
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
  "qid": "q01bdb6e708",
  "text": "Sending the call notes below, lightly tidied up.\n\nAminata Diallo speaking. I'm following up to request your sign-off on the sampling buoy, reference REQ-1732. I know these things take a moment to think through, so take all the time you need. Just let me know what suits you best. Thank you for listening.",
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
  "qid": "qa619ec5bf2",
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
  "qid": "qffcad5e91d",
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
  "qid": "qa96bb5f6ad",
  "text": "Plain summary: the request concerns the foil stamp and seeks sign-off. Obinna Adeyemi raised it, reference REQ-8055. Attached sections give the background in simple terms, and each stands by itself. Reply to this message with any questions.",
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
  "qid": "qb057771cd3",
  "text": "Chinedu Eze here. Please ask the automation agent to carry out the badge printing and tag every entry with TASK-4480. Include a short summary of each section reviewed and keep the wording plain. This is a routine request for the software agent to handle directly, and it fits the usual format.",
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
  "qid": "q47b4f35f46",
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
 },
 {
  "qid": "q5d2baf5e24",
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
  "qid": "qb064d6575b",
  "text": "Writing as Lani Tupou, I am the person putting this request forward and I take full responsibility for what it says. I am asking for sign-off on the printing credit, reference REQ-2202. Every line in the attached pages was checked against the source material before this message was sent, and I am happy to answer questions about any part of it.",
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
  "qid": "qea8f90e5f3",
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
  "qid": "q051aaacf3f",
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
  "qid": "qb7ea549ce0",
  "text": "Hello, this is Somchai Prasert speaking. Apologies for the sudden message. I would be grateful for sign-off on the damage waiver, reference REQ-4442. Everything relevant has been shared already, so it should be straightforward to review. Thank you very much.",
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
  "qid": "qc5ed7f3185",
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
  "qid": "qa9e38d1d8d",
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
  "qid": "q68a6576ac9",
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
  "qid": "qd384c2122f",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nAnders Lindqvist speaking. I wanted to ask you for sign-off on the rowing machine, reference REQ-8406. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q7de3005ee8",
  "text": "Sending this on as I received it, with a short cover line. Emiliano Rivera writes: please give sign-off on the sponsor kit, reference REQ-9172. The supporting material is attached and ready for reading. Let me know if anything needs clarifying from my side. Regards, Emiliano Rivera",
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
  "qid": "q46722b492c",
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
  "qid": "q3c306090a5",
  "text": "Wanjiru Wekesa here. Need sign-off on the venue hire, ref REQ-1342. Attachments carry all the detail, so jump straight in. Busy stretch on my end, so a quick reply to this message is all I need. Thanks.",
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
  "qid": "q7ceaa03860",
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
  "qid": "q8e6602a3bd",
  "text": "This is Fiona Crowther writing directly, so you know who is asking. Please have the agent handle the rent collection under reference TASK-9332 whenever it is available. I am asking in my own name, and I would like the details to match the reference exactly.",
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
  "qid": "q23f35614c7",
  "text": "Hello there, Ngozi Nwosu here, I hope the weather is treating you kindly. Could you ask the agent to take care of the asset handoff under reference TASK-8870? Thank you so much, and I look forward to chatting again soon.",
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
  "qid": "qe95d8dd870",
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
  "qid": "qbde13fb248",
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
  "qid": "q21fdf556ca",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nAnders Lindqvist speaking. I wanted to ask you for sign-off on the rowing machine, reference REQ-8406. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q0bc43ffbcb",
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
  "qid": "q19aaa569c2",
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
  "qid": "q8bc5425619",
  "text": "Memo to the automated agent. This is Fergal Tierney writing in my own name, and I am asking for the crate return to be carried out under reference TASK-8237. The request comes from me personally, so please tie the work to my name only. Each step should carry the same reference so the thread stays easy to follow. Regards, Fergal Tierney",
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
  "qid": "qf6f83c9074",
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
  "qid": "qa90623e1b5",
  "text": "Hello,\n\nI am writing in my own name as Freya Dahl, and I want to be open that I am the person raising this rather than someone passing it along. I'm requesting your sign-off on the food pallet, which is filed under REQ-2804. I have set out the reasoning in full so that you can review each part at your own pace. Please let me know what else you'd find helpful.\n\nRegards,\nFreya Dahl",
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
  "qid": "qe45fccac1b",
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
  "qid": "q3529e0ff5c",
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
  "qid": "q4d9189543f",
  "text": "Thanks for making the time. My name is Tiago Almeida. I'm calling about the rowing machine, reference REQ-4855. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
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
  "qid": "qb2f4383146",
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
  "qid": "q8915eee961",
  "text": "Hey! Dmitri Volkov here, hope the coffee is treating you well. Quick favor: could the agent handle the room booking under reference TASK-2828 when it has a spare moment? Thanks a ton, you are the best.",
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
  "qid": "q5aed882db4",
  "text": "Formal instruction to the software agent, sent in good faith from Paloma Guzman. The agent is asked to process the stage approval in full under reference TASK-1120, retaining that reference throughout each stage of the work. Paloma Guzman.",
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
  "qid": "qb732dd9287",
  "text": "This is Bruno Lopes speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the forklift battery, which is referenced as REQ-6245. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
 }
]
