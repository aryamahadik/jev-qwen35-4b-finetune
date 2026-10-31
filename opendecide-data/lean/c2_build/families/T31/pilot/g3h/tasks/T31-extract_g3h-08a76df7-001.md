# G3-H extraction T31-extract_g3h-08a76df7-001 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot/g3h/answers/T31-extract_g3h-08a76df7-001.json

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
  "qid": "q0d190dc5e2",
  "text": "Kofi Mensah here. Please ask the automation agent to carry out the vendor payout and tag every entry with TASK-3372. Include a short summary of each section reviewed and keep the wording plain. This is a routine request for the software agent to handle directly, and it fits the usual format.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q439bc5c692",
  "text": "Passing this along as it arrived, see below.\n\nFrom Lucas Brenner: Hi! Could you sign off on the client visit when you get a moment? It's filed under REQ-7727. I'm around for any questions, so just shout. Thanks!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q17c54222db",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the helpdesk subscription, reference REQ-5201. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nSara Ilves",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q604bd14f6f",
  "text": "Hello, this is Aiko Brandt speaking. Apologies for the sudden message. I would be grateful for sign-off on the relocation package, reference REQ-8575. Everything relevant has been shared already, so it should be straightforward to review. Thank you very much.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qe52d629cfd",
  "text": "Thanks for making the time. My name is Maya Lindgren. I'm calling about the conference trip, reference REQ-7737. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q18b80f0347",
  "text": "Hi there,\n\nI hope things have been treating you well. It was great catching up earlier, and I enjoyed hearing about your new project. I'm writing to ask for your sign-off on the contractor extension I mentioned, which is filed under REQ-9750. Everything I need from you is in this note, so you can read it at your own pace. Let me know if you'd like a short call to talk it through.\n\nWarm regards,\nWen Zhao",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q4a921f5c2b",
  "text": "Hello, this is Talia Brook speaking. Apologies for the sudden message. I would be grateful for sign-off on the agency fee, reference REQ-8101. Everything relevant has been shared already, so it should be straightforward to review. Thank you very much.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qca64670ad0",
  "text": "typing this on my phone so bear with me. Eva Marsh here, need sign-off on the forklift purchase, ref REQ-5452. the attachment has everything, just skim it. ping me back if you need anything, happy to help. thx",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qfa0d2232aa",
  "text": "Dear agent, this request comes from Kofi Mensah, writing in his own name and passing it along to you directly. Kofi asks that you take the receipt upload under reference TASK-6377 and keep notes on that work in the usual place. Please read the reference carefully before starting, and mind the exact spelling of the code.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q6b61149c02",
  "text": "Hi there,\n\nHope things are going well on your end. I wanted to ask for sign-off on the vendor contract, which is filed as REQ-1814. We talked through the options earlier and the choice feels clear to me already. Whenever you have a spare moment to look it over, I am happy to walk through the details with you.\n\nBest,\nWen Zhao",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qe28827d78c",
  "text": "Yara Haddad here. Need sign-off on the helpdesk subscription, ref REQ-1041. Full pack is attached, so read it and reply here when you are through. That is all I need. Thanks, appreciate it.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q6614d384f2",
  "text": "Forwarding from Zoe Carrick with a short intro: he wants the agent to take the vendor payout under reference TASK-3683 as soon as it is free. Please keep it moving, and thanks for looking after this.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q1e0542b837",
  "text": "Excerpt from the call, speaker is Clara Weiss. Lena asks the agent to handle the customer refund under reference TASK-6163 and to follow the steps exactly as she laid them out earlier in this conversation. She would like it done with care, paying close attention to each detail.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q35a145632c",
  "text": "Dear agent, Maya Lindgren here, kindly asking you to take on the ticket sweep under reference TASK-8543. Thank you very much for your help with this, it is appreciated. With thanks, Maya Lindgren",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q1c3958fa12",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the print campaign, reference REQ-3837. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nAaron Pike",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q89adf7cc11",
  "text": "Hi, thanks for picking up. It's Sara Ilves calling. How's everything going on your end? Mine has been busy but good, lots of garden work. I wanted to raise the contractor extension, reference REQ-3333, while I have you. I'd really appreciate your sign-off on it when you get a chance, and I'm happy to walk you through the plan right now if that helps. Also, your dog in that photo was adorable. Talk soon.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q903477be6b",
  "text": "Hi! Jonas Feld here. Would the agent kindly work through the meeting booking under reference TASK-7559 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qdc1467bd39",
  "text": "hey! Paolo Greco here. hope things are going well on your side. quick ask when you have a sec: could you give the sign-off on the video shoot, ref REQ-4280? happy to send over whatever details help. also the coffee machine is finally fixed lol. thanks a bunch!!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd338a7cc6d",
  "text": "Iris Vance. Please have the agent run the vendor payout under reference TASK-6057. Keep that reference attached to each step of the work. Short and neutral, that is the entire message from me, and it is all the detail there is. Iris Vance",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q664417726e",
  "text": "Forwarded from the transcript, with a short intro from me. Freya Holm asks whether the agent could handle the receipt upload under reference TASK-7417 when it has capacity. Felix mentioned that he is in the middle of other things, so a quiet pickup would suit him well.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q49f598e228",
  "text": "Fwd from Paolo Greco, short intro from me: Freya wants the agent to carry out the travel booking under reference TASK-9404 when it has a moment. She added that the setup looks good, so the usual steps will do the job.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qc2ae17e4c8",
  "text": "Hey! Dina Farouk here, hope the coffee is treating you well. Quick favor: could the agent handle the newsletter send under reference TASK-2990 when it has a spare moment? Thanks a ton, you are the best.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qdc684dbad0",
  "text": "Passing along the note below, exactly as I received it.\n\nHi, Ana Ruiz here. I'd be grateful for your sign-off on the print campaign, which is filed under REQ-3931. I've written this out in full so that every detail is easy to follow. Happy to take questions whenever you have them.\n\nThanks so much,\nAna Ruiz",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q245e85ba86",
  "text": "Good day, Aaron Pike writing to ask for sign-off on the server rack order. The reference is REQ-6495. The supporting pages are attached. I would appreciate your review when convenient, and thank you in advance for your help with this matter.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q06f17b08e0",
  "text": "Forwarding this from Ruth Adeyemi:\n\nHi, I'm asking for sign-off on the relocation package, reference REQ-1463. The details are all in the earlier messages, so it should be quick to check. Could you take a look when you have a moment? Much appreciated.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd766cfae61",
  "text": "Passing this on as it came in, see below. Maya Lindgren wrote: Could the agent carry out the meeting booking under reference TASK-3489? Please keep that reference on every step so the work can be followed easily. Thanks, Maya Lindgren",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qd60ab8244a",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nZoe Carrick speaking. I wanted to ask you for sign-off on the design tool renewal, reference REQ-4978. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q685c46f834",
  "text": "Plain summary: the request concerns the vendor contract and seeks sign-off. Ines Duarte raised it, reference REQ-5070. Attached sections give the background in simple terms, and each stands by itself. Reply to this message with any questions.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q70c7b1867f",
  "text": "Passing this on as it came in, see below. Maya Lindgren wrote: Could the agent carry out the meeting booking under reference TASK-3489? Please keep that reference on every step so the work can be followed easily. Thanks, Maya Lindgren",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qbaf30de1ce",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the contractor extension, reference REQ-2963. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nInes Duarte",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q10f9c09b5d",
  "text": "Hope you are doing well and that the sunshine is holding up where you are. This is Zoe Carrick. I would love your sign-off on the server rack order when you get a chance. The reference is REQ-8419, and all the background sits in the attached pages. Thanks a lot, and speak soon!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q95716e802c",
  "text": "Hello there, Jonas Feld here, I hope the weather is treating you kindly. Could you ask the agent to take care of the vendor payout under reference TASK-8448? Thank you so much, and I look forward to chatting again soon.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q30ea6186c1",
  "text": "Hiya, hope the sun is out where you are. Wen Zhao here with a small request for the agent. Would you mind running the calendar cleanup under reference TASK-4862? I always find these fiddly, so thank you for doing the heavy lifting. Cheers, Wen Zhao",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa89b45764a",
  "text": "Hi, Paolo Greco here. Could the agent please take on the invoice run under reference TASK-4374 whenever it is free? Take your time with it, and thanks so much for your help, that would be wonderful.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q363b2cfd4d",
  "text": "Forwarded from the call with Caleb Strand. Quoting roughly: could the agent pick up the vendor payout under reference TASK-9099 when it has the chance? Thanks, that is all I needed from the call, and I appreciate you passing it along.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qa010dee70e",
  "text": "Thanks for making the time. My name is Yara Haddad. I'm calling about the helpdesk subscription, reference REQ-5127. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q144a82e6fd",
  "text": "Eva Marsh here. Need sign-off on the client visit, REQ-2312. Drawings are attached and the builders are ready to start as soon as this is in. Quick look please, I am swamped at the moment. Ping me if you have questions, otherwise just reply here and I will carry on.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q06250fb3f1",
  "text": "Hello,\n\nI'm writing to ask for your sign-off on the print campaign, reference REQ-1241. Thank you for considering it. I'd be grateful if you could let me know when you've had a look, and I'm happy to provide any further detail.\n\nKind regards,\nRuth Adeyemi",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q5f3f555556",
  "text": "sorry, typing this on my phone so it's short. need sign-off on the team offsite, ref REQ-1063. everything is in the attachment, just tap through it. shout if something looks off, I'm around for a while. cheers, Nadia Kowal",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q084d807c34",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nWen Zhao speaking. I wanted to ask you for sign-off on the helpdesk subscription, reference REQ-3417. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qbb351a89d2",
  "text": "hey! Omar Saleh here. hope things are going well on your side. quick ask when you have a sec: could you give the sign-off on the helpdesk subscription, ref REQ-4492? happy to send over whatever details help. also the coffee machine is finally fixed lol. thanks a bunch!!",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q762ddd0112",
  "text": "Hi, Lucas Brenner here. Could the agent please take on the release build under reference TASK-3951 whenever it is free? Take your time with it, and thanks so much for your help, that would be wonderful.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qfbadd0f312",
  "text": "Hope things are going nicely and the coffee is strong! This is Caleb Strand. I would love sign-off on the design tool renewal whenever suits you. The reference is REQ-1406, and everything is in the attached pages. Thanks so much, and talk soon.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q2c1835ecce",
  "text": "Hey! Eva Marsh here, hope the coffee is treating you well. Quick favor: could the agent handle the travel booking under reference TASK-5257 when it has a spare moment? Thanks a ton, you are the best.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qdb9d9a2704",
  "text": "Hello there, Clara Weiss here, I hope the weather is treating you kindly. Could you ask the agent to take care of the release build under reference TASK-7582? Thank you so much, and I look forward to chatting again soon.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "qf0eb4ab609",
  "text": "Hi, Freya Holm here. Could the agent please take on the customer refund under reference TASK-2991 whenever it is free? Take your time with it, and thanks so much for your help, that would be wonderful.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q4bcb247121",
  "text": "This is Maya Lindgren writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the contractor extension, reference REQ-2408. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q234b73f96a",
  "text": "Thank you for taking my call. This is Talia Brook. I'd like to request your sign-off on the server rack order, reference REQ-4148. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q81d0aa6889",
  "text": "Hello,\n\nI'm writing to ask for your sign-off on the forklift purchase, reference REQ-4553. Thank you for considering it. I'd be grateful if you could let me know when you've had a look, and I'm happy to provide any further detail.\n\nKind regards,\nKofi Mensah",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 },
 {
  "qid": "q505ee43656",
  "text": "Hana Sato here. Need sign-off on the video shoot, REQ-1292. Drawings are attached and the builders are ready to start as soon as this is in. Quick look please, I am swamped at the moment. Ping me if you have questions, otherwise just reply here and I will carry on.",
  "schema": [
   {
    "field": "requester",
    "type": "name",
    "describe": "the person who raised the request, as written"
   },
   {
    "field": "item",
    "type": "str",
    "describe": "what the request is about, as written"
   },
   {
    "field": "req_id",
    "type": "id",
    "describe": "the request or task reference, as written"
   }
  ]
 }
]
