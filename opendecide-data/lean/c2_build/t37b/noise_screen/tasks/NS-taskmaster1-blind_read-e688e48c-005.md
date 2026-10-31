# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-005 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-005.json

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
  "qid": "qbe2970f172",
  "kind": "yes/no",
  "text": "Customer: Great anything else?\nAssistant: keep your speed to a steady pace.\nCustomer: Fine. Tell them it is a 2004 Chevy Trailblazer with a 4.2 litre",
  "question": "In the customer's last message, does \"2004\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q54c75110d7",
  "kind": "yes/no",
  "text": "Assistant: When would you like the pizza?\nCustomer: As soon a possible\nAssistant: Confirmed for one large thin crust pizza with sausage and onions toppings",
  "question": "According to the assistant's last message, is \"sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q330016f95a",
  "kind": "yes/no",
  "text": "Customer: Can you find me an Italian restaurant in Detroit, Michigan?",
  "question": "In the customer's last message, does \"Detroit, Michigan\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0c7c90a297",
  "kind": "yes/no",
  "text": "Customer: Please get me a Caffe mocha from Starbucks.",
  "question": "In the customer's last message, does \"Caffe mocha\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf23a4e411e",
  "kind": "yes/no",
  "text": "Assistant: And which number do you want them to have?\nCustomer: My cell is fine. 212-440-3391\nAssistant: Okay so you are booked for your 2012 Ford Escape today at 4 PM at Intelligent Auto Solutions for them to look at your door open light that won't go off. The appointment is under Sarah Johnson and number 212-440-3391. The initial inspection fee will be $99.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6d8ffdc855",
  "kind": "yes/no",
  "text": "Customer: I think 8 would be the best choice, just to be safe.\nAssistant: Okay, great. How many am I buying? Just two for you and your sister?\nCustomer: Yeah, two is fine. We're having a girl's night.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc35b386bbb",
  "kind": "yes/no",
  "text": "Customer: Okay, so let's start with 2 pizza pies, one with cheese only and one with vegetables and meatballs.\nAssistant: It looks like Benny's is out of the meatball topping today, did you want a different topping or should I order from a different location?\nCustomer: Stay at the Avenue J location and change the meatballs to pepperoni but only on half the second pie of pizza.",
  "question": "In the customer's last message, does \"Avenue J\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7ce9033c39",
  "kind": "yes/no",
  "text": "Customer: Hi, I want to buy some tickets for Aquaman for tonight.\nAssistant: Okay, what theater would you like to use?\nCustomer: Which ones are closest to Sussex, NJ?",
  "question": "In the customer's last message, does \"Sussex, NJ\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb7ab30a57d",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to order a pizza from Papa Johns in Willow Grove, PA",
  "question": "In the customer's last message, does \"Willow Grove, PA\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdf61d31f07",
  "kind": "yes/no",
  "text": "Customer: I would like a caramel macchiato\nAssistant: What size would you like me to get you?\nCustomer: I would like a venti please.",
  "question": "In the customer's last message, does \"venti\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0fc9f4d0fd",
  "kind": "yes/no",
  "text": "Customer: Tomorrow night.\nAssistant: Nothing available for the next couple of days.\nCustomer: Hmm, well, is \" Pet Sematary\" available.",
  "question": "In the customer's last message, does \"Pet Sematary\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3d50c9dea2",
  "kind": "yes/no",
  "text": "Customer: I need to be picked up at the Los Angeles Airport and will be dropped off at the Marriott.\nAssistant: Which Marriott are you staying at?\nCustomer: The one near the airport at West Century Blvd.",
  "question": "In the customer's last message, does \"near the airport at West Century Blvd\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd0ffa4b78b",
  "kind": "yes/no",
  "text": "Customer: Good\nAssistant: By the way, what year is your vehicle?\nCustomer: A 2018.",
  "question": "In the customer's last message, does \"2018\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4c32cc27d5",
  "kind": "yes/no",
  "text": "Customer: No, but I'm thinking of having Japanese\nAssistant: Which area are you thinking about\nCustomer: Anywhere near midtown in Manhattan",
  "question": "In the customer's last message, does \"near midtown in Manhattan\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q31fcc74224",
  "kind": "yes/no",
  "text": "Customer: ok ! Try it for 03/29/2019\nAssistant: ok ! You like to watch the movie on Morning or Evening?\nCustomer: Look for Evening",
  "question": "In the customer's last message, does \"Evening\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe9e0df4f5b",
  "kind": "yes/no",
  "text": "Assistant: Approximately 6 minutes.\nCustomer: Ok, go ahead and schedule it.\nAssistant: I have reserved your UberX for tonight at 6:30. You can check the status on your phone.",
  "question": "According to the assistant's last message, is \"UberX\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q65476fd21f",
  "kind": "yes/no",
  "text": "Assistant: Yes, the cost of the initial inspection will be $50.\nCustomer: Okay. That sounds good.\nAssistant: Great! To confirm you will be paying $50 for initial inspection and the appointment is at 9:00 AM Tuesday. You are experiencing brake light issues on your 2002 Ford Edge.",
  "question": "According to the assistant's last message, is \"9:00 AM\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe04eb1bcad",
  "kind": "yes/no",
  "text": "Assistant: Is there anything else I can help you with?\nCustomer: No thank you.\nAssistant: Ok, I have ordered 2 adult tickets to The Prodigy tonight at 7:20 at the AMC River East 21.",
  "question": "According to the assistant's last message, is \"AMC River East 21\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb79ec0276d",
  "kind": "yes/no",
  "text": "Customer: Two.\nAssistant: What time?\nCustomer: 7 PM",
  "question": "In the customer's last message, does \"7 PM\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5686b9786f",
  "kind": "yes/no",
  "text": "Customer: Fantastic. Let's see if you have any availability for my party of 16 on Saturday March 23 around 6pm.\nAssistant: I'm afraid I don't have 6pm available for that party size. For such a large party we would have to have you come in around 5pm before we get too busy.\nCustomer: I see. Well, I guess that's not too bad. Let's go ahead and book that for 5pm then.",
  "question": "In the customer's last message, does \"5pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbc9fdb1994",
  "kind": "yes/no",
  "text": "Customer: Please go to the Intelligent Auto Solutions website and book an appointment for me.\nAssistant: Which car are you taking in?\nCustomer: The 2018 Subaru Outlander.",
  "question": "In the customer's last message, does \"Subaru Outlander\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qadfad5ea0c",
  "kind": "yes/no",
  "text": "Customer: Hello Sharon, I was wondering if you could order me tickets for Dragon Ball Super: Broly.\nAssistant: Sure, that would be no problem Brad. Could you please tell me the city you're going to seeDragon Ball Super: Broly at?\nCustomer: Normally I'd be seeing it here in Tampa but I'm actually visiting a friend in Ocala.",
  "question": "In the customer's last message, does \"Ocala\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6d781afbb7",
  "kind": "yes/no",
  "text": "Assistant: Yes.\nCustomer: Ok. Let's get a medium hand tossed meat lovers pizza for the second one\nAssistant: Ok. Your large hand tossed pepperoni and black olive and your medium hand tossed meat lovers will be ready to pick up in 25 minutes. Do you want to pay for that now with your credit card m",
  "question": "According to the assistant's last message, is \"hand tossed\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf148c7394f",
  "kind": "yes/no",
  "text": "Customer: Hey, I would like to order a carryout special $7.99 large 2 topping pizza from Domino's.",
  "question": "In the customer's last message, does \"Domino's\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q157ade74ba",
  "kind": "yes/no",
  "text": "Assistant: Would you like me to place the order for you?\nCustomer: Yes.\nAssistant: Ok, I see that this Starbucks is all out of almond milk. Would you like to change the milk or try something else?",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd1bf11e7bd",
  "kind": "yes/no",
  "text": "Assistant: Ok, would you love to see the fairs on uber select?\nCustomer: yes please do.\nAssistant: Unfortunately Uber select is unavailable in your area right now, what do you want to do?",
  "question": "According to the assistant's last message, is \"Uber select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qebae6a1d73",
  "kind": "yes/no",
  "text": "Customer: I need some tickets for DUMBO playing!",
  "question": "In the customer's last message, does \"DUMBO\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6430942803",
  "kind": "yes/no",
  "text": "Customer: Order the larger car, one of the associates is uncomfortable in close spaces.\nAssistant: So then you would like the XL level ride?\nCustomer: Yes, please schedule it for 12:30.",
  "question": "In the customer's last message, does \"12:30\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q188c0874c3",
  "kind": "yes/no",
  "text": "Assistant: Sure. What day\nCustomer: Opening day\nAssistant: It looks like the tickets are sold out at your nearest theater. Is Saturday okay?",
  "question": "According to the assistant's last message, is \"nearest theater\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q76a5c346e3",
  "kind": "yes/no",
  "text": "Customer: I would like for you to purchase tickets to the movie Glass",
  "question": "In the customer's last message, does \"Glass\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc18b94c8a3",
  "kind": "yes/no",
  "text": "Customer: My air conditioning is not working\nAssistant: What make and model is your car?\nCustomer: 2015 Ford Focus",
  "question": "In the customer's last message, does \"Ford Focus\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q04119a2fe6",
  "kind": "yes/no",
  "text": "Assistant: There's a $70 diagnostics fee, but they don't charge you for it if the repair ends up costing more than $100.\nCustomer: Okay perfect.\nAssistant: Okay, it's submitted. Just to confirm, your appointment is at 4pm today, for a 2018 Nissan Altima, and they'll be looking at why your power steering isn't working. It'll cost $70 unless they spend more than $100 repairing the problem.",
  "question": "According to the assistant's last message, is \"Nissan Altima\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9b05aac7ff",
  "kind": "yes/no",
  "text": "Assistant: The gift card was used and it was sufficient. You still have a balance on it.\nCustomer: Ok, thank you.\nAssistant: I have booked your UberX for Miami Airport to 1940 Madison St.",
  "question": "According to the assistant's last message, is \"1940 Madison St\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf253d8e6ff",
  "kind": "yes/no",
  "text": "Customer: I'm not sure, something unique would be good.\nAssistant: OK, based on your preferences and search area, how about the Stinking Rose on La Cienega? Or Noshi Sushi on Beverly?\nCustomer: Stinking Rose would be great, can they do tonight at 8PM?",
  "question": "In the customer's last message, does \"Stinking Rose\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q09f1485c3d",
  "kind": "yes/no",
  "text": "Assistant: what size do you need?\nCustomer: make it a venti, and I want it extra foamy.\nAssistant: oh no. it looks like the Vanilla Bean Coconutmilk Latte isn't currently available at that location, would you like to select something else?",
  "question": "According to the assistant's last message, is \"Vanilla Bean Coconutmilk Latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8b892518ea",
  "kind": "yes/no",
  "text": "Customer: Great. Buy me tickets for a 2:45 pm showing on Sunday.\nAssistant: There are no 2:45 p.m. showings on that day. The closest times are 2:15 p.m. or 3:15 p.m.\nCustomer: I guess the 3:15 will have to work. Do they serve beer?",
  "question": "In the customer's last message, does \"3:15\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcee8b5a66e",
  "kind": "yes/no",
  "text": "Customer: hey i need you to schedule me an appointment at a repair shop\nAssistant: ok do you have a specific shop in mind?\nCustomer: yes i would like to get my car in at Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3e39813335",
  "kind": "yes/no",
  "text": "Customer: I need an appointment to Intelligent Auto Solutions\nAssistant: OK, what name should I make the appointment under?\nCustomer: Shelly Thompson",
  "question": "In the customer's last message, does \"Shelly Thompson\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe85d32ac35",
  "kind": "yes/no",
  "text": "Customer: I think everyone likes Italian - - a really good Italian place. We're going to spend some time there.\nAssistant: What about Luigi's on McPherson Church Road?\nCustomer: We've been there before, it's really good. What about 6:00 tomorrow with an outside table since the weather is going to be really nice.",
  "question": "In the customer's last message, does \"6:00\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6d5ec898cd",
  "kind": "yes/no",
  "text": "Customer: Thank You.\nAssistant: What name should I put the reservation under?\nCustomer: Please put the reservation under McCall.",
  "question": "In the customer's last message, does \"McCall\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2e3687b5a7",
  "kind": "yes/no",
  "text": "Customer: I am at a restaurant in Houston, TX\nAssistant: What is the name of the restaurant?\nCustomer: Taste of Texas",
  "question": "In the customer's last message, does \"Taste of Texas\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q66e5a6e39f",
  "kind": "yes/no",
  "text": "Assistant: Perfect! I will call them back now.\nCustomer: That is late, but I really want to go there.\nAssistant: I called and have you booked for that 9 o'clock spot. I am sure it will be worth going late.",
  "question": "According to the assistant's last message, is \"9 o'clock\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe7929a62db",
  "kind": "yes/no",
  "text": "Assistant: Yes, that one is playing this evening in Richland\nCustomer: Great, I need 2 tickets for the 730 show.\nAssistant: Im sorry, the 730 show is booked. There is a 6pm showing and an 830pm showing available.",
  "question": "According to the assistant's last message, is \"730\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaad020e498",
  "kind": "yes/no",
  "text": "Customer: Hellboy.\nAssistant: What theater are you wanting to go to? The usual?\nCustomer: No, I am in Ocean City. I want to go to the Sun & Surf Cinema.",
  "question": "In the customer's last message, does \"Ocean City\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf2c104ff26",
  "kind": "yes/no",
  "text": "Assistant: Any toppings should I add?\nCustomer: Just ask to put extra cheese and mushroom.\nAssistant: I am sorry , but Grandma is sold out . Is there any other pizza you would like to have?",
  "question": "According to the assistant's last message, is \"Grandma\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8e683380cc",
  "kind": "yes/no",
  "text": "Assistant: Yes, they've said it will like be an initial 250 dollars and then dependent on the issue, anywhere from 50 to 500 dollars.\nCustomer: That's prefect.\nAssistant: Okay, so your appointment is tomorrow morning, feb 12 at 8AM and initial fee is 250 dollars.",
  "question": "According to the assistant's last message, is \"feb 12\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95d76d6f1e",
  "kind": "yes/no",
  "text": "Assistant: Yes, of course are you ready to be picked up now?\nCustomer: Yes, the four of us are ready to go.\nAssistant: I see that there is no XL , only standard right now.",
  "question": "According to the assistant's last message, is \"XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd47b4f6b1b",
  "kind": "yes/no",
  "text": "Assistant: No problem! That will be a large loaded crust pizza with pepperoni, sausage, mushrooms and green peppers\nCustomer: That's perfect!\nAssistant: Your order will be ready to pick up at the Millersburg location in about 25 minutes",
  "question": "According to the assistant's last message, is \"Millersburg\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q39f791d886",
  "kind": "yes/no",
  "text": "Customer: I need to book movie tickets\nAssistant: For what city is this\nCustomer: this is for the seattle area",
  "question": "In the customer's last message, does \"seattle area\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1a02769067",
  "kind": "yes/no",
  "text": "Customer: There will be 9.\nAssistant: Okay 9 people.\nCustomer: Oh I would like to make this for tomorrow which is Friday.",
  "question": "In the customer's last message, does \"tomorrow which is Friday\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
