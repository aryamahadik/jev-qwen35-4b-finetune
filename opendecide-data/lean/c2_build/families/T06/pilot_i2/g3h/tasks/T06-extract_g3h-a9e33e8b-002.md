# G3-H extraction T06-extract_g3h-a9e33e8b-002 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot_i2/g3h/answers/T06-extract_g3h-a9e33e8b-002.json

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
  "qid": "q4d9490385c",
  "text": "Customer: Grace Oduya\nStore: Fennick Apothecary\nRequest: send back\nI bought the beach chair in the app and I want to send it back. Please help me.",
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
  "qid": "qec6fc422df",
  "text": "Customer: Gabriela Souza\nStore: Stonefall Outfitters\nTopic: Sending the face flannel back\nHi there, I bought the face flannel online in your app and I really want to send it back. Thanks for helping me with that!",
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
  "qid": "qb80d955959",
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
  "qid": "q1ca3f955e7",
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
  "qid": "q580dcb0800",
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
  "qid": "qf325cb599c",
  "text": "Hi Amberlane Keepsakes team,\nHope you are doing well! I bought the deodorant stick online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Tobias Kaiser",
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
  "qid": "q3aed86d0e2",
  "text": "Hello Ravenmoor Cycles team,\nI bought the ear stud set online and I want to send them back to Ravenmoor Cycles. Please help me with the return.\nThanks, Tomasz Wrona",
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
  "qid": "q530504ac9f",
  "text": "Kwame Asante has been in touch about the resistance band. They want to send it back to Bramblecot Nursery and bought it online through the online shop. Thank you for your help with this.",
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
  "qid": "q90e427f440",
  "text": "Dear Pennyfold Stationery,\nI am sorry to bother you. I want to send the music box back, and I bought it online in your app.\nWith thanks and apologies,\nLukas Brenner",
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
  "qid": "qdcda546ef7",
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
  "qid": "q0679c6c7d5",
  "text": "Yara Mansour: I bought the name-printed pill pouch online on the Tidecastle Holidays website and I want to send it back.",
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
  "qid": "q2d275a3bed",
  "text": "Happy to help with this! Hana Sato wants to send the wool blanket back to Carrowell Emporium. They bought it online through the app and are glad to start the return.",
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
  "qid": "q944c85e80c",
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
  "qid": "qa82c7dd936",
  "text": "Dear Oldenhaw Growers team,\nI am writing to return the ring binder that I bought online on your website. Kindly help me with the return.\nYours faithfully, Noor Rahman",
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
  "qid": "qda061d2a88",
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
  "qid": "qf8c4489652",
  "text": "Yara Mansour: I bought the name-printed pill pouch online on the Tidecastle Holidays website and I want to send it back.",
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
  "qid": "qcda743a7e7",
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
  "qid": "q18e1757a1e",
  "text": "Grace Oduya: Hello, I bought the name-stitched linen napkin online from Brinehollow Trading and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
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
  "qid": "qa10ccf5dc2",
  "text": "Tariq Haddad: Greetings. I bought the made-to-measure apron online on the Amberlane Keepsakes website and I wish to send it back. Kindly assist me with the return.",
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
  "qid": "qe12001f033",
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
  "qid": "qcba1f0fed0",
  "text": "Aiko Tanaka: I wish to send the made-to-measure sun shade back to Mellowbrook Linens, which I bought online on the website.\nsupport: Thank you for contacting us, Aiko Tanaka. Happy to help with that.",
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
  "qid": "q8da4367b86",
  "text": "Customer: Grace Oduya\nStore: Fennick Apothecary\nRequest: send back\nI bought the beach chair in the app and I want to send it back. Please help me.",
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
  "qid": "qf7a8dca344",
  "text": "Owen Callister has written to ask for the return. The building block set was bought online in the Bramblecot Nursery app, and the customer wishes to send it back.",
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
  "qid": "qadb3bc2745",
  "text": "Service desk note: Gabriel Santos wants to send the digital thermometer back to Oakmantle Commons. They bought the digital thermometer online in the Oakmantle Commons app.",
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
  "qid": "qc5d1198cd6",
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
  "qid": "qe988d292b2",
  "text": "Gabriel Ferreira has written to say that he bought the jigsaw puzzle online from Amberlane Keepsakes and wishes to send it back to the store. Please forward this to the help desk.",
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
  "qid": "q16d3b69195",
  "text": "Hey there Kettlecrumb Bakehouse team,\nI bought the hand soap pump on the website and I really want to send it back! Thanks for being so kind about it.\nCheers,\nDev Chaudhary",
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
  "qid": "q31fca9e883",
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
  "qid": "q58e1f8bc7a",
  "text": "Mireille Fontaine wants to send the wooden spoon back to Whiskerfold Home. They bought it online through the website. Please assist them with the return.",
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
  "qid": "q775e19ddcf",
  "text": "Hello Lyrewind Gifts team,\nSorry for bothering you. I bought the hummus tub online and I want to send it back to Lyrewind Gifts.\nKind regards, Ruben Castellanos",
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
  "qid": "qdf4878c859",
  "text": "Dear Sablewood Studio team,\nI am writing to send the serving tray back to you. I bought it online on your website.\nYours sincerely, Ravi Subramanian",
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
  "qid": "qc25d9d5005",
  "text": "Gabriel Ferreira has written to say that he bought the jigsaw puzzle online from Amberlane Keepsakes and wishes to send it back to the store. Please forward this to the help desk.",
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
  "qid": "qe9f1facb20",
  "text": "Hi Sorrelmere Pantry team,\nHope you are doing well! I bought the cat scratcher online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Mei Tran",
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
  "qid": "q18effece70",
  "text": "Dear Oldenhaw Growers team,\nI am writing to return the ring binder that I bought online on your website. Kindly help me with the return.\nYours faithfully, Noor Rahman",
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
  "qid": "qbf67e3d46b",
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
  "qid": "q3f24f09eb0",
  "text": "Happy to help with this! Yara Mansour wants to send the shower cap back to Quellan Tea Kitchen. They bought it online through the app and are glad to start the return.",
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
  "qid": "q3c9d7a76d9",
  "text": "Amara Okafor: Hello, I bought the tub of clotted cream online from Kettlecrumb Bakehouse and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
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
  "qid": "q1d83545f99",
  "text": "Dear Tinselwick Parties team,\nI am writing to send the carnation posy back to you. I bought it online on your website.\nYours sincerely, Diego Morales",
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
  "qid": "q9d1a3c9535",
  "text": "Desk summary: Nkechi Eze says hi and wants to send the shower cap back to Carrowell Emporium. They bought it online on the website. Thanks for helping them out with the return!",
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
  "qid": "q69a82d9582",
  "text": "Maya Cohen: I bought the tube of toothpaste online on the Dunmere Provisions website and I want to send it back.",
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
  "qid": "qd83b761be6",
  "text": "Nadia Haddad: Yay, hello there! I bought the hammock online in the Quarrymoor Nutrition app and I want to send it back. Thank you for helping with the return!",
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
  "qid": "q5ec0decf75",
  "text": "Dear Tinselwick Parties team,\nI am writing to send the carnation posy back to you. I bought it online on your website.\nYours sincerely, Diego Morales",
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
  "qid": "qef40dfd71b",
  "text": "Hannah Kowalski: Hi, I bought the dollhouse online from Lumenwick Home. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
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
  "qid": "q4d5023efa0",
  "text": "Dear Sorrelmere Pantry,\nI am sorry to bother you. I want to send the bodyboard back, and I bought it online in your app.\nWith thanks and apologies,\nChloe Nguyen",
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
  "qid": "qf91da6f391",
  "text": "Service desk note: Samir Qureshi wants to send the tube of shaving foam back to Quarrymoor Nutrition. They bought the tube of shaving foam online in the Quarrymoor Nutrition app.",
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
  "qid": "qa9cfaf17a4",
  "text": "Grace Oduya: Hello, I bought the name-stitched linen napkin online from Brinehollow Trading and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
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
  "qid": "qd639a7b175",
  "text": "Hi there,\nI bought the wooden spoon online and I want to send it back to Brindlewood Acres. Thanks for your help with the return.\nThanks,\nCiaran Walsh",
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
  "qid": "q40377722c4",
  "text": "Desk summary: Nkechi Eze says hi and wants to send the shower cap back to Carrowell Emporium. They bought it online on the website. Thanks for helping them out with the return!",
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
  "qid": "q4fb09d5063",
  "text": "Hello Mirrowmere Lodge,\nI want to send the portable speaker back, and I bought it online on the website. Please just sort this out with me.\nBest regards, Cormac Doyle",
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
  "qid": "q59b447e15d",
  "text": "Service desk note: Gabriel Santos wants to send the digital thermometer back to Oakmantle Commons. They bought the digital thermometer online in the Oakmantle Commons app.",
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
