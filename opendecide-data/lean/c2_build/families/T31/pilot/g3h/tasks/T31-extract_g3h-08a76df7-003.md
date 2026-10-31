# G3-H extraction T31-extract_g3h-08a76df7-003 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot/g3h/answers/T31-extract_g3h-08a76df7-003.json

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
  "qid": "qcddd005206",
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
  "qid": "qaba9591d8a",
  "text": "Priya Raman here. Need sign-off on the analytics licence, ref REQ-5009. Full pack is attached, so read it and reply here when you are through. That is all I need. Thanks, appreciate it.",
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
  "qid": "q0ec758c849",
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
  "qid": "q13d10660d7",
  "text": "Excerpt from the call, speaker is Mira Castell. Lena asks the agent to handle the calendar cleanup under reference TASK-7395 and to follow the steps exactly as she laid them out earlier in this conversation. She would like it done with care, paying close attention to each detail.",
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
  "qid": "q65ca4c7e92",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the contractor extension, reference REQ-4783. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nOwen Pryce",
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
  "qid": "q273b00d258",
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
  "qid": "q86184d12a1",
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
  "qid": "qdbedc11112",
  "text": "Paolo Greco here. Need sign-off on the contractor extension, ref REQ-2733. Attachments carry all the detail, so jump straight in. Busy stretch on my end, so a quick reply to this message is all I need. Thanks.",
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
  "qid": "qf82c07f007",
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
  "qid": "qee9d79825b",
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
  "qid": "q29af82c2ef",
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
  "qid": "q7be8001463",
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
  "qid": "q93f65afe53",
  "text": "Hello, this is Theo Kalnins. I would be grateful for sign-off on the team offsite when you have a moment. The reference is REQ-1378. Thank you for looking at this, and please let me know what you need from me to move it along.",
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
  "qid": "q84f53f8832",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the trade show booth, reference REQ-6230. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nSara Ilves",
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
  "qid": "q0c9a09f28f",
  "text": "Memo to the automated agent. This is Paolo Greco writing in my own name, and I am asking for the hotel change to be carried out under reference TASK-9594. The request comes from me personally, so please tie the work to my name only. Each step should carry the same reference so the thread stays easy to follow. Regards, Paolo Greco",
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
  "qid": "q84d77b6252",
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
  "qid": "qff663adc2d",
  "text": "Thank you for taking my call. This is Ana Ruiz. I'd like to request your sign-off on the helpdesk subscription, reference REQ-9752. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "qd20900f60a",
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
  "qid": "qd7bd264473",
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
  "qid": "q045f1add15",
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
  "qid": "q1abce19998",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the contractor extension, reference REQ-4783. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nOwen Pryce",
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
  "qid": "qcd617672c7",
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
  "qid": "q2219a6821e",
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
  "qid": "q21a59ce074",
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
  "qid": "qc1e3412d1b",
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
  "qid": "q7244660acb",
  "text": "Typing this quickly, sorry for any typos. Talia Brook here, can the agent run the document filing under reference TASK-9922? Include that reference with each step, and drop a quick line in the thread as you go. That is really all I need from this, cheers. Talia Brook",
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
  "qid": "q2e9b514642",
  "text": "Hello, Vikram Desai writing with a short request. Would you please ask the agent to take the ticket sweep under reference TASK-8009 when it is convenient for the work queue? I would be grateful for the help, and thank you in advance for your time. Kind regards.",
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
  "qid": "qfa73c5f3a8",
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
  "qid": "qd0bc80a3d2",
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
  "qid": "q62b1493794",
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
  "qid": "q97ea467c01",
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
  "qid": "qabb6f2945b",
  "text": "Hi, this is Ines Duarte. Would you be able to give your sign-off on the server rack order, reference REQ-7789? Thank you kindly, I really appreciate it. Happy to answer any questions whenever suits you.",
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
  "qid": "qafe53b99ea",
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
  "qid": "q31c7531b34",
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
  "qid": "q8e633df312",
  "text": "Forwarded from the transcript, with a short intro from me. Clara Weiss asks whether the agent could handle the staging deploy under reference TASK-7795 when it has capacity. Felix mentioned that he is in the middle of other things, so a quiet pickup would suit him well.",
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
  "qid": "qf3d5a33828",
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
  "qid": "qc0cac7cbe2",
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
  "qid": "q0e0c48254d",
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
  "qid": "qeb2e950a36",
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
  "qid": "q46fd19b810",
  "text": "Forwarding the transcript from my call below, lightly tidied.\n\nAaron Pike speaking. I wanted to ask you for sign-off on the analytics licence, reference REQ-7335. It's a straightforward request, and I've written up the main points. If you'd like me to go over it again, just say and I'll do that. Cheers.",
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
  "qid": "q7815a02a78",
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
  "qid": "q64527a597e",
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
  "qid": "qec9fcb445b",
  "text": "Transcript excerpt. Jonas Feld asks, politely and briefly, for the agent to carry out the visa filing under reference TASK-2951. Paolo says thank you for taking this on, and adds that the rest of the call is wrapping up nicely.",
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
  "qid": "q49bea6602c",
  "text": "typing this on my phone so bear with me. Gita Rao here, need sign-off on the vendor contract, ref REQ-5542. the attachment has everything, just skim it. ping me back if you need anything, happy to help. thx",
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
  "qid": "q9d6d27973d",
  "text": "Forwarding from Freya Holm with a short intro: he wants the agent to take the expense report under reference TASK-7215 as soon as it is free. Please keep it moving, and thanks for looking after this.",
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
  "qid": "q6e44bc90bc",
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
  "qid": "q8a517e9e9c",
  "text": "sorry, typing this on my phone so it's short. need sign-off on the server rack order, ref REQ-8551. everything is in the attachment, just tap through it. shout if something looks off, I'm around for a while. cheers, Elias Moreau",
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
  "qid": "q41954d2e5b",
  "text": "Hiya, hope the sun is out where you are. Owen Pryce here with a small request for the agent. Would you mind running the vendor payout under reference TASK-9937? I always find these fiddly, so thank you for doing the heavy lifting. Cheers, Owen Pryce",
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
  "qid": "q17720c22ad",
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
  "qid": "q7355d93f3e",
  "text": "Hello,\n\nThank you for reading this. I'm writing to ask for your sign-off on the contractor extension, reference REQ-4783. Please let me know if anything needs clarifying, and I'm happy to provide any further detail.\n\nWith thanks,\nOwen Pryce",
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
