# G3-H extraction T06-extract_g3h-b13342ed-002 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot/g3h/answers/T06-extract_g3h-b13342ed-002.json

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
  "qid": "q175cc48e38",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q570c6464f8",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q5a867c5bb0",
  "text": "Mateo Vargas: Hello, I want to send the vinyl record player back to Quarrymoor Nutrition. I bought it online.\nsupport: Hi, thank you. Please help us with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q7d943deae6",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qbbb467d101",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q0a24ed0963",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q32b02986d3",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd31ad377ec",
  "text": "Amara Nwosu: I wish to send the wooden serving board back to Tidecastle Holidays, which I bought online on the website.\nsupport: Thank you for contacting us, Amara Nwosu. Happy to help with that.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd0297680a2",
  "text": "Hannah Kimura: Hello, I bought the hair dryer online from Pennyfold Stationery and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qffa2114cf4",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qfc88b1a446",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q563c12e5fe",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q3e89cc51ef",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q39efedf940",
  "text": "Hello there,\nI bought the fitness tracker on the website from Puddlecrest Toys and I want to send it back.\nThank you, Yuna Park",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qa25b061c9d",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q15afa5ea11",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q9ee9ee6dc4",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q47955ba00c",
  "text": "Customer: Anja Kowalczyk\nStore: Brackwell Summit\nTopic: send back\nI bought the tub of ice cream on the website and I want to send it back. Please just reply to me with the steps.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q6f5d713629",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q68214f29d6",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q77743b437f",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q90a43abdf1",
  "text": "Customer: Eva Lindgren\nItem: the insect repellent\nStore: Thistlemoor Atelier\nI want to send the insect repellent back to Thistlemoor Atelier, which I bought online in the Thistlemoor Atelier online shop. Please reply to this message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q09dba91eba",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qdd21c51897",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q3da4a71de0",
  "text": "Sven Lindqvist: Hi, I bought the study planner online from Lumenwick Home. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q02a7ae8132",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qe9d3abb440",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q71363015eb",
  "text": "Mateo Vargas: Hello. I bought the lip balm stick online from Thistlemoor Atelier and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qec6f6aef9d",
  "text": "Happy to help with this! Yara Mansour wants to send the ironing board back to Quellan Tea Kitchen. They bought it online through the app and are glad to start the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qf598912afd",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q0f7ddc02f2",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q890cbd7fab",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qdfc7dff284",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qfe9050b7bb",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q60cd8d2eb1",
  "text": "Hi Mirrowmere Lodge team,\nHope you are doing well! I bought the dog harness online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Adaeze Okafor",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qbf92882872",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qefb455204e",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q112fc79076",
  "text": "Ravi Chandra has written to say that he bought the wristband online from Brackwell Summit and wishes to send it back to the store. Please forward this to the help desk.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q39b546b609",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q32c045def4",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q6a604b1017",
  "text": "Noor Rahman: Greetings. I bought the fishing rod online on the Tallowmere Table website and I wish to send it back. Kindly assist me with the return.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qc99ca15b51",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q3198c87366",
  "text": "Customer: Hugo Lefevre\nStore: Puddlecrest Toys\nTopic: Sending the photo printed sun hat back\nHi there, I bought the photo printed sun hat online in your app and I really want to send it back. Thanks for helping me with that!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q8d49353fa7",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q4bc4385d78",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qec52628664",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q6d9f0ee970",
  "text": "Gabriel Ferreira has written to say that he bought the charm bracelet online from Brackwell Summit and wishes to send it back to the store. Please forward this to the help desk.",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qd9bbae5106",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "q665b514c4c",
  "text": "Desk summary: Nkechi Eze says hi and wants to send the fruit hamper back to Carrowell Emporium. They bought it online on the website. Thanks for helping them out with the return!",
  "schema": [
   {
    "field": "customer",
    "type": "name",
    "describe": "the person who wants to send the goods back, as written"
   },
   {
    "field": "item",
    "type": "name",
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 },
 {
  "qid": "qcfd675233e",
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
    "describe": "the goods the person bought, as written"
   },
   {
    "field": "store",
    "type": "name",
    "describe": "the store the goods came from, as written"
   }
  ]
 }
]
