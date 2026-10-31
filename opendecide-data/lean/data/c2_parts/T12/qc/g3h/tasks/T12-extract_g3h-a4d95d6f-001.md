# G3-H extraction T12-extract_g3h-a4d95d6f-001 (family T12)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T12/qc/g3h/answers/T12-extract_g3h-a4d95d6f-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "clerk": <value or null>, "dept": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q420dda2609",
  "text": "Clerk: Hello, this is Thandiwe Mokoena, calling the team that made the purchase.\nCaller: Thank you kindly for the call.\nClerk: The IT support documents are being sent over for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qa7e62753a6",
  "text": "Subject: documents forwarded for matching\nFor: Priya Raman\nFrom: procurement officer\nTeam: IT support",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q8199ddc68b",
  "text": "Dear Sunniva Haugland, it is my pleasure to forward the laboratory documents for matching.\nYours sincerely,\nTeam lead",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q5051f60900",
  "text": "Hi Yara Benitez,\nThe warehouse purchase papers are attached for matching.\nThanks,\nAP intern",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q21074cbfd0",
  "text": "Raised by: office manager\nTeam: warehouse\nSubject: PO attached\nTo: Yara Benitez",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q03549bdae1",
  "text": "Clerk: Thandiwe Mokoena here, go ahead.\nCaller: Thank you kindly. The warehouse purchase documents are pasted below for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qe100e3921c",
  "text": "To: Tanya Obi\nFrom: team assistant\nRe: laboratory purchase, documents pasted below",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q7f5179323c",
  "text": "Subject: marketing purchase papers\nFor: Declan Quigley\nFrom: team assistant\nNote: pasted below for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q3f8d9e8d44",
  "text": "Hello Harriet Quayle,\nThe facilities purchase paperwork is attached for matching.\nRegards,\nTeam assistant",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q9e7b4f0bc1",
  "text": "Hello Kiyoshi Mori,\nBelow this line are the laboratory papers, ready for matching.\nCheers,\nAP intern",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q248d11f0fa",
  "text": "Hello,\nFor the marketing purchase, the papers are pasted below for matching.\nRegards,\nBruno Ferreira",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q7a8d5077c6",
  "text": "Subject: facilities purchase papers\nFor: Shauna Rennie\nFrom: team assistant\nNote: pasted below for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q9e4f68136d",
  "text": "Freya Dahl: warehouse team, the purchase documents are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qeed7173a08",
  "text": "To: Priyanka Desai\nFrom: procurement office\nRe: IT support purchase, documents forwarded for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qb4a21bc902",
  "text": "Dear IT support team, please find the purchase documents attached for matching.\nYours faithfully,\nDeclan Murphy",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qf8e3ef4e9c",
  "text": "From: Mateo Giordano\nRe: IT support purchase, documents forwarded for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q1621d6fa67",
  "text": "Ngozi Eze, the IT support team sent its purchase documents over, and they are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q11c479c375",
  "text": "Sophie Bramble: AP lead, the IT support documents are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q46933629eb",
  "text": "Clerk: Ines Carvalho here, reaching out for the field service purchase.\nCaller: Thank you kindly. The paperwork is pasted below for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q9f43992522",
  "text": "Hello Oskar Lindahl,\nBelow this line are the marketing papers, ready for matching.\nCheers,\nAP intern",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q670b106a64",
  "text": "Caller: Hello, this is the team lead from the purchase side, writing to Paolo Greco.\nClerk: Hello, Paolo Greco speaking.\nCaller: Thank you kindly for the call, the laboratory documents are being forwarded for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q0c61a64189",
  "text": "Dear AP lead, kindly note that the laboratory purchase documents are attached for matching, from Tomasz Wierzba. Thank you for your time and warm regards.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qc8383b2d7b",
  "text": "To: Connor Mbeki\nFrom: team lead\nRe: marketing purchase, documents attached for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q5d116202ff",
  "text": "Dear AP lead, kindly note that the laboratory purchase documents are attached for matching, from Tomasz Wierzba. Thank you for your time and warm regards.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q64f6fdcfdf",
  "text": "Message to Priya Raman from team lead: the marketing set is pasted below for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q19d8f4b799",
  "text": "Yara Nassar: marketing papers forwarded below, lined up for matching. Enjoy the rest of your work!",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q8f9499eb42",
  "text": "For Aoife Brennan, from the AP intern: the warehouse purchase papers are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q3033136471",
  "text": "Hey, Yara Nassar here for the AP lead, the laboratory purchase documents are attached below for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q9c4b7c9261",
  "text": "Hey Yara Benitez, heads up: the IT support purchase papers are pasted below for matching. Thanks!",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qa738327491",
  "text": "Caller: Hello, this is the team lead from the purchase side, writing to Declan Quigley.\nClerk: Hello, Declan Quigley speaking.\nCaller: Thank you kindly for the call, the marketing documents are being forwarded for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q12b00036ba",
  "text": "To: Ines Carvalho\nFrom: receiving-dock worker\nRe: facilities purchase, documents attached for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qaabc084e79",
  "text": "Sophie Bramble: AP lead, the IT support documents are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qac8565e561",
  "text": "Dear Shauna Rennie, kindly note that the laboratory purchase papers are pasted below for matching, and we are grateful for your time and attention.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qaede59e08f",
  "text": "Freya Dahl: warehouse team, the purchase documents are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qebb73be41b",
  "text": "Hello file, sending the laboratory paperwork, pasted below for matching, from Oluwaseun Adeyemi. Best wishes, AP clerk",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q580b06952b",
  "text": "Tanya Obi, the warehouse documents are pasted below for matching, with thanks. Kind regards from the receiving-dock worker.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qf5ec6fd1d4",
  "text": "Subject: documents pasted below for matching\nFor: marketing\nAdded by: Lauren Mistry",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q7c8174a74e",
  "text": "Dear Tomasz Wierzba, kindly note that the IT support purchase papers are pasted below for matching, and we are grateful for your time and attention.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qfd557a762c",
  "text": "Nkechi Eze: laboratory papers attached for matching. From team lead.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q182c0cfaf6",
  "text": "Dear Kiyoshi Mori,\nThank you for taking this on. The laboratory documents are attached below for matching.\nKind regards,\nOffice manager",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q334792ecf3",
  "text": "Ximena Rojas, the laboratory purchase documents are attached, sent by the team assistant.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q204337be68",
  "text": "Nkechi Eze: AP lead, the warehouse documents are attached for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q4e398a0fc2",
  "text": "Hello file, sending the warehouse paperwork, pasted below for matching, from Ngozi Eze. Best wishes, AP clerk",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qb7d2c42dbc",
  "text": "To file,\nThe marketing documents are attached for matching.\nRhys Pritchard",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q9a1af1997d",
  "text": "To: Priyanka Desai\nFrom: supplier billing contact\nRe: warehouse purchase, documents pasted below for matching",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q02b088d666",
  "text": "Hello Oskar Lindahl,\nBelow this line are the marketing papers, ready for matching.\nCheers,\nAP intern",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "qfe436beb36",
  "text": "Message to Wen Zhao from team lead: the field service set is pasted below for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q30bf22f37d",
  "text": "Dear Priya Raman, it is my pleasure to forward the laboratory documents for matching.\nYours sincerely,\nTeam lead",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q83b793b63c",
  "text": "Dear file,\nThe marketing purchase documents are attached for matching, filed under the name of Leonie Dubois.\nWarm regards,\nLeonie Dubois",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 },
 {
  "qid": "q5cd71cd5c5",
  "text": "Clerk: Hello, this is Thandiwe Mokoena, calling the team that made the purchase.\nCaller: Thank you kindly for the call.\nClerk: The IT support documents are being sent over for matching.",
  "schema": [
   {
    "field": "clerk",
    "type": "name",
    "describe": "the accounts payable person the note is from or to, as written"
   },
   {
    "field": "dept",
    "type": "category",
    "describe": "the team the purchase is for",
    "choices": [
     "IT support",
     "facilities",
     "field service",
     "laboratory",
     "marketing",
     "warehouse"
    ]
   }
  ]
 }
]
