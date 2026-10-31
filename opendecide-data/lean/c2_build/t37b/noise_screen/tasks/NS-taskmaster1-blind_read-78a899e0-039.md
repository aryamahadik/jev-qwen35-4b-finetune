# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-039 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-039.json

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
  "qid": "qb8c1c3af16",
  "kind": "yes/no",
  "text": "Customer: The one in Fort Gratiot, Michigan.\nAssistant: Okay, and what would you like to order?\nCustomer: I was thinking a Black and White Mocha.",
  "question": "In the customer's last message, does \"Black and White Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9fbd7db27f",
  "kind": "yes/no",
  "text": "Customer: Intelligent Auto Solutions please.\nAssistant: Great, I just got access to their online interface. Could you share the make, model, and year of your car?\nCustomer: Sure, it's the BMW i8, 2016.",
  "question": "In the customer's last message, does \"2016\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf83065cf0a",
  "kind": "yes/no",
  "text": "Customer: from Vitto's\nAssistant: where is this located\nCustomer: on 3rd street",
  "question": "In the customer's last message, does \"3rd street\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q572f215abc",
  "kind": "yes/no",
  "text": "Assistant: Would you like to order an additional drink or food?\nCustomer: No\nAssistant: I have one hot Venti Caramel Macchiato with whole milk and whipped cream, upside down stirred ready for you to pick up at the S Main location at 9:46 pm. Your order will be available in store or drive through with this confirmation number> #485819.",
  "question": "According to the assistant's last message, is \"upside down stirred\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q43effb16b7",
  "kind": "yes/no",
  "text": "Customer: I feel it needs a replacement of the front shocks and also the brake buds need replacement.\nAssistant: What car do you have in mind madam?\nCustomer: My black Chevrolet, double cabin, 2000 cc and 2017 model",
  "question": "In the customer's last message, does \"2017\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0544bcf9e3",
  "kind": "yes/no",
  "text": "Assistant: do you like your coffee sweetened or unsweetened ?\nCustomer: unsweetened\nAssistant: Sorry this location is no longer serving the Iced Coffee Blend with milk , do you have another choice ?",
  "question": "According to the assistant's last message, is \"Iced Coffee Blend\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc7f537cf9b",
  "kind": "yes/no",
  "text": "Assistant: Same time, place, and seating, outside, Thursday 8PM?\nCustomer: Yes\nAssistant: They also don't have seating outside at that time, but they do have tables inside. Should we go with that or find another place?",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q390c5b1c56",
  "kind": "yes/no",
  "text": "Customer: Hello, Can you assist me in ordering my regular from Pizza Hut?",
  "question": "In the customer's last message, does \"Pizza Hut\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q00127c455b",
  "kind": "yes/no",
  "text": "Assistant: Ok. They say you can bring it in first thing in the morning, 7:00am tomorrow.\nCustomer: I really can't wait that long. Can they see me today, preferably around 3:30?\nAssistant: Hold on, checking on that. They're saying 3:30 is no good but they can squeeze you in at 4:00.",
  "question": "According to the assistant's last message, is \"3:30\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4b8834f704",
  "kind": "yes/no",
  "text": "Customer: It's a 2008 Toyota Corolla S model.\nAssistant: Great, what name and phone number do you want me to make the appointment under?\nCustomer: Make it under the name Jane Williams and phone number 555-678-7878.",
  "question": "In the customer's last message, does \"Jane Williams\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbfc12a582a",
  "kind": "yes/no",
  "text": "Assistant: I'm not sure. Let me check with them.\nCustomer: Take your time.\nAssistant: Unfortunately, they don't have zucchini. Do you want something else?",
  "question": "According to the assistant's last message, is \"zucchini\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb7030e0685",
  "kind": "yes/no",
  "text": "Customer: Okay, great thanks!\nAssistant: Here is your coffee and extra creamer.\nCustomer: Yummy, I'm so excited. I love Iced White Chocolate Mocha.",
  "question": "In the customer's last message, does \"Iced White Chocolate Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe77e82019a",
  "kind": "yes/no",
  "text": "Assistant: Sorry but there's a problem.\nCustomer: What?\nAssistant: They're out of whole milk.",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q697b05b0c9",
  "kind": "yes/no",
  "text": "Customer: I'd like to have it delivered as soon as possible. I will pay the tip in cash.\nAssistant: Okay. That's one large barbeque chicken pizza, original crust, with mushrooms instead of onions. Using the credit card on file and you will pay the tip in cash at the door. Delivery as soon as possible\nCustomer: Well, I guess I should make that an extra large.",
  "question": "In the customer's last message, does \"extra large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9d168394f5",
  "kind": "yes/no",
  "text": "Customer: Is there an extra charge?\nAssistant: No.\nCustomer: Extra thick, then.",
  "question": "In the customer's last message, does \"Extra thick\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf9861a1282",
  "kind": "yes/no",
  "text": "Assistant: Awesome, however, I just tried to place your order, and there was a complication.\nCustomer: What was the complication?\nAssistant: The Starbucks is out of 2% milk, so did you want an alternative milk?",
  "question": "According to the assistant's last message, is \"2% milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qebd7249a4e",
  "kind": "yes/no",
  "text": "Assistant: What size would you like?\nCustomer: Medium\nAssistant: It turns out that mushrooms are currently not available, would you like to make an alteration.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3f5928e332",
  "kind": "yes/no",
  "text": "Customer: I would like to order pizza.\nAssistant: which establishment do you want to order from?\nCustomer: I am in the mood for dominoes stuffed pizza.",
  "question": "In the customer's last message, does \"dominoes\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q53d1022261",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, there aren't any minivans available at this time. Through Uber XL, you can get a 6 seater SUV though. Is that acceptable?\nCustomer: Sure, that will work. Let's book the Uber XL SUV for 6 passengers. How long will it take for the SUV to arrive?\nAssistant: Ok, no problem. Your ride will be there in 6 minutes and the total for your UberXL SUV will be $79.82 from Regal Magnolia 18 parkland to Morton's Steak House in Fort Lauderdale, FL.",
  "question": "According to the assistant's last message, is \"Regal Magnolia 18 parkland\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q991efd199c",
  "kind": "yes/no",
  "text": "Customer: hey assistant, can you book a table for me for tomorrow dinner\nAssistant: sure, where would you like to go?\nCustomer: founding farmers in washing DC",
  "question": "In the customer's last message, does \"washing DC\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf35ebc4624",
  "kind": "yes/no",
  "text": "Customer: Barbuto\nAssistant: What time?\nCustomer: 7 pm please.",
  "question": "In the customer's last message, does \"7 pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbaa04021cd",
  "kind": "yes/no",
  "text": "Customer: No I cant, whats the earliest the next morning they can take it?\nAssistant: They open at 8am and can take it them. Would like me to book that time for you?\nCustomer: Yes, book it under Josh Smith and phone number 8767778899.",
  "question": "In the customer's last message, does \"Josh Smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qec489b514f",
  "kind": "yes/no",
  "text": "Assistant: okay let me check on that.\nCustomer: Sounds good\nAssistant: There is seating available but for 7:20 pm not 7:00 pm like you wanted.",
  "question": "According to the assistant's last message, is \"7:00 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe089689133",
  "kind": "yes/no",
  "text": "Assistant: So mushrooms and sausage?\nCustomer: Yes, thank you.\nAssistant: your pizza order of mushroom and sausage small personal pan pizza is complete and the pizzas will be ready for pickup in about 25 minutes. your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"personal pan pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q22ed346946",
  "kind": "yes/no",
  "text": "Customer: Hello, I need to schedule an appointment to have my car repaired.\nAssistant: Alright, which car?\nCustomer: It's the 2016 Hyundai Elantra GT.",
  "question": "In the customer's last message, does \"2016\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q259b0813fd",
  "kind": "yes/no",
  "text": "Assistant: Do you want a double shot?\nCustomer: No just regular please.\nAssistant: I wasn't able to place an order for your Venti Iced Mocha. They are out of the mocha sauce at the moment.",
  "question": "According to the assistant's last message, is \"mocha sauce\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d4a6af1a6",
  "kind": "yes/no",
  "text": "Assistant: Yes. Anything else?\nCustomer: No, that's it.\nAssistant: Okay, your reservation is set for December 16th at 8PM for four people at a booth seat.",
  "question": "According to the assistant's last message, is \"booth\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q60bfa6acea",
  "kind": "yes/no",
  "text": "Customer: Hey, I want to buy a ticket for The Lego Movie 2.\nAssistant: Do you want to see it here in Clarksville?\nCustomer: No, I want to see it in Louisville. I'm meeting a friend there to see a movie tonight.",
  "question": "In the customer's last message, does \"Louisville\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q372d123293",
  "kind": "yes/no",
  "text": "Customer: no thanks that's all.\nAssistant: okay .\nCustomer: Can I get a another mocha for take with me?",
  "question": "In the customer's last message, does \"mocha\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd0a6696a8a",
  "kind": "yes/no",
  "text": "Assistant: I will get that ordered for you\nCustomer: thank you\nAssistant: you will still get the receipt sent to your phone and it will be ready for pick up in 25 minutes. Enjoy your large double mushroom pizza",
  "question": "According to the assistant's last message, is \"double mushroom pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q73331ab708",
  "kind": "yes/no",
  "text": "Customer: Okay... Is there any availability for the 4:45 showing?\nAssistant: There are 3 tickets still available for that showing, how many did you want to buy?\nCustomer: I need 4... Will the 7:30 work instead?",
  "question": "In the customer's last message, does \"7:30\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0b764fe9a3",
  "kind": "yes/no",
  "text": "Customer: I'd like to buy two tickets for Us tonight.\nAssistant: Okay, what theater would you like to go to?\nCustomer: AMC River East 21 in Chicago",
  "question": "In the customer's last message, does \"AMC River East 21\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1da88bc10a",
  "kind": "yes/no",
  "text": "Assistant: Sounds good. And are there any special requirements you want to add?\nCustomer: Yes, I would like the keto crust instead of the original crust for that pizza.\nAssistant: Okay, it seems that they are out of the keto crust for the supreme pizza.",
  "question": "According to the assistant's last message, is \"keto crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc00b2cab09",
  "kind": "yes/no",
  "text": "Assistant: Yes, 8 is better anyway, cooler weather.\nCustomer: Then I can show off my new lilac shawl!\nAssistant: I'm sorry Madam, they are booked at 8:00 too.",
  "question": "According to the assistant's last message, is \"8:00\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q834681de87",
  "kind": "yes/no",
  "text": "Customer: I drive a Subaru Outback.\nAssistant: Sounds good. What name and number should I leave with the mechanic?\nCustomer: Say it's for Joe. They can call me back at 123-555-1234.",
  "question": "In the customer's last message, does \"Joe\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6f9199b463",
  "kind": "yes/no",
  "text": "Customer: Would you book a dinner for me for tomorrow night at 7PM?\nAssistant: Sure, where would you like to eat?\nCustomer: Can we try Holdfast on 11th Avenue?",
  "question": "In the customer's last message, does \"Holdfast\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q24366474b9",
  "kind": "yes/no",
  "text": "Customer: No, just the cappuccino.\nAssistant: No replacements or anything? Any health issues we need to be aware of?\nCustomer: No I'll be fine with the plain grande cappuccino.",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q888a825651",
  "kind": "yes/no",
  "text": "Customer: Okay, well then change our reservation to the Chophouse.\nAssistant: Indeed.\nCustomer: For 7:20 on 03/30.",
  "question": "In the customer's last message, does \"7:20\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6dd9e4ebd3",
  "kind": "yes/no",
  "text": "Assistant: OK, they have that,\nCustomer: Good, so we're all set?\nAssistant: Yes, I ordered one 16-cut thin crust pizza with classic red sauce with pepperoni and mushroom.",
  "question": "According to the assistant's last message, is \"thin crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6417c75570",
  "kind": "yes/no",
  "text": "Assistant: What is your method of payment?\nCustomer: I want them charged to my account.\nAssistant: Your order for two extra large BBQ Chicken pizzas is now complete. They will be ready for pickup in 25 minutes.",
  "question": "According to the assistant's last message, is \"BBQ Chicken pizzas\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc597b30a1b",
  "kind": "yes/no",
  "text": "Customer: 2010 Honda Civic\nAssistant: Whats the issue?\nCustomer: Batteries not charging, have to keep jump starting it.",
  "question": "In the customer's last message, does \"Batteries not charging, have to keep jump starting it\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q130f7bafdd",
  "kind": "yes/no",
  "text": "Customer: Okay no problem\nAssistant: Alright so two ticket at the Victorville Mall are available what seat do you want?\nCustomer: Yeah if the two in the middle on the second to the last row are available get me those should be seat D5 and D4",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf5f623fc4a",
  "kind": "yes/no",
  "text": "Assistant: ok that's Uber select right?\nCustomer: yes\nAssistant: unfortunately Uber select is unavailable in your area, what kind of ride would you love to be in?",
  "question": "According to the assistant's last message, is \"Uber select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q995858137c",
  "kind": "yes/no",
  "text": "Customer: Hey Rondley, I'm planning on seeing a movie tonight, could you purchase me some tickets?\nAssistant: Sure! What theater will you be going to?\nCustomer: We'll be going to the AMC DINE-IN Block 37 on 108th N street",
  "question": "In the customer's last message, does \"AMC DINE-IN Block 37\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5fa8fa94e2",
  "kind": "yes/no",
  "text": "Customer: Hey can you order an Uber XL for us?\nAssistant: Where are you and to where?\nCustomer: From LAX to the Staples Center",
  "question": "In the customer's last message, does \"LAX\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2ec04a9f80",
  "kind": "yes/no",
  "text": "Customer: Hello I need a appointment made at Intelligent Auto Solutions please.\nAssistant: For which car would you need the appointment for?\nCustomer: I need it for my Toyota Celica.",
  "question": "In the customer's last message, does \"Toyota Celica\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb8eaea8e6b",
  "kind": "yes/no",
  "text": "Customer: head lights are not working\nAssistant: Is there any other things to be rectified in your car?\nCustomer: oil needs to be checked and wheel allignment has to be done",
  "question": "In the customer's last message, does \"oil needs to be checked and wheel allignment has to be done\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe95d40bb9f",
  "kind": "yes/no",
  "text": "Assistant: Sure. Do you want anything added to it?\nCustomer: Can you ask them for whipped cream, please.\nAssistant: It seems that today they are out of whipped cream. Do you want something different?",
  "question": "According to the assistant's last message, is \"whipped cream\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbff7adefd7",
  "kind": "yes/no",
  "text": "Customer: I want to make a reservation at Katherine's at the CasaBlanca Resort.",
  "question": "In the customer's last message, does \"Katherine's\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6b00b2a419",
  "kind": "yes/no",
  "text": "Assistant: Will do. Do you want me to see if you can sit outside?\nCustomer: My husband would love that!\nAssistant: Oh darn. You can't sit outside.",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
