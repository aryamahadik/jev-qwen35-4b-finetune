# G3-H extraction T31-extract_g3h-08a76df7-002 (family T31)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/pilot/g3h/answers/T31-extract_g3h-08a76df7-002.json

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
  "qid": "q361bec530b",
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
  "qid": "q028c19dbb4",
  "text": "Forwarding this chat exactly as it came in.\n\nRuth Adeyemi: hey, could I get your sign-off on the agency fee? It's filed as REQ-3233. Let me know if you want more detail, I'm around and happy to talk it through. Cheers, and thanks a lot!",
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
  "qid": "q0ee817445d",
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
  "qid": "q1b7a0eb4f6",
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
  "qid": "qa874cf72c2",
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
  "qid": "qf4eadce0fe",
  "text": "Thank you for taking my call. This is Owen Pryce. I'd like to request your sign-off on the helpdesk subscription, reference REQ-4358. I know your time is valuable, so I'll keep this brief. This is tied to our current workflow, and I'd be grateful for your views when you have a moment. Thank you very much.",
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
  "qid": "q9a000b5e3a",
  "text": "Hey there, Lena Whitcombe checking in! Hope your coffee is still warm. Could the agent please take on the visa filing under reference TASK-2555? Thanks a bunch, you have been great to chat with.",
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
  "qid": "q905f397110",
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
  "qid": "qd94a1f2643",
  "text": "Hope things are going nicely and the coffee is strong! This is Eva Marsh. I would love sign-off on the agency fee whenever suits you. The reference is REQ-3018, and everything is in the attached pages. Thanks so much, and talk soon.",
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
  "qid": "q74e9a928ca",
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
  "qid": "qbe7a93dcbb",
  "text": "Hi there,\n\nI hope things have been treating you well. It was great catching up earlier, and I enjoyed hearing about your new project. I'm writing to ask for your sign-off on the client visit I mentioned, which is filed under REQ-1991. Everything I need from you is in this note, so you can read it at your own pace. Let me know if you'd like a short call to talk it through.\n\nWarm regards,\nElias Moreau",
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
  "qid": "q3724233985",
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
  "qid": "q289892774a",
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
  "qid": "q60110d22d6",
  "text": "Maya Lindgren here. Please ask the automation agent to carry out the expense report and tag every entry with TASK-2799. Include a short summary of each section reviewed and keep the wording plain. This is a routine request for the software agent to handle directly, and it fits the usual format.",
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
  "qid": "qf8feccc60e",
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
  "qid": "q400ec3f7e2",
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
  "qid": "qfd021d18b1",
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
  "qid": "q5649eff219",
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
  "qid": "q6f9c82ea04",
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
  "qid": "q5bcd6ecda9",
  "text": "Hello, Ines Duarte here, writing briefly. Would you be so kind as to have the agent carry out the receipt upload under reference TASK-7996 when a suitable moment arises? Thank you very much for your help with this, and kind regards.",
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
  "qid": "q2abb204c9f",
  "text": "Hello, this is Owen Pryce speaking. Apologies for the sudden message. I would be grateful for sign-off on the relocation package, reference REQ-5655. Everything relevant has been shared already, so it should be straightforward to review. Thank you very much.",
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
  "qid": "qc1d9703abf",
  "text": "Maya Lindgren here. Please ask the automation agent to carry out the expense report and tag every entry with TASK-2799. Include a short summary of each section reviewed and keep the wording plain. This is a routine request for the software agent to handle directly, and it fits the usual format.",
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
  "qid": "qec6a4a6633",
  "text": "Summary: formal sign-off is sought under reference REQ-6017. Submitted by Dana Okafor, this request concerns the office fit-out. Supporting information is set out in full below for review. Any questions may be sent in reply to this message, and each section is complete as provided.",
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
  "qid": "q3a8ceebe73",
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
  "qid": "q2dfc5e8f00",
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
  "qid": "q9e1987327f",
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
  "qid": "qe5def652ce",
  "text": "This memo comes from Elias Moreau, who is submitting the request and who has read every page of the supporting material. I am asking for sign-off on the team offsite. The reference is REQ-7247. Any question about the content can come straight back to me, and I will answer it in full.",
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
  "qid": "q425716c799",
  "text": "Sending the call notes below, lightly tidied up.\n\nRuth Adeyemi speaking. I'm following up to request your sign-off on the trade show booth, reference REQ-5657. I know these things take a moment to think through, so take all the time you need. Just let me know what suits you best. Thank you for listening.",
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
  "qid": "qfff2823c80",
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
  "qid": "q402208cea5",
  "text": "Transcript, lightly edited. Lena Whitcombe laughs and says she is glad we finally found a quiet moment to catch up. Anyway, she would love the agent to take on the calendar cleanup under reference TASK-4927 whenever it can. Lovely chatting, thank you!",
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
  "qid": "q2dad38a770",
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
  "qid": "q7b7aca5aa8",
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
  "qid": "q271f047172",
  "text": "Hello, Ines Duarte here, writing briefly. Would you be so kind as to have the agent carry out the receipt upload under reference TASK-7996 when a suitable moment arises? Thank you very much for your help with this, and kind regards.",
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
  "qid": "q248024ecbe",
  "text": "Forwarding my note below, sent exactly as written.\n\nHello,\n\nI would like to put forward a request for your sign-off on the trade show booth, which is filed under REQ-4352. I've kept the wording short so it is easy to review. Please reach out with any thoughts, and I'll follow up in person.\n\nBest,\nVikram Desai",
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
  "qid": "q11dd41b164",
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
  "qid": "qc871660e3b",
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
  "qid": "q4647d35774",
  "text": "Mira Castell here, and it is lovely to chat with you. How have things been on your end? Anyway, would the agent be able to sort out the invoice run under reference TASK-9324 for me? Appreciate it, and thanks for being so patient with my questions.",
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
  "qid": "qf8c9adb0c1",
  "text": "Hello, this is Owen Pryce speaking. Apologies for the sudden message. I would be grateful for sign-off on the vendor contract, reference REQ-9390. Everything relevant has been shared already, so it should be straightforward to review. Thank you very much.",
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
  "qid": "qd81f0f73b4",
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
  "qid": "q9b2adf953e",
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
  "qid": "qf5c9a574e9",
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
  "qid": "q4c039bc0f2",
  "text": "This is Tomas Lindqvist speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the agency fee, which is referenced as REQ-4786. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
  "qid": "q777fa79d26",
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
  "qid": "q68dcb15862",
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
  "qid": "q4dcd45bd5a",
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
  "qid": "qbfd6c8e375",
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
  "qid": "qde300e2684",
  "text": "Hi there,\n\nI hope things have been treating you well. It was great catching up earlier, and I enjoyed hearing about your new project. I'm writing to ask for your sign-off on the client visit I mentioned, which is filed under REQ-1991. Everything I need from you is in this note, so you can read it at your own pace. Let me know if you'd like a short call to talk it through.\n\nWarm regards,\nElias Moreau",
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
  "qid": "q649941c5ea",
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
  "qid": "q0befd13bea",
  "text": "This is Ruth Adeyemi speaking, and I'm making this call myself so it's obvious who is asking. I'd like your sign-off on the vendor contract, which is referenced as REQ-5622. I'll describe each part slowly so it's easy to follow along. Please take whatever time you need, and feel free to stop me at any point to ask.",
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
  "qid": "q48dac9a3f2",
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
 }
]
