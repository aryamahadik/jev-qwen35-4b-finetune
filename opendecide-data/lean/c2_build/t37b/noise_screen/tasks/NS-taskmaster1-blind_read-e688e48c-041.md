# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-041 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-041.json

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
  "qid": "q2ee62bb037",
  "kind": "yes/no",
  "text": "Assistant: How about sauce type?\nCustomer: Let's go with pesto.\nAssistant: Unfortunately pesto sauce is unavailable, would you like to try garlic sauce instead?",
  "question": "According to the assistant's last message, is \"pesto sauce\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1a7603a0d6",
  "kind": "yes/no",
  "text": "Assistant: Sure, what would you like to order?\nCustomer: I would like to order a large pizza with onions, mushrooms, garlic, and pepperoni.\nAssistant: Unfortunately, they are out of mushrooms.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcb432ec5d3",
  "kind": "yes/no",
  "text": "Customer: Yep.\nAssistant: thanks, what model is your car?\nCustomer: It's a 2011 Nissan Rogue.",
  "question": "In the customer's last message, does \"Nissan Rogue\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q82a4781c42",
  "kind": "yes/no",
  "text": "Assistant: Would you like to confirm your appointment?\nCustomer: Yes, please.\nAssistant: Appointment with Intelligent Auto Solutions set for today at 3pm, costing $75. Confirmed.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa672a3cb5a",
  "kind": "yes/no",
  "text": "Assistant: Is there anything else I can help you with?\nCustomer: That will all for today.\nAssistant: The reservation has been made, for April 10th at 6:00pm.",
  "question": "According to the assistant's last message, is \"April 10th at 6:00pm.\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q669f18a099",
  "kind": "yes/no",
  "text": "Customer: No, let me try Scheme Resteraunt and Bar\nAssistant: Okay what location would you like to try?\nCustomer: The one on North 7th Street in Salina, Ks please",
  "question": "In the customer's last message, does \"North 7th Street in Salina, Ks\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69b4059fa6",
  "kind": "yes/no",
  "text": "Customer: Flint, Michigan\nAssistant: Okay, and what company would you like to book the appointment for?\nCustomer: Belle Tire",
  "question": "In the customer's last message, does \"Belle Tire\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb9bad3b014",
  "kind": "yes/no",
  "text": "Customer: Hi, I need you to book an appointment for me at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q308d7b71bb",
  "kind": "yes/no",
  "text": "Customer: 300 E Colorado Blvd, Pasadena, CA 91101\nAssistant: And for Kosuke?\nCustomer: 618 W Main St, Alhambra, CA 91801",
  "question": "In the customer's last message, does \"618 W Main St, Alhambra, CA 91801\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb61fa75f85",
  "kind": "yes/no",
  "text": "Customer: I would like a reservation at 8pm, for 3 people in a booth inside please.\nAssistant: Okay, I will set up a reservation for 3 people, what name would you like me to put in under?\nCustomer: Put it down for Mitchell, please.",
  "question": "In the customer's last message, does \"Mitchell\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q16bdbede9b",
  "kind": "yes/no",
  "text": "Assistant: And your destination is the Troubadour in West Hollywood?\nCustomer: Right.\nAssistant: Ok. I have your Uber Lux on its way to you.",
  "question": "According to the assistant's last message, is \"Uber Lux\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q96da9204e5",
  "kind": "yes/no",
  "text": "Customer: I would like to order something from Bosses Pizza can you put in an order for me?\nAssistant: Sure I can just let me know what you want and where I need to order like the location.\nCustomer: Fort Worth 76108",
  "question": "In the customer's last message, does \"Fort Worth 76108\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q587dd81ca5",
  "kind": "yes/no",
  "text": "Assistant: For what time?\nCustomer: As soon as possible.\nAssistant: There are no Uber Black drivers available at the moment.",
  "question": "According to the assistant's last message, is \"Uber Black\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q819ea30d9b",
  "kind": "yes/no",
  "text": "Assistant: Ok, a Tall latte- do you want a plain or flavored latte?\nCustomer: A chai latte with no water and soy milk.\nAssistant: I'm sorry, we're out of soy- is almond milk ok?",
  "question": "According to the assistant's last message, is \"soy\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q979052ba3c",
  "kind": "yes/no",
  "text": "Customer: Hey, can you send a Lyft to come get me?\nAssistant: Sure, where are you at currently?\nCustomer: I'm at The Grind Coffee House in Apple Valley.",
  "question": "In the customer's last message, does \"The Grind Coffee House in Apple Valley\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q37c480f1f8",
  "kind": "yes/no",
  "text": "Customer: I would like 2 tickets to see Alita in theaters.",
  "question": "In the customer's last message, does \"Alita\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5799cf6d71",
  "kind": "yes/no",
  "text": "Assistant: What kind of pizza would you like?\nCustomer: I'd like a large pepperoni and sardines pizza\nAssistant: Unfortunately, the store does not have sardines available as a topping",
  "question": "According to the assistant's last message, is \"sardines\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8d8d5e5256",
  "kind": "yes/no",
  "text": "Customer: Ok thank you\nAssistant: They don't have that either.\nCustomer: Ok how about at Beverly's",
  "question": "In the customer's last message, does \"Beverly's\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0a09892f96",
  "kind": "yes/no",
  "text": "Assistant: And would you like whipped cream on it?\nCustomer: Yes, I would.\nAssistant: It looks like they are out of coconut milk. Is there another milk that you would like?",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qae5a99506d",
  "kind": "yes/no",
  "text": "Assistant: Any topping you want.\nCustomer: I would like one pizza with sausage, and green olives. I would like the second pizza to have black olives and bacon.\nAssistant: I'm sorry, we don't have green olives.",
  "question": "According to the assistant's last message, is \"green olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q41b3bc2f1d",
  "kind": "yes/no",
  "text": "Customer: Cynthia, find Howies in towns menu",
  "question": "In the customer's last message, does \"Howies\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1bfb07c93d",
  "kind": "yes/no",
  "text": "Customer: The one in Orange City, Fl.\nAssistant: Sure, what would you like.\nCustomer: I would like a caramel macchiato",
  "question": "In the customer's last message, does \"caramel macchiato\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdb2644b1aa",
  "kind": "yes/no",
  "text": "Assistant: Okay, let me check the availability.\nCustomer: Can you request Lux for me?\nAssistant: I don't see any Lux in the area now.",
  "question": "According to the assistant's last message, is \"Lux\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf27ea42d7b",
  "kind": "yes/no",
  "text": "Customer: Yes, I would also like to get a medium taco pizza, without black olives.\nAssistant: I have also ordered a medium taco pizza without black olives. Would you like to add anything else to your order?\nCustomer: I want a medium pizza with hamburger and sausage as well please.",
  "question": "In the customer's last message, does \"medium\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q843b21aaf4",
  "kind": "yes/no",
  "text": "Assistant: Ok. They say you can bring it in first thing in the morning, 7:00am tomorrow.\nCustomer: I really can't wait that long. Can they see me today, preferably around 3:30?\nAssistant: Hold on, checking on that. They're saying 3:30 is no good but they can squeeze you in at 4:00.",
  "question": "According to the assistant's last message, is \"3:30\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb7e37ef279",
  "kind": "yes/no",
  "text": "Customer: hello can you please make me an appointment for auto repair?\nAssistant: ok where should i make your appointment?\nCustomer: Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q167e95906b",
  "kind": "yes/no",
  "text": "Customer: Hey, could you get me some tickets to see Pet Semetary tonight?",
  "question": "In the customer's last message, does \"Pet Semetary\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7578e84297",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to order tickets to After.\nAssistant: What location?\nCustomer: Dallas, TX please",
  "question": "In the customer's last message, does \"Dallas, TX\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q58a138b9cf",
  "kind": "yes/no",
  "text": "Customer: Yes, you will need my vehicle information, are you ready?\nAssistant: Yes, go ahead\nCustomer: It is a 2010 GMC Yukon XL",
  "question": "In the customer's last message, does \"2010\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q088147c126",
  "kind": "yes/no",
  "text": "Assistant: Sorry, US at Malco Wolfchase Cinema Grill is sold out in 3d and regular showings.\nCustomer: What about Malco Studio on the Square?\nAssistant: Checking, no 3d showings.",
  "question": "According to the assistant's last message, is \"3d\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd4b4187c45",
  "kind": "yes/no",
  "text": "Assistant: Will do. Do you want me to see if you can sit outside?\nCustomer: My husband would love that!\nAssistant: Oh darn. You can't sit outside.",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc1bc231423",
  "kind": "yes/no",
  "text": "Assistant: ok there is an open for 7:15pm, does that work\nCustomer: Yes thats fine\nAssistant: Ok I have you down for Monday at 7:15pm also thre is a 50 dollar fee for this job is that ok",
  "question": "According to the assistant's last message, is \"Monday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcf00e5c03a",
  "kind": "yes/no",
  "text": "Assistant: Ok let me try and book it for you.\nCustomer: Thanks\nAssistant: Ok they are full at 9:00 am, but they are available at 9:15 am would that work for you?",
  "question": "According to the assistant's last message, is \"9:00 am\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q63c63f910a",
  "kind": "yes/no",
  "text": "Assistant: What size?\nCustomer: Small, please.\nAssistant: They said they're out of mushrooms and garlic.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdc7397bf81",
  "kind": "yes/no",
  "text": "Customer: Hi I'd like to watch a movie tonight in San Francisco.",
  "question": "In the customer's last message, does \"San Francisco\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfc0f1a7c70",
  "kind": "yes/no",
  "text": "Customer: I need to get a ride to Cracker Barrel.\nAssistant: Where is your current location?\nCustomer: I am at the Greenwood Mall.",
  "question": "In the customer's last message, does \"Greenwood Mall\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2395dfc005",
  "kind": "yes/no",
  "text": "Customer: Hello, can you please order me a car?\nAssistant: Yes, where are you located and where are you going?\nCustomer: I am at Ford Field, I would like to go to Birmingham.",
  "question": "In the customer's last message, does \"Ford Field\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4fb748750e",
  "kind": "yes/no",
  "text": "Customer: I would like to get a pizza from papa johns",
  "question": "In the customer's last message, does \"papa johns\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q58a718f693",
  "kind": "yes/no",
  "text": "Customer: That sounds great. I would like 2% milk and no sugar, liquid or from a packet\nAssistant: I can do that. Have you had iced coffee with cinnamon? I always enjoy it\nCustomer: That does sound good. Put a couple shakes of cinnamon in that iced coffee.",
  "question": "In the customer's last message, does \"iced coffee\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qae414be8c7",
  "kind": "yes/no",
  "text": "Assistant: Okay. That is available.\nCustomer: Can I get extra toppings of spinach and bell pepper?\nAssistant: Spinach is not available. Would you like something else?",
  "question": "According to the assistant's last message, is \"Spinach\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q204b1c1562",
  "kind": "yes/no",
  "text": "Assistant: Okay. Placing the order now.\nCustomer: Ok.\nAssistant: 2% milk is no longer available. Would you like to change your order?",
  "question": "According to the assistant's last message, is \"2% milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3de6bfe629",
  "kind": "yes/no",
  "text": "Customer: Yes!\nAssistant: And this order will be placed to your local Pizza Hut.\nCustomer: That is correct. Make sure it is the one on Madison Avenue.",
  "question": "In the customer's last message, does \"Madison Avenue\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q99f850a593",
  "kind": "yes/no",
  "text": "Assistant: I will take your order now.\nCustomer: I want a 14 inch Hawaiian Chicken.\nAssistant: The Hawaiian Chicken is not available tonight.",
  "question": "According to the assistant's last message, is \"Hawaiian Chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q372a332939",
  "kind": "yes/no",
  "text": "Assistant: Okay, I'm making that reservation now.\nCustomer: Thanks\nAssistant: You're all set, a table for 4 at outback on beritennia road, in Honolulu at 7pm.",
  "question": "According to the assistant's last message, is \"beritennia road, in Honolulu\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q69d74d37cd",
  "kind": "yes/no",
  "text": "Customer: Search for Mexican restaurants instead.\nAssistant: I found 12 Mexican restaurants in Berkeley.\nCustomer: Search instead in Oakland.",
  "question": "In the customer's last message, does \"Oakland\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q29c16f90c4",
  "kind": "yes/no",
  "text": "Customer: Hey can you put a pizza order in for me online?\nAssistant: Sure from what place?\nCustomer: You can order from toppers pizza. It's pretty easy online.",
  "question": "In the customer's last message, does \"toppers pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5960970860",
  "kind": "yes/no",
  "text": "Customer: i would like a table for 2\nAssistant: what time\nCustomer: for 5 oclock",
  "question": "In the customer's last message, does \"5 oclock\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q477564e80e",
  "kind": "yes/no",
  "text": "Customer: Large please.\nAssistant: Okay. I think they have different kinds of crust. Do you know what kind you want?\nCustomer: Oh yes. I want the hand tossed garlic seasoned one.",
  "question": "In the customer's last message, does \"hand tossed garlic seasoned\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q78d34a387b",
  "kind": "yes/no",
  "text": "Customer: It is a 2016 Ford Fiesta\nAssistant: Can I get your name please?\nCustomer: My name is Rocky Thrust.",
  "question": "In the customer's last message, does \"Rocky Thrust\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa7c5c6a5c2",
  "kind": "yes/no",
  "text": "Assistant: What time would you like to be picked up at Wake Tech?\nCustomer: We need to leave about 5:00 PM. I'm sure there is going to be traffic.\nAssistant: It looks like the Uber XL won't be available at that time... not until 5:30 pm.",
  "question": "According to the assistant's last message, is \"Uber XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
