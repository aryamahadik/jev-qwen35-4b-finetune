# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-049 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-049.json

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
  "qid": "qc99bb2c73a",
  "kind": "yes/no",
  "text": "Assistant: not a problem, any thing else?\nCustomer: no thank you\nAssistant: starbucks is out of almond milk",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf6fd4ff807",
  "kind": "yes/no",
  "text": "Customer: Hi, I am thinking about ordering pizza for our lunchtime meeting tomorrow from Regina's pizzeria",
  "question": "In the customer's last message, does \"Regina's pizzeria\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q050d5f6b93",
  "kind": "yes/no",
  "text": "Customer: That's fine. I need assistance soon.\nAssistant: Okay. Would you like me to give him your information?\nCustomer: Yes. Please schedule an appointment for Jim Bob at 449-509-0004",
  "question": "In the customer's last message, does \"Jim Bob\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q56cb5fdd20",
  "kind": "yes/no",
  "text": "Customer: Yeah.\nAssistant: Oh I almost forgot, what kind of crust do you want?\nCustomer: Hand tossed is fine.",
  "question": "In the customer's last message, does \"Hand tossed\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2750bf0777",
  "kind": "yes/no",
  "text": "Customer: I'd like to order from Starbucks in Wooster\nAssistant: Okay, which drink would you like to order?\nCustomer: I will take a Tall",
  "question": "In the customer's last message, does \"Tall\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q84a3fb9eee",
  "kind": "yes/no",
  "text": "Assistant: Looks good.\nCustomer: great\nAssistant: You are all set for Friday, 3/29 at 7 for 4, booth at Kyota Ka",
  "question": "According to the assistant's last message, is \"Kyota Ka\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0d7fae6025",
  "kind": "yes/no",
  "text": "Assistant: They cannot estimate that at this time\nCustomer: Ok, please schedule\nAssistant: Thank you, you are reserved at Intelligent Auto Solutions tomorrow at 8 am under Peter 702-555-3434 for a 2015 Ford Focus for a air conditioning diagnostic for $100",
  "question": "According to the assistant's last message, is \"air conditioning diagnostic\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1ff744a78c",
  "kind": "yes/no",
  "text": "Customer: what are the prices\nAssistant: uberx is $34.52 and uberxl is $54.42\nCustomer: ok reserve the uberx for tomorrow at 4pm from carlisle theatre to the indian restaurant on 56 paxton street, harrisburg",
  "question": "In the customer's last message, does \"tomorrow at 4pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q31c4b6cbbf",
  "kind": "yes/no",
  "text": "Customer: Let's go with that one then. Less travel, a little cheaper.\nAssistant: What date/time are you looking to book?\nCustomer: Is there a five top available for this coming Saturday?",
  "question": "In the customer's last message, does \"five\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q733fa10128",
  "kind": "yes/no",
  "text": "Assistant: No. Unless you cancel it, then there's a flat fee plus a few cents for every minute it drove without you canceling it.\nCustomer: Okay, that sounds fair.\nAssistant: Great, your order is 10.70 for UberXL!",
  "question": "According to the assistant's last message, is \"UberXL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q28aaa5bac5",
  "kind": "yes/no",
  "text": "Assistant: great i will order\nCustomer: okay let me know\nAssistant: unfortunately they are out of ziti",
  "question": "According to the assistant's last message, is \"ziti\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe40cb2d73d",
  "kind": "yes/no",
  "text": "Customer: Yes, book it under Josh Smith and phone number 8767778899.\nAssistant: What is the year, make and model of the car you will be bringing in?\nCustomer: Im going be dropping off a 2016 BMW M5.",
  "question": "In the customer's last message, does \"2016\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0fe648f4f8",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza for pick-up, please.\nAssistant: What size pizza would you like?\nCustomer: I would like to order a large pizza.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1739752963",
  "kind": "yes/no",
  "text": "Assistant: Okay one moment.\nCustomer: Thanks.\nAssistant: Hello, unfortunately we're out of almond milk, is there anything else I can substitute for it or a different drink I can make you?",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qea1a21bb22",
  "kind": "yes/no",
  "text": "Assistant: What name and number should I put it under?\nCustomer: Jane Doe, put my business cell - it's (412) 888-0011\nAssistant: Okay Jane. I have you all scheduled to bring in your 2014 Jeep Cherokee so that they can examine the rear hatchback issues. You should drop off your vehicle no later than 8am on Monday, March 4th. Don't forget to bring $30 at the time of drop off.",
  "question": "According to the assistant's last message, is \"Jeep Cherokee\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf5f005ba07",
  "kind": "yes/no",
  "text": "Customer: Are there any theaters in Clay? I don't feel like driving into the city tonight.\nAssistant: Well, there is a regal cinema at the Great Northern Mall.\nCustomer: What times are they showing US?",
  "question": "In the customer's last message, does \"US\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9734961eeb",
  "kind": "yes/no",
  "text": "Customer: Can you order me some pizza from Myles Pizza?",
  "question": "In the customer's last message, does \"Myles Pizza\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd74d0b681b",
  "kind": "yes/no",
  "text": "Assistant: Same size?\nCustomer: Yes, a large.\nAssistant: Okay, I placed an order, one large pizza with mushrooms, garlic, and extra cheese.",
  "question": "According to the assistant's last message, is \"extra cheese\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1cf503f129",
  "kind": "yes/no",
  "text": "Customer: That is later than I would like to go as I have to drive back to Louisville tonight.\nAssistant: I've noticed that the Movie Tavern at Brannon Crossing has a 6:20pm time for $13.50 ticket price.\nCustomer: Hamburg Pavillion is rather far from where we are having dinner. See if US is playing at the Kentucky Theatre tonight.",
  "question": "In the customer's last message, does \"Kentucky Theatre\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q545eb9fcb2",
  "kind": "yes/no",
  "text": "Assistant: How about Chart House?\nCustomer: Please book a reservation at the chart House for 4, April 2 at 7 pm. Make sure the lobster is available.\nAssistant: April 2nd has no openings at 7pm",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa4ea9d9c68",
  "kind": "yes/no",
  "text": "Customer: I'm interested in your Seasonal Offerings\nAssistant: Ok, which flavor?\nCustomer: Black and White Mocha",
  "question": "In the customer's last message, does \"Black and White Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0f6d89b173",
  "kind": "yes/no",
  "text": "Customer: I need my left headlight replaced.\nAssistant: Okay, I need the details on your car.\nCustomer: Toyta Camry.",
  "question": "In the customer's last message, does \"Toyta Camry\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q40e49cfb03",
  "kind": "yes/no",
  "text": "Customer: Can you help me order pizza for my family for dinner tonight?\nAssistant: Yes, where would you like me to order from?\nCustomer: Fire Slice Pizza in Amarillo",
  "question": "In the customer's last message, does \"Fire Slice Pizza\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcf7048a45c",
  "kind": "yes/no",
  "text": "Customer: Hi, what are good retauranuts that serve seafood in orlando",
  "question": "In the customer's last message, does \"orlando\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc5a32fe678",
  "kind": "yes/no",
  "text": "Customer: get me an uber\nAssistant: okay where are you and where do you want to go?\nCustomer: I'm at Universal studios and i want to go to cafe tu tu tango.",
  "question": "In the customer's last message, does \"cafe tu tu tango\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q15a14f108b",
  "kind": "yes/no",
  "text": "Customer: What about the following evening, and make that three total my husband can then join.\nAssistant: Looks as if they don't have anything available then either, should we try another day?\nCustomer: No, let me try Scheme Resteraunt and Bar",
  "question": "In the customer's last message, does \"Scheme Resteraunt and Bar\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa9dbcda1d1",
  "kind": "yes/no",
  "text": "Customer: Oh no, do they have any other substitutes?\nAssistant: Yes, they have soy and coconut milk.\nCustomer: Eh, ok I'll actually just change my order to a cold brew please.",
  "question": "In the customer's last message, does \"cold brew\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b31703b55",
  "kind": "yes/no",
  "text": "Customer: On Main Street, outside of Clark University.\nAssistant: Excellent. And when would you like to be picked up on the way back?\nCustomer: I think I'll be done around 5:30 shopping.",
  "question": "In the customer's last message, does \"5:30\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q93fe495800",
  "kind": "yes/no",
  "text": "Customer: Hello, I'd like to make a reservation for a nice Italian Restaurant.\nAssistant: Sure, for which city?\nCustomer: Los Angeles",
  "question": "In the customer's last message, does \"Los Angeles\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9ddaad7fe5",
  "kind": "yes/no",
  "text": "Customer: its running hot\nAssistant: ok anything else\nCustomer: yes backup lights don't work",
  "question": "In the customer's last message, does \"backup lights don't work\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc9113f8bde",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza from Rosatis.",
  "question": "In the customer's last message, does \"Rosatis\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qda7f1e5eec",
  "kind": "yes/no",
  "text": "Customer: No thanks, just the movie.\nAssistant: Okay, how many adults and how many children?\nCustomer: There will be 2 adults and 3 children. How much is that?",
  "question": "In the customer's last message, does \"2 adults and 3 children\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4eb18d7b08",
  "kind": "yes/no",
  "text": "Customer: I want picked up at the Tavern on the Hill located at 109 Howard St, Enola, PA 17025\nAssistant: What time Naomi?\nCustomer: At 7:00pm please.",
  "question": "In the customer's last message, does \"7:00pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbf11c2c6e3",
  "kind": "yes/no",
  "text": "Assistant: Next boss\nCustomer: OK let me know\nAssistant: Chief inform me that special pizza is not available",
  "question": "According to the assistant's last message, is \"special pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q113b2b4b34",
  "kind": "yes/no",
  "text": "Assistant: For which showing would you like these two tickets?\nCustomer: The ten thirty showing, please.\nAssistant: I'm sorry, there is no ten thirty showing. They do have a seven thirty showing, though.",
  "question": "According to the assistant's last message, is \"ten thirty\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1cc242786d",
  "kind": "yes/no",
  "text": "Assistant: Oh yeah, he's in the best movies. I just love him.\nCustomer: He's the man. Let me know once you purchase the tickets and send me the address of the theatre.\nAssistant: I just purchased 2 tickets for Cold Pursuit at 6:45pm at the Showcase Cinema in Revere. The address is 565 Squire Rd Revere, MA 02151.",
  "question": "According to the assistant's last message, is \"Cold Pursuit\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0703740fa0",
  "kind": "yes/no",
  "text": "Assistant: Sorry but looks like they are out of one of the veggies.\nCustomer: Which one?\nAssistant: They don't have mushrooms.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8c5b754120",
  "kind": "yes/no",
  "text": "Customer: Hi I want to get some tickets to Us for tomorrow.",
  "question": "In the customer's last message, does \"Us\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbb595dd38f",
  "kind": "yes/no",
  "text": "Assistant: Sorry the Pacific Veggie pizza is out of stock today. Do you want something else?\nCustomer: Please order Philly Cheese Steak pizza, also X-Large and Hand Tossed.\nAssistant: Okay. They confirmed your order: one X-Large Hand Tossed Philly Cheese Steak pizza.",
  "question": "According to the assistant's last message, is \"Philly Cheese Steak pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0b3b9b7e14",
  "kind": "yes/no",
  "text": "Assistant: ok that's Uber select right?\nCustomer: yes\nAssistant: unfortunately Uber select is unavailable in your area, what kind of ride would you love to be in?",
  "question": "According to the assistant's last message, is \"Uber select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe267d76316",
  "kind": "yes/no",
  "text": "Customer: Okay Google, can you book me an appointment at Intelligent Auto Solutions?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q753cacd37a",
  "kind": "yes/no",
  "text": "Customer: No, the service there has gotten really poor. I've been meaning to visit the new Alamo theater that just opened. Are there any tickets there for 8 p.m. tonight?\nAssistant: Let me see.... no but there is one at 7:30. Is that okay with you?\nCustomer: Sure, that works. How much are two tickets?",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69d5c5b9e2",
  "kind": "yes/no",
  "text": "Assistant: What would you like on your pizza?\nCustomer: I would like sausage and pepperoni on it.\nAssistant: We are currently out of pepperoni. Is there another topping you would like?",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa5b8d89d05",
  "kind": "yes/no",
  "text": "Customer: Would next tuesday be available at 10 a.m.\nAssistant: Where at?\nCustomer: At Schmid'ts auto repair",
  "question": "In the customer's last message, does \"Schmid'ts auto repair\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe12fcc7e1f",
  "kind": "yes/no",
  "text": "Customer: thank you\nAssistant: what name and number\nCustomer: Jane Go(999-999-999)",
  "question": "In the customer's last message, does \"Jane Go\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc1a2b42c4c",
  "kind": "yes/no",
  "text": "Customer: Okay, that will be fine.\nAssistant: Okay, last question - what contact information should I provide them with?\nCustomer: Sarah Zylck, phone number 781-820-3702",
  "question": "In the customer's last message, does \"Sarah Zylck\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc684dfbdc8",
  "kind": "yes/no",
  "text": "Customer: That’s too late. How about Saturday at 6:45?\nAssistant: I’m looking at Saturday. The only times are 8:00 and 9:30.\nCustomer: Those won’t work at all. Can we try for a table at Din Tai Fung in Century City?",
  "question": "In the customer's last message, does \"Century City\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb120753734",
  "kind": "yes/no",
  "text": "Assistant: Where can I meet you?\nCustomer: Oh, I'm in a secured building, let's say I meet you at the corner of Broadway and Citrus in 20 minutes.\nAssistant: Ok I'm here and inexplicably they are out of Americanos. I don't know how that is possible.",
  "question": "According to the assistant's last message, is \"Americanos\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc59bf44ecb",
  "kind": "yes/no",
  "text": "Customer: 2005 N Ocean Blvd, Myrtle Beach, SC.\nAssistant: Great, what would you like to order?\nCustomer: I'd like a Grande Starbucks® Blonde Caramel Cloud Macchiato",
  "question": "In the customer's last message, does \"Grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7a0a5512b6",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry, 1:30 is sold out. The 4:40 and 7:30 still have tickets available.\nCustomer: OK, I'll take 4:40.\nAssistant: I've booked two tickets for Pet Sematary for the 4:40 showing.",
  "question": "According to the assistant's last message, is \"Pet Sematary\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
