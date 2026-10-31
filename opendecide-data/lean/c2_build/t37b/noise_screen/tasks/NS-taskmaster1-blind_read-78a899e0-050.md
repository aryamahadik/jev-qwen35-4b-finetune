# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-050 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-050.json

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
  "qid": "qe5d233cddb",
  "kind": "yes/no",
  "text": "Assistant: Okay, your total will be $15.34.\nCustomer: Okay sounds good.\nAssistant: Your estimated travel time will be 13 mins. Your ride is on it's way and you can check the status of your ride on your phone.",
  "question": "According to the assistant's last message, is \"13 mins\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2cbe6b1700",
  "kind": "yes/no",
  "text": "Assistant: Yes, but it was the only shop that had an available appointment for today.\nCustomer: Well, I guess I don't have a choice.\nAssistant: I will send you a text with the details of the appointment, but just to review - the appointment is for today at 5pm. The cost of the service is $90, but that price could go up if repairs have to be made.",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc6809fb71c",
  "kind": "yes/no",
  "text": "Assistant: Okay, sounds great. What name did you want me to put the reservation under?\nCustomer: Put it under Bryan M. please.\nAssistant: Okay I have you down for 6:30pm. See ya then. Thanks!",
  "question": "According to the assistant's last message, is \"6:30pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd211b27fb4",
  "kind": "yes/no",
  "text": "Assistant: Will do.\nCustomer: Thank you.\nAssistant: Bad news. They don't have any bacon.",
  "question": "According to the assistant's last message, is \"bacon\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb2ea9a17f8",
  "kind": "yes/no",
  "text": "Customer: Thank you very much.\nAssistant: Well, they now are saying that they can't get you in until 9:00pm.  Would you like me to reserve that time or call somewhere else?\nCustomer: Oh goodness. What a pain. Let's skip The Chophouse and try Ruth Chris for the original 7pm.",
  "question": "In the customer's last message, does \"7pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc5de60428d",
  "kind": "yes/no",
  "text": "Customer: Hi, Its been a long morning and I need you to order me a coffee from Starbucks.\nAssistant: I will get right on it..what do you have in mind?\nCustomer: I'm thinking a Iced caffe mocha",
  "question": "In the customer's last message, does \"Iced caffe mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q52494440d8",
  "kind": "yes/no",
  "text": "Customer: Yes\nAssistant: And at what time you would want to be picked up?\nCustomer: At 8.30pm tonite",
  "question": "In the customer's last message, does \"8.30pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf385c47d87",
  "kind": "yes/no",
  "text": "Assistant: I'll check with them on that.\nCustomer: Thanks\nAssistant: They said that they do not have any 6:30PM reservations but have a 7:00PM reservation is that okay?",
  "question": "According to the assistant's last message, is \"6:30PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2242433bb7",
  "kind": "yes/no",
  "text": "Assistant: Morning it is. They have a 7:30 appointment.\nCustomer: Great.\nAssistant: Ok. Your appointment has been booked. For your 2001 F250 at 7:30am tomorrow. The initial inspection fee is $50.",
  "question": "According to the assistant's last message, is \"7:30am\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd29bff3b59",
  "kind": "yes/no",
  "text": "Customer: Hi, I need you to book an appointment for me at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6778bef895",
  "kind": "yes/no",
  "text": "Assistant: 7:30 PM is not available on Thursday. Is 8:30 PM possible?\nCustomer: Yes that works fine. Can you please make the reservation.\nAssistant: I have reserved your table for 2 at Hall's Chophouse at 8:30 PM on Thursday. Thanks.",
  "question": "According to the assistant's last message, is \"Hall's Chophouse\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9dd1392501",
  "kind": "yes/no",
  "text": "Customer: It's going to the Miami Airport.\nAssistant: I remember now. Okay, picking up from the hotel you at I'm guessing?\nCustomer: Yep, I'm staying at the Delano Beach Club.",
  "question": "In the customer's last message, does \"the Delano Beach Club\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9e5361978b",
  "kind": "yes/no",
  "text": "Customer: I'll go with Mountain Mike's in Ukiah.\nAssistant: What size?\nCustomer: Mountain size, the largest.",
  "question": "In the customer's last message, does \"Mountain size\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1a52607b47",
  "kind": "yes/no",
  "text": "Customer: An iced latte with almond milk and vanilla syrup.\nAssistant: What size would you like?\nCustomer: A venti.",
  "question": "In the customer's last message, does \"venti\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q28e21d1e50",
  "kind": "yes/no",
  "text": "Assistant: Superb! Can I book UberX for you?\nCustomer: That's great with me.\nAssistant: Excellent. I have UberX at $32.70 confirmed.",
  "question": "According to the assistant's last message, is \"$32.70\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2ea33c6f86",
  "kind": "yes/no",
  "text": "Assistant: I also need your contact information - name and phone number.\nCustomer: Jack Smith - 978-555-1212\nAssistant: OK. You're all set for tomorrow at 700 AM. The oil change will be 69.99 and the tire check will be 19.99.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6bb1a88c10",
  "kind": "yes/no",
  "text": "Customer: awww bummer. can you try to get the 9:20 showing at picture show instead?\nAssistant: Let me check. Bad news, that showing is also sold out. can I interest you in another film?\nCustomer: how about, instead of wonder park, you find me tickets for Captain marvel after 8pm today",
  "question": "In the customer's last message, does \"Captain marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6c071b7a10",
  "kind": "yes/no",
  "text": "Customer: Tonight\nAssistant: Ok, which theater?\nCustomer: The Regal in Warrington",
  "question": "In the customer's last message, does \"Warrington\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q57d5bea5d5",
  "kind": "yes/no",
  "text": "Customer: 45 Liberty is my address and I want to go to the Safeway.",
  "question": "In the customer's last message, does \"Safeway\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1c7a18473f",
  "kind": "yes/no",
  "text": "Customer: Las Vegas.\nAssistant: great, let me send your order to that location, one moment.\nAssistant: i have ordered you a venti cherry mocha with 2%, a venti caramel macchiato with 2%, and a caramel brulee latte with 2% to be picked up on rainbow street in las vegas.",
  "question": "According to the assistant's last message, is \"2\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q780c1d424a",
  "kind": "yes/no",
  "text": "Customer: I want to build my own.\nAssistant: The crust type?\nCustomer: That garlic-rolled crust looks good.",
  "question": "In the customer's last message, does \"garlic-rolled crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q88d353454e",
  "kind": "yes/no",
  "text": "Customer: Hi, what are good retauranuts that serve seafood in orlando",
  "question": "In the customer's last message, does \"orlando\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q40409b8bea",
  "kind": "yes/no",
  "text": "Customer: Hello, I would like to order a pizza for carry-out.\nAssistant: What kind of pizza do you want to order?\nCustomer: I would like a large pizza with peppers, mushrooms and onions.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcd68af0f5a",
  "kind": "yes/no",
  "text": "Customer: Either a Hawaiian or a pepperoni and salami.\nAssistant: What size are you thinking of ordering?\nCustomer: A large.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe90a89e774",
  "kind": "yes/no",
  "text": "Assistant: Ok. What would you like to order?\nCustomer: I need to get a small cheese pizza. Can I also get a large pizza with green olives, mushrooms and sausage?\nAssistant: I'm sorry, green olives are not available from this restaurant.",
  "question": "According to the assistant's last message, is \"green olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q672bff8200",
  "kind": "yes/no",
  "text": "Assistant: The total comes to $10.99.\nCustomer: That is fine.\nAssistant: Ok, your 14 inch hand tossed pizza with white sauce, spinach, tomato, feta will be ready for pickup in 25 minutes. Your receipt is being sent to your phone through text.",
  "question": "According to the assistant's last message, is \"hand tossed\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdaca9cecd4",
  "kind": "yes/no",
  "text": "Customer: Hello, I want you to get me a pizza from Anthony's",
  "question": "In the customer's last message, does \"Anthony's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8e132aceb3",
  "kind": "yes/no",
  "text": "Customer: Book me a reservation at Zelos with the same info.\nAssistant: Let me repeat that back to you. You want a reservation at Zelos for 3 on April 10 at 7 PM. You need handicap seating available.\nCustomer: No, I want it at 6 PM.",
  "question": "In the customer's last message, does \"6 PM\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q56942dea3a",
  "kind": "yes/no",
  "text": "Customer: Willis Tower in Chicago\nAssistant: Where is your destination\nCustomer: John Hancock Center in Chicago",
  "question": "In the customer's last message, does \"John Hancock Center in Chicago\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb284ddf9f7",
  "kind": "yes/no",
  "text": "Assistant: No, the largest size is the large at 14 inches.\nCustomer: Ok, I'd like to order a large pineapple bbq chicken pizza with Asiago cheese.\nAssistant: Pandini's is currently out of Asiago cheese. Would you like to substitute Parmesan or extra mozzarella?",
  "question": "According to the assistant's last message, is \"Asiago cheese\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd8a90d5398",
  "kind": "yes/no",
  "text": "Assistant: ok the table is unavailable that day. i can change the time or would you like a booth?\nCustomer: the booth will be fine i cannot change the time\nAssistant: ok your reservation is made i have it for next Tuesday at 8pm at Morton's steakhouse in downtown sacramento",
  "question": "According to the assistant's last message, is \"Morton's steakhouse\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd17681d006",
  "kind": "yes/no",
  "text": "Assistant: Okay, I will ask for a short delay.\nCustomer: Use my Visa to pay.\nAssistant: Got it. I've ordered the car and confirmed the fee of $34.37.",
  "question": "According to the assistant's last message, is \"$34.37\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q731c11d0f1",
  "kind": "yes/no",
  "text": "Customer: That sounds Good what is the latest time and do they have in in 3D?\nAssistant: They have it at 10 in 3D Imax or 11 with just 3D.\nCustomer: Lets do two tickets for 3D Imax at 11 then",
  "question": "In the customer's last message, does \"11\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9ce299821a",
  "kind": "yes/no",
  "text": "Customer: Can you make a reservation at Micheal Jordan's at 9 o clock\nAssistant: Checking, Micheal Jordan's does not have any opening tonight.\nCustomer: Can you make a reservation at Ruth Chris at 9 o clock",
  "question": "In the customer's last message, does \"9 o clock\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5b92b15118",
  "kind": "yes/no",
  "text": "Assistant: okay I will have the coffee delivered to you in fifteen minutes\nCustomer: thank you\nAssistant: sorry boss, they ran out of soy milk",
  "question": "According to the assistant's last message, is \"soy milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qebb946622c",
  "kind": "yes/no",
  "text": "Customer: Yes, I would like to have pepperoni instead of ham for the Maria pizza.\nAssistant: Ok. What size do you want to pizza's to be?\nCustomer: I would like the Maria to be 14 inches and the Susana to be 10 inches.",
  "question": "In the customer's last message, does \"10 inches\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfb54b1acc6",
  "kind": "yes/no",
  "text": "Assistant: What sort of pizza would you like me to order?\nCustomer: I've got friends over so I need a X-Large, maybe a pepperoni?\nAssistant: Okay, they don't have pepperoni.",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc816694636",
  "kind": "yes/no",
  "text": "Assistant: Do you want to be picked up now or is this for later?\nCustomer: I want to schedule it for 6:30 tonight.\nAssistant: Unfortunately, Uber Black is not currently available. Do you have another choice?",
  "question": "According to the assistant's last message, is \"Uber Black\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf7aebb0aab",
  "kind": "yes/no",
  "text": "Customer: Hello. Can you please call me a Lyft Lux please?\nAssistant: I can do that for you. Where are you now?\nCustomer: I'm at the Olive Garden in Orlando on International Drive",
  "question": "In the customer's last message, does \"Olive Garden in Orlando on International Drive\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b20b05769",
  "kind": "yes/no",
  "text": "Customer: Intelligent Auto Solutions please\nAssistant: Let me look up how to book it\nCustomer: Its urgent for my 2018 Toyota Carolla",
  "question": "In the customer's last message, does \"Toyota Carolla\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa8665dd875",
  "kind": "yes/no",
  "text": "Customer: I want tickets to see Dumbo\nAssistant: Okay and where would you like to see this movie?\nCustomer: In dallas at cinemark 17 IMAX",
  "question": "In the customer's last message, does \"dallas\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfbe3e696ef",
  "kind": "yes/no",
  "text": "Customer: Perfect I'll head there now.\nAssistant: Okay but they need more information first, what is the make and model?\nCustomer: It is a Ram 1500 SLV",
  "question": "In the customer's last message, does \"Ram 1500 SLV\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf2fa7d8c3c",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza from Marco's\nAssistant: Ok, what city and state are you ordering from?\nCustomer: Alliance, Ohio",
  "question": "In the customer's last message, does \"Alliance, Ohio\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb2fa802f08",
  "kind": "yes/no",
  "text": "Customer: I'd like to bring it in tomorrow sometime after 12 noon.\nAssistant: Sure. I can book that for you. One moment please. What is your name and phone number?\nCustomer: My name is Suzy Q and my phone number is 555 555-5555",
  "question": "In the customer's last message, does \"Suzy Q\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q307416ba55",
  "kind": "yes/no",
  "text": "Customer: Hello, can you run by Starbucks and pick up a coffee for me?\nAssistant: Sure thing, your usual?\nCustomer: Yes, the Cafe Latte",
  "question": "In the customer's last message, does \"Cafe Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3e3f96a67b",
  "kind": "yes/no",
  "text": "Customer: I want to order a pizza from Pizza Hut\nAssistant: Okay. Where are you located today?\nCustomer: Sacamento, California",
  "question": "In the customer's last message, does \"Sacamento, California\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q052fb004c1",
  "kind": "yes/no",
  "text": "Customer: Ok thank you\nAssistant: They don't have that either.\nCustomer: Ok how about at Beverly's",
  "question": "In the customer's last message, does \"Beverly's\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7ae5506128",
  "kind": "yes/no",
  "text": "Customer: Party size please!\nAssistant: Great, and what kind of dough? Options are hand tossed or pan pizza.\nCustomer: Pan Pizza please.",
  "question": "In the customer's last message, does \"Pan Pizza\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69fb182d76",
  "kind": "yes/no",
  "text": "Assistant: i will look up times for you\nCustomer: okay let me know now!\nAssistant: unfortunately 2:30 is fully booked, what other times?",
  "question": "According to the assistant's last message, is \"2:30\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q55abd8aad7",
  "kind": "yes/no",
  "text": "Customer: No, but I'm thinking of having Japanese\nAssistant: Which area are you thinking about\nCustomer: Anywhere near midtown in Manhattan",
  "question": "In the customer's last message, does \"near midtown in Manhattan\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
