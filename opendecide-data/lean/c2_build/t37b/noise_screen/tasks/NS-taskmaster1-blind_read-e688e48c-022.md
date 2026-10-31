# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-022 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-022.json

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
  "qid": "q018f8b9edf",
  "kind": "yes/no",
  "text": "Customer: What about rooftop seating?\nAssistant: Hacienda has rooftop seating!\nCustomer: Great, then let's go with Hacienda.",
  "question": "In the customer's last message, does \"Hacienda\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q089133e35d",
  "kind": "yes/no",
  "text": "Customer: April 18.\nAssistant: What time?\nCustomer: 5:30 pm.",
  "question": "In the customer's last message, does \"5:30 pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4a50fd54b1",
  "kind": "yes/no",
  "text": "Assistant: For how many people?\nCustomer: 8 people.\nAssistant: Im sorry indoor seating is unavailable for 8 people.",
  "question": "According to the assistant's last message, is \"indoor seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q397ab5778a",
  "kind": "yes/no",
  "text": "Customer: Hi I want to order a Lyft ride.\nAssistant: Hi, where from and to would like to go?\nCustomer: I need to go from the airport to Virginia street 509",
  "question": "In the customer's last message, does \"Virginia street 509\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q30b08736fb",
  "kind": "yes/no",
  "text": "Customer: after we get to Jacks house can you put the last address as the cheese cake factory we wanna go for dinner\nAssistant: Yes, in what city?\nCustomer: Try Riverside by the tyler Mall",
  "question": "In the customer's last message, does \"Riverside by the tyler Mall\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf4ed7d1c01",
  "kind": "yes/no",
  "text": "Customer: I would like to get a lyft\nAssistant: Okay what is your location?\nCustomer: 4325 Glenwood Ave, Raleigh, NC 27612",
  "question": "In the customer's last message, does \"4325 Glenwood Ave, Raleigh, NC 27612\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q364853d173",
  "kind": "yes/no",
  "text": "Customer: I'll take two, one for my wife as well. What are showtimes.\nAssistant: Well it's a Friday so it may be a little busy, but there's one at 7:10 that has a few open seats.\nCustomer: Ok, book two seats for the 7:10 showing please.",
  "question": "In the customer's last message, does \"7:10\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q95e58b4d79",
  "kind": "yes/no",
  "text": "Assistant: Sure, let me check.\nCustomer: Thank you.\nAssistant: Sorry, there is no more olives available at that time.",
  "question": "According to the assistant's last message, is \"olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q62a10c7679",
  "kind": "yes/no",
  "text": "Assistant: That will be $5.00 exactly. I can charge that to your card.\nCustomer: Great!\nAssistant: Your drink is on order and will be ready for pick-up very soon at the Starbucks 14607 Memorial Dr Houston, TX location. Your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"14607 Memorial Dr Houston, TX\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d5932c186",
  "kind": "yes/no",
  "text": "Customer: Dark Chocolate Orange Mocha\nAssistant: I'm sorry, that's a seasonal drink and is no longer available.\nCustomer: OK, then I'll take a Cafe Mocha",
  "question": "In the customer's last message, does \"Cafe Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3a92c0d3a1",
  "kind": "yes/no",
  "text": "Assistant: Should I order that just the same?\nCustomer: Yes please, Grande and just the way it is made will be fine. You do have my Starbucks account?\nAssistant: Yes I do. That Caramel Cloud Machiatto is in stock. I ordered it hot.",
  "question": "According to the assistant's last message, is \"Caramel Cloud Machiatto\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1c514e5aa1",
  "kind": "yes/no",
  "text": "Customer: Haley, I need two pizzas from Dominos.\nAssistant: O.K, the one closer to us?\nCustomer: Yes. it should be 415 Summer St, Boston, MA 02210",
  "question": "In the customer's last message, does \"415 Summer St, Boston, MA 02210\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q148c515f1c",
  "kind": "yes/no",
  "text": "Customer: Hello Assistant! I need assistance! Can you purchase me tickets for the new Dragon Ball Movie.\nAssistant: Yes of course! What city would you like to see it in?\nCustomer: In Paramus! I don't think that there will be many people watching it there!",
  "question": "In the customer's last message, does \"Paramus\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q76ad4695b7",
  "kind": "yes/no",
  "text": "Customer: Gainesville Florida, please\nAssistant: what would you like to order?\nCustomer: Chicken BBQ pizza, large, site of special sauce.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe7b669101d",
  "kind": "yes/no",
  "text": "Customer: Hey Amanda, I'm having some issues with my car on my way to work today can you make me an appointment with the shop?\nAssistant: I absolutely can! Which shop do you prefer?\nCustomer: I went to Intelligent Auto Solutions last time and they did a wonderful job can you see if there are any openings today?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbb46c9dc33",
  "kind": "yes/no",
  "text": "Assistant: Ok the initial appointment fee is 250.\nCustomer: That is fine.\nAssistant: Ok the appointment is for a 2019 Honda Civic. That is having black smoke from the rear, check engine light and \"funny\" noises.",
  "question": "According to the assistant's last message, is \"Honda Civic\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7dbd607b29",
  "kind": "yes/no",
  "text": "Customer: Change location to the one on park place.\nAssistant: Park place bertuccis in Salem\nCustomer: No the Bertuccis in Patterson on Park Place",
  "question": "In the customer's last message, does \"Patterson on Park Place\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q764ba5263a",
  "kind": "yes/no",
  "text": "Customer: I would like to request a ride from Lyft.\nAssistant: Okay, where would you like to be picked up and where do you want to go?\nCustomer: Im at the DFW airport, and I need a ride to my hotel, the Fairmont Dallas.",
  "question": "In the customer's last message, does \"DFW airport\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4c842a1835",
  "kind": "yes/no",
  "text": "Assistant: when did you need a reseravtion for?\nCustomer: I need a reservation for next week at 2:00 a.m. on a Monday.\nAssistant: Unfortunately, 54 mint SF is not open at 2 am.",
  "question": "According to the assistant's last message, is \"2 am\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q621408d91a",
  "kind": "yes/no",
  "text": "Customer: I will need to be picked up at Miller Park after the game. i will be to be taken to brother's bar in grill in Milwaukee after.\nAssistant: What time does the game end? I can have them meet you right outside the doors.\nCustomer: I'm thinking around 10 pm should be good. We are in the 8th inning now.",
  "question": "In the customer's last message, does \"around 10 pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q66aa556321",
  "kind": "yes/no",
  "text": "Assistant: OK, they have that,\nCustomer: Good, so we're all set?\nAssistant: Yes, I ordered one 16-cut thin crust pizza with classic red sauce with pepperoni and mushroom.",
  "question": "According to the assistant's last message, is \"thin crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d36deff59",
  "kind": "yes/no",
  "text": "Customer: Same answer.\nAssistant: When is your date?\nCustomer: I'll need an Uber by 5pm and need to get to dinner at 7pm",
  "question": "In the customer's last message, does \"5pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdc94c3a8eb",
  "kind": "yes/no",
  "text": "Assistant: Okay. Your total will be 18.99.\nCustomer: Great.\nAssistant: Your order for one large Meat Lover's pizza has been placed and will be ready for pickup in about 25 minutes.",
  "question": "According to the assistant's last message, is \"Meat Lover's pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4d79e27d55",
  "kind": "yes/no",
  "text": "Customer: Hello, can you book a table for me for this Friday night?\nAssistant: Sure, which restaurant do you prefer?\nCustomer: Royal Buffet at Hoffman Estates.",
  "question": "In the customer's last message, does \"Hoffman Estates\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd464812db2",
  "kind": "yes/no",
  "text": "Customer: I want to order some pizzas from my favorite pizza restaurant, Veto Pizza.",
  "question": "In the customer's last message, does \"Veto Pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9aeaafdc90",
  "kind": "yes/no",
  "text": "Assistant: Okay, I've added it. So your order is now a tall extra hot almond milk latte with no whip, and a mango coconut yogurt bowl. Is that correct?\nCustomer: Yes, that's it.\nAssistant: Great. I've put in the order to the marginal way Starbucks and will be ready for pick up shortly. The receipt has been sent to your phone via text.",
  "question": "According to the assistant's last message, is \"marginal way\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5d23f5599e",
  "kind": "yes/no",
  "text": "Customer: Tuesday, and 2d\nAssistant: Unfortunately all showings on tuesday are full. Is there any other day or movie I could look into for you?\nCustomer: Can you see if there are any showings of Pet Sematary showing on tuesday?",
  "question": "In the customer's last message, does \"Pet Sematary\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf39d34b667",
  "kind": "yes/no",
  "text": "Customer: Well then I don't want to go there at all.\nAssistant: Well do you have another restaurant in mind?\nCustomer: Yeah Sammy's Trattoria, if all options are available.",
  "question": "In the customer's last message, does \"Sammy's Trattoria\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa351c7dabc",
  "kind": "yes/no",
  "text": "Customer: Hi, I would like to book two movie tickets.\nAssistant: Hi there, I can help you with that.\nCustomer: I would like to buy two movie tickets for Captain Marvel.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6d24516a70",
  "kind": "yes/no",
  "text": "Assistant: Of course sir. I will make that reservation right away.\nCustomer: Thank you. Please put it on my calendar as well.\nAssistant: I’m sorry sir, but Houston’s does not have any outdoor seating at 6pm. Would you prefer another time?",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q11fb929877",
  "kind": "yes/no",
  "text": "Customer: I need tickets for The Grinch tonight.",
  "question": "In the customer's last message, does \"The Grinch\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q75ce043c0a",
  "kind": "yes/no",
  "text": "Customer: Hi there, I'd like to make an order.\nAssistant: What location are you trying to order from?\nCustomer: Mankato, Minnesota.",
  "question": "In the customer's last message, does \"Mankato, Minnesota\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qba1174d602",
  "kind": "yes/no",
  "text": "Assistant: I just checked and they don't have any tables available for that time.\nCustomer: Hm, how about 7:30.\nAssistant: Unfortunately, they are fully booked that night from 6 until 8:30. Shall I keep trying?",
  "question": "According to the assistant's last message, is \"6 until 8:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3695f4327c",
  "kind": "yes/no",
  "text": "Assistant: Yes! Would you like me to go ahead and book the time slot?\nCustomer: Go ahead!\nAssistant: Great! I have booked your appointment at Intelligent Auto Solutions under the name Chaz Adkins with the phone number 606-555-4321.",
  "question": "According to the assistant's last message, is \"Chaz Adkins\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc4d51740ed",
  "kind": "yes/no",
  "text": "Customer: 2% is fine.\nAssistant: Would you like a Tall, Grande, or Venti Iced?\nCustomer: Grande would be fine.",
  "question": "In the customer's last message, does \"Grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdb68af7230",
  "kind": "yes/no",
  "text": "Assistant: There's a table available at 6pm\nCustomer: Great, let's book it\nAssistant: I have reserved a table for you at Nodoguro at 6pm",
  "question": "According to the assistant's last message, is \"Nodoguro\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf41f7f7fcc",
  "kind": "yes/no",
  "text": "Customer: Hello, Can you assist me in ordering my regular from Pizza Hut?",
  "question": "In the customer's last message, does \"Pizza Hut\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf3b4b62a75",
  "kind": "yes/no",
  "text": "Customer: Okay. Sounds good.\nAssistant: What is the make, model and year of your car?\nCustomer: It is a 2016 Toyota Tercel",
  "question": "In the customer's last message, does \"Toyota Tercel\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1c952f9da0",
  "kind": "yes/no",
  "text": "Assistant: did u want soy for both?\nCustomer: Yes, I did.\nAssistant: great. i have you down for 1 grande iced caramel macchiato with soy milk and 1 venti iced caramel macchiato with soy milk from the starbucks on course street.",
  "question": "According to the assistant's last message, is \"caramel macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q762cc675b7",
  "kind": "yes/no",
  "text": "Customer: Ummm order from the one on North Charles street.\nAssistant: Ok and what kind of coffee drink do you want?\nCustomer: I'll take the Caffe Americano please.",
  "question": "In the customer's last message, does \"Caffe Americano\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfd70211979",
  "kind": "yes/no",
  "text": "Assistant: Ok any special requests?\nCustomer: Yes we'd also like a booth.\nAssistant: Ok I have you booked for May 1st at 5 in a booth at Bricco for two people.",
  "question": "According to the assistant's last message, is \"May 1st at 5\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc8405fc2eb",
  "kind": "yes/no",
  "text": "Customer: After\nAssistant: Ok so they have a 4 p.m. and 5:30 p.m. which one?\nCustomer: 4 sounds good. Can you check to see if they have DBOX seats?",
  "question": "In the customer's last message, does \"4\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q74c077ff56",
  "kind": "yes/no",
  "text": "Customer: hi i need to make a reservation at a restaurant\nAssistant: ok, where would you like to book?\nCustomer: can you find something in sacramento?",
  "question": "In the customer's last message, does \"sacramento\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8872ea3f75",
  "kind": "yes/no",
  "text": "Customer: okay thanks\nAssistant: what type of coffee you want\nCustomer: a Cinnamon Dolce Latte",
  "question": "In the customer's last message, does \"Cinnamon Dolce Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q88e04a8719",
  "kind": "yes/no",
  "text": "Customer: Hello i would like some information on getting a tune up for my 2017 chevy cruise.",
  "question": "In the customer's last message, does \"chevy cruise\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbe86592c98",
  "kind": "yes/no",
  "text": "Assistant: No problem. I am booking it now.\nCustomer: Thanks.\nAssistant: OK, your car is on its way. You have a LyftXL on its way to you now. The car will pick the 6 of you up at Minnetrista and drop you off at the Elm Street Brewery. You should be able to track the car's progress on your phone.",
  "question": "According to the assistant's last message, is \"LyftXL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf75f6ece92",
  "kind": "yes/no",
  "text": "Customer: Mushrooms please\nAssistant: one large pizza with sausage and mushrooms, would you like that with hand tossed crust or deep dish?\nCustomer: Deep dish",
  "question": "In the customer's last message, does \"Deep dish\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd37e365361",
  "kind": "yes/no",
  "text": "Customer: When do you have available?\nAssistant: We have 12 noon, as well as anything after 3:00PM available.\nCustomer: How about 3:15 PM, then.",
  "question": "In the customer's last message, does \"3:15 PM\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1d13014fb3",
  "kind": "yes/no",
  "text": "Assistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.\nAssistant: Okay, I have booked you for 6 pm tonight for your Hyundai Elantra 2010..",
  "question": "According to the assistant's last message, is \"Hyundai Elantra\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q567cf61601",
  "kind": "yes/no",
  "text": "Customer: I need to have the oil changed.\nAssistant: What is the make, model, and year of the vehicle?\nCustomer: It's a 2015 Ford F 150.",
  "question": "In the customer's last message, does \"2015\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
