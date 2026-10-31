# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-051 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-051.json

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
  "qid": "q0ae08deb97",
  "kind": "yes/no",
  "text": "Customer: Not really. They both meet all of my other requirements though?\nAssistant: Yes they do. Would you like to purchase the tickets at either of the places?\nCustomer: Yes go ahead and purchase the cheaper ones at NCG please.",
  "question": "In the customer's last message, does \"NCG\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q813f65f336",
  "kind": "yes/no",
  "text": "Customer: Hey, can you call an Uber for me?\nAssistant: Sure. Where are you coming from and what will your destination be?\nCustomer: I'd like to come from SNA airport to the Santa Ana Esports Arena.",
  "question": "In the customer's last message, does \"Santa Ana Esports Arena\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qca34e7aeaa",
  "kind": "yes/no",
  "text": "Customer: Haley, the Lexus is not letting me close all doors with the autolock. Can you please get me an appointment at Intelligent Auto Solutions.\nAssistant: That's new. O.K, make, model and year please.\nCustomer: 2014 Lexus es 300",
  "question": "In the customer's last message, does \"2014\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe4d87834ad",
  "kind": "yes/no",
  "text": "Customer: I'd like to order pizza from Papa John's\nAssistant: What is your location?\nCustomer: I'm in Boston Massachusetts",
  "question": "In the customer's last message, does \"Boston Massachusetts\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdd4651d573",
  "kind": "yes/no",
  "text": "Assistant: Alright so they'll take a look into the weird shifting noise and perform the regular scheduled maintenance. Which phone number do you want to add to the appointment? They'll send text reminders.\nCustomer: You can use more work cell: 215-888-1234\nAssistant: Alright. Just to confirm, I have you booked for tomorrow at 2:00 with Intelligent Auto Solutions on Maple Ave.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaf73e83207",
  "kind": "yes/no",
  "text": "Customer: Perfect.\nAssistant: What time would you like to get picked up?\nCustomer: Does 3 pm sound okay?",
  "question": "In the customer's last message, does \"3 pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q96afc5bc30",
  "kind": "yes/no",
  "text": "Customer: My name is John Wayne and my phone number is 503-555-4929.\nAssistant: Great John, we'll get you fixed up in no time. What type of vehicle needs serviced?\nCustomer: It's a 2015 Dodge Ram 1500 pickup truck.",
  "question": "In the customer's last message, does \"2015\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1a92eed454",
  "kind": "yes/no",
  "text": "Assistant: Ok, I'll get right back to you to confirm that your order is ready.\nCustomer: Thanks\nAssistant: Hi, I'm confirming that your Cafe au Lait is on order at 1365 Park Street Alameda, CA. and will be ready for pickup shortly and that your receipt will be sent to your iPhone via text message. Ok, thank you until next time.",
  "question": "According to the assistant's last message, is \"1365 Park Street Alameda, CA\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1ff2132d60",
  "kind": "yes/no",
  "text": "Assistant: Ok. What time and day would you like to book the reservation?\nCustomer: Today at 6pm.\nAssistant: There are no spots for 6pm. Other timeslots are 6:15pm, 6:30pm and 7:20pm.",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q450a7ad7f1",
  "kind": "yes/no",
  "text": "Customer: OK. I think I will order an iced black and white mocha\nAssistant: Good. What size?\nCustomer: A tall.",
  "question": "In the customer's last message, does \"tall\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfe2d166c55",
  "kind": "yes/no",
  "text": "Customer: no we wont be off work till 5 pm and would be rushed\nAssistant: ok let me look again for you\nCustomer: ok thank you. we could do a 7:15",
  "question": "In the customer's last message, does \"7:15\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q989317e1b7",
  "kind": "yes/no",
  "text": "Customer: I'm dropping my car off at Tires Plus in about 20 minutes. Then I'm heading to the University library.\nAssistant: Okay, any specific type of Uber?\nCustomer: Check my options on the Fare Locator online. I'm heading from Tires Plus to the Chester Fritz Library.",
  "question": "In the customer's last message, does \"Tires Plus\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q52b70cb098",
  "kind": "yes/no",
  "text": "Assistant: They have that date open.\nCustomer: Can I get a confirmation of how much it's going to cost?\nAssistant: Yes, the total will come to $96 for a diagnostic fee. I have you booked for the 24th in the morning, for a differential lock issue with a 2012 Jeep Wrangler Rubicon Unlimited.",
  "question": "According to the assistant's last message, is \"differential lock issue\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc9c58f65fc",
  "kind": "yes/no",
  "text": "Assistant: Okay your total will be $22.50\nCustomer: Great, charge it to my account.\nAssistant: Your order has been placed for a large thin crust pizza, with salami, pepperoni, onions and mushrooms",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q526fb01f47",
  "kind": "yes/no",
  "text": "Customer: I want the one in Center City Philadelphia\nAssistant: ok how many people\nCustomer: It is for four people.",
  "question": "In the customer's last message, does \"four\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0fcb216fa2",
  "kind": "yes/no",
  "text": "Customer: Hey, can you send a Lyft to come get me?\nAssistant: Sure, where are you at currently?\nCustomer: I'm at The Grind Coffee House in Apple Valley.",
  "question": "In the customer's last message, does \"The Grind Coffee House in Apple Valley\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe24b36c669",
  "kind": "yes/no",
  "text": "Customer: I'd like to take it to the Intelligent Auto Solutions downtown.\nAssistant: Can do! Can you please tell me the make and model of your car?\nCustomer: Yes, I drive a Tesla Model S.",
  "question": "In the customer's last message, does \"Tesla Model S\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa2e36d852e",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to call a lyft\nAssistant: Ok. Where would you like to be picked up and dropped off?\nCustomer: I'm going from the SF MOMA to SFO.",
  "question": "In the customer's last message, does \"SFO\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q187945cdab",
  "kind": "yes/no",
  "text": "Customer: Hi Stacy, can you book a table for 5 at Blue Hill for this Saturday evening at 6?",
  "question": "In the customer's last message, does \"Blue Hill\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5d079c127d",
  "kind": "yes/no",
  "text": "Customer: Well, on the screen says: 'ABS check/SVC system'\nAssistant: Any other indication I should be letting him know?\nCustomer: Yes, my car seems to loose power, and traction.",
  "question": "In the customer's last message, does \"my car seems to loose power, and traction\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbd40ebedee",
  "kind": "yes/no",
  "text": "Assistant: It will be $100\nCustomer: Okay, that will work.\nAssistant: An appointment for John Smith at 916-555-1212 has been scheduled for today at 2 pm for your 2018 Subraru Impreza for a hundred dollar inspection for the noise made when turning.",
  "question": "According to the assistant's last message, is \"Subraru Impreza\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q820b96e944",
  "kind": "yes/no",
  "text": "Assistant: Would you like to order anything else today?\nCustomer: No, just the pizza.\nAssistant: Sorry sir, it turns out we've run out of pineapple tonight. Would you like to replace it with a different topping?",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q55cda9b5ff",
  "kind": "yes/no",
  "text": "Customer: No that's too late, what is the showing right before the 9 pm one?\nAssistant: There is a 5:30 pm and a 7:55 pm viewing times, which would you like to search?\nCustomer: The 7:55 pm would be perfect",
  "question": "In the customer's last message, does \"7:55 pm\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2f928d3836",
  "kind": "yes/no",
  "text": "Customer: Peets\nAssistant: What kind of coffee do you like?\nCustomer: I would like to have espresso.",
  "question": "In the customer's last message, does \"espresso\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3c2dcc34fa",
  "kind": "yes/no",
  "text": "Customer: Yep.\nAssistant: thanks, what model is your car?\nCustomer: It's a 2011 Nissan Rogue.",
  "question": "In the customer's last message, does \"Nissan Rogue\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4d03fa3cfd",
  "kind": "yes/no",
  "text": "Customer: MJs in chicago\nAssistant: Ooh that’s tough boss\nCustomer: For 3 at 6, just try",
  "question": "In the customer's last message, does \"3\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q431f7904f4",
  "kind": "yes/no",
  "text": "Customer: Thanks!\nAssistant: No problem! Which cinema do you want to go to?\nCustomer: AMC Palace 9",
  "question": "In the customer's last message, does \"AMC Palace 9\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q252bf83ed7",
  "kind": "yes/no",
  "text": "Customer: I would like to request a ride from Lyft.\nAssistant: Okay, where would you like to be picked up and where do you want to go?\nCustomer: Im at the DFW airport, and I need a ride to my hotel, the Fairmont Dallas.",
  "question": "In the customer's last message, does \"DFW airport\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q795e1705c1",
  "kind": "yes/no",
  "text": "Customer: Hey, I'm going to need tickets for The Lego Movie 2: The Second Part\nAssistant: Ok, what theatre would you like to see the movie at?\nCustomer: I want to see the movie at the Regency Village Theatre, in Westwood, Los Angeles.",
  "question": "In the customer's last message, does \"Westwood, Los Angeles\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q961f27dbd8",
  "kind": "yes/no",
  "text": "Customer: Phoenix\nAssistant: Okay, I have found that\nCustomer: I want a table for 2 at 7 o clock",
  "question": "In the customer's last message, does \"7 o clock\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5b0e20b8e4",
  "kind": "yes/no",
  "text": "Customer: Hey can you put a pizza order in for me online?\nAssistant: Sure from what place?\nCustomer: You can order from toppers pizza. It's pretty easy online.",
  "question": "In the customer's last message, does \"toppers pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q51f91029ee",
  "kind": "yes/no",
  "text": "Customer: Yeah, let's delete that pizza and start over\nAssistant: Ok. What do you want on that pizza?\nCustomer: Let's get a medium ham and pineapple instead",
  "question": "In the customer's last message, does \"medium\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf396d1fd78",
  "kind": "yes/no",
  "text": "Customer: Friday April 5th at 7pm.\nAssistant: How many people should I set the reservation for?\nCustomer: For 5 people please.",
  "question": "In the customer's last message, does \"5\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1ae57af802",
  "kind": "yes/no",
  "text": "Assistant: Okay, let me check on that for you.\nCustomer: Thanks.\nAssistant: I'm sorry I don't see any XL in your area.",
  "question": "According to the assistant's last message, is \"XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q601d6d3d9b",
  "kind": "yes/no",
  "text": "Customer: I need to take my car in to get checked out by a mechanic\nAssistant: What problem are you having with your car?\nCustomer: I noticed an engine light appearing on the dash and I'm not sure what the exact issue is",
  "question": "In the customer's last message, does \"I noticed an engine light appearing on the dash\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa405a359a6",
  "kind": "yes/no",
  "text": "Assistant: Thank you and what is a good number for them to contact you at?\nCustomer: It's 930-644-1784\nAssistant: Perfect. I have you scheduled for tonight at 6pm. They should be expecting you and will call you if there are any changes",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6b159f10f8",
  "kind": "yes/no",
  "text": "Assistant: Ok, I have one 16\" \"The Princess,\" will that complete your order?\nCustomer: Yes.\nAssistant: Great. Your pizza will be ready for pickup at Piezon's in 25 minutes.",
  "question": "According to the assistant's last message, is \"Piezon's\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0f5824ea64",
  "kind": "yes/no",
  "text": "Customer: I'd like 7 pm then.\nAssistant: I'm sorry, that is also not available.\nCustomer: What about Tiffen at 6 pm on March 21 for four people?",
  "question": "In the customer's last message, does \"Tiffen\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5435e1a1ab",
  "kind": "yes/no",
  "text": "Customer: Okay, I need to change that restaurant.\nAssistant: What is the new restaurant you need a reservation for?\nCustomer: East Garden Chinese, NYC.",
  "question": "In the customer's last message, does \"NYC\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc94b79e81d",
  "kind": "yes/no",
  "text": "Assistant: Ok. I need what is a best phone number?\nCustomer: They can reach me at 123-456-8989\nAssistant: TOday does not work. Would tomorrow morning at 8 a.m. be Ok?",
  "question": "According to the assistant's last message, is \"TOday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q76455b905e",
  "kind": "yes/no",
  "text": "Customer: Hellboy.\nAssistant: What theater are you wanting to go to? The usual?\nCustomer: No, I am in Ocean City. I want to go to the Sun & Surf Cinema.",
  "question": "In the customer's last message, does \"Ocean City\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8e1eba0553",
  "kind": "yes/no",
  "text": "Assistant: Sounds good. Will place it now.\nCustomer: Thanks.\nAssistant: Unfortunately, they ran out of feta cheese and black olives. Would you like to change your order?",
  "question": "According to the assistant's last message, is \"black olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1a0bd4a4ec",
  "kind": "yes/no",
  "text": "Assistant: Ok, searching for options now.\nCustomer: Thank you, just let me know the price please.\nAssistant: Sure. I'm not showing an UberX available in your area for your time, but there is an UberXL.",
  "question": "According to the assistant's last message, is \"UberX\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q47454b8ff2",
  "kind": "yes/no",
  "text": "Customer: I'll go for dark roast today\nAssistant: What size would you like?\nCustomer: I want grande please.",
  "question": "In the customer's last message, does \"grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd5df987d59",
  "kind": "yes/no",
  "text": "Customer: Yeah, I like that theater.\nAssistant: Ok, so they have showings at 3pm, 5pm, and 7pm. Which one do you want?\nCustomer: I think the 5pm one is best for me.",
  "question": "In the customer's last message, does \"5pm\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb96662b497",
  "kind": "yes/no",
  "text": "Assistant: Do you have any other requests?\nCustomer: I would like to add outside seating.\nAssistant: Your reservation for 6 people at Maggiano's on Sunday for outside seating has been confirmed",
  "question": "According to the assistant's last message, is \"outside seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q943a1d0f9d",
  "kind": "yes/no",
  "text": "Customer: I'd like to get a pizza from Domenico's.",
  "question": "In the customer's last message, does \"Domenico's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe909047dbd",
  "kind": "yes/no",
  "text": "Customer: Home’s Chinese.\nAssistant: Where is this restaurant?\nCustomer: New York City.",
  "question": "In the customer's last message, does \"New York City\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6652915ce1",
  "kind": "yes/no",
  "text": "Customer: It is a 2016 Audi A7\nAssistant: What name and number are you going to be giving them?\nCustomer: Andrew Smith 2078424371",
  "question": "In the customer's last message, does \"Andrew Smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc547cebf49",
  "kind": "yes/no",
  "text": "Assistant: The Cedars offers several hot meals from the grill.\nCustomer: Great, get the tickets at The Cedars.\nAssistant: I've booked you for 2 tickets to The Upside at The Cedars for 6pm",
  "question": "According to the assistant's last message, is \"The Upside\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
