# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-041 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-041.json

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
  "qid": "q6338a9f3f9",
  "kind": "yes/no",
  "text": "Assistant: Shall I reserve the table at Avanti\nCustomer: yes\nAssistant: I have confirmed table for 6 at 6 PM tomorrow at Avanti downtown dalls",
  "question": "According to the assistant's last message, is \"downtown dalls\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd1d6b811b4",
  "kind": "yes/no",
  "text": "Customer: I'll be in Washington. We'll be in the Capitol district when I leave work.\nAssistant: Okay, sounds good. Do you know which theatre you want this time? The Landmark, The Burke, or Regal?\nCustomer: The Landmark will be closest I think. We should be able to walk there and take an Uber home afterwards.",
  "question": "In the customer's last message, does \"The Landmark\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6e94e6ddf0",
  "kind": "yes/no",
  "text": "Customer: I would like to order a Iced Caffè Mocha.\nAssistant: Ok, got it, Iced Caffe Mocha from Peets. What size did you want?\nCustomer: Better go with a Large since we have a lot to do today",
  "question": "In the customer's last message, does \"Large\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd7a1a36037",
  "kind": "yes/no",
  "text": "Customer: Need some pizzas for the event\nAssistant: Okay I can help with that\nCustomer: Okay. Can you pull up pizza huts site ?",
  "question": "In the customer's last message, does \"pizza huts\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa7273f27f0",
  "kind": "yes/no",
  "text": "Customer: Yes, a black and white mocha\nAssistant: Sure. What size.\nCustomer: I'll take a grande.",
  "question": "In the customer's last message, does \"grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbc0bf09fe8",
  "kind": "yes/no",
  "text": "Customer: Hello, can you order a pizza from Papa John for me?\nAssistant: Sure, which location do you want?\nCustomer: I want Papa John on New York Street at Aurora.",
  "question": "In the customer's last message, does \"Papa John\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2fbd3e316a",
  "kind": "yes/no",
  "text": "Customer: Let's make it Three Boys from Italy. They're the best.\nAssistant: Okay, great! Which location?\nCustomer: The one on Burke.",
  "question": "In the customer's last message, does \"Burke\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6c21f472b7",
  "kind": "yes/no",
  "text": "Assistant: Ok. What would you like to order?\nCustomer: A large sausage, sundried tomatoes and bell peppers.\nAssistant: Ok, but Pizza Hut does not have sundried tomatoes.",
  "question": "According to the assistant's last message, is \"sundried tomatoes\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qada103e19a",
  "kind": "yes/no",
  "text": "Assistant: Yes, they have an opening at 5:45.\nCustomer: Okay. I think we can make it. Can you request two high chairs?\nAssistant: I'm sorry but they do not have high chairs.",
  "question": "According to the assistant's last message, is \"high chairs\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8f1abec635",
  "kind": "yes/no",
  "text": "Customer: How many people does it feed?\nAssistant: Their menu says it serves 5-6 people.\nCustomer: Yeah let's do the extra large.",
  "question": "In the customer's last message, does \"extra large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfd85f5766c",
  "kind": "yes/no",
  "text": "Assistant: What type of pizza would you like?\nCustomer: I would like the pineapple fresca without ham.\nAssistant: Im sorry, the pineapple fresca is unavailable.",
  "question": "According to the assistant's last message, is \"pineapple fresca\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaff26e0f87",
  "kind": "yes/no",
  "text": "Customer: I need to make a reservation for a restaurant, please\nAssistant: OK sure. Which restaurant?\nCustomer: The Polo Bar at 1 E 55th St",
  "question": "In the customer's last message, does \"The Polo Bar\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7d3fef16ea",
  "kind": "yes/no",
  "text": "Customer: San Diego.\nAssistant: Which theater did you want to see it at?\nCustomer: AMC Fashion Valley 18, please.",
  "question": "In the customer's last message, does \"AMC Fashion Valley 18\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf2bd58a814",
  "kind": "yes/no",
  "text": "Assistant: And do you want any flavoring or sweetener?\nCustomer: Yes, sugar free mocha. And add Stevia.\nAssistant: Unfortunatly they are out of sugar free mocha flavor today. Would you like another flavor?",
  "question": "According to the assistant's last message, is \"sugar free mocha flavor\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q48f2bc4a77",
  "kind": "yes/no",
  "text": "Customer: I need to find a restaurant in Las Vegas for up coming function with the client at the end of the month.",
  "question": "In the customer's last message, does \"Las Vegas\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb370ba6664",
  "kind": "yes/no",
  "text": "Customer: Hey, can you get me two tickets to Pet Sematary?",
  "question": "In the customer's last message, does \"Pet Sematary\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q379449110f",
  "kind": "yes/no",
  "text": "Assistant: Got it. Would you like to add any other flavors, sugar, honey, or whipped cream?\nCustomer: No thanks.\nAssistant: Ok. I'm sorry, it looks like they are out of whole milk. Would you like another type of milk instead?",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd02c674a43",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry but there are not two tickets available at 7pm tonight. Would you like to try another time?\nCustomer: Sure, how about at 6pm?\nAssistant: I'm sorry, but there is no standard viewing at 6pm tonight. Would you like to try another time?",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2489383c3e",
  "kind": "yes/no",
  "text": "Customer: Large, please.\nAssistant: And will that be hand-tossed or thin crust?\nCustomer: Let's go with thin crust this time. Can I get that with the garlic sauce instead of red?",
  "question": "In the customer's last message, does \"thin crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9555886161",
  "kind": "yes/no",
  "text": "Assistant: Absolutely!\nCustomer: Thank you!\nAssistant: Ok I have booked you two tickets to see The Lego movie 2 tonight at 8:05 and you should have received a text for confirmation!",
  "question": "According to the assistant's last message, is \"The Lego movie 2\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5558a01ad1",
  "kind": "yes/no",
  "text": "Assistant: Certainly. Did you want the whip topping on that?\nCustomer: No whip- but ask to have it lightly salted.\nAssistant: I'm sorry, it seems that they are out of the mocha syrup at this time. They do however have the toffee syrup which can offer a similar taste, would that work?",
  "question": "According to the assistant's last message, is \"mocha syrup\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9e36258d73",
  "kind": "yes/no",
  "text": "Assistant: Ok. What name and phone number should I give them?\nCustomer: Leann Goldberg. My number is 616-255-3920.\nAssistant: Ok. You'll be all set. They'll see you at 9AM to see if they can't figure out what is going on with the power steering on your 2015 Ford Mustang. Their inspection fee is $75.",
  "question": "According to the assistant's last message, is \"power steering\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q84e4bfbf9b",
  "kind": "yes/no",
  "text": "Customer: Hello, Kara. I would like to order pizzas from Mellow Mushroom.\nAssistant: Of course - which store do you want to order from?\nCustomer: Let's order from the location in Chapel Hill.",
  "question": "In the customer's last message, does \"Chapel Hill\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfc78adfef2",
  "kind": "yes/no",
  "text": "Customer: For me and a friend, so two\nAssistant: Okay, what time were you thinking?\nCustomer: At 7 o clock would be best",
  "question": "In the customer's last message, does \"7 o clock\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe0a15f066d",
  "kind": "yes/no",
  "text": "Customer: I think 8 would be the best choice, just to be safe.\nAssistant: Okay, great. How many am I buying? Just two for you and your sister?\nCustomer: Yeah, two is fine. We're having a girl's night.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6954e13169",
  "kind": "yes/no",
  "text": "Assistant: And do you want to sit indoors or outdoors?\nCustomer: I want to sit indoors\nAssistant: Okay, I have booked a table for you for 8PM tonight indoors for 2 people",
  "question": "According to the assistant's last message, is \"indoors\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q74900eeb91",
  "kind": "yes/no",
  "text": "Assistant: Reservations for 4 at 7:30 PM on April 5th? and you want a booth?\nCustomer: Yes that's correct.\nAssistant: I'm sorry. All of our booths are in the Sky View room and that room has been reserved for that evening.",
  "question": "According to the assistant's last message, is \"booths\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe3067cfa01",
  "kind": "yes/no",
  "text": "Customer: Yeah, there's an auto body shop called 'Intelligent Auto Solutions' that's been good. Let's go there - you can book online.\nAssistant: Okay one second - what's the make, model, and year of your car?\nCustomer: It's a 2015 Mazda CX-5.",
  "question": "In the customer's last message, does \"2015\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2c5e9d73f7",
  "kind": "yes/no",
  "text": "Customer: Sounds tasty. What kind of food do they have?\nAssistant: They specialize in fondues. They serve cheese, chocolate, and broth fondue, as well as a variety of local and classic dishes.\nCustomer: That sounds so good! Alright, book me a table there on Friday for 6:00 P.M., and make sure it's outside.",
  "question": "In the customer's last message, does \"6:00 P.M\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q745fd39ea4",
  "kind": "yes/no",
  "text": "Assistant: you will need to park the car in the back lot and drop the keys off in the lobby\nCustomer: ok that sounds good\nAssistant: i have your appointment confirmed for 1pm tommorow for the sputtering and stalling of your vehicle and just a reminder the fee for this inspection is 130 dollars",
  "question": "According to the assistant's last message, is \"sputtering and stalling of your vehicle\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf05bc968cc",
  "kind": "yes/no",
  "text": "Assistant: Alright. What toppings would you like?\nCustomer: I would like to have pepperoni, pineapple, and jalapenos.\nAssistant: I'm sorry, but jalapenos are not currently available.",
  "question": "According to the assistant's last message, is \"jalapenos\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdc0b1b3c16",
  "kind": "yes/no",
  "text": "Assistant: Ok so that's two large pepperoni and black olive pizzas, an order of 12 hot wings with ranch dipping sauce, four chocolate lava cakes, and a 2 liter of Coke\nCustomer: That's it.\nAssistant: Just found out they're out of black olives",
  "question": "According to the assistant's last message, is \"black olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qefded33667",
  "kind": "yes/no",
  "text": "Customer: Bob, I need to get an Uber to go over to shopping center on 7th street.\nAssistant: Ok, like right now?\nCustomer: In 15 minutes would be good.",
  "question": "In the customer's last message, does \"15 minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe90b0d6439",
  "kind": "yes/no",
  "text": "Customer: what is the closet hours available\nAssistant: there is one playing at 7:30 and one playing at 9:00\nCustomer: let's get the ticket for the 9:00",
  "question": "In the customer's last message, does \"9:00\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8a56063fc8",
  "kind": "yes/no",
  "text": "Assistant: Yes, is there anything else wrong with the car?\nCustomer: No, that is the immediate concern.\nAssistant: OK, we have you booked for an appointment today at noon, for your alternator issue for your 2009 Honda Pilot.",
  "question": "According to the assistant's last message, is \"Honda Pilot\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q05381928ce",
  "kind": "yes/no",
  "text": "Assistant: I will make that request for you.\nCustomer: Great.\nAssistant: Okay, I've made the reservation for 3 at Schmidt and Mccormick on S. Broad St., Philadelphia, PA for tomorrow at 8PM.",
  "question": "According to the assistant's last message, is \"S. Broad St., Philadelphia, PA\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q24f6629ec4",
  "kind": "yes/no",
  "text": "Assistant: What time are you looking to reserve for?\nCustomer: I would say 6pm\nAssistant: Let's see, we have nothing available for 6pm, would you try another time?",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1cbb4b742e",
  "kind": "yes/no",
  "text": "Customer: hsve them pick me up at the american legion and take me to longhorns in griffin\nAssistant: what time would you like the car here\nCustomer: have them arrive at 6 p.m.",
  "question": "In the customer's last message, does \"6 p.m\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qefb1ceccee",
  "kind": "yes/no",
  "text": "Customer: That one is going to be pepperoni and jalapenos.\nAssistant: Got it, and what else?\nCustomer: The second one will be a medium deep dish.",
  "question": "In the customer's last message, does \"medium\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q16f9e05cf3",
  "kind": "yes/no",
  "text": "Assistant: You're welcome. Anything else?\nCustomer: No, that's all.\nAssistant: Okay. You're all set! Great. You can drop off your 2013 Honda Civic at Intelligent Auto Solutions tonight at 6pm. There's a $10 inspection fee as well.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc986c97b81",
  "kind": "yes/no",
  "text": "Customer: I was thinking Chinese or Mexican.\nAssistant: What city are you located in?\nCustomer: Port Huron, Michigan",
  "question": "In the customer's last message, does \"Port Huron, Michigan\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q53ccac531d",
  "kind": "yes/no",
  "text": "Assistant: Extra cheese is two dollars more.\nCustomer: That's fine. Please order the extra cheese.\nAssistant: You got it. I've ordered a large pepperoni and mushroom pan pizza with extra cheese, from the Oregano's on Speedway and Swan, in Tucson, Arizona.",
  "question": "According to the assistant's last message, is \"Speedway and Swan, in Tucson, Arizona\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q643943236b",
  "kind": "yes/no",
  "text": "Customer: That sounds pretty good. But I'm kind of feeling like pepperoni and mushrooms. Besides, my wife hates sausage on her pizza.\nAssistant: Okay, just let me know what to order and when.\nCustomer: You can place an order on the Johnny's website. It's super easy.",
  "question": "In the customer's last message, does \"Johnny's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q64c2383766",
  "kind": "yes/no",
  "text": "Customer: Hey, I want to order the heart shaped pizza from Donates.\nAssistant: Which Donatos did you have in mind?\nCustomer: The one at 6965 E Broad St, Columbus, OH.",
  "question": "In the customer's last message, does \"6965 E Broad St, Columbus, OH\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb047a289fb",
  "kind": "yes/no",
  "text": "Customer: I want to order a pizza from pizza hut.",
  "question": "In the customer's last message, does \"pizza hut\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q13891024e8",
  "kind": "yes/no",
  "text": "Customer: Yes, I'll need it delivered around 8 pm.\nAssistant: Do you want it from the Westside location or the Eastside location?\nCustomer: Eastside, it will be faster.",
  "question": "In the customer's last message, does \"Eastside\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4e53883aed",
  "kind": "yes/no",
  "text": "Customer: The Broadway location\nAssistant: You got it.\nCustomer: I would like an large cheese and mushroom and green pepper",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe1f9fb70c3",
  "kind": "yes/no",
  "text": "Assistant: Let me check and see what available time we have.\nCustomer: Sure, take your time.\nAssistant: Upon checking, it looks like 11 a.m. is not available. Is 10:30 a.m. okay?",
  "question": "According to the assistant's last message, is \"11 a.m\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q389c02146b",
  "kind": "yes/no",
  "text": "Customer: I want to order 2 pizzas from Rosatti's.",
  "question": "In the customer's last message, does \"Rosatti's\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q84e37e66aa",
  "kind": "yes/no",
  "text": "Assistant: any other requests?\nCustomer: we want to sit in the garden area.\nAssistant: Sorry, it looks like there's no seating at 7:00, would you like to try another time?.",
  "question": "According to the assistant's last message, is \"7:00\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
