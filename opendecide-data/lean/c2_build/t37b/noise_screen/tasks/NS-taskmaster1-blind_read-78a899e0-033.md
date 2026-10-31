# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-033 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-033.json

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
  "qid": "q2bf08f0675",
  "kind": "yes/no",
  "text": "Customer: I want a Cinnamon Dolce Latte, please.\nAssistant: Sorry, they said they're out of the dolce syrup that goes in that drink right now. Do you want to try something else?\nCustomer: Yes, that's fine. In that case, I'll just go with an Iced Caffe Mocha.",
  "question": "In the customer's last message, does \"Iced Caffe Mocha\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd4f1aa2e2c",
  "kind": "yes/no",
  "text": "Customer: I need you to order a carryout pizza from Papa John's",
  "question": "In the customer's last message, does \"Papa John's\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2acec6af7c",
  "kind": "yes/no",
  "text": "Assistant: All right, I'll place that order right away.\nCustomer: Thank you.\nAssistant: Ma'am, I'm sorry but they ran out of chicken as a topping.",
  "question": "According to the assistant's last message, is \"chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q02b3f925fa",
  "kind": "yes/no",
  "text": "Assistant: Great. I've found your address on file. Should I charge your visa ending in 6754?\nCustomer: Yes please.\nAssistant: Great. Your order is being placed at Main Street Pizza for your address.",
  "question": "According to the assistant's last message, is \"Main Street Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7192f8fcb5",
  "kind": "yes/no",
  "text": "Assistant: Uber Black and Uber Pool are two more options that are less common.\nCustomer: Could I request an Uber Select driver?\nAssistant: Sorry, there are no Uber Select drivers available right now.",
  "question": "According to the assistant's last message, is \"Uber Select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdf805a19c1",
  "kind": "yes/no",
  "text": "Customer: I am having a work gathering this evening at the company's headquarter.\nAssistant: What type of pizza are you interested?\nCustomer: Please order ten Pepperoni Pizza and make them all large for size.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0cc1809264",
  "kind": "yes/no",
  "text": "Customer: How about the 10:00 a.m. please.\nAssistant: Ok 10:00 a.m. on Friday March 1st. What is make and model of car?\nCustomer: It's for my 2015 Ford F150.",
  "question": "In the customer's last message, does \"Ford F150\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q10e317c3c1",
  "kind": "yes/no",
  "text": "Assistant: What can I get for you today?\nCustomer: I would like a large royal feast Pizza.\nAssistant: Okay, I am sorry to inform you but they are currently out of bacon for the Royal Feast Pizza. Would it be okay if they left off the begin?",
  "question": "According to the assistant's last message, is \"bacon\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbf9ba03f5b",
  "kind": "yes/no",
  "text": "Customer: I need you to buy me tickets to a movie tonight.\nAssistant: Sure, what do you need?\nCustomer: Tickets to Bumblebee in LA.",
  "question": "In the customer's last message, does \"LA\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q435dae792a",
  "kind": "yes/no",
  "text": "Assistant: Alright I'll call right now.\nCustomer: Thank you\nAssistant: Okay I got some bad news. It looks like they are sold out for the 8:00 showing, would you want to go at a different time or theater?",
  "question": "According to the assistant's last message, is \"8:00\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc8245860b2",
  "kind": "yes/no",
  "text": "Customer: Order a pizza from Pizza Hut\nAssistant: which location\nCustomer: chapel plaza cherry hill",
  "question": "In the customer's last message, does \"chapel plaza cherry hill\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1c8ab9308e",
  "kind": "yes/no",
  "text": "Customer: Get it from the one on 3rd street.\nAssistant: I know the location, what type of drink would you like.\nCustomer: I have heard a lot about the Vanilla Bean Coconutmilk Latte, can you get me one of those?",
  "question": "In the customer's last message, does \"Vanilla Bean Coconutmilk Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q79842fdfeb",
  "kind": "yes/no",
  "text": "Customer: I need to schedule a repair of my car's brakes.",
  "question": "In the customer's last message, does \"repair of my car's brakes\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe5f92dcd73",
  "kind": "yes/no",
  "text": "Customer: Hello, my name is Ricardo Gibbs and I'm calling to reserve a table for six for Friday night, April 12th at 6pm.",
  "question": "In the customer's last message, does \"six\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q02ba09b1d4",
  "kind": "yes/no",
  "text": "Customer: Two.\nAssistant: What time?\nCustomer: 7 PM",
  "question": "In the customer's last message, does \"7 PM\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q20cc2fde8c",
  "kind": "yes/no",
  "text": "Customer: What about the following evening, and make that three total my husband can then join.\nAssistant: Looks as if they don't have anything available then either, should we try another day?\nCustomer: No, let me try Scheme Resteraunt and Bar",
  "question": "In the customer's last message, does \"Scheme Resteraunt and Bar\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q551d8d0db5",
  "kind": "yes/no",
  "text": "Customer: The one in South Tuscon\nAssistant: ok no problem, They have some question I need to fill out, the first is What is the make model and year of your car\nCustomer: 2008 Ford Mustang",
  "question": "In the customer's last message, does \"Ford Mustang\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc4d6964ecd",
  "kind": "yes/no",
  "text": "Customer: April 18.\nAssistant: What time?\nCustomer: 5:30 pm.",
  "question": "In the customer's last message, does \"5:30 pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q560beeb33e",
  "kind": "yes/no",
  "text": "Customer: I've used Uber in the past so let's go with them.\nAssistant: Okay so you need pick up at the airport?\nCustomer: Yes at Jackson Hartfield Airport.",
  "question": "In the customer's last message, does \"Jackson Hartfield Airport\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdafb3c5072",
  "kind": "yes/no",
  "text": "Assistant: It's going to be $43.98\nCustomer: Okay great, get me the two large specialty pizzas for pickup.\nAssistant: Okay, your order has been placed for two large pizzas, the GOURMET VEGGIE, and the Ulti-Meat. It will be ready for pickup in 25 minutes.",
  "question": "According to the assistant's last message, is \"GOURMET VEGGIE\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1e18a2c710",
  "kind": "yes/no",
  "text": "Assistant: What screen would you prefer?\nCustomer: 3D\nAssistant: 8PM is not available. The closest options are 7PM and 9:30.",
  "question": "According to the assistant's last message, is \"8PM\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9d81fc0f7a",
  "kind": "yes/no",
  "text": "Assistant: Okay, sounds good.\nCustomer: Okay let me know when you get there.\nAssistant: I'm here but they are out of pineapple. Do you want to get something else?",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4336a7362d",
  "kind": "yes/no",
  "text": "Assistant: What type of milk would you like?\nCustomer: Can I have almond milk?\nAssistant: Im sorry, almond milk is unavailable?",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0193db4f57",
  "kind": "yes/no",
  "text": "Customer: Intelligent Auto Solutions\nAssistant: Can I get the year, make and model?\nCustomer: It's a 2000 Honda Civic EX",
  "question": "In the customer's last message, does \"2000\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5e5231df70",
  "kind": "yes/no",
  "text": "Customer: I want 2 Meatlovers pizzas\nAssistant: Alright what size?\nCustomer: I want one Large and one medium, both meat lovers",
  "question": "In the customer's last message, does \"medium\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q583cbbea91",
  "kind": "yes/no",
  "text": "Assistant: about 20-30 minutes.\nCustomer: Alright that sounds great.\nAssistant: So you have your appointment booked first thing tomorrow morning at 8am. and it will be texted to you.",
  "question": "According to the assistant's last message, is \"morning at 8am\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q45b14765f0",
  "kind": "yes/no",
  "text": "Customer: Yes. How much is the fare?\nAssistant: The fare according to Uber's trip estimator will cost $25.96.\nCustomer: Okay great. I would like my car to arrive in 30 minutes please.",
  "question": "In the customer's last message, does \"30 minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb64c10b4d0",
  "kind": "yes/no",
  "text": "Assistant: None that I see. The rates are based on age. Who are you taking?\nCustomer: I'm taking one of the kids I sponsor. So, that'll be one adult and one teen.\nAssistant: Okay. I've purchased two tickets for you on row 10 in the middle for the 7PM time slot tonight for a total of $32.69.",
  "question": "According to the assistant's last message, is \"$32.69\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q96ab04b039",
  "kind": "yes/no",
  "text": "Assistant: Well, there's Regal Cinemas City North 14 IMAX & RPX.\nCustomer: Oh yeah! We want to see it in IMAX. Is there a 7 pm showing?\nAssistant: Sorry, it's not showing in IMAX at this location, and the latest showing they have tonight is 6 pm.",
  "question": "According to the assistant's last message, is \"IMAX\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q75752c3b4c",
  "kind": "yes/no",
  "text": "Customer: Hello please book me an appointment Uber XL to soldier field.\nAssistant: Ok what is your current lcation\nCustomer: I am at home.",
  "question": "In the customer's last message, does \"at home\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q944e4f6665",
  "kind": "yes/no",
  "text": "Customer: AMC at Pembrooke Lakes Mall.\nAssistant: How many tickets are you looking to get?\nCustomer: Im looking to get two tickets to To an 8pm showing in Imax3D.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2b6fc9964d",
  "kind": "yes/no",
  "text": "Customer: Hey Beyonce, can you book me two tickets for How to Train Your Dragon?\nAssistant: Sure I can. In which city?\nCustomer: I'm in Seattle right now.",
  "question": "In the customer's last message, does \"Seattle\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe749736eaf",
  "kind": "yes/no",
  "text": "Assistant: All right. I'll give them a call right away.\nCustomer: Sounds great!\nAssistant: Okay, I just got off the phone... apparently the pretzel crust pizza was a limited time offer and is currently unavailable.",
  "question": "According to the assistant's last message, is \"pretzel crust pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4732f0bba2",
  "kind": "yes/no",
  "text": "Customer: Can you find me an Italian restaurant in Detroit, Michigan?",
  "question": "In the customer's last message, does \"Detroit, Michigan\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe34183dda7",
  "kind": "yes/no",
  "text": "Customer: The Houston Zoo.\nAssistant: And where will you be picked up?\nCustomer: Barnaby's Cafe",
  "question": "In the customer's last message, does \"Barnaby's Cafe\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8acce6a695",
  "kind": "yes/no",
  "text": "Customer: I want to go see How To Train Your Dragon 3.\nAssistant: What location would you like to see the movie at?\nCustomer: Elder Theater, Jackson Center Ohio.",
  "question": "In the customer's last message, does \"Jackson Center Ohio\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7874141717",
  "kind": "yes/no",
  "text": "Assistant: What kind of milk would you like with that?\nCustomer: Id like to get it with coconut milk.\nAssistant: They are out of coconut milk at this location.",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q898929eb53",
  "kind": "yes/no",
  "text": "Customer: Alita: Battle Angel",
  "question": "In the customer's last message, does \"Alita: Battle Angel\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4a00f92ba6",
  "kind": "yes/no",
  "text": "Customer: Haley, the Lexus is not letting me close all doors with the autolock. Can you please get me an appointment at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Lexus\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q63aea4832a",
  "kind": "yes/no",
  "text": "Assistant: Do you have any special requests?\nCustomer: No thanks.\nAssistant: Okay, unfortunately, skim milk is not presently available, do you have another preference?",
  "question": "According to the assistant's last message, is \"skim milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qee9838381f",
  "kind": "yes/no",
  "text": "Assistant: You can eat outside at 7:30. Would that be ok?\nCustomer: That would be fine.\nAssistant: Ok, I have made the reservation at The Palm for four people, outdoors at 7:30pm tonight.",
  "question": "According to the assistant's last message, is \"The Palm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa8281eb6c4",
  "kind": "yes/no",
  "text": "Customer: Which place is generally Lower priced?\nAssistant: That would be Maxwells\nCustomer: Can you check to see if they have a table for two on the plaza",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7fdbd581cc",
  "kind": "yes/no",
  "text": "Assistant: Ok, at what time?\nCustomer: I need the reservation for 7pm\nAssistant: 7pm is not available, please request a different time",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q516abd8238",
  "kind": "yes/no",
  "text": "Customer: Las Vegas.\nAssistant: What movie theatre do you prefer?\nCustomer: You can book them at the Regal Summerlin Luxury 5.",
  "question": "In the customer's last message, does \"Regal Summerlin Luxury 5\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbeb9e9c646",
  "kind": "yes/no",
  "text": "Assistant: yes there is a 6pm slot open. i will book it.\nCustomer: fantastic thats perfect, thank you.\nAssistant: not a problem sir. 6pm is booked and will be waiting for your arrival at the olive garden in st.charles.",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2ba81bb6a9",
  "kind": "yes/no",
  "text": "Assistant: Do you want cream or almond milk?\nCustomer: I'll have cream with the cold brew.\nAssistant: Oh no, I tried to order the drink, but they're all out of the Blond roast. Do you want the regular cold foam cappuccino or a different drink?",
  "question": "According to the assistant's last message, is \"Blond roast\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q69e17e1dd4",
  "kind": "yes/no",
  "text": "Assistant: Okay. What size? And do you just want one?\nCustomer: Yes, just one large with the thin crust.\nAssistant: Just checked. That was just a special for the Super Bowl. They don't have crab any more.",
  "question": "According to the assistant's last message, is \"crab\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q61e5bb017e",
  "kind": "yes/no",
  "text": "Customer: 5678223687\nAssistant: Thanks for the info Ma'am Jen. Can I get your order pls?\nCustomer: I would like a large chicken supreme pizza",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2e7e2f55a9",
  "kind": "yes/no",
  "text": "Assistant: No problem, is there anything else I can help you with?\nCustomer: Yes, can you see if they can change the oil while it's there. Then, everything will be good to go.\nAssistant: Ok, so you're all set to drop off your 2012 Subaru WRX at Intelligent Auto Solutions, 11:00 AM, and will be charged $120 diagnostic fee and $47 for the oil change.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qee999e92ca",
  "kind": "yes/no",
  "text": "Assistant: How do you want to pay?\nCustomer: Pay with my PEETS account\nAssistant: OK, coffee has been ordered and will be ready to pick up at Giants Carisle 698 Downingtown Pike West Chester, PA and you will receive a text when it is ready.",
  "question": "According to the assistant's last message, is \"Giants Carisle 698 Downingtown Pike West Chester, PA\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
