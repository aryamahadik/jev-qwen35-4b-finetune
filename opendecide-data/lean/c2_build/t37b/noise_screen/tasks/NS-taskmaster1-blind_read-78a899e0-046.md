# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-046 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-046.json

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
  "qid": "q395202780b",
  "kind": "yes/no",
  "text": "Customer: I am looking for a solid bistro in columbus ohio for 7PM tomorrow.",
  "question": "In the customer's last message, does \"7PM\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9de6f517f4",
  "kind": "yes/no",
  "text": "Customer: Yes, and can you also check if they offer a nice selection of desserts?\nAssistant: Certainly, I see now that there is a booth available by the window.\nCustomer: Wonderful! Is it available at 6:00?",
  "question": "In the customer's last message, does \"6:00\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q685421443f",
  "kind": "yes/no",
  "text": "Assistant: also, Intelligent Auto Solutions provides a shuttle service for customers who live within 15 miles of their facility. will you need them to provide a ride for you?\nCustomer: no, I have a coworker who will follow me over when I drop the vehicle off.\nAssistant: understood. you are confirmed to drop off your vehicle tomorrow morning at 8am for an oil change at Intelligent Auto Solutions. their phone number is (999)666-7777.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe2b709e6cd",
  "kind": "yes/no",
  "text": "Assistant: Are these tickets all adult tickets.\nCustomer: Yes.\nAssistant: Ok, I've confirmed that there are three adult tickets available for the 7:50 show. Would you like to proceed.",
  "question": "According to the assistant's last message, is \"three\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q92593bd67b",
  "kind": "yes/no",
  "text": "Customer: OK, do they have high chairs?\nAssistant: They all offer high chairs.\nCustomer: OK, Let's go with The Pirani",
  "question": "In the customer's last message, does \"The Pirani\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q60efb1f296",
  "kind": "yes/no",
  "text": "Customer: I would like to order pizza from Ray's Pizza.",
  "question": "In the customer's last message, does \"Ray's Pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8221f2c4ad",
  "kind": "yes/no",
  "text": "Assistant: Okay, I called them but they have nothing for 7:00, but could do 6:30 or 7:30 for two people.\nCustomer: Okay, that is fine. Either time is good for me.\nAssistant: Okay, I called and confirmed for 7:30 tonight for two people.",
  "question": "According to the assistant's last message, is \"7:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q34250d56ad",
  "kind": "yes/no",
  "text": "Customer: I want to order a ride.\nAssistant: From where to where?\nCustomer: I want to use Uber and I want to go from The Second City to Jin Thai.",
  "question": "In the customer's last message, does \"The Second City\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe1a4579e9d",
  "kind": "yes/no",
  "text": "Assistant: Do you want a hot coffee, or an iced coffee?\nCustomer: Cold Brew, Only a quarter cup of ice, Large, with two splashes of Coconut milk.\nAssistant: They are out of coconut. Is Almond Okay?",
  "question": "According to the assistant's last message, is \"coconut\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q45d94617ad",
  "kind": "yes/no",
  "text": "Assistant: OK, what day do you want to schedule?\nCustomer: I need it to be this afternoon.\nAssistant: There are no appointments available for today.",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q74b21a0220",
  "kind": "yes/no",
  "text": "Assistant: Okay. I'm going to order now.\nCustomer: Thank you.\nAssistant: Bad news. They don't have any chicken. Do you still want pizza?",
  "question": "According to the assistant's last message, is \"chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa3ccdcb6a9",
  "kind": "yes/no",
  "text": "Assistant: What type of car are you wanting?\nCustomer: I'd like an UberXL if it is under 15 bucks.\nAssistant: I am sorry, the UberXL is nearly 20 being 19.86. Do you still want that ride?",
  "question": "According to the assistant's last message, is \"UberXL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6028e30193",
  "kind": "yes/no",
  "text": "Assistant: Okay, I'm booking your ride now.\nCustomer: Thanks\nAssistant: All set, your drivers name is Dave, and he'll be there promptly at 7pm at gate C-7",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q42dd3ff1e5",
  "kind": "yes/no",
  "text": "Customer: 1234 Main Street, Apartment 1A\nAssistant: I will take your order now.\nCustomer: I want a 14 inch Hawaiian Chicken.",
  "question": "In the customer's last message, does \"14 inch\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q537a6b147f",
  "kind": "yes/no",
  "text": "Customer: How much is the fare estimate for Uber XL?\nAssistant: It is $22.27.\nCustomer: And they can be here within 5 minutes?",
  "question": "In the customer's last message, does \"5 minutes\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1d0d46d9c0",
  "kind": "yes/no",
  "text": "Customer: Yes, please.\nAssistant: According to Map Quest, without traffic, the travel time will takes between 3 to 9 minutes.\nCustomer: Ok, I will need to move up my pick up time to 2:15pm.",
  "question": "In the customer's last message, does \"2:15pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfff86f8492",
  "kind": "yes/no",
  "text": "Customer: Not that I can tell.\nAssistant: What name should I place the appointment under?\nCustomer: Ted Moseby.",
  "question": "In the customer's last message, does \"Ted Moseby\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7af5695c37",
  "kind": "yes/no",
  "text": "Customer: I would like to order pizza for the team for dinner tonight\nAssistant: Where would you like the pizzas from?\nCustomer: Pizza Hut",
  "question": "In the customer's last message, does \"Pizza Hut\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q40f3b1eedb",
  "kind": "yes/no",
  "text": "Assistant: Okay great. I'll place that order right away.\nCustomer: Thanks.\nAssistant: The order is placed at 2698 Route 22 East Union, NJ 07083. It will be ready for pickup on your way to the office.",
  "question": "According to the assistant's last message, is \"2698 Route 22 East Union, NJ 07083\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe15cf76147",
  "kind": "yes/no",
  "text": "Customer: I would like to get a lyft\nAssistant: Okay what is your location?\nCustomer: 4325 Glenwood Ave, Raleigh, NC 27612",
  "question": "In the customer's last message, does \"4325 Glenwood Ave, Raleigh, NC 27612\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5f6fc993db",
  "kind": "yes/no",
  "text": "Customer: I'm not sure. They have a rotating menu, what are some things they on the menu this week?\nAssistant: There's duck, smelt, spaghetti with anchovy, should I keep going?\nCustomer: No, that's good, why don't you book that for 8PM Thursday inside, but let them know to move the reservation to outside if something opens up.",
  "question": "In the customer's last message, does \"8PM Thursday\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q61fd2bf68b",
  "kind": "yes/no",
  "text": "Assistant: How many are riding?\nCustomer: Just 1\nAssistant: OK, I've booked you a Lyft XL that will pick you up in 20 minutes at The Walton Arts Center.",
  "question": "According to the assistant's last message, is \"20 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7af15514c2",
  "kind": "yes/no",
  "text": "Assistant: Okay. And what exactly are you looking to order?\nCustomer: I'd like to order a large hand tossed pizza with pepperoni and onions as toppings.\nAssistant: It looks like they are out of onions. Would you like to choose a different topping?",
  "question": "According to the assistant's last message, is \"onions\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q962cc00b49",
  "kind": "yes/no",
  "text": "Assistant: It looks like 6:30pm and 9:10pm but let me verify if they are available. Which time would you prefer?\nCustomer: I would want the 6:30pm showing.\nAssistant: Ok, it looks like that is not available at the Regal",
  "question": "According to the assistant's last message, is \"Regal\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qddd037a99e",
  "kind": "yes/no",
  "text": "Assistant: Let me check.\nCustomer: Thanks.\nAssistant: They have a booth available on Friday, but it's not at 6pm. It's at 8pm",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0b8c267263",
  "kind": "yes/no",
  "text": "Assistant: Okay, anything else.\nCustomer: No, just charge it to my account\nAssistant: Your order can not be placed, This store is out of Caramel drizzle",
  "question": "According to the assistant's last message, is \"Caramel drizzle\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4ed43b1a8c",
  "kind": "yes/no",
  "text": "Customer: Hi, can I get a lyft car please?\nAssistant: Sure, where would your pick up location be?\nCustomer: AMC Theater in New Brunswick, New Jersey.",
  "question": "In the customer's last message, does \"AMC Theater in New Brunswick, New Jersey.\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7508965b3d",
  "kind": "yes/no",
  "text": "Customer: Of course I did! Now please, order it up.\nAssistant: So, I called and they can only do square cut on thin crust. Do you still want original crust?\nCustomer: Geez. Is the thin crust the same price?",
  "question": "In the customer's last message, does \"thin crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b7e26b60a",
  "kind": "yes/no",
  "text": "Assistant: Okay. What other toppings would you like other than sausage.\nCustomer: I would like sausage, fresh basil, and pineapple.\nAssistant: Unfrotunately, we are out of pineapple. Would you like another topping.",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q528b799f5d",
  "kind": "yes/no",
  "text": "Assistant: Sure thing, I will call and find out what will work out for your time table.\nCustomer: Great, I really appreciate your help on this.\nAssistant: I've called but there are no 6:30ish times available, will a 7:20pm be okay instead?",
  "question": "According to the assistant's last message, is \"6:30ish\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9fcb091e4a",
  "kind": "yes/no",
  "text": "Customer: Hey! I'm looking for a nice unique or old style restaurant, generally a quiet restaurant with delicious food choices that takes reservations.\nAssistant: Okay, did you have any restaurants in mind or did you want me to search a particular area for you?\nCustomer: I've searched and The Boone Tavern would be nice, or maybe even The Still at AMBRAbev both are located in the city of Lexington, Ky.",
  "question": "In the customer's last message, does \"The Boone Tavern\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2eb7725e25",
  "kind": "yes/no",
  "text": "Customer: Yes.\nAssistant: How many tickets would you like to buy?\nCustomer: I would like two please.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q984f214db1",
  "kind": "yes/no",
  "text": "Assistant: There is not a table available at 6 pm\nCustomer: How about 7 pm?\nAssistant: No tables available at 7 pm either",
  "question": "According to the assistant's last message, is \"7 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc905108056",
  "kind": "yes/no",
  "text": "Customer: Yo I need some pizza from Dominos.\nAssistant: Which Dominos are you ordering from?\nCustomer: The one on East Broad near the mall.",
  "question": "In the customer's last message, does \"East Broad near the mall\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q776ee0e40c",
  "kind": "yes/no",
  "text": "Customer: I'll take drip.\nAssistant: ok want flavor do you want?\nCustomer: I'll take Cafe au Lait",
  "question": "In the customer's last message, does \"Cafe au Lait\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc5472e4668",
  "kind": "yes/no",
  "text": "Customer: What if just my wife and I go? it's her favorite\nAssistant: It looks like the restaurant is fully booked this short of notice I'm so sorry.\nCustomer: Can we try Dream Dance steak?",
  "question": "In the customer's last message, does \"Dream Dance steak\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe99c697a36",
  "kind": "yes/no",
  "text": "Assistant: Will you like a table or booth?\nCustomer: Let's go with the booth\nAssistant: Okay, I'm sorry no booths are available at this time",
  "question": "According to the assistant's last message, is \"booths\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2f6f2e0d7f",
  "kind": "yes/no",
  "text": "Customer: Check with Intelligent Auto Solutions.\nAssistant: Which car are you bringing in?\nCustomer: The Lexus IS250. I'm driving it now.",
  "question": "In the customer's last message, does \"Lexus IS250\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1fbac0850c",
  "kind": "yes/no",
  "text": "Customer: Yes, we'll start heading over now.\nAssistant: So were all set then, I'll enter in the request?\nCustomer: Yes, please do. The kids are getting really anxious and want to get to the airport.",
  "question": "In the customer's last message, does \"the airport\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbf7c241c9c",
  "kind": "yes/no",
  "text": "Customer: Order the larger car, one of the associates is uncomfortable in close spaces.\nAssistant: So then you would like the XL level ride?\nCustomer: Yes, please schedule it for 12:30.",
  "question": "In the customer's last message, does \"12:30\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb7a3a4aea3",
  "kind": "yes/no",
  "text": "Assistant: Ok. Confirming 4 people for Friday, Oct 1 at 7pm.\nCustomer: Ok.\nAssistant: I'm sorry, there are no tables available on Friday Oct 1 at 7pm. There are tables available on Friday Oct 1 at 6 pm and 8 pm.",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbf00ddd0f6",
  "kind": "yes/no",
  "text": "Customer: Hey, can you get me two tickets to Pet Sematary?\nAssistant: Sure, where would you like to see it?\nCustomer: An AMC in Phoenix would be good.",
  "question": "In the customer's last message, does \"AMC\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q72ff38033e",
  "kind": "yes/no",
  "text": "Customer: Oh god. Okay, well how about 6:15? That is the very latest we can go.\nAssistant: Sorry, that's not available either. The earliest time I can get you is 7:00.\nCustomer: Okay, let's try Ichibon then.",
  "question": "In the customer's last message, does \"Ichibon\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5ad5a22b8d",
  "kind": "yes/no",
  "text": "Customer: OK. Can you order me a ticket for Hell boy instead?\nAssistant: Ok in what location is it Kevin?\nCustomer: AMC Empire 25.",
  "question": "In the customer's last message, does \"AMC Empire 25\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q89d3fb8b26",
  "kind": "yes/no",
  "text": "Customer: Oh okay, then regular tickets will work.\nAssistant: Okay how many tickets?\nCustomer: I would like two tickets please.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe1108e7b51",
  "kind": "yes/no",
  "text": "Customer: Yes could you do me a favor and place an order for a pizza.\nAssistant: Sure thing, what pizza place do you want to order from?\nCustomer: I would like to order from Pizzeria Bianco",
  "question": "In the customer's last message, does \"Pizzeria Bianco\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5835829f62",
  "kind": "yes/no",
  "text": "Customer: Tim Lakes and contact number is 482.924.5193.\nAssistant: What is the make, model and year\nCustomer: It is a 2017 Hyundai Veloster.",
  "question": "In the customer's last message, does \"2017\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe4f049113d",
  "kind": "yes/no",
  "text": "Customer: Hey I'd like to get some tickets for the movie Glass.\nAssistant: Which location do you want the tickets for?\nCustomer: Eclipse Theaters in Vegas.",
  "question": "In the customer's last message, does \"Eclipse Theaters\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3800b8d54f",
  "kind": "yes/no",
  "text": "Customer: I'll go with UberX.\nAssistant: When do you want the ride?\nCustomer: Have it pick me up in 15 minutes if possible?",
  "question": "In the customer's last message, does \"15 minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf4e795637d",
  "kind": "yes/no",
  "text": "Assistant: Outside?\nCustomer: Yes please.\nAssistant: Your reservation for 3 people at 9PM tonight is confirmed with Yoko Sushi at 325 S. Grant in San Diego, 96570.",
  "question": "According to the assistant's last message, is \"325 S. Grant in San Diego, 96570\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
