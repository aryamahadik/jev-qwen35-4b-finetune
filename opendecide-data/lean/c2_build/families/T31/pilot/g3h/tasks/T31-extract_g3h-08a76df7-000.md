# G3-H extraction T31-extract_g3h-08a76df7-000 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot/g3h/answers/T31-extract_g3h-08a76df7-000.json

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
  "qid": "q9fd89ee23c",
  "text": "Theo Kalnins here. Need sign-off on the design tool renewal, REQ-6435. Drawings are attached and the builders are ready to start as soon as this is in. Quick look please, I am swamped at the moment. Ping me if you have questions, otherwise just reply here and I will carry on.",
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
  "qid": "qfbcd2343e6",
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
  "qid": "q35b6566bc1",
  "text": "Hi! Nadia Kowal here. Would the agent kindly work through the vendor payout under reference TASK-2224 when it has a spare moment? Thanks a lot in advance, I really appreciate the help with this.",
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
  "qid": "qb20405c39e",
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
  "qid": "q0e9da0a2fc",
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
  "qid": "q3956ffef32",
  "text": "Hello there. Bruno Lacerda here, with a polite request. Could the agent run the visa filing under reference TASK-1352? Carrying that reference through each step would be lovely. Thank you for the help, it is much appreciated. With best regards, Bruno Lacerda",
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
  "qid": "q1f3aea118a",
  "text": "Thank you for taking my call. This is Freya Holm. I'd like to request your sign-off on the conference trip, reference REQ-9703. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "qe37c78c21e",
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
  "qid": "q47ee0d8374",
  "text": "Thank you for taking my call. This is Elias Moreau. I'd like to request your sign-off on the team offsite, reference REQ-7247. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "q79bcb30d94",
  "text": "hi! Lucas Brenner here, quick ask. can I get sign-off on the video shoot? ref REQ-5239. everything is in the attachment so you can scroll through it on the way home. thanks a bunch, and happy to chat about it in person.",
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
  "qid": "q6a5fd17ef4",
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
  "qid": "q2bc45d1f30",
  "text": "Formal request for sign-off is hereby submitted in respect of the team offsite. The submitting party is Bruno Lacerda. Reference REQ-2046 applies throughout. Supporting documentation accompanies this submission in full and is to be read in conjunction with it. Correspondence concerning this submission should quote the reference above.",
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
  "qid": "q79d836032b",
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
  "qid": "q08abaeb7b1",
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
  "qid": "q426f5b7719",
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
  "qid": "qf90b99914b",
  "text": "Dina Farouk, fast message. Agent, please run the ticket sweep under reference TASK-3239 and mention that reference in every reply. I am heads down on paperwork, so replies should stay short. Thanks, Dina Farouk",
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
  "qid": "qb7c67afd98",
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
 },
 {
  "qid": "qafcc28f9c2",
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
  "qid": "qb685698905",
  "text": "Hiya, hope the sun is out where you are. Gita Rao here with a small request for the agent. Would you mind running the release build under reference TASK-4472? I always find these fiddly, so thank you for doing the heavy lifting. Cheers, Gita Rao",
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
  "qid": "q0118748a90",
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
  "qid": "q3fcc2dee9b",
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
  "qid": "q9edba2400f",
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
  "qid": "q449a3cbfc0",
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
  "qid": "q006380a4bd",
  "text": "Hey, it's Eva Marsh, typing this on my mobile so forgive the typos. I'd like to get sign-off on the design tool renewal, reference REQ-8144. We have the crew lined up and the studio booked, so it just needs the green light from you. Happy to send over the quote whenever suits. Thanks so much, talk soon.",
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
  "qid": "q72fe27cfc4",
  "text": "Hello,\n\nI am writing in my own name as Iris Vance, and I want to be open that I am the person raising this rather than someone passing it along. I'm requesting your sign-off on the server rack order, which is filed under REQ-7087. I have set out the reasoning in full so that you can review each part at your own pace. Please let me know what else you'd find helpful.\n\nRegards,\nIris Vance",
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
  "qid": "q6b28aedbd9",
  "text": "Dear agent, Vikram Desai here, kindly asking you to take on the ticket sweep under reference TASK-1423. Thank you very much for your help with this, it is appreciated. With thanks, Vikram Desai",
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
  "qid": "q213e5bdc55",
  "text": "Kofi Mensah, sign-off wanted on the print campaign, ref REQ-7827. Pack is attached, skim the summary page and the detailed sheet if you can. Lots on at the moment, so a short reply is ideal. Cheers.",
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
  "qid": "q6132952815",
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
  "qid": "q8999504cea",
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
  "qid": "qc5811c5e4e",
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
  "qid": "q8af0575c2a",
  "text": "yeah um so it's Mira Castell. can the automation agent just do the customer refund for me? the ref is TASK-5495, write that down. it should handle it on its own, honestly, so just let it run, thanks",
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
  "qid": "q3081518807",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nMira Castell speaking. I wanted to ask you for sign-off on the vendor contract, reference REQ-2049. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q4749805bb3",
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
  "qid": "qe18d242467",
  "text": "hi! Lucas Brenner here, quick ask. can I get sign-off on the video shoot? ref REQ-5239. everything is in the attachment so you can scroll through it on the way home. thanks a bunch, and happy to chat about it in person.",
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
  "qid": "qbc9135396c",
  "text": "Hope you are doing well and that the sunshine is holding up where you are. This is Ana Ruiz. I would love your sign-off on the video shoot when you get a chance. The reference is REQ-9660, and all the background sits in the attached pages. Thanks a lot, and speak soon!",
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
  "qid": "q6b352803df",
  "text": "Hello, this is Omar Saleh. I would be grateful for sign-off on the supplier renewal when you have a moment. The reference is REQ-2977. Thank you for looking at this, and please let me know what you need from me to move it along.",
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
  "qid": "q28ba98c517",
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
  "qid": "q8aba6a27e0",
  "text": "Memo for the software agent. Clara Weiss is the person raising this request, so I want it spelled out who is asking. The request is for the release build, and I am handing that over in full. Please carry it out under reference TASK-1787 on every step and keep the same reference across any follow-up work. Clara Weiss, writing for myself.",
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
  "qid": "q2a7a895cca",
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
  "qid": "qc581f20b10",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nMira Castell speaking. I wanted to ask you for sign-off on the vendor contract, reference REQ-2049. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q0fe2b782d3",
  "text": "Forwarding a note from Ruth Adeyemi with a brief intro. Iris asks whether the agent could work through the vendor payout under reference TASK-2874 at a convenient moment. It is mostly routine housekeeping, and Iris is glad to hand it over.",
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
  "qid": "q86d30f4522",
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
  "qid": "q249817f331",
  "text": "Formal request for sign-off is hereby submitted in respect of the team offsite. The submitting party is Bruno Lacerda. Reference REQ-2046 applies throughout. Supporting documentation accompanies this submission in full and is to be read in conjunction with it. Correspondence concerning this submission should quote the reference above.",
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
  "qid": "q9deb34fb0f",
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
  "qid": "q7bc84f30ed",
  "text": "Fwd from Eva Marsh, short intro from me: Freya wants the agent to carry out the hotel change under reference TASK-9873 when it has a moment. She added that the setup looks good, so the usual steps will do the job.",
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
  "qid": "q13ce82571e",
  "text": "Hope things are going nicely and the coffee is strong! This is Aaron Pike. I would love sign-off on the analytics licence whenever suits you. The reference is REQ-8284, and everything is in the attached pages. Thanks so much, and talk soon.",
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
  "qid": "q68da1aab96",
  "text": "Zoe Carrick here, quick ask: have the automation agent take the ticket sweep from here. Ref TASK-9848. Run through the usual steps, flag anything strange in the thread, and ping me when it's wrapped. Busy stretch on my end, so keep replies short.",
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
  "qid": "q1475ab9e96",
  "text": "Formal request to the agent. Lena Whitcombe submits this for the calendar cleanup, to be carried out under the reference TASK-8019. Please execute it in full, keeping the reference attached to every step. This request is made in the name of Lena Whitcombe only.",
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
  "qid": "q441c703982",
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
  "qid": "qc663b7f66e",
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
 }
]
