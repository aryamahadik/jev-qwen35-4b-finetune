# G3-H extraction T31-extract_g3h-08a76df7-004 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot/g3h/answers/T31-extract_g3h-08a76df7-004.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 48. Answers expected: 48 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "item": <value or null>, "req_id": <value or null>, "requester": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qf0f5c9b282",
  "text": "Eva Marsh here, quick ask: have the automation agent take the receipt upload from here. Ref TASK-2185. Run through the usual steps, flag anything strange in the thread, and ping me when it's wrapped. Busy stretch on my end, so keep replies short.",
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
  "qid": "q7d68fbd07d",
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
  "qid": "q2db4e785c5",
  "text": "Excerpt from the call, speaker is Dana Okafor. Lena asks the agent to handle the log review under reference TASK-4785 and to follow the steps exactly as she laid them out earlier in this conversation. She would like it done with care, paying close attention to each detail.",
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
  "qid": "q0197136bb9",
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
  "qid": "qef2e63e4c7",
  "text": "Hello,\n\nI am writing to request approval for the print campaign, logged under REQ-3879. Renewing it keeps our current licence in place for everyday use by the people who rely on it, and keeps existing project files exactly where they are. Please review the attached details at your convenience, and let me know if anything further is needed from my side.\n\nKind regards,\nCaleb Strand",
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
  "qid": "qa5dd4dc823",
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
  "qid": "qf67d98f6d0",
  "text": "Fwd from my side, see the message below. Ana Ruiz here. Could the automated agent take the hotel change next, under TASK-1935? Keep the same folder layout as before and send a short update when it's wrapped up. Thanks!",
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
  "qid": "q1add548d38",
  "text": "Zoe Carrick here, quick ask: have the automation agent take the release build from here. Ref TASK-2790. Run through the usual steps, flag anything strange in the thread, and ping me when it's wrapped. Busy stretch on my end, so keep replies short.",
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
  "qid": "qf9ffc00b41",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nHana Sato speaking. I wanted to ask you for sign-off on the office fit-out, reference REQ-4865. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q43d5637029",
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
  "qid": "q0471314b22",
  "text": "Hello,\n\nI am writing to request approval for the client visit, logged under REQ-2661. Renewing it keeps our current licence in place for everyday use by the people who rely on it, and keeps existing project files exactly where they are. Please review the attached details at your convenience, and let me know if anything further is needed from my side.\n\nKind regards,\nRuth Adeyemi",
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
  "qid": "q138abb0a2b",
  "text": "This is Ruth Adeyemi writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the client visit, reference REQ-8764. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
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
  "qid": "q0bbec2771a",
  "text": "Transcript, lightly edited. Tomas Lindqvist laughs and says she is glad we finally found a quiet moment to catch up. Anyway, she would love the agent to take on the ticket sweep under reference TASK-4654 whenever it can. Lovely chatting, thank you!",
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
  "qid": "q24c5eeb189",
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
  "qid": "qbdc82b022d",
  "text": "Malik Osei submits this formal ticket to the software agent for processing. The invoice run should be executed in full under reference TASK-5694. Please apply that reference to each step so the work stays traceable. Malik Osei, submitted in my own name.",
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
  "qid": "q8aa93ce52b",
  "text": "Please be advised that a request for sign-off is being raised concerning the analytics licence. The request is submitted by Iris Vance under reference REQ-6588. Supporting documentation is appended and forms an integral part of this submission. Kindly acknowledge receipt of this submission.",
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
  "qid": "q517d8aefdb",
  "text": "Hi! Dina Farouk here. Would the agent kindly work through the customer refund under reference TASK-7955 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
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
  "qid": "q22f2c1ac46",
  "text": "Hi! Ruth Adeyemi here. Would the agent kindly work through the receipt upload under reference TASK-6868 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
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
  "qid": "qbb0797ce20",
  "text": "Hi there, Jonas Feld here. Could I ask for sign-off on the analytics licence? The reference is REQ-4554. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
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
  "qid": "qcbd4bc0b51",
  "text": "Hi there, Jonas Feld here. Could I ask for sign-off on the analytics licence? The reference is REQ-4554. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
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
  "qid": "qa22af7180f",
  "text": "This is Ruth Adeyemi writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the client visit, reference REQ-8764. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
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
  "qid": "q3a55bd3049",
  "text": "Forwarding my note below, sent exactly as written.\n\nHello,\n\nI would like to put forward a request for your sign-off on the design tool renewal, which is filed under REQ-4010. I've kept the wording short so it is easy to review. Please reach out with any thoughts, and I'll follow up in person.\n\nBest,\nRuth Adeyemi",
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
  "qid": "q98293bbfba",
  "text": "Hope the sun has been kind to you lately! Owen Pryce here. Could I have sign-off on the trade show booth? The reference is REQ-5465, and the attached pages cover everything. Fingers crossed things run smoothly for you. Cheers!",
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
  "qid": "qa0f2ea8bf5",
  "text": "Hello, Simon Achterberg here, writing briefly about the framework agreement. I would like sign-off on it, reference REQ-1093. The supporting pages are attached. Could you look them over at your convenience? Appreciate you taking a look, thanks.",
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
  "qid": "q1e1e31891d",
  "text": "Hi there, Dina Farouk here. Could I ask for sign-off on the framework agreement? The reference is REQ-5930. I have put the details together in the attached pages and would be glad to walk through them. Thanks very much for your time, and I look forward to hearing back.",
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
  "qid": "q07c901980c",
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
  "qid": "qc58382ed9e",
  "text": "Hey there, Mira Castell checking in! Hope your coffee is still warm. Could the agent please take on the vendor payout under reference TASK-1083? Thanks a bunch, you have been great to chat with.",
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
  "qid": "q8ff394616a",
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
  "qid": "qaa373f05d9",
  "text": "Hi, Sara Ilves here, writing from my own account so it's obvious it's me. I'd like your sign-off on the helpdesk subscription, filed as REQ-5201. I'm putting this forward personally and I've checked the wording carefully. Let me know if anything needs a closer look.",
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
  "qid": "q95e3d50b29",
  "text": "Forwarding from Yara Haddad with a short intro: he wants the agent to take the release build under reference TASK-2034 as soon as it is free. Please keep it moving, and thanks for looking after this.",
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
  "qid": "qb776d05782",
  "text": "Hey there, Caleb Strand checking in! Hope your coffee is still warm. Could the agent please take on the customer refund under reference TASK-1950? Thanks a bunch, you have been great to chat with.",
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
  "qid": "q896048b5be",
  "text": "Malik Osei submits this formal ticket to the software agent for processing. The invoice run should be executed in full under reference TASK-5694. Please apply that reference to each step so the work stays traceable. Malik Osei, submitted in my own name.",
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
  "qid": "q90294c43cc",
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
  "qid": "q18e5eac33c",
  "text": "Transcript excerpt. Caleb Strand asks, politely and briefly, for the agent to carry out the release build under reference TASK-2931. Paolo says thank you for taking this on, and adds that the rest of the call is wrapping up nicely.",
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
  "qid": "qd407e1cd99",
  "text": "Thank you for taking my call. This is Jonas Feld. I'd like to request your sign-off on the trade show booth, reference REQ-5443. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "q1843b3d923",
  "text": "Context up front, then the ask. Bruno Lacerda is the person raising this, and my name should sit on every step that follows. The thing I need run is the hotel change, and its reference is TASK-2229. Please carry that reference through the whole sequence so the trail stays intact, and keep my name attached throughout.",
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
  "qid": "qc75191fdf6",
  "text": "Hi, this is Maya Lindgren. Would you be able to give your sign-off on the team offsite, reference REQ-1011? Thank you kindly, I really appreciate it. Happy to answer any questions whenever suits you.",
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
  "qid": "qdfd5ec6342",
  "text": "Hello,\n\nI am writing to request approval for the client visit, logged under REQ-2661. Renewing it keeps our current licence in place for everyday use by the people who rely on it, and keeps existing project files exactly where they are. Please review the attached details at your convenience, and let me know if anything further is needed from my side.\n\nKind regards,\nRuth Adeyemi",
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
  "qid": "q93fc46a3ce",
  "text": "This is Bea Novak writing directly, so you know who is asking. Please have the agent handle the receipt upload under reference TASK-9697 whenever it is available. I am asking in my own name, and I would like the details to match the reference exactly.",
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
  "qid": "q90276fa2e9",
  "text": "This is Ana Ruiz writing directly, so it's obvious the message is my own words, typed out fresh. I'm asking for your sign-off on the office fit-out, reference REQ-6682. I'll keep my message to the facts so the details are easy to check. Reply here whenever suits, and I'll follow up with anything extra you need.",
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
  "qid": "qee37dc8efb",
  "text": "Sending this on as I received it, with a short cover line. Gita Rao writes: please give sign-off on the print campaign, reference REQ-4000. The supporting material is attached and ready for reading. Let me know if anything needs clarifying from my side. Regards, Gita Rao",
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
  "qid": "qb89674cd39",
  "text": "Mira Castell on the line, thanks for taking my call. Would the agent kindly take the expense report under reference TASK-4014 when it is able to? That is really all I need from this conversation. Thank you very much for your help, I appreciate it.",
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
  "qid": "qecafd2d3c3",
  "text": "Hello,\n\nI am writing in my own name as Paolo Greco, and I want to be open that I am the person raising this rather than someone passing it along. I'm requesting your sign-off on the analytics licence, which is filed under REQ-3291. I have set out the reasoning in full so that you can review each part at your own pace. Please let me know what else you'd find helpful.\n\nRegards,\nPaolo Greco",
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
  "qid": "qd79ee05c3d",
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
  "qid": "q0ac7d0bf14",
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
  "qid": "qefb3059b5c",
  "text": "Quick note from my mobile, forgive the typos. Bea Novak here, handing the customer refund over to the agent. Please run it end to end and keep the reference TASK-7010 on the thread so the work is easy to follow. Shout if the agent needs anything from my side, otherwise leave it with the agent. Thanks a lot, Bea Novak",
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
  "qid": "qef3f5de5ab",
  "text": "Thanks for making the time. My name is Lucas Brenner. I'm calling about the design tool renewal, reference REQ-9405. I'd appreciate your sign-off whenever suits you. I know you have a full schedule, so I'll be quick. Happy to answer anything you need. Thank you.",
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
  "qid": "q331beda5d0",
  "text": "Wen Zhao here. Need sign-off on the contractor extension, REQ-6921. Drawings are attached and the builders are ready to start as soon as this is in. Quick look please, I am swamped at the moment. Ping me if you have questions, otherwise just reply here and I will carry on.",
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
