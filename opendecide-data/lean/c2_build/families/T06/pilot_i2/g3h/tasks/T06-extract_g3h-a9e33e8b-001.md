# G3-H extraction T06-extract_g3h-a9e33e8b-001 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot_i2/g3h/answers/T06-extract_g3h-a9e33e8b-001.json

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
  "qid": "q0ddf211713",
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
  "qid": "q787fbda91e",
  "text": "Ravi Chandra: Hi, I bought the table runner online from Kettlecrumb Bakehouse. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
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
  "qid": "q0907860ca4",
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
  "qid": "q3658c8893f",
  "text": "Customer: Oscar Dubois\nStore: Oakmantle Commons\nItem: the fresh custard tart\nI bought it online and I want to send it back to Oakmantle Commons. Please help me with the return, and I want a reply from you.",
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
  "qid": "qad4d1a3578",
  "text": "Oscar Lindgren has written to ask for the return. The pair of running socks was bought online in the Mellowbrook Linens app, and the customer wishes to send it back.",
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
  "qid": "q8302402778",
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
  "qid": "qb6ea1dcc2e",
  "text": "Aisha Rahman: I want to send the saddle bag back to Tidecastle Holidays. I bought it online in the app.\nsupport: Understood, please share your order details.",
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
  "qid": "qa3a7568ae9",
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
  "qid": "qbd1a3abc9b",
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
  "qid": "q52304f18c1",
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
  "qid": "qedf1f1d462",
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
  "qid": "qabca473fed",
  "text": "Hello there,\nI bought the nail polish bottle on the website from Tidecastle Holidays and I want to send it back.\nThank you, Femi Bello",
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
  "qid": "qd088c1c63b",
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
  "qid": "qe662d8de6f",
  "text": "Aidan Murphy has contacted us about sending the scooter back to Brackwell Summit. This was bought online via the website. Please provide assistance with the return.",
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
  "qid": "q75f16c75a5",
  "text": "Leila Haidari: Sorry to bother you. I bought the hand cream online from Puddlecrest Toys and I want to send it back to the store.\nsupport: Thank you for getting in touch.",
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
  "qid": "q1693b0789b",
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
  "qid": "q5b2526f129",
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
  "qid": "q0ba4ec42d2",
  "text": "Customer: Leilani Kekoa\nStore: Bramblecourt Flowers\nItem: the picnic blanket\nHi there, I bought it online and I want to send it back to Bramblecourt Flowers. Thanks for your help, you are lovely.",
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
  "qid": "q68fd749783",
  "text": "Dear Quarrymoor Nutrition team,\nI purchased my school backpack online through your website and I am writing to return it. Kindly help me with the return.\nYours sincerely, Jorge Almeida",
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
  "qid": "q2c8f1fad7c",
  "text": "Hello there,\nI bought the nail polish bottle on the website from Tidecastle Holidays and I want to send it back.\nThank you, Femi Bello",
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
  "qid": "q7c00b31331",
  "text": "Customer: Anja Kowalczyk\nStore: Brackwell Summit\nTopic: send back\nI bought the cake stand on the website and I want to send it back. Please just reply to me with the steps.",
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
  "qid": "qdd63b86f0d",
  "text": "Ingrid Solberg has been in touch about the picnic cooler. They want to send it back to Quarrymoor Nutrition and bought it online through the online shop. Thank you for your help with this.",
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
  "qid": "qee514eea8f",
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
  "qid": "qc009b94b3c",
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
  "qid": "q1873c9f7a3",
  "text": "Customer: Esther Abebe\nItem: the pottery wheel\nStore: Bramblecot Nursery\nHappy to be in touch! I want to send the pottery wheel back to Bramblecot Nursery, which I bought online on the Bramblecot Nursery website.",
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
  "qid": "q521c0aaddc",
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
  "qid": "q8ae35f6c18",
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
  "qid": "q452912be3c",
  "text": "Yara Khoury: Hello, I bought the engraved key ring online from Tidecastle Holidays and I want to send it back. Thank you.\nsupport: Hello, thanks for writing in.",
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
  "qid": "q08d6aa96b1",
  "text": "Mateo Vargas: Hello. I bought the tube of shaving foam online from Thistlemoor Atelier and I really want to send it back to the store. Please just help me with this.\nsupport: Thank you for your message.",
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
  "qid": "q201fe928b1",
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
  "qid": "q5307d1da7b",
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
  "qid": "qd2537fcf20",
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
  "qid": "q4c42e7dd4d",
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
  "qid": "q3a6ccb0af7",
  "text": "Hey there Bramblecot Nursery team,\nI bought the canvas parasol on the website and I really want to send it back! Thanks for being so kind about it.\nCheers,\nAhmed Rahman",
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
  "qid": "q33f9d0e066",
  "text": "Hey there Bramblecot Nursery team,\nI bought the canvas parasol on the website and I really want to send it back! Thanks for being so kind about it.\nCheers,\nAhmed Rahman",
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
  "qid": "qb8de7749e5",
  "text": "Oscar Lindgren has written to ask for the return. The pair of running socks was bought online in the Mellowbrook Linens app, and the customer wishes to send it back.",
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
  "qid": "q19aa2cab6a",
  "text": "Hi Mirrowmere Lodge team,\nHope you are doing well! I bought the memo pad online and I am hoping to send it back to you. Just tell me how to go ahead with that.\nCheers, Adaeze Okafor",
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
  "qid": "q0d04302ca0",
  "text": "Sven Lindqvist: Hi, I bought the hummus tub online from Lumenwick Home. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
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
  "qid": "q0be4ebb682",
  "text": "Desk summary: Ngozi Eze says hi and wants to send the nasal spray back to Kettlecrumb Bakehouse. They bought it online on the website. Thanks for helping them out with the return!",
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
  "qid": "qcc04ee024b",
  "text": "Desk summary: Callum Ross says hi and wants to send the hammock back to Ferrowby Cheese House. They bought it online on the website. Thanks for helping them out with the return!",
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
  "qid": "qf1ecd3dd06",
  "text": "Mateo Herrera: Hi, I bought the vinyl record player online from Sablewood Studio. Please help me send it back to the store.\nsupport: Thank you for your message. Please go ahead.",
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
  "qid": "q49c0ca2b2b",
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
  "qid": "qebf0487c43",
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
  "qid": "q5125d3c644",
  "text": "Ruben Castellanos: Hello, I bought the garden trowel on the website from Quarrymoor Nutrition. I want to send it back.\nsupport: Hello there. Thank you for writing in.\nRuben Castellanos: Thank you. Please help me with the return of it.",
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
  "qid": "qa168fb3e72",
  "text": "Oscar Dubois: I want to send the cheese grater back to Bramblecot Nursery. I bought it online in the app.\nsupport: Understood, please share your order details.",
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
  "qid": "q1260abcb6f",
  "text": "Happy to help with this! Mei Lim wants to send the pet bed back to Sorrelmere Pantry. They bought it online through the app and are glad to start the return.",
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
  "qid": "qf9dea872ab",
  "text": "Store staff: Yusuf Demir wrote in cheerfully and wants to send the bamboo toothbrush back. They bought it on the website from Brackwell Summit. Happy to help with the return of it!",
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
  "qid": "q8ff001547a",
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
  "qid": "q76643b84d5",
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
  "qid": "q61c61cf3db",
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
 }
]
