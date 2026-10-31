# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-009 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-009.json

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
  "qid": "qa36d6e630b",
  "kind": "yes/no",
  "text": "Assistant: I'll make the call right now.\nCustomer: Thanks. I'll just wait.\nAssistant: 2 tickets have been confirmed and will be sent to your mobile device as a text message.",
  "question": "According to the assistant's last message, is \"2\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q29043de901",
  "kind": "yes/no",
  "text": "Assistant: Where do you want it from?\nCustomer: Papa Johns\nAssistant: Checking, sorry, the nearest pizza is all out of sausage",
  "question": "According to the assistant's last message, is \"sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbdeefdaf4f",
  "kind": "yes/no",
  "text": "Customer: I'll choose a different place.\nAssistant: Okay, which one, please?\nCustomer: The Capital Grille, also in Philly.",
  "question": "In the customer's last message, does \"Philly\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb02fa0084c",
  "kind": "yes/no",
  "text": "Assistant: It will be $5.65.\nCustomer: Great! I'm ready for it.\nAssistant: Well, it will be ready to pick up at Starbucks Memorial Parkway in 20 minutes!",
  "question": "According to the assistant's last message, is \"Memorial Parkway\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q07fd32384c",
  "kind": "yes/no",
  "text": "Customer: I would like a hawiian pizza\nAssistant: What size?\nCustomer: A large please",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q79aaac08f6",
  "kind": "yes/no",
  "text": "Assistant: Great so one medium BBQ Chicken pizza with pineapple and onion added to it.\nCustomer: Yes that is correct.\nAssistant: Oh no. Sorry they don't have pineapple right now.",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb78d221de5",
  "kind": "yes/no",
  "text": "Assistant: Do you want me to check for another time today?\nCustomer: Yes, please. How about 7PM?\nAssistant: I'm very sorry 7PM is not available either. They seem to only have reservations for 4PM or earlier.",
  "question": "According to the assistant's last message, is \"7PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8791d8a231",
  "kind": "yes/no",
  "text": "Assistant: Alright let me check.\nCustomer: Sounds good\nAssistant: They actually do not have outside seating currently.",
  "question": "According to the assistant's last message, is \"outside seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q00f4a6e892",
  "kind": "yes/no",
  "text": "Customer: I would like to change my headlight",
  "question": "In the customer's last message, does \"change my headlight\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfe6a42a60a",
  "kind": "yes/no",
  "text": "Assistant: How many tickets would you like?\nCustomer: I'll need two.\nAssistant: Ok, I've booked two tickets for the 6:40 showing of Green Book tonight at the Alamo Drafthouse Cinema Mueller.",
  "question": "According to the assistant's last message, is \"Alamo Drafthouse Cinema Mueller\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc866291673",
  "kind": "yes/no",
  "text": "Customer: No, that's okay, do they have thin or pan crust?\nAssistant: Yes, both of those are available\nCustomer: I'll have it with the pan crust then.",
  "question": "In the customer's last message, does \"pan crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1883c97b20",
  "kind": "yes/no",
  "text": "Customer: Great, make a reservation\nAssistant: For how many?\nCustomer: 4 people",
  "question": "In the customer's last message, does \"4\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbb3e8c95e9",
  "kind": "yes/no",
  "text": "Assistant: Yes, all the others are available.\nCustomer: Okay, can I book the UberX?\nAssistant: Yes, UberX is available. I booked it for you. Your ride will arrive in about 9 minutes.",
  "question": "According to the assistant's last message, is \"9 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4a6f59a618",
  "kind": "yes/no",
  "text": "Customer: It's a 2015 Ford F150.\nAssistant: Okay. What contact details do you want me to put down?\nCustomer: James Johnson and for my phone number put 416-423-9500.",
  "question": "In the customer's last message, does \"James Johnson\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q542cd238fa",
  "kind": "yes/no",
  "text": "Customer: Are there any BBQ restaurants near me?\nAssistant: Where are you looking to find a restaurant?\nCustomer: Rochester, NY",
  "question": "In the customer's last message, does \"Rochester, NY\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8c56fffdfc",
  "kind": "yes/no",
  "text": "Customer: I'd like one with spinach, artichokes, and ricotta.\nAssistant: Hand tossed or deep dish?\nCustomer: Deep dish.",
  "question": "In the customer's last message, does \"Deep dish\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc1e7b74513",
  "kind": "yes/no",
  "text": "Assistant: Great the order is in, do you need someone to pick it up for you?\nCustomer: No, I'll just swing by on my break in 10 minutes\nAssistant: Alright then. Your drink is on order at the Starbucks on 4th Street in Colorado Springs, and will be ready for pickup shortly. Your receipt will be sent to your mobile device via text message so you won't have to pay in store.",
  "question": "According to the assistant's last message, is \"4th Street in Colorado Springs\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd6cf12cc9a",
  "kind": "yes/no",
  "text": "Customer: Yea I'll add whipped cream.\nAssistant: Got it. Anything else you would like to order?\nCustomer: Yes I'd like a grande cappuccino as well.",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1c84322299",
  "kind": "yes/no",
  "text": "Customer: Hello, could you order a pizza for me from East of Chicago?\nAssistant: Sure, I'll be happy to assist you! What would you like to order?\nCustomer: I would like to order a large pizza",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qde48c44670",
  "kind": "yes/no",
  "text": "Customer: I want 2 Meatlovers pizzas\nAssistant: Alright what size?\nCustomer: I want one Large and one medium, both meat lovers",
  "question": "In the customer's last message, does \"medium\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa4ef518f85",
  "kind": "yes/no",
  "text": "Customer: Yes, that's the one!\nAssistant: What would you like?\nCustomer: I think a large pepperoni and a breakfast pizza.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qae129189b3",
  "kind": "yes/no",
  "text": "Customer: REGAL CINEMAS GATEWAY 16, Austin, Texas\nAssistant: OK, where is the next destination?\nCustomer: COUNTER CULTURE, 2337 E Cesar Chavez St, Austin, TX 78702",
  "question": "In the customer's last message, does \"COUNTER CULTURE, 2337 E Cesar Chavez St, Austin, TX 78702\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4734c6982d",
  "kind": "yes/no",
  "text": "Customer: Sure, what flavors do you offer?\nAssistant: We have cajun, garlic and ranch flavored crusts.\nCustomer: I'd like cajun crust on both the pizzas.",
  "question": "In the customer's last message, does \"cajun crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3634b1bc2d",
  "kind": "yes/no",
  "text": "Assistant: How will you be paying for this?\nCustomer: Use the gift card that I have on file.\nAssistant: Venti Iced, Iced Cinnamon Macchiato for Alex will be ready for pickup in 10 minutes.",
  "question": "According to the assistant's last message, is \"Iced Cinnamon Macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q86d43d51b9",
  "kind": "yes/no",
  "text": "Customer: How about this Saturday at 7 pm?\nAssistant: I'm sorry, it seems like they're all booked at that time.\nCustomer: How about 6 pm?",
  "question": "In the customer's last message, does \"6 pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdcacbe3164",
  "kind": "yes/no",
  "text": "Customer: Hey I want to order a pizza from Mr. Moto's.",
  "question": "In the customer's last message, does \"Mr. Moto's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7c2a7f1f07",
  "kind": "yes/no",
  "text": "Customer: Haley, our Honda Civic is making a noise. Can you please get me an appointment at Intelligent Auto Solutions.\nAssistant: O.K. Do you know the year of the car?\nCustomer: 2013. It should auto-populate with our account.",
  "question": "In the customer's last message, does \"2013\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9021f31b92",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to order a ride from Uber?\nAssistant: I got you. Where is your from location?\nCustomer: J. Liu Of Dublin, in Dublin Ohio.",
  "question": "In the customer's last message, does \"J. Liu Of Dublin, in Dublin Ohio\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q27290a39d8",
  "kind": "yes/no",
  "text": "Assistant: What type of car would you like?\nCustomer: Uber Pool.\nAssistant: UberPool is not available for parties of 6.",
  "question": "According to the assistant's last message, is \"UberPool\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd510000824",
  "kind": "yes/no",
  "text": "Assistant: Ok and what kind of car do you want\nCustomer: Uber X please\nAssistant: Um, Uber X isn't available, is Uber XL ok?",
  "question": "According to the assistant's last message, is \"Uber X\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q78380a655c",
  "kind": "yes/no",
  "text": "Customer: Great.\nAssistant: It appears there are only four tickets left for that show time, however.\nCustomer: Okay, four tickets is fine.",
  "question": "In the customer's last message, does \"four\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5b645d49cd",
  "kind": "yes/no",
  "text": "Assistant: A large pizza black olives and green peppers. Is that right?\nCustomer: Yes.\nAssistant: Order confirmed for a large pizza black olives and green peppers. It will be ready for pickup shortly.",
  "question": "According to the assistant's last message, is \"green peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6c0096d3a2",
  "kind": "yes/no",
  "text": "Customer: Yes i am from new york city. any starbucks coffee shop available.\nAssistant: Yes, near by newyork. May I take your order?\nCustomer: Yes. I'd like the flat white order of coffee.",
  "question": "In the customer's last message, does \"flat white\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q68502eafdf",
  "kind": "yes/no",
  "text": "Assistant: Do you want whipped cream?\nCustomer: No I don't.\nAssistant: OK. Your drink will be ready to collect at 55th Street in 15 minutes.",
  "question": "According to the assistant's last message, is \"55th Street\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5a4ef543a4",
  "kind": "yes/no",
  "text": "Customer: can you get me into intelligent auto solutions today?\nAssistant: what should i say is wrong with the car?\nCustomer: there is some noise in the right front and it gets louder when i speed up.",
  "question": "In the customer's last message, does \"noise in the right front\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc14557e7e8",
  "kind": "yes/no",
  "text": "Customer: OK, sounds good. Can you book me a table for six at Koi on Friday January 25 at 8pm?\nAssistant: I'm sorry, there are no tables that size available at 8pm.\nCustomer: What about a table for two and a separate table for four?",
  "question": "In the customer's last message, does \"two\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa31e72fddf",
  "kind": "yes/no",
  "text": "Customer: Hey can you find out what time Us is playing in theatres?",
  "question": "In the customer's last message, does \"Us\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q80f7f5b08a",
  "kind": "yes/no",
  "text": "Customer: Thank you very much.\nAssistant: Well, they now are saying that they can't get you in until 9:00pm.  Would you like me to reserve that time or call somewhere else?\nCustomer: Oh goodness. What a pain. Let's skip The Chophouse and try Ruth Chris for the original 7pm.",
  "question": "In the customer's last message, does \"7pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9bcaa41603",
  "kind": "yes/no",
  "text": "Customer: Yep.\nAssistant: The AMC Cinema at the Universal CityWalk is playing Us in IMAX, but the next showing time is at 8 PM. Is that ok?\nCustomer: Hm, I'd rather go earlier. What about the ArcLight theater in Sherman Oaks?",
  "question": "In the customer's last message, does \"Sherman Oaks\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa2f338d624",
  "kind": "yes/no",
  "text": "Assistant: Sounds good\nCustomer: thank you!\nAssistant: i ordered the drink (cafe mocha - 2 percent - grande - whipped creme) from the Harris Teeter on 9th street",
  "question": "According to the assistant's last message, is \"whipped creme\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0237eca294",
  "kind": "yes/no",
  "text": "Assistant: What is the name and number you would like me to put it under\nCustomer: Rico Suave 777-777-7777\nAssistant: Ok. Appointment booked for today at 4pm. Contact information is Rico Suave 777-777-7777. The diagnostics fee will be $100 to check out all the warning lights",
  "question": "According to the assistant's last message, is \"check out all the warning lights\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb1481e8b1c",
  "kind": "yes/no",
  "text": "Customer: Pickup.\nAssistant: What pizza shop would you like to order from?\nCustomer: Gino's on Grant and 1st.",
  "question": "In the customer's last message, does \"Grant and 1st\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3136be3b23",
  "kind": "yes/no",
  "text": "Assistant: Is that all?\nCustomer: Yes.\nAssistant: Ok. Sorry they don't have peppermint right now.",
  "question": "According to the assistant's last message, is \"peppermint\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5cfe225224",
  "kind": "yes/no",
  "text": "Customer: i need to order an ride with uber\nAssistant: Ok, where are you?\nCustomer: I am at 1801 Mountain Rd NW, Albuquerque, NM 87104",
  "question": "In the customer's last message, does \"1801 Mountain Rd NW, Albuquerque, NM 87104\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf932fdf7da",
  "kind": "yes/no",
  "text": "Customer: No, it isn't!  So I'd like to get it in as soon as possible.\nAssistant: I can do that, but I'll also need to know the make and model, for the online form?\nCustomer: Yes, it's a ford focus 2014.",
  "question": "In the customer's last message, does \"2014\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbda1b5f3f3",
  "kind": "yes/no",
  "text": "Customer: Hi, Do you have any specials today?\nAssistant: We do, We have a special on small 2 topping for $12.00\nCustomer: No, I need a larger size.",
  "question": "In the customer's last message, does \"larger\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa06a97c4a0",
  "kind": "yes/no",
  "text": "Assistant: Ok, I'll order a Venti Iced Caffe Latte with Non Fat milk. At the Lyon Village store.\nCustomer: That sounds even better than the Vanilla.  Please put the order in!\nAssistant: Ok, I have placed the order and you'll have a Venti Iced Caffe Latte with Non Fat milk waiting for you at the Lyon Village store in 10 minutes.",
  "question": "According to the assistant's last message, is \"Iced Caffe Latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q51cebc2d4a",
  "kind": "yes/no",
  "text": "Assistant: They want your name and phone number now, so they know who to expect\nCustomer: Johanna Douglass 555-981-3549\nAssistant: Okay, it's set up, but they said if you don't get there by 5:30 no shuttle service",
  "question": "According to the assistant's last message, is \"5:30\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q970d837531",
  "kind": "yes/no",
  "text": "Customer: Anchor Bar or Buffalo chop house\nAssistant: In what city are those?\nCustomer: Buffalo, Ny.. can you tell me more about them?",
  "question": "In the customer's last message, does \"Buffalo, Ny\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q178228156c",
  "kind": "yes/no",
  "text": "Customer: I am currently at a restaurant on the north side of town and I need to get to the mall on the east side.\nAssistant: Ok what is the name of the restaurant\nCustomer: It is o malleys irish pub",
  "question": "In the customer's last message, does \"o malleys irish pub\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
