# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-034 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-034.json

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
  "qid": "qa98811576b",
  "kind": "yes/no",
  "text": "Assistant: Well tell her happy birthday!\nCustomer: Thank you.\nAssistant: Ok, we have you all set for your birthday dinner for 2 inside at 8:30 Saturday night.",
  "question": "According to the assistant's last message, is \"inside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb794d64452",
  "kind": "yes/no",
  "text": "Assistant: Left tail light out, got it.\nCustomer: So I bring it in tomorrow morning?\nAssistant: You cannot bring it in tomorrow morning, but Thursday morning is open.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd39b41a2c2",
  "kind": "yes/no",
  "text": "Assistant: OK, I am ready to place the order. The total will be $13. Should we bill this to your credit card on file?\nCustomer: Yes. When will the pizza be ready?\nAssistant: Your order of a large pizza with with pepperoni, mushrooms, black olives, green peppers, and extra cheese will be ready in 25 minutes. A receipt will be sent to your mobile phone via a text message.",
  "question": "According to the assistant's last message, is \"green peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q33cba794d9",
  "kind": "yes/no",
  "text": "Customer: Great, please go ahead and order a large Pepperoni pizza for me.\nAssistant: No problem. They confirmed your order of a large Pepperoni pizza.\nCustomer: Excellent. Please pay them from my account with Pizza Hut.",
  "question": "In the customer's last message, does \"Pizza Hut\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4fc40fddc4",
  "kind": "yes/no",
  "text": "Customer: Yes, ASAP please haha.\nAssistant: Gotcha, what do you want and from where?\nCustomer: Starbucks' new Iced CInnamon Shortbread Latte looks sooo delicious.",
  "question": "In the customer's last message, does \"Iced CInnamon Shortbread Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qda4b99264c",
  "kind": "yes/no",
  "text": "Customer: OK Google, please schedule an appointment with Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q275bfd713b",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry, but there are no reservations available at Samurai tonight at the Teppan tables. Would you like me to try for a different seating location?\nCustomer: Oh, fine. Reserve a regular table, then.\nAssistant: Unfortunately, Samurai is fully booked tonight, so I cannot make a reservation for tonight.",
  "question": "According to the assistant's last message, is \"Samurai\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q58f9e4ebbf",
  "kind": "yes/no",
  "text": "Customer: A Vanilla Sweet Cream Cold Brew\nAssistant: What size would you like?\nCustomer: A venti please",
  "question": "In the customer's last message, does \"venti\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q19071387ff",
  "kind": "yes/no",
  "text": "Assistant: So you want to get it serviced today, you cant wait until tomorrow?\nCustomer: No, I am not available tomorrow, must be today.\nAssistant: Ok, so I have scheduled an emergency appointment for tomorrow at 1230.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q52d773a3b1",
  "kind": "yes/no",
  "text": "Assistant: Okay, I'll go ahead and order that for you, I'll let you know when it can be picked up\nCustomer: Okay, thank you\nAssistant: They are all out of traditional crust at this location for the size you were wanting to get, do you want me to order from another location?",
  "question": "According to the assistant's last message, is \"traditional crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qeb2edc60b6",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, that drink is unavailable.\nCustomer: Okay, then I went a grande Caffe Latte with almond milk.\nAssistant: There is no almond milk available.",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb4c0dcf1b5",
  "kind": "yes/no",
  "text": "Assistant: Mohawk Bend offers craft beers, an American Menu with Vegan and Vegetarian selections\nCustomer: Please make a reservation for table of 10 Saturday March 9th at 9pm\nAssistant: 9pm is not not available the available times are 8 and 10 pm",
  "question": "According to the assistant's last message, is \"9pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd8c9c4e031",
  "kind": "yes/no",
  "text": "Customer: i want it scheduled at the auto repair shop called the \"Intelligent Auto Solutions\".\nAssistant: Ok, no problem. Which car are we talking about?\nCustomer: My 2018 Dodge Charger",
  "question": "In the customer's last message, does \"Dodge Charger\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5c2479832f",
  "kind": "yes/no",
  "text": "Assistant: I can book that would you like to finalize it now\nCustomer: Yes please do that we can always have a few cocktails at the bar.\nAssistant: All booked 9pm Saturday at the dock with a water side table for 4.",
  "question": "According to the assistant's last message, is \"water side table\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfdca8bff05",
  "kind": "yes/no",
  "text": "Assistant: You're welcome. Give me second.\nCustomer: Sure.\nAssistant: Ok, your drink has been ordered from the Starbucks on Hasler Blvd. It will be ready shortly and your receipt will come to your mobile phone via text.",
  "question": "According to the assistant's last message, is \"Hasler Blvd\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdd8e18dfc3",
  "kind": "yes/no",
  "text": "Customer: Is there a showtime earlier than 8:45 pm?\nAssistant: 5:55 pm.\nCustomer: Oh... That too early... Okay I'll take the 8:45 pm showing. How much are tickets at Regal Union Square?",
  "question": "In the customer's last message, does \"8:45 pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qadae70dd75",
  "kind": "yes/no",
  "text": "Assistant: yes\nCustomer: I want a pizza with extra cheese and black olives\nAssistant: We are all out of black olives",
  "question": "According to the assistant's last message, is \"black olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2aed2cff9b",
  "kind": "yes/no",
  "text": "Assistant: Sounds good\nCustomer: it is\nAssistant: oh, wait, they are out of pineapple, do you want something else?",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb44a00b323",
  "kind": "yes/no",
  "text": "Assistant: I am sorry, but the only theater showing Captain Marvel that is within ten miles is sold out for tonight.\nCustomer: How about expanding to 20 miles?\nAssistant: I am sorry, but no Captain Marvel tickets are available within 20 miles.",
  "question": "According to the assistant's last message, is \"Captain Marvel\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q362a8f5e74",
  "kind": "yes/no",
  "text": "Customer: Hi Rachel, are you busy? I could use some Starbucks coffee right about now\nAssistant: Sounds great! What can I order you?\nCustomer: I'm gonna try a White Chocolate Mocha like the one you had yesterday",
  "question": "In the customer's last message, does \"White Chocolate Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qffb61cbc41",
  "kind": "yes/no",
  "text": "Customer: Yep.\nAssistant: And what can I get you today?\nCustomer: A grande iced skinny mocha.",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q08590263cb",
  "kind": "yes/no",
  "text": "Assistant: Great, and I’m seeing you are only 12 minutes away from your destination is this correct?\nCustomer: Yes correct\nAssistant: Okay, So that is going to put you around $8-10 for this trip. Let me get you set up with a driver!!!",
  "question": "According to the assistant's last message, is \"$8-10\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9f87543f9b",
  "kind": "yes/no",
  "text": "Customer: Hi Kim\nAssistant: Hello\nCustomer: Can you please book a reservation at Pasta Too for two on Saturday, July 4th?",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc0bc53f081",
  "kind": "yes/no",
  "text": "Customer: Reno\nAssistant: Which theatre?\nCustomer: Century Summit Sierra",
  "question": "In the customer's last message, does \"Century Summit Sierra\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5cb7bc60e6",
  "kind": "yes/no",
  "text": "Customer: Great, I want to make a reservation at Sky Sushi.\nAssistant: Okay, give me the details.\nCustomer: Its for 6 people, tomorrow at 8 pm and outside seating.",
  "question": "In the customer's last message, does \"8 pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q277ae89d54",
  "kind": "yes/no",
  "text": "Assistant: Alright, I'll reserve your tickets.\nCustomer: Thank you!\nAssistant: Unfortunately there are no showing left at that time at the Kalli 12.",
  "question": "According to the assistant's last message, is \"Kalli 12\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q494b756e39",
  "kind": "yes/no",
  "text": "Assistant: Sure here you go.\nCustomer: Thanks.\nAssistant: Your Mad Dog will be ready for pickup in about 25 minutes.",
  "question": "According to the assistant's last message, is \"Mad Dog\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2af125bb9a",
  "kind": "yes/no",
  "text": "Customer: What's the problem?\nAssistant: They cannot seat that many at 7.\nCustomer: Ok, what about 8?",
  "question": "In the customer's last message, does \"8\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5e402f29ed",
  "kind": "yes/no",
  "text": "Customer: Two please, I am taking a friend.\nAssistant: Any special requests?\nCustomer: No, just the regular showing at 3:50pm",
  "question": "In the customer's last message, does \"3:50pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qaae9a75cb9",
  "kind": "yes/no",
  "text": "Assistant: Ok the fee for the inspection is $90. Are you ok with that?\nCustomer: Yes that is fine\nAssistant: Ok I have booked an appointment for you bob at 9:15 am, gave Intelligent Auto Solutions your phone number 384-958-9049, and the cost will be $90.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q85ac1dcef0",
  "kind": "yes/no",
  "text": "Assistant: I forgot to ask the size.\nCustomer: A large, please.\nAssistant: Okay. I ordered a large gluten free crust pepperoni pizza with half black olives, half mushrooms from Brunos on Main. It will be ready for pickup in 25 minutes.",
  "question": "According to the assistant's last message, is \"pepperoni pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1c8883bac5",
  "kind": "yes/no",
  "text": "Customer: Diedre, I need you to book an appointment at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa31dcd6f59",
  "kind": "yes/no",
  "text": "Customer: 3 people on January 24.\nAssistant: Okay, at what time?\nCustomer: 6 pm.",
  "question": "In the customer's last message, does \"6 pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc4d644de94",
  "kind": "yes/no",
  "text": "Customer: Yup, that's correct.\nAssistant: Could you provide me with a name and number to give them?\nCustomer: Sure: Jenny Peters (555) 555-5555",
  "question": "In the customer's last message, does \"Jenny Peters\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q59b6f30df9",
  "kind": "yes/no",
  "text": "Customer: I would like to buy tickets for the movie Us.",
  "question": "In the customer's last message, does \"Us\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb11ead2bca",
  "kind": "yes/no",
  "text": "Assistant: Okay. One moment while I book that for you.\nCustomer: okay, thanks.\nAssistant: No problem, your ride has been booked for 3pm for 4 people.",
  "question": "According to the assistant's last message, is \"3pm\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3ec65087fb",
  "kind": "yes/no",
  "text": "Assistant: yeah i can understand\nCustomer: yeah especially in the cold like this\nAssistant: ok so i made the appointment with Intelligent Auto Solutions at 7am tomorrow for your drop off time, i gave them your business cell of 555-555-1234 and its booked and ready for you to go",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9aa340564f",
  "kind": "yes/no",
  "text": "Customer: Yes please.\nAssistant: I'm sorry, but 8:00 is not available either. Would you like to try a different time?\nCustomer: No that's okay. Let's try Joe's on State and Grand.",
  "question": "In the customer's last message, does \"Joe's\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa31af06362",
  "kind": "yes/no",
  "text": "Customer: I need to book an appointment with Intelligent Auto Solutions.\nAssistant: What name will that be under?\nCustomer: Tom Hanks",
  "question": "In the customer's last message, does \"Tom Hanks\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbd3f7016cb",
  "kind": "yes/no",
  "text": "Customer: No\nAssistant: Okay, I tried to order your Cinnamon Shortbread Latte but they are out of shortbread syrup. Would you like me to order a different drink?\nCustomer: Yes. Can I get a Cinnamon Dolce Latte instead?",
  "question": "In the customer's last message, does \"Cinnamon Dolce Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcf294bc980",
  "kind": "yes/no",
  "text": "Customer: My air conditioning is not working\nAssistant: What make and model is your car?\nCustomer: 2015 Ford Focus",
  "question": "In the customer's last message, does \"Ford Focus\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd62b3df912",
  "kind": "yes/no",
  "text": "Assistant: Alright, what toppings would you like\nCustomer: Pepperoni and chicken.\nAssistant: They no longer have chicken; i guess it was a limited time only thing.",
  "question": "According to the assistant's last message, is \"chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4962d20b99",
  "kind": "yes/no",
  "text": "Customer: I would like the Chicago deep crust.\nAssistant: I am sorry. That crust is unavailable at this time. Is there another type of crust that you would find acceptable?\nCustomer: Yes. I would like the deep crust.",
  "question": "In the customer's last message, does \"deep crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc19fd91c57",
  "kind": "yes/no",
  "text": "Assistant: Ok let me try to place the order for you\nCustomer: Ok thanks\nAssistant: I tried to place the order but they not longer carry the meat lovers specialty pizza. Would you like a different speciality pizza?",
  "question": "According to the assistant's last message, is \"meat lovers specialty pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfd1a0e79dc",
  "kind": "yes/no",
  "text": "Customer: Thank you. I'd like it done as soon as possible.\nAssistant: No problem. Let me get some basic info from you. What is the Make and Model of your car?\nCustomer: It's a Jeep Liberty",
  "question": "In the customer's last message, does \"Jeep Liberty\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfc60fa946b",
  "kind": "yes/no",
  "text": "Assistant: Okay, which restaurant?\nCustomer: Drunken Monkey please at 8PM tonight for 4 people.\nAssistant: I'm sorry they are not available tonight for 4 people at 8PM.",
  "question": "According to the assistant's last message, is \"8PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1158f20407",
  "kind": "yes/no",
  "text": "Customer: I'd like you to help me get tickets to see Creed 2.\nAssistant: Where would you like to see it?\nCustomer: I'd like to see it at the theater in Toms River.",
  "question": "In the customer's last message, does \"Toms River\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qebe15793ec",
  "kind": "yes/no",
  "text": "Assistant: Ok. No problem.\nCustomer: Thanks.\nAssistant: Bad news. They don't have any chicken. Anything else you want?",
  "question": "According to the assistant's last message, is \"chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qff920bcdaa",
  "kind": "yes/no",
  "text": "Customer: Hey Janice, me and an old friend are thinking of seeing Aquaman tonight.",
  "question": "In the customer's last message, does \"me and an old friend\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q48cb88f391",
  "kind": "yes/no",
  "text": "Assistant: What additional items would you like to add?\nCustomer: I would like to add some whipped cream.\nAssistant: Great, let me check. Sorry whipped cream is not available.",
  "question": "According to the assistant's last message, is \"whipped cream\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
