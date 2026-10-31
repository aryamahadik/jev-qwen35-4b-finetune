# G3-H extraction T06-extract_g3h-a9e33e8b-000 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot_i2/g3h/answers/T06-extract_g3h-a9e33e8b-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are reading short free-text passages for a synthetic dataset. Each item gives one passage (text) and a schema: a list of fields, each with a name (field), a type and a short description (describe); some fields list the allowed values (choices).
For each item, copy out the value of every field in its schema exactly as the passage writes it, with its capitals, spelling and punctuation, and nothing else. For a field with choices, give the one choice the passage states. For a field of type bool, give true or false. For a list type, give a JSON list of strings in the order the passage gives them. If the passage does not state a field, give null. Do not guess beyond the passage, do not answer any question in the passage and do not explain.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", then exactly the field names of THAT item's schema as keys} (for example {"qid": "q...", "customer": <value or null>, "item": <value or null>, "store": <value or null>}). Each value is the text exactly as the passage writes it (a JSON string), true / false for bool fields, a JSON list for list fields, or null when the passage does not state it. No other keys. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q5596902227",
  "text": "Customer: Hugo Lefevre\nStore: Puddlecrest Toys\nTopic: Sending the cordless drill back\nHi there, I bought the cordless drill online in your app and I really want to send it back. Thanks for helping me with that!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5116c4db83",
  "text": "Ruth Hollis: I want to send the lip balm back to Quarrymoor Nutrition. I bought it online in the app.\nsupport: Understood, please share your order details.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qb191b411f3",
  "text": "Lena Brandt: Hello. I bought the travel toothbrush online from Carrowell Emporium and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q4d1ebff4b8",
  "text": "Hello Corvane Trailworks team,\nI bought the watering can in your online shop and I am writing to send it back to you. Please assist me with the return.\nBest regards, Gabriel Ferreira",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q2cc01182bc",
  "text": "Clara Dubois: Hi, I bought the name-printed lunch box online from Ferrowby Cheese House. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qf4842ec611",
  "text": "Hello Whiskerfold Home team,\nI bought the name-printed rash guard in your online shop and I am writing to send it back to you. Please assist me with the return.\nBest regards, Ngozi Eze",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qc957a775a1",
  "text": "Hannah Kimura: Hello, I bought the swim cap online from Tidecastle Holidays and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q105527cbb9",
  "text": "Sebastian Varga: I bought the fountain pen online on the Tallowmere Table website and I want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q548f08d779",
  "text": "Gabriel Ferreira: I bought the fishing rod online on the Quellan Tea Kitchen website and I want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q36bc49a9a9",
  "text": "Chloe Nakamura: I bought the hand lotion online on the Sorrelmere Pantry website and I want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5765c17570",
  "text": "Desk summary: Elena Petrova says hi and wants to send the study planner back to Lyrewind Gifts. They bought it online on the website. Thanks for helping them out with the return!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q041fdae633",
  "text": "Yuki Watanabe: Hello, I bought the charm bracelet online from Brindlewood Acres and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q2d3c771093",
  "text": "Hi there,\nI bought the clay pot online and I want to send it back to Tallowgate Kitchen. Thanks for your help with the return.\nThanks,\nRosa Delgado",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q64e74a9194",
  "text": "Declan Doyle: I bought the daypack online on the Tidecastle Holidays website and I want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qf67beb823b",
  "text": "Store staff: Yusuf Haddad wrote in cheerfully and wants to send the sketch pad back. They bought it on the website from Lyrewind Gifts. Happy to help with the return of it!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q9ef276b707",
  "text": "Rafael Quiroga: Hi there! I bought the pastry brush online in the Sablewood Studio app and I want to send it back.\nsupport: Thanks for getting in touch!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd4ea2096e3",
  "text": "Ravi Chandra has written to say that he bought the baby monitor online from Brackwell Summit and wishes to send it back to the store. Please forward this to the help desk.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q1ebdb3395c",
  "text": "Hi Mirrowmere Lodge team,\nHope you are doing well! I bought the engraved cheese board online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Hugo Lefevre",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q530bea02d4",
  "text": "Leila Haidari: Sorry to bother you. I bought the made-to-measure picture frame online from Thistlemoor Atelier and I want to send it back to the store.\nsupport: Thank you for getting in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q8b03a913ee",
  "text": "Hello Bramblecourt Flowers team,\nI bought the wristband in your online shop and I am writing to send it back to you. Please assist me with the return.\nBest regards, Kofi Boateng",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q3dc5a17acc",
  "text": "Hi Mirrowmere Lodge team,\nHope you are doing well! I bought the engraved cheese board online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Hugo Lefevre",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5cdb50969c",
  "text": "Nikhil Rao: Hello. I bought the cutting board online from Sorrelmere Pantry and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q1e15be05ce",
  "text": "Customer: Olu Adebayo\nStore: Mirrowmere Lodge\nTopic: send back\nI bought the picture frame on the website and I want to send it back. Please just reply to me with the steps.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q321c7233fe",
  "text": "Customer: Ciaran Walsh\nItem: the sandwich platter\nStore: Sorrelmere Pantry\nI want to send the sandwich platter back to Sorrelmere Pantry. I bought it online on the Sorrelmere Pantry website.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q20c17fe60d",
  "text": "Nikhil Rao: Hello. I bought the cutting board online from Sorrelmere Pantry and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q701dbb0c69",
  "text": "Customer: Omar Haidari\nStore: Brindlewood Acres\nRequest: send back\nI bought the name-printed lunch box in the app and I want to send it back. Please help me.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qb9b9dd1c00",
  "text": "Nikhil Rao: Hello. I bought the cutting board online from Sorrelmere Pantry and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q567c8e17fc",
  "text": "Dear Mellowbrook Linens team,\nI purchased my engraved tea caddy online through your website and I am writing to return it. Kindly help me with the return.\nYours sincerely, Tariq Haddad",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q2829e850aa",
  "text": "Idris Bello: Greetings. I bought the face mask online on the Oldenhaw Growers website and I wish to send it back. Kindly assist me with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q6093aa8367",
  "text": "Dear Corvane Trailworks,\nI am sorry to bother you. I want to send the hammock back, and I bought it online in your app.\nWith thanks and apologies,\nPriya Natarajan",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q37fa0520da",
  "text": "Amara Okafor: I bought the silicone earplug set online on the Quarrymoor Nutrition website and I want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q8c38dc8110",
  "text": "Dear Tinselwick Parties team,\nI am writing to return the wall clock that I bought online on your website. Kindly help me with the return.\nYours faithfully, Zainab Yusuf",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5b19f9bb00",
  "text": "Felix Abernathy: Hello. I bought the shampoo bottle online from Hobbleton Parlour and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qdd0d7238c4",
  "text": "Pedro Almeida: Hello, I bought the disco ball on the website from Stonefall Outfitters. I want to send it back.\nsupport: Hello there. Thank you for writing in.\nPedro Almeida: Thank you. Please help me with the return of it.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q1a8326e592",
  "text": "Customer: Nadia Petrescu\nStore: Lyrewind Gifts\nItem: the electric razor\nI bought it online and I want to send it back to Lyrewind Gifts. Please help me with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q3e64dfc5ea",
  "text": "Nadia Haddad has contacted us about sending the yoghurt pot back to Stonefall Outfitters. This was bought online via the website. Please provide assistance with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q7296b7430b",
  "text": "Customer: Viktor Halvorsen\nStore: Marrowdale Home\nTopic: send back\nI bought the bar of soap on the website and I want to send it back. Please just reply to me with the steps.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q84653790aa",
  "text": "Aidan Murphy: Sorry to bother you. I bought the headlamp online from Bramblecot Nursery and I want to send it back to the store.\nsupport: Thank you for getting in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd34ed94df1",
  "text": "Hello Fennick Apothecary,\nI want to send the hand lotion tube back, and I bought it online on the website. Please just sort this out with me.\nBest regards, Camille Dubois",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q29ff9cf1dd",
  "text": "Sorry to bother you, writes Mariana Costa. The study planner was bought online on the Whiskerfold Home website and they want to send it back.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q727e0e276c",
  "text": "Felix Abernathy: Hello. I bought the shampoo bottle online from Hobbleton Parlour and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qa32338c2ec",
  "text": "Dear Mellowbrook Linens,\nI am sorry to bother you. I want to send the table lamp back, and I bought it online in your app.\nWith thanks and apologies,\nMateo Vargas",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qf701508a07",
  "text": "Dev Chaudhary: Sorry to bother you. I bought the yoga mat online from Marrowdale Home and I want to send it back to the store.\nsupport: Thank you for getting in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q2c452d521f",
  "text": "Lucia Romero: I wish to send the leather handbag back to Ferrovox Audio Bar, which I bought online on the website.\nsupport: Thank you for contacting us, Lucia Romero. Happy to help with that.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5a8ef3bb32",
  "text": "Dev Chaudhary: I bought the photo-printed mouse mat on the website from Fennick Apothecary and I want to send it back.\nsupport: Hello there. Please reply with your order details.\nDev Chaudhary: My name is Dev Chaudhary.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qa89cfecd4c",
  "text": "Rahul Dasgupta wrote to say she bought the hair dryer online from Tidecastle Holidays and wants to send it back to the store. Please ask the help desk to help her with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd477c2fe7c",
  "text": "Desk summary: Sebastian Varga says hi and wants to send the fruit salad back to Sablewood Studio. They bought it online on the website. Thanks for helping them out with the return!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q2cd4cfaef1",
  "text": "Ravi Sundaram: Sorry to bother you. I bought the photo-printed bandana online from Oakmantle Commons and I want to send it back to the store.\nsupport: Thank you for getting in touch.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qe179b17fe4",
  "text": "Oscar Dubois: Greetings. I bought the made-to-measure apron online on the Quellan Tea Kitchen website and I wish to send it back. Kindly assist me with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qaed97dcc3a",
  "text": "Dear Sorrelmere Pantry team,\nI am writing to return the kettlebell that I bought online on your website. Kindly help me with the return.\nYours faithfully, Tariq Haddad",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the name of the goods the person bought, as written, without any article or possessive before it (leave out the, my, a, an)"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 }
]
