# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-007 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-007.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q2d232a2fe9",
  "kind": "yes/no",
  "text": "Assistant: Sure, I will place that order for you.\nCustomer: How much will it be?\nAssistant: It will be $20. To confirm, I placed a large pizza with garlic, jalapeno, broccoli, and mushrooms.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd510ae4b51",
  "kind": "yes/no",
  "text": "Customer: What about the Tower? Do they have 2 together?\nAssistant: They have 2 seated together at 6pm.\nCustomer: OK, you can buy them from the Tower.",
  "question": "In the customer's last message, does \"Tower\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q49dc917e33",
  "kind": "yes/no",
  "text": "Assistant: Okay, they do have patio seating available at 7 pm on Friday.\nCustomer: Sounds good, please book it for a table for 4.\nAssistant: Certainly, Okay, I have made a reservation for you at Pad Thai on main at 7 pm on Friday. It will be a patio seating for 4 people.",
  "question": "According to the assistant's last message, is \"4\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcaee15af6d",
  "kind": "yes/no",
  "text": "Assistant: Uber XL is 12.64 Uber Black is $28.38\nCustomer: book Uber XL\nAssistant: I have confirmed your ride today at 4 PM picking up at moorestown mall and dropping off at residence inn",
  "question": "According to the assistant's last message, is \"4 PM\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2a6accf0ee",
  "kind": "yes/no",
  "text": "Customer: It's 2128973421.\nAssistant: Your car's make, model, and year?\nCustomer: Telsa, S3, 2017",
  "question": "In the customer's last message, does \"Telsa, S3\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdeb932ee91",
  "kind": "yes/no",
  "text": "Customer: Hello John, I need you to book a service appointment for my car at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfc408e255c",
  "kind": "yes/no",
  "text": "Assistant: I'll run you over a bottle of cold water. Please be safe. Its hot out there.\nCustomer: I'm pulled over on Main Street. Please hurry...\nAssistant: On my way. I;m bringing you a note about what we spoke about. as a reminder, You're taking your 2017 Honda civic to Intelligent Auto because your air conditioner isnt working. appointment is today at 2pm. Dont forget the $100 fee. Bring the key to the office.",
  "question": "According to the assistant's last message, is \"Intelligent Auto\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8d77a1daf2",
  "kind": "yes/no",
  "text": "Customer: It is a 2016 Audi A7\nAssistant: What name and number are you going to be giving them?\nCustomer: Andrew Smith 2078424371",
  "question": "In the customer's last message, does \"Andrew Smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdb75ee7141",
  "kind": "yes/no",
  "text": "Customer: The Phoenix City Grille\nAssistant: How many people?\nCustomer: 2 and I want it for Friday",
  "question": "In the customer's last message, does \"2\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe1a26fd348",
  "kind": "yes/no",
  "text": "Assistant: $10 each.\nCustomer: Use my account to order them.\nAssistant: Alright, your tickets for The Lego Movie 2 at 7PM tonight at Cinemark Mall St. Matthews have been ordered.",
  "question": "According to the assistant's last message, is \"Cinemark Mall St. Matthews\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa9a9a69ad3",
  "kind": "yes/no",
  "text": "Customer: I feel it needs a replacement of the front shocks and also the brake buds need replacement.\nAssistant: What car do you have in mind madam?\nCustomer: My black Chevrolet, double cabin, 2000 cc and 2017 model",
  "question": "In the customer's last message, does \"2017\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb0853b457a",
  "kind": "yes/no",
  "text": "Customer: 2017, Ford Fusion, Hybrid.\nAssistant: Name and Phone number I should make appointment under?\nCustomer: Victor Forrester 515-458-5285",
  "question": "In the customer's last message, does \"Victor Forrester\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2096a688e1",
  "kind": "yes/no",
  "text": "Customer: I need you to order some pizza from Pizza Hut.\nAssistant: Which one do you want me to order from?\nCustomer: The one in Macon.",
  "question": "In the customer's last message, does \"Macon\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe79c9da35f",
  "kind": "yes/no",
  "text": "Customer: I need to make a reservation for a restaurant, please\nAssistant: OK sure. Which restaurant?\nCustomer: The Polo Bar at 1 E 55th St",
  "question": "In the customer's last message, does \"The Polo Bar\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8e4f8268d0",
  "kind": "yes/no",
  "text": "Customer: To the NWA Mall\nAssistant: What is your pick up time?\nCustomer: in 15 minutes.",
  "question": "In the customer's last message, does \"15 minutes\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q647ab216fd",
  "kind": "yes/no",
  "text": "Customer: What time is US showing tonight?\nAssistant: What city?\nCustomer: Reno, Nevada",
  "question": "In the customer's last message, does \"Reno, Nevada\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe67391e44a",
  "kind": "yes/no",
  "text": "Customer: Yes.\nAssistant: How many tickets would you like to buy?\nCustomer: I would like two please.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8e856f7407",
  "kind": "yes/no",
  "text": "Customer: Medium\nAssistant: What crust do you prefer?\nCustomer: Thick please.",
  "question": "In the customer's last message, does \"Thick\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb1928d3e65",
  "kind": "yes/no",
  "text": "Customer: I need it picked up from 123 Mulberry Lane, Annapolis, MD 21403.\nAssistant: Sure, not a problem. Let me first get some information about the car. What is the make, model and year of the car?\nCustomer: It is a 1999 Honda Civic. A four door sedan type car with a V6 engine.",
  "question": "In the customer's last message, does \"Honda Civic\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8d6f395d88",
  "kind": "yes/no",
  "text": "Assistant: It will be $100\nCustomer: Okay, that will work.\nAssistant: An appointment for John Smith at 916-555-1212 has been scheduled for today at 2 pm for your 2018 Subraru Impreza for a hundred dollar inspection for the noise made when turning.",
  "question": "According to the assistant's last message, is \"Subraru Impreza\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q245459b971",
  "kind": "yes/no",
  "text": "Customer: Ok, thank you. Is there any other information that you need from me?\nAssistant: What is the name you want the appointment set under?\nCustomer: Use my husband's name, Evan Phillips, he will be dropping it off for me.",
  "question": "In the customer's last message, does \"Evan Phillips\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q162488f22d",
  "kind": "yes/no",
  "text": "Customer: Book me a reservation at Zelos with the same info.\nAssistant: Let me repeat that back to you. You want a reservation at Zelos for 3 on April 10 at 7 PM. You need handicap seating available.\nCustomer: No, I want it at 6 PM.",
  "question": "In the customer's last message, does \"6 PM\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q93c89a12de",
  "kind": "yes/no",
  "text": "Customer: OK. Can you order me a ticket for Hell boy instead?\nAssistant: Ok in what location is it Kevin?\nCustomer: AMC Empire 25.",
  "question": "In the customer's last message, does \"AMC Empire 25\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q693071f5a1",
  "kind": "yes/no",
  "text": "Customer: Lexington, Kentucky.\nAssistant: Okay. Which theater?\nCustomer: Cinemark at the Fayette Mall, please.",
  "question": "In the customer's last message, does \"Cinemark\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q921c4efe47",
  "kind": "yes/no",
  "text": "Customer: Hi, I need to order a pizza!\nAssistant: Okay. What pizza place would you like to order from?\nCustomer: Norton's Pizza on 23rd Street in West Essex.",
  "question": "In the customer's last message, does \"23rd Street in West Essex\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q54f41bbc7c",
  "kind": "yes/no",
  "text": "Customer: Anaheim, California\nAssistant: What's your starting point?\nCustomer: Anaheim Majestic Garden Hotel",
  "question": "In the customer's last message, does \"Anaheim Majestic Garden Hotel\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8981d1391b",
  "kind": "yes/no",
  "text": "Assistant: Yes, I will provide an update.\nCustomer: Thanks.\nAssistant: Mazzio is out of bacon.",
  "question": "According to the assistant's last message, is \"bacon\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7ac0a2cc92",
  "kind": "yes/no",
  "text": "Customer: It's a Nissan.\nAssistant: Okay thanks. What's the model?\nCustomer: It's an Ultima.",
  "question": "In the customer's last message, does \"Ultima\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2ef0a565c9",
  "kind": "yes/no",
  "text": "Assistant: I will. I'm dialing now.\nCustomer: Have you contacted them yet?\nAssistant: Yes, they are on the way they should arrive within the next 5 min.",
  "question": "According to the assistant's last message, is \"5 min\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q01becf4409",
  "kind": "yes/no",
  "text": "Assistant: The standard rate for a check-up and oil change at Intelligent Auto Solutions is $79, then they will give you an estimate of any additional costs for work needed.\nCustomer: Thanks.\nAssistant: Okay, please drop off your 2005 Ford Focus at Intelligent Auto Solutions tomorrow morning. Your appointment is for 3:00 PM and your car should be ready by the evening. Please be prepared to pay the $79. They accept cash or credit card.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q50f6fa9929",
  "kind": "yes/no",
  "text": "Customer: Hi. I'm looking to make a reservation at a very nice Seafood restaurant in the Dallas area.\nAssistant: I have found two restaurants for you. Truluck's which is rated at 4.7 stars and Pappadeaux Seafood Kitchen which is rated at 4.5 stars.\nCustomer: Does Truluck's have a full bar?",
  "question": "In the customer's last message, does \"Truluck's\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf99cbbe8e9",
  "kind": "yes/no",
  "text": "Customer: 8pm please.\nAssistant: Unfortunately 8pm is not available. 9Pm is though.\nCustomer: Okay 9pm.",
  "question": "In the customer's last message, does \"9pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qeaba1cc57f",
  "kind": "yes/no",
  "text": "Customer: Roma's pizza please.\nAssistant: In which city?\nCustomer: One in Madison.",
  "question": "In the customer's last message, does \"Madison\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0d88e63857",
  "kind": "yes/no",
  "text": "Customer: Hi, I need to schedule an appointment with an auto mechanic.\nAssistant: Hi, what mechanic would you like to use?\nCustomer: Intelligent Auto Solutions on 300 Main Street in Boston",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2ea863fff4",
  "kind": "yes/no",
  "text": "Customer: There is just me and my wife.\nAssistant: OK, do you need a return trip?\nCustomer: Yes, the movie will end at 9:45.",
  "question": "In the customer's last message, does \"9:45\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q773e0cee10",
  "kind": "yes/no",
  "text": "Customer: Bob, I need to get an Uber to go over to shopping center on 7th street.\nAssistant: Ok, like right now?\nCustomer: In 15 minutes would be good.",
  "question": "In the customer's last message, does \"15 minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9253f2a03d",
  "kind": "yes/no",
  "text": "Assistant: Do you want a hot coffee, or an iced coffee?\nCustomer: Cold Brew, Only a quarter cup of ice, Large, with two splashes of Coconut milk.\nAssistant: They are out of coconut. Is Almond Okay?",
  "question": "According to the assistant's last message, is \"coconut\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5a1168f8d2",
  "kind": "yes/no",
  "text": "Customer: Thank you , no.\nAssistant: Ok. The second pizza?\nCustomer: For the second one I'd like a medium pepperoni, with extra cheese and canadian bacon.",
  "question": "In the customer's last message, does \"medium\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3982d0dfc5",
  "kind": "yes/no",
  "text": "Assistant: Let me see if that ride is available\nCustomer: Thanks\nAssistant: Unfortunately, there is no UberXL driver in your area",
  "question": "According to the assistant's last message, is \"UberXL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3065dc0989",
  "kind": "yes/no",
  "text": "Assistant: Wednesday showings are 5:45 pm and 9:00 pm.\nCustomer: Okay. Let’s do the Wednesday showing at 5:45 pm please.\nAssistant: Absolutely. I called and booked 2 tickets for the Wednesday showing at 5:45 pm for you and your guest.",
  "question": "According to the assistant's last message, is \"2 tickets\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qef07b222fc",
  "kind": "yes/no",
  "text": "Assistant: How about cream or almond milk?\nCustomer: None of that.\nAssistant: So bad news, they are all out of the cold brew salted cream cold foam.",
  "question": "According to the assistant's last message, is \"salted cream cold foam\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q278f3ae863",
  "kind": "yes/no",
  "text": "Customer: I want a Uber in San Antonio.\nAssistant: Where to where?\nCustomer: I want to go from the River Center to Sea World.",
  "question": "In the customer's last message, does \"River Center\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69347f20ba",
  "kind": "yes/no",
  "text": "Customer: Hello, I have an oil leak and need assistance.",
  "question": "In the customer's last message, does \"oil leak\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf57cd90668",
  "kind": "yes/no",
  "text": "Customer: Intelligent Auto Solutions.\nAssistant: Okay, we'll book an appointment at Intelligent Auto Solutions. Please give the make, model, and year of your car to start.\nCustomer: Ford Focus, 2005",
  "question": "In the customer's last message, does \"2005\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfa8f64c202",
  "kind": "yes/no",
  "text": "Customer: OK Google, please schedule an appointment with Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2121f920b8",
  "kind": "yes/no",
  "text": "Customer: Yes, that's perfect.\nAssistant: And how many tickets do you need?\nCustomer: I need two tickets, I'm going on a date.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b0739f8fa",
  "kind": "yes/no",
  "text": "Customer: Yes, please\nAssistant: What date and time would you like to go?\nCustomer: Saturday at 6pm",
  "question": "In the customer's last message, does \"6pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe610e3f7d0",
  "kind": "yes/no",
  "text": "Customer: Thank you.\nAssistant: There is a showtime at 8:15 at the AMC Kabuki.\nCustomer: I am not going to be available at that time and I cannot be in San Francisco.",
  "question": "In the customer's last message, does \"San Francisco\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7ff2d1e2bd",
  "kind": "yes/no",
  "text": "Customer: Ok, that all sounds good. You can book it for me.\nAssistant: What name would you like it under?\nCustomer: You can put it under the name Jane Lawson.",
  "question": "In the customer's last message, does \"Jane Lawson\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0571237fa3",
  "kind": "yes/no",
  "text": "Assistant: Any other requests?\nCustomer: Yes, I'd like a booth please.\nAssistant: I'm sorry but a booth isn't available at that time.",
  "question": "According to the assistant's last message, is \"booth\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
