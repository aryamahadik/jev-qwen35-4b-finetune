# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-021 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-021.json

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
  "qid": "q1ae8737f0a",
  "kind": "yes/no",
  "text": "Customer: What is the closest movie theatre that's playing The Lego Movie part 2?",
  "question": "In the customer's last message, does \"The Lego Movie part 2\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q83294c3b85",
  "kind": "yes/no",
  "text": "Customer: I would like to be picked up from the Atlanta airport and driven to the Atlanta zoo.\nAssistant: When do you want to be picked up?\nCustomer: Today at 2:00 pm.",
  "question": "In the customer's last message, does \"2:00 pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6534206512",
  "kind": "yes/no",
  "text": "Assistant: Ok - let me set it up. Hold on.\nCustomer: Make sure to text me the confirmation numbers.\nAssistant: OK - I texted you the info. Please confirm you got it. I have Gricos scheduled for 8:25 and a table for 4.",
  "question": "According to the assistant's last message, is \"Gricos\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6a3bdd5a82",
  "kind": "yes/no",
  "text": "Assistant: Ok great. Anything else?\nCustomer: Yes, we'll need a highchair too.\nAssistant: Ok got it. It looks like 5:00 pm is not available. Is there another time you would like to try?",
  "question": "According to the assistant's last message, is \"5:00 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4c3ed4244d",
  "kind": "yes/no",
  "text": "Customer: Hmm, alright then which movies have a food delivery option?\nAssistant: Both the Cinemark and the AMC have food delivery options.\nCustomer: I think I will go with the AMC option.",
  "question": "In the customer's last message, does \"AMC\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe5810fff8f",
  "kind": "yes/no",
  "text": "Assistant: what seems to be the issue you are having?\nCustomer: My car is stuttering when I accel\nAssistant: thats fine, I can get an appointment set up for you with Intelligent Auto Solutions",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q814ad9459f",
  "kind": "yes/no",
  "text": "Customer: Hey Sean, It's Marcus. Can you get me an appointment at Intelligent Auto Solutions?",
  "question": "In the customer's last message, does \"Marcus\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf2009f9d5d",
  "kind": "yes/no",
  "text": "Customer: The Brighton one, please.\nAssistant: Okay. What would you like?\nCustomer: Can I have a tall cafe mocha with whole milk, please?",
  "question": "In the customer's last message, does \"cafe mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q60fef69da6",
  "kind": "yes/no",
  "text": "Customer: Arlington, VA\nAssistant: Do you know what theater it is playing at?\nCustomer: I want to go to the AMC in Courthouse plaza.",
  "question": "In the customer's last message, does \"AMC in Courthouse plaza\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q62d58d7b50",
  "kind": "yes/no",
  "text": "Customer: Yup, that's correct.\nAssistant: Could you provide me with a name and number to give them?\nCustomer: Sure: Jenny Peters (555) 555-5555",
  "question": "In the customer's last message, does \"Jenny Peters\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0a156c71cd",
  "kind": "yes/no",
  "text": "Assistant: What are you ordering today?\nCustomer: I'd like a Hawaiian style gigante pizza.\nAssistant: At the moment, you are unable to order Hawaiian specialty pizzas.",
  "question": "According to the assistant's last message, is \"Hawaiian specialty pizzas\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qec36011300",
  "kind": "yes/no",
  "text": "Assistant: 8:00pm.\nCustomer: Wow. Is outdoor seating available at 12:00pm\nAssistant: Im sorry, outdoor seating is unavailable at 12:00pm",
  "question": "According to the assistant's last message, is \"outdoor seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q829d66bb29",
  "kind": "yes/no",
  "text": "Customer: I would like to order a Lyft ride.\nAssistant: Where do you want to go from and to?\nCustomer: I need to get from Union Square to Astor Place A.S.A.P.",
  "question": "In the customer's last message, does \"Union Square\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1509cbeb8f",
  "kind": "yes/no",
  "text": "Assistant: Okay, can I get a name and phone number to contact you at?\nCustomer: Dany Turk, 555-555-5555\nAssistant: Got it, I've booked that in under Dany Turk and they will contact you at 555-555-5555 when the vehicle is ready",
  "question": "According to the assistant's last message, is \"Dany Turk\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q95e14715d3",
  "kind": "yes/no",
  "text": "Customer: I'm not sure, something vegetarian. What do you think?\nAssistant: I love mushrooms, so i always do that and tomatoes.\nCustomer: That sounds good. Get a large please.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69d1897788",
  "kind": "yes/no",
  "text": "Customer: I like to see a movie Aquaman can you please book a ticket for me?\nAssistant: Sure Sir. where can i book your tickets?\nCustomer: Book my tickets in the Stuart Cinema",
  "question": "In the customer's last message, does \"Stuart Cinema\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe71b9840eb",
  "kind": "yes/no",
  "text": "Customer: I want a ride through Lyft.\nAssistant: Okay, Lyft. Got it. What time?\nCustomer: 8pm tonight, as close as possible.",
  "question": "In the customer's last message, does \"8pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q81f771ea39",
  "kind": "yes/no",
  "text": "Customer: Okay, great thanks!\nAssistant: Here is your coffee and extra creamer.\nCustomer: Yummy, I'm so excited. I love Iced White Chocolate Mocha.",
  "question": "In the customer's last message, does \"Iced White Chocolate Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa5414f10c0",
  "kind": "yes/no",
  "text": "Assistant: O.k. I've passed this information along to Intelligent Auto.\nCustomer: Would you please also let them know to reserve this appointment under my name - Jane Doe - and phone (310) 326-2019.\nAssistant: O.k. Your appoinment for your 2011 Toyota Camry is confirmed for Saturday, March 30, at 8 a.m. for an oil change.",
  "question": "According to the assistant's last message, is \"Saturday, March 30\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q236b2c094a",
  "kind": "yes/no",
  "text": "Assistant: What type of car would you like?\nCustomer: UberX\nAssistant: An UberX is not currently available. Would you like a different type?",
  "question": "According to the assistant's last message, is \"UberX\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf7ec4011db",
  "kind": "yes/no",
  "text": "Assistant: Let me put the order in for you sir.\nCustomer: Thank you Alice.\nAssistant: Okay, the grande cherry mocha espresso with 2 percent milk and whipped cream will be ready for pickup shortly at the Starbucks on Capital Blvd in Raleigh, Robert.",
  "question": "According to the assistant's last message, is \"2 percent milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q76bc626d64",
  "kind": "yes/no",
  "text": "Assistant: You would like to put in the order now, correct?\nCustomer: Yes.\nAssistant: Ok. An order for a tall, iced pumpkin spice chai latte with coconut milk has successfully been placed.",
  "question": "According to the assistant's last message, is \"iced pumpkin spice chai latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3ad76cf028",
  "kind": "yes/no",
  "text": "Customer: Tonight\nAssistant: Ok, which theater?\nCustomer: The Regal in Warrington",
  "question": "In the customer's last message, does \"Warrington\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9814ac7f57",
  "kind": "yes/no",
  "text": "Customer: That's great\nAssistant: What's your name?\nCustomer: Jim Roberts",
  "question": "In the customer's last message, does \"Jim Roberts\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0d1a667cb3",
  "kind": "yes/no",
  "text": "Assistant: Okay, there is a table available at that time for 6 people.\nCustomer: I suppose that is okay, what about seating near the bar?\nAssistant: There is not actual bar at Nubuo.",
  "question": "According to the assistant's last message, is \"Nubuo\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2b9f738cb9",
  "kind": "yes/no",
  "text": "Assistant: To confirm, the issue is with your drive shaft?\nCustomer: That's what I suspect, yes.\nAssistant: OK. To confirm, your appointment is at 10 a.m. Thursday at the Autobahn.",
  "question": "According to the assistant's last message, is \"Thursday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3356957dbb",
  "kind": "yes/no",
  "text": "Assistant: What type of milk would you like?\nCustomer: Almond milk.\nAssistant: Im sorry, almond milk is unavailable.",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd222d01caa",
  "kind": "yes/no",
  "text": "Assistant: What is the destination location?\nCustomer: Long Island MacArthur Airport.\nAssistant: I don't see an Uber Black available.",
  "question": "According to the assistant's last message, is \"Uber Black\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfccc8c91a2",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, there is nothing available for 6:30 pm\nCustomer: Ok, how about 8:00 pm?\nAssistant: There is a showing for 8:00 pm, but it's in 35mm, not 3D",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2fd1e37f4c",
  "kind": "yes/no",
  "text": "Assistant: That's how much they charge for AC repair.\nCustomer: OK, then that sounds ok to me.\nAssistant: Great, you are all set to drop off at 5 pm this afternoon at Intelligent Auto Solutions for a $1200 AC service repair.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q33c3a75dfc",
  "kind": "yes/no",
  "text": "Assistant: There is one appointment available at 6 pm today.\nCustomer: Yes, I'll take it.\nAssistant: Ok, you have an appointment booked for 6 pm today with Intelligent Auto Solutions.",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q75b656b157",
  "kind": "yes/no",
  "text": "Customer: I would like to order pizza from Villa monte\nAssistant: From which location are you ordering from?\nCustomer: The Arden avenue one",
  "question": "In the customer's last message, does \"The Arden avenue\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa25b26bac6",
  "kind": "yes/no",
  "text": "Customer: Hi. I am interested in tickets for \"Pet Semetary'",
  "question": "In the customer's last message, does \"Pet Semetary\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q051ad94222",
  "kind": "yes/no",
  "text": "Customer: Ok, that makes sense. I'll have a regular farmville pizza than\nAssistant: would you like the 12 inch, 18 inch, or 21 inch?\nCustomer: I'll get the 18 inch",
  "question": "In the customer's last message, does \"18 inch\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q591f10a403",
  "kind": "yes/no",
  "text": "Assistant: Ok, no problem. Could you hold for one moment while I check availability?\nCustomer: Sure.\nAssistant: I apologize for the wait, but Country Hill does not have availability for 4 people at 7pm. Is there another time that would work for you?",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbb9d15a8b5",
  "kind": "yes/no",
  "text": "Customer: sounds ood\nAssistant: which movie?\nCustomer: I'd like to see captain marvel",
  "question": "In the customer's last message, does \"captain marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2c50414ad6",
  "kind": "yes/no",
  "text": "Customer: I need to order a pizza for pick up at Papa johns\nAssistant: Which location do you need it ordered from?\nCustomer: The one on Horizon ridge in Henderson",
  "question": "In the customer's last message, does \"Horizon ridge in Henderson\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0ca8502d12",
  "kind": "yes/no",
  "text": "Customer: I want to take it to Intelligent Auto Solutions. I don't need a tow.\nAssistant: I will need to know the details about the car and the time.\nCustomer: It is a 2010 Ford Ranger. There is a loud banging noise coming from the engine when I accelerate.",
  "question": "In the customer's last message, does \"2010\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qab011454da",
  "kind": "yes/no",
  "text": "Assistant: Can you please provide your last name?\nCustomer: Smith.\nAssistant: To confirm, your reservation will be booked under the name \"Mary Smith\".",
  "question": "According to the assistant's last message, is \"Mary Smith\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qebaa964bd4",
  "kind": "yes/no",
  "text": "Assistant: i sure can, is there anything else that i can order for you?\nCustomer: no i think thats it\nAssistant: ok great i have your nonfat caramel frapp with extra whip extra caramel ordered at the dewey and madison starbucks",
  "question": "According to the assistant's last message, is \"caramel frapp\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q70e41b5d09",
  "kind": "yes/no",
  "text": "Customer: I need to order 2 large pizzas from Pizza Hut",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8aee569909",
  "kind": "yes/no",
  "text": "Assistant: would you like whipped cream\nCustomer: hell yeah\nAssistant: sorry they do not have hemp milk",
  "question": "According to the assistant's last message, is \"hemp milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8550bb24b5",
  "kind": "yes/no",
  "text": "Customer: Could you book a table for me?\nAssistant: Of course!\nCustomer: Great. Chilis, Louisville, CO at 7 for 5 people. Outdoors.",
  "question": "In the customer's last message, does \"Chilis\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q71d51392d3",
  "kind": "yes/no",
  "text": "Customer: It's a 1986 VW Jetta.\nAssistant: Thank you. What is your issue with the car\nCustomer: It's making a weird noise whenever I turn",
  "question": "In the customer's last message, does \"It's making a weird noise whenever I turn\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb62f0b375a",
  "kind": "yes/no",
  "text": "Customer: That sounds Good what is the latest time and do they have in in 3D?\nAssistant: They have it at 10 in 3D Imax or 11 with just 3D.\nCustomer: Lets do two tickets for 3D Imax at 11 then",
  "question": "In the customer's last message, does \"11\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8d256a255a",
  "kind": "yes/no",
  "text": "Customer: Hello. I would like assistance making a restaurant reservation.\nAssistant: No problem. Where do you want to make the reservation at?\nCustomer: I want a reservation for the Cheesecake Factory in Walnut Creek, California.",
  "question": "In the customer's last message, does \"Walnut Creek, California\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa766b62b65",
  "kind": "yes/no",
  "text": "Customer: 235 555-1212\nAssistant: And what is the reason for the appointment?\nCustomer: The trunk keeps flying open.",
  "question": "In the customer's last message, does \"The trunk keeps flying open\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3928860617",
  "kind": "yes/no",
  "text": "Customer: Please select 7:00pm showing\nAssistant: How many tickets would you like?\nCustomer: 2 tickets please",
  "question": "In the customer's last message, does \"2 tickets\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q856d1d0f9d",
  "kind": "yes/no",
  "text": "Customer: Yes, I think I might as well get a basic inspection. As long as it covers the spark plugs that works for me.\nAssistant: Very well, can I have your name and phone number?\nCustomer: My name is Chris Smith and my phone number is 555-555-5555.",
  "question": "In the customer's last message, does \"Chris Smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3dfb8eecd6",
  "kind": "yes/no",
  "text": "Customer: Oh I would like a 14 inch then.\nAssistant: What type of crust do you want?\nCustomer: Hand tossed please.",
  "question": "In the customer's last message, does \"Hand tossed\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
