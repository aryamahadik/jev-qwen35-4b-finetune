# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-015 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-015.json

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
  "qid": "q540f5f834e",
  "kind": "yes/no",
  "text": "Customer: i need to order a pick up service.\nAssistant: where do you need picked up and where do you want to go?\nCustomer: I need to be picked up from crossroads mall to kitchen 324.",
  "question": "In the customer's last message, does \"crossroads mall\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1cfa6b8760",
  "kind": "yes/no",
  "text": "Customer: It's for Columbus, Ohio.\nAssistant: Okay. Which movie theater?\nCustomer: Easton Town Center AMC.",
  "question": "In the customer's last message, does \"Easton Town Center AMC\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q308e000e30",
  "kind": "yes/no",
  "text": "Assistant: I can check, but the shop is really busy on most Fridays.\nCustomer: I understand.\nAssistant: I am sorry, there is not an opening for today at 1:00pm, I can check any other time for today that is good for you.",
  "question": "According to the assistant's last message, is \"1:00pm\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3faa021e45",
  "kind": "yes/no",
  "text": "Assistant: I found Tacos A Go Go, Cyclone, and Saint Daine's.\nCustomer: Can you book a table for 4 outside at Tacos A Go Go for 5:30?\nAssistant: Tacos A Go Go does not have outside seating.",
  "question": "According to the assistant's last message, is \"outside seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa333e6e69f",
  "kind": "yes/no",
  "text": "Assistant: What size and crust do you want the pizza?\nCustomer: I want a large pizza with a stuffed crust.\nAssistant: I understood you want a large pizza. There is a problem with the crust. Lobo Pizza does not offer a stuffed crust. The crust choices are thin, tossed, or Chicago style. What is your choice?",
  "question": "According to the assistant's last message, is \"stuffed crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4d03e929b7",
  "kind": "yes/no",
  "text": "Assistant: Okay. I will do that now.\nCustomer: Thanks\nAssistant: Starbucks is out of Almond milk.",
  "question": "According to the assistant's last message, is \"Almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdac334ac05",
  "kind": "yes/no",
  "text": "Customer: Wow. Is outdoor seating available at 12:00pm\nAssistant: Im sorry, outdoor seating is unavailable at 12:00pm\nCustomer: Is there indoor seating available at Ross Grill at 12:00pm for two people?",
  "question": "In the customer's last message, does \"Ross Grill\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q889b199de9",
  "kind": "yes/no",
  "text": "Assistant: Okay, and what kind of pizza would you like?\nCustomer: Pepperoni and mushroom.\nAssistant: Sorry, apparently they're out of mushrooms. Would you like another topping?",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3f00bd726e",
  "kind": "yes/no",
  "text": "Customer: Thanks\nAssistant: Which restaurant?\nCustomer: Rapscallion, also in Reno.",
  "question": "In the customer's last message, does \"Rapscallion\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc2263690aa",
  "kind": "yes/no",
  "text": "Customer: Thank you!\nAssistant: You are welcome. How may I help you with today?\nCustomer: I would like to request an Uber ride from Arden Fair to Pavilions Shopping Center.",
  "question": "In the customer's last message, does \"Arden Fair\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf0e9dd4af2",
  "kind": "yes/no",
  "text": "Assistant: And you want to schedule for 7 pm, correct\nCustomer: Yes\nAssistant: Okay, I booked a booth for 4 at Long Horn Steakhouse tomorrow evening at 4 pm and included a request for a high chair",
  "question": "According to the assistant's last message, is \"tomorrow evening at 4 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6a62662dae",
  "kind": "yes/no",
  "text": "Customer: Can you order me a ride from Uber?\nAssistant: Sure, what locations do you want to be picked up and dropped off?\nCustomer: From 555 S Flower St, Los Angeles, CA to 200 Santa Monica Pier, Santa Monica, CA",
  "question": "In the customer's last message, does \"200 Santa Monica Pier, Santa Monica, CA\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa9695a7461",
  "kind": "yes/no",
  "text": "Customer: An extra large please.\nAssistant: Sorry, they only have single slices, smalls and larges. Which one did you want?\nCustomer: The large then.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q90913affe5",
  "kind": "yes/no",
  "text": "Customer: Yes. Are there any available tickets for the 7:10 showing\nAssistant: Let me see. It's saying that show is also sold out. Would you like to see another movie?\nCustomer: Yes. Lets try SHAZAM! at 10:30",
  "question": "In the customer's last message, does \"10:30\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q104b45dd88",
  "kind": "yes/no",
  "text": "Customer: Hi.! this is robert",
  "question": "In the customer's last message, does \"robert\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q01ceba9376",
  "kind": "yes/no",
  "text": "Customer: Can you change the ham and replace it with lots of mushroom?\nAssistant: No problem. I'll make that request. Do you want it thin crust or hand tossed?\nCustomer: Make it thin crust.",
  "question": "In the customer's last message, does \"thin crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q530be3083f",
  "kind": "yes/no",
  "text": "Customer: Hello, can I still get some tickets for Captain Marvel by any chance?",
  "question": "In the customer's last message, does \"Captain Marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa6b1dfa6ff",
  "kind": "yes/no",
  "text": "Customer: Ok then lets see Hellboy in 3D then.\nAssistant: How many tickets and what time?\nCustomer: 8:35 showing and two tickets.",
  "question": "In the customer's last message, does \"8:35\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf65b0fea65",
  "kind": "yes/no",
  "text": "Customer: I'd like to place a pizza order at Blaze Pizza for delivery please.",
  "question": "In the customer's last message, does \"Blaze Pizza\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf0c715a9ed",
  "kind": "yes/no",
  "text": "Customer: hey tom its me dick\nAssistant: hey dick what can i do for you?\nCustomer: My car is pulling to the left when i am in motion.",
  "question": "In the customer's last message, does \"car is pulling to the left when i am in motion\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qceb1447c8f",
  "kind": "yes/no",
  "text": "Customer: I want to find a good restaurant that serves classic American food.\nAssistant: OK, where should I look?\nCustomer: Try Hudson or River Falls in western Wisconsin.",
  "question": "In the customer's last message, does \"Hudson\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q58fb55424a",
  "kind": "yes/no",
  "text": "Assistant: I am going to reserve the Uber XL.\nCustomer: Thank you.\nAssistant: Your Uber XL is reserved. Your driver is Todd and your estimated wait time is 16 minutes.",
  "question": "According to the assistant's last message, is \"Uber XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe182cfe6cb",
  "kind": "yes/no",
  "text": "Customer: do you have booth\nAssistant: sorry sir not available\nCustomer: ok can you book at 8.30pm",
  "question": "In the customer's last message, does \"8.30pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8dea163ae9",
  "kind": "yes/no",
  "text": "Assistant: anything else?\nCustomer: That will do it\nAssistant: Okay, well there are no onions available",
  "question": "According to the assistant's last message, is \"onions\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9f686dd444",
  "kind": "yes/no",
  "text": "Customer: Is UberX available to Downtown Sheraton.\nAssistant: No, only Uber XL is available.\nCustomer: Is UberX available from downtown central library to bricktown ballpark?",
  "question": "In the customer's last message, does \"downtown central library\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc55d2bfe2d",
  "kind": "yes/no",
  "text": "Assistant: And should we use the acount we already have with them\nCustomer: we should\nAssistant: Actually, there seem to be no Uber X available",
  "question": "According to the assistant's last message, is \"Uber X\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6bcf91fe91",
  "kind": "yes/no",
  "text": "Assistant: The 3D option will cost $15 per ticket.\nCustomer: That's fine.\nAssistant: I'm sorry. It looks like we're sold out of tickets for DUMBO 3D as well.",
  "question": "According to the assistant's last message, is \"DUMBO\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4bdd868ffb",
  "kind": "yes/no",
  "text": "Assistant: Would you like to order an additional drink or food?\nCustomer: No\nAssistant: I have one hot Venti Caramel Macchiato with whole milk and whipped cream, upside down stirred ready for you to pick up at the S Main location at 9:46 pm. Your order will be available in store or drive through with this confirmation number> #485819.",
  "question": "According to the assistant's last message, is \"upside down stirred\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9dfad5ebc4",
  "kind": "yes/no",
  "text": "Assistant: No problem. Would you like to be in the VIP section where you can order drinks from the bar?\nCustomer: Yes, that sounds like a great idea\nAssistant: Ok I got you down for two movie tickets in the VIP section at the ShowPlace ICON Theatres in St Louis Park for the 7:50PM showing",
  "question": "According to the assistant's last message, is \"St Louis Park\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2751e0125f",
  "kind": "yes/no",
  "text": "Customer: I want to go to a Bar. so i need one of the cab\nAssistant: Sure Sir. Can you tell me the exact Zipcode for your Location\nCustomer: My location was 06820",
  "question": "In the customer's last message, does \"06820\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc8d954f315",
  "kind": "yes/no",
  "text": "Customer: Do they have venti for that drink, do you know?\nAssistant: Yes they do, ma'am.\nCustomer: Okay great! Then make it a venti iced please.",
  "question": "In the customer's last message, does \"venti\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q29fbe0827f",
  "kind": "yes/no",
  "text": "Customer: what other theaters is it playing at?\nAssistant: Laurelhurst, and Studio One Theaters\nCustomer: What time is it at Studio One Theaters",
  "question": "In the customer's last message, does \"Studio One Theaters\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe3b4b01c48",
  "kind": "yes/no",
  "text": "Customer: awww bummer. can you try to get the 9:20 showing at picture show instead?\nAssistant: Let me check. Bad news, that showing is also sold out. can I interest you in another film?\nCustomer: how about, instead of wonder park, you find me tickets for Captain marvel after 8pm today",
  "question": "In the customer's last message, does \"Captain marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1dd776b310",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, they don't have honey available at the moment.\nCustomer: Wow, that's surprising. How about a Venti Coffee Frappacino with skim milk.\nAssistant: Okay, I have ordered that for you, a Venti Coffee Frappacino with skim milk.",
  "question": "According to the assistant's last message, is \"Coffee Frappacino\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q915fa22121",
  "kind": "yes/no",
  "text": "Customer: That's right. Make sure we're not seated at the bar though\nAssistant: Okay. Making the reservation now. Is there anything else you need?\nCustomer: Yes. Text me the directions to Rasika, and then text Carl, John, and Albert with the details",
  "question": "In the customer's last message, does \"Rasika\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3ca2db9e13",
  "kind": "yes/no",
  "text": "Assistant: Okay, I am ordering it now. Looking for drivers.\nCustomer: Okay.\nAssistant: Your trip has been booked. Your driver will arrive in 4 minutes.",
  "question": "According to the assistant's last message, is \"4 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q025bfeba73",
  "kind": "yes/no",
  "text": "Customer: Phoenix\nAssistant: Okay, I have found that\nCustomer: I want a table for 2 at 7 o clock",
  "question": "In the customer's last message, does \"7 o clock\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q76f0e175e5",
  "kind": "yes/no",
  "text": "Customer: I want to take a roaadtrip, so find me tickets in Lansing, MI\nAssistant: Got it. How many tickets should I be looking for?\nCustomer: Well it'll be just my son and I, so two please.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2fbd218d20",
  "kind": "yes/no",
  "text": "Customer: Great, Bob's Auto Shop is fine.\nAssistant: Great, and what type of car will you be maintenance?\nCustomer: A 2000 Honda Odyssey.",
  "question": "In the customer's last message, does \"2000\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q37028a2bc6",
  "kind": "yes/no",
  "text": "Customer: As soon as possible. Later today would be best.\nAssistant: Ok. What kind of car do you have?\nCustomer: It's a 2014 Chevy Tahoe.",
  "question": "In the customer's last message, does \"2014\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf7ed4dd998",
  "kind": "yes/no",
  "text": "Customer: It seems like something just came up and I will not be able to leave the restaurant for another hour.\nAssistant: Okay, so what time would you like me to arrange the trip.\nCustomer: Arrange the trip for 9pm pickup.",
  "question": "In the customer's last message, does \"9pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3d06a04b63",
  "kind": "yes/no",
  "text": "Customer: I need two movie tickets to see Alita: Battle Angel?",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1bb69c34f5",
  "kind": "yes/no",
  "text": "Assistant: Okay, how many people are in your party?\nCustomer: 4 people in total.\nAssistant: I'm sorry, but a regular ride is not big enough to accommodate your party.",
  "question": "According to the assistant's last message, is \"regular\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q039da0db0a",
  "kind": "yes/no",
  "text": "Customer: Phoenix, AZ\nAssistant: Do you have a preference for which theater you would like to see the movie at?\nCustomer: Yes I would like to see the movie at AMC Arizona 24 theater",
  "question": "In the customer's last message, does \"AMC Arizona 24 theater\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1133fd3d60",
  "kind": "yes/no",
  "text": "Assistant: Thank you and what is a good number for them to contact you at?\nCustomer: It's 930-644-1784\nAssistant: Perfect. I have you scheduled for tonight at 6pm. They should be expecting you and will call you if there are any changes",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qeb6254b80b",
  "kind": "yes/no",
  "text": "Customer: Ok, do you have any ideas of five star restaurants in Harrisburg?\nAssistant: Yes, I normally deal with a few.\nCustomer: Ok, I'm hoping this one will work out, I'm really in the mood for a great family get together so I do absolutely need a table for six.",
  "question": "In the customer's last message, does \"six\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q304a17bb74",
  "kind": "yes/no",
  "text": "Customer: Do you have any other times for this movie?\nAssistant: Sorry, all the tickets have been sold out for that movie.\nCustomer: Okay, can I have two tickets for Dumbo 3D at 7:30 in the AMC Theatre in Denver?",
  "question": "In the customer's last message, does \"AMC Theatre\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q57de994278",
  "kind": "yes/no",
  "text": "Assistant: Alright then, one moment while I work for you.\nCustomer: Thanks, I appreciate it.\nAssistant: Just want to confirm, you have 2 tickets booked at the AMC Classic Theater for 8PM to see the movie \"Us.\" I used your membership card to get 20% off so the total is $16.50",
  "question": "According to the assistant's last message, is \"AMC Classic Theater\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6854e49b47",
  "kind": "yes/no",
  "text": "Assistant: I did not know you had an estate in Atherton.\nCustomer: I inherited it from my grandfather last year. I prefer the climate there, instead of my other estate in Lafayette.\nAssistant: Very good. Your appointment has been confirmed for 2 p.m. today at the shop, where they will inspect your 2018 Bentley Mulsanne for the \"check engine light\" issue.",
  "question": "According to the assistant's last message, is \"Bentley Mulsanne\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q151c32b4f7",
  "kind": "yes/no",
  "text": "Assistant: And do you want to sit indoors or outdoors?\nCustomer: I want to sit indoors\nAssistant: Okay, I have booked a table for you for 8PM tonight indoors for 2 people",
  "question": "According to the assistant's last message, is \"indoors\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
