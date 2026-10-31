# G3-H extraction T06-extract_g3h-1738ef3e-002 (family T06)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/pilot_i3/g3h/answers/T06-extract_g3h-1738ef3e-002.json

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
  "qid": "q1711d01908",
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
  "qid": "q651c85cda9",
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
  "qid": "q58570398c6",
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
  "qid": "qa6c9691b9c",
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
  "qid": "qe56732578c",
  "text": "Gabriel Ferreira has written to say that he bought the made-to-measure blind online from Amberlane Keepsakes and wishes to send it back to the store. Please forward this to the help desk.",
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
  "qid": "q2fd1a3b0e7",
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
  "qid": "qb6ba4afa49",
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
  "qid": "qafd69682ac",
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
  "qid": "q5514deee2b",
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
  "qid": "q7fdf671078",
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
  "qid": "qdf7895d056",
  "text": "Viktor Lindgren has been in touch about the bar of cedar soap. They want to send it back to Tinselwick Parties and bought it online through the online shop. Thank you for your help with this.",
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
  "qid": "q11703535f1",
  "text": "Yuna Park: Hello, I want to send the made-to-measure ski jacket back to Marrowdale Home. I bought it online.\nsupport: Hi, thank you. Please help us with the return.",
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
  "qid": "q877053fc74",
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
  "qid": "qc233445704",
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
  "qid": "qa6f1f7a62d",
  "text": "Hello Lyrewind Gifts team,\nSorry for bothering you. I bought the tray of minced beef online and I want to send it back to Lyrewind Gifts.\nKind regards, Ruben Castellanos",
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
  "qid": "q6f48db7c9b",
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
  "qid": "q64621d6003",
  "text": "Dear Tinselwick Parties team,\nI am writing to send the name-printed apron back to you. I bought it online on your website.\nYours sincerely, Diego Morales",
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
  "qid": "q60888d8f10",
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
  "qid": "q18fc956d52",
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
  "qid": "qa718fea52d",
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
  "qid": "qba9b5ef512",
  "text": "Gabriel Ferreira has written to say that he bought the made-to-measure blind online from Amberlane Keepsakes and wishes to send it back to the store. Please forward this to the help desk.",
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
  "qid": "qb4578c41c0",
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
  "qid": "qbd40f12697",
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
