# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-053 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-053.json

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
  "qid": "qa49d9b5db6",
  "kind": "yes/no",
  "text": "Assistant: To confirm, I've got one grande gingerbread latte with soy milk and extra whipped cream. Is that right?\nCustomer: Yes.\nAssistant: I have place the order and it will be ready for pickup shortly at the Starbucks on 1134 Lancaster Dr, Salem, Oregon.",
  "question": "According to the assistant's last message, is \"1134 Lancaster Dr, Salem, Oregon\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdcc49e6aff",
  "kind": "yes/no",
  "text": "Assistant: ok a regular Lyft personal ride it is. what time would you like to be picked up.\nCustomer: I'm ready now.\nAssistant: Alright, I have ordered you a regular Lyft for pickup now at the Oakland Civic Center going to the Oakland Airport",
  "question": "According to the assistant's last message, is \"regular Lyft\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdbf43324cf",
  "kind": "yes/no",
  "text": "Customer: Thank you.\nAssistant: Hello there. I hate to inform you, but they are out of the gluten free crust as well as pineapples of all things.\nCustomer: Let's see, a thin hand tossed crust then, and what kind of fruits do they have?",
  "question": "In the customer's last message, does \"thin hand tossed crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3042698275",
  "kind": "yes/no",
  "text": "Assistant: Do you want me to book it?\nCustomer: Yes please.\nAssistant: Okay, I just booked you two reserved seats for 7:30pm for Hellboy tonight. The tickets are going to be sent to your phone.",
  "question": "According to the assistant's last message, is \"Hellboy\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q921c4b2229",
  "kind": "yes/no",
  "text": "Customer: Hmm.. how about an iced vanilla latte instead?\nAssistant: Sure. What size?\nCustomer: Grande please.",
  "question": "In the customer's last message, does \"Grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qebddc24c0b",
  "kind": "yes/no",
  "text": "Assistant: there's a problmem wi that order\nCustomer: Go ahead\nAssistant: The taco pizz was seasonal. no longer available",
  "question": "According to the assistant's last message, is \"taco pizz\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qea485ba105",
  "kind": "yes/no",
  "text": "Assistant: It's a PG rated film, so very safe for the kid you're bringing.\nCustomer: I thought so! I just wanted to make sure!\nAssistant: Alright then, you're all set. Three tickets have been booked for the 6:50 showing at Menomonie 7 Theaters, and a confirmation and the tickets are on their way to your email.",
  "question": "According to the assistant's last message, is \"Menomonie 7 Theaters\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6ea9681e36",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry but there are not two tickets available at 7pm tonight. Would you like to try another time?\nCustomer: Sure, how about at 6pm?\nAssistant: I'm sorry, but there is no standard viewing at 6pm tonight. Would you like to try another time?",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfed4eb7519",
  "kind": "yes/no",
  "text": "Assistant: Would you like whipped cream?\nCustomer: no\nAssistant: I am sorry, they are all out of sugar free syrup.",
  "question": "According to the assistant's last message, is \"sugar free syrup\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qed8457544c",
  "kind": "yes/no",
  "text": "Assistant: Okay. One moment while I confirm\nCustomer: Thank you\nAssistant: Your appointment is for a 20,000 mile checkup tomorrow afternoon at 3pm. I have your name as Suzy Q and your phone number as 555 555-5555",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qeed0a23a9e",
  "kind": "yes/no",
  "text": "Assistant: Alright, great. Would you like any special food\nCustomer: We will just be getting popcorn\nAssistant: Alright great. The total price for your tickets will be 20$",
  "question": "According to the assistant's last message, is \"20$\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbfc96dfb5f",
  "kind": "yes/no",
  "text": "Assistant: It should be about 25 minutes. Is there anything else?\nCustomer: No, but can I get a confirmation of my order.\nAssistant: Sure, you're order of one large pizza with mushrooms and black olives will be ready for pickup in 25 minutes at Dion's. A receipt will be sent to you via text message at the number provided.",
  "question": "According to the assistant's last message, is \"black olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qca7c3991a7",
  "kind": "yes/no",
  "text": "Customer: Try Intelligent Auto Solutions they have a good online interface.\nAssistant: It needs your car's make.\nCustomer: It's a Kia.",
  "question": "In the customer's last message, does \"Kia\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9a5c5471fa",
  "kind": "yes/no",
  "text": "Assistant: Great. I'll book it right now.\nCustomer: Perfect.\nAssistant: It appears there are no Select cars currently available.",
  "question": "According to the assistant's last message, is \"Select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q09b58e1a38",
  "kind": "yes/no",
  "text": "Assistant: So you want the heart shaped pizza with bruschetta fresh tomato, fresh mozzarella, and spinach?\nCustomer: That is correct.\nAssistant: Your total comes to $11.26 your order has been placed and will be ready for pickup in 25 minutes at 6965 E Broad St, Columbus, OH.",
  "question": "According to the assistant's last message, is \"6965 E Broad St, Columbus, OH\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd57e348eaf",
  "kind": "yes/no",
  "text": "Assistant: Ok, Bern's Steakhouse dinner for 2 for 7:00 tomorrow night, right?\nCustomer: You got it!\nAssistant: Ok, one small problem, they don't have anything available for 7:00, will 8:00 be ok?",
  "question": "According to the assistant's last message, is \"7:00\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa0d7f2885e",
  "kind": "yes/no",
  "text": "Assistant: Perfect, It looks like it's going to be about $25 to get everyone to Megan's house. Since you live right down the road it shouldn't cost too much more. I'll get it set up for you now.\nCustomer: Great! Tell them to hurry, these girls are getting rowdy.\nAssistant: They are on the way, should be to you in four minutes.",
  "question": "According to the assistant's last message, is \"four minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfa5a856fb0",
  "kind": "yes/no",
  "text": "Assistant: What name and phone number would you like on the reservation?\nCustomer: Natalie Brandon. My number is 616-229-6112.\nAssistant: Great. You're all set for 4pm with your 2018 Jeep Grand Cherokee. Just so you know the inspection fee is $100.",
  "question": "According to the assistant's last message, is \"Jeep Grand Cherokee\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q903bd74076",
  "kind": "yes/no",
  "text": "Assistant: Do you want whipped cream?\nCustomer: Yes, definitely.\nAssistant: Okay, I've ordered a grande Caffe Mocha for you from the Starbucks on 5th and Main. It will be available to be picked up shortly.",
  "question": "According to the assistant's last message, is \"Caffe Mocha\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaab1819614",
  "kind": "yes/no",
  "text": "Customer: I did, thanks. Is it playing around 6 pm tonight?\nAssistant: Unfortunately, no. There's a screening at 5:30 and another at 7.\nCustomer: Darn. Ok, 7:30 pm it is then.",
  "question": "In the customer's last message, does \"7:30 pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q01644a03d6",
  "kind": "yes/no",
  "text": "Customer: Get me a Iced Peppermint White Chocolate Mocha.\nAssistant: What size?\nCustomer: Grande. And I want it with whole milk",
  "question": "In the customer's last message, does \"Grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q366a0f4aec",
  "kind": "yes/no",
  "text": "Customer: Make sure to ask them to hold the whipped cream.\nAssistant: I'm sorry, but it turns out Starbucks on High is out of the Caramel Macchiato. It seems to be popular this time of year.\nCustomer: That's ok. Can you ask them if they have the Cinnamon Cloud Macchiato?",
  "question": "In the customer's last message, does \"Cinnamon Cloud Macchiato\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe9edb06d38",
  "kind": "yes/no",
  "text": "Customer: Assistant, can you buy tickets for Pet Semetary?\nAssistant: Sure, what movie theater?\nCustomer: Well I'm actually in Chicago this weekend... so somewhere here.",
  "question": "In the customer's last message, does \"Chicago\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q15102efd3a",
  "kind": "yes/no",
  "text": "Customer: Perfect, can you please order me a drink?\nAssistant: Yes, what would you like?\nCustomer: Can you order me an iced Americano with 3 pumps syrup and coconut milk?",
  "question": "In the customer's last message, does \"iced Americano\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa6e5ac5e61",
  "kind": "yes/no",
  "text": "Customer: I am looking for a solid bistro in columbus ohio for 7PM tomorrow.",
  "question": "In the customer's last message, does \"7PM\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3eb6cc0f25",
  "kind": "yes/no",
  "text": "Assistant: Yeah, no problem, I will charge your Visa on file\nCustomer: Yes, please\nAssistant: Ok, all set, I have that order placed with the Diamond st Starbucks. Your Java Chip should be ready in just a few minutes.",
  "question": "According to the assistant's last message, is \"Diamond st\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3c5227ce4f",
  "kind": "yes/no",
  "text": "Assistant: OK. I'll place the order.\nCustomer: Thanks. Let me know what time to pick it up.\nAssistant: Sambino's is out of mushrooms. Would you like a different topping?",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6d881e0d54",
  "kind": "yes/no",
  "text": "Customer: It's a 2014 Chevrolet Cruise, Black.\nAssistant: Alright, what name and number should I give them?\nCustomer: Samantha, 942-203-4918",
  "question": "In the customer's last message, does \"Samantha\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q41a882920f",
  "kind": "yes/no",
  "text": "Customer: sometime tonight.\nAssistant: There are showings in XD at 4:00pm, 7:00pm and 10:05pm at the century 25\nCustomer: oh cool, get me 2 tickets to the 7:00pm showing.",
  "question": "In the customer's last message, does \"2\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9a3ff1a536",
  "kind": "yes/no",
  "text": "Customer: I'm going to be flying Virgin America.\nAssistant: Great. Now, what time do you need to be picked up.\nCustomer: I need to be picked up no later than 2 pm.",
  "question": "In the customer's last message, does \"2 pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8ddeb1bb61",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry, they are all out of banana peppers. Would you like to try adding another topping?\nCustomer: A little bit of pineapple.\nAssistant: Pineapple is unavailable as well.",
  "question": "According to the assistant's last message, is \"Pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q48d80466db",
  "kind": "yes/no",
  "text": "Customer: We're at a restaurant called Milos, in Downtown Los Angeles.\nAssistant: Where are you going?\nCustomer: The gallery is called Gallery Nucleus.",
  "question": "In the customer's last message, does \"Gallery Nucleus\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8c3f8f6c45",
  "kind": "yes/no",
  "text": "Customer: I would like one of their Hawaiian pizzas.\nAssistant: All right. Do you want the thin or thick crust?\nCustomer: Thick. And I want to make a change in the toppings.",
  "question": "In the customer's last message, does \"Thick\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe38b54b46a",
  "kind": "yes/no",
  "text": "Assistant: They have booths. Do you want to be on the main dining floor or in the bar area.\nCustomer: I think the main floor would be best.\nAssistant: Ok. I have you set up for a booth on the main floor at 6PM.",
  "question": "According to the assistant's last message, is \"booth on the main floor\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc6284d66a6",
  "kind": "yes/no",
  "text": "Customer: Hello, can you run by Starbucks and pick up a coffee for me?\nAssistant: Sure thing, your usual?\nCustomer: Yes, the Cafe Latte",
  "question": "In the customer's last message, does \"Cafe Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2692ecc312",
  "kind": "yes/no",
  "text": "Assistant: Anything else\nCustomer: That should do it.\nAssistant: Your order has been place for a grande Caffe Mocha extra hot with coconut milk and whipped cream",
  "question": "According to the assistant's last message, is \"whipped cream\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdaf1058bcf",
  "kind": "yes/no",
  "text": "Customer: Assistant, please schedule a service appointment for my car at Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8fd67ed111",
  "kind": "yes/no",
  "text": "Assistant: The restaurant does not have green peppers. Would you like to change your order?\nCustomer: Yes, instead of green peppers, I would like yellow peppers instead.\nAssistant: The restaurant is out of yellow peppers. Would you like to change your order?",
  "question": "According to the assistant's last message, is \"yellow peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6fb29325ee",
  "kind": "yes/no",
  "text": "Customer: How Captian Marvel at 2pm?\nAssistant: Which location?\nCustomer: Van Nuys",
  "question": "In the customer's last message, does \"Van Nuys\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6c2bcfdf99",
  "kind": "yes/no",
  "text": "Customer: I have my Visa debit card handy if you take debit.\nAssistant: That works just as well.\nCustomer: Okay, and do they provide any other amenities at Saint James theater?",
  "question": "In the customer's last message, does \"Saint James theater\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q48d7d29316",
  "kind": "yes/no",
  "text": "Customer: Okay, can I please get it for 9:00 pm?\nAssistant: All the showings are sold out for today at that movie theater.\nCustomer: What about the screening for 8:00 pm at AMC DINE-IN 600 North Michigan 9?",
  "question": "In the customer's last message, does \"AMC DINE-IN 600 North Michigan 9\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd947dadc38",
  "kind": "yes/no",
  "text": "Assistant: Shall I reserve the table at Avanti\nCustomer: yes\nAssistant: I have confirmed table for 6 at 6 PM tomorrow at Avanti downtown dalls",
  "question": "According to the assistant's last message, is \"downtown dalls\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4c16fc4f5d",
  "kind": "yes/no",
  "text": "Assistant: What would you like on your Maddy Pizza?\nCustomer: Please add tomotoes and green peppers.\nAssistant: Mod Pizza does not have green peppers. Can I offer you something else?",
  "question": "According to the assistant's last message, is \"green peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qece210f6f2",
  "kind": "yes/no",
  "text": "Assistant: Ok let me try to place the order.\nCustomer: Ok thanks.\nAssistant: Ok they do not have any more vanilla flavor. Would you like another flavor",
  "question": "According to the assistant's last message, is \"vanilla flavor\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q710d2b9f10",
  "kind": "yes/no",
  "text": "Customer: I'd like you to order a pizza for my family's dinner tonight.\nAssistant: Ok, where would you like me to order it from?\nCustomer: How about Domino's Pizza tonight.",
  "question": "In the customer's last message, does \"Domino's Pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q26ae5b78d8",
  "kind": "yes/no",
  "text": "Assistant: Okay, a booth for 5, at 8 pm correct?\nCustomer: Yep! That's right.\nAssistant: Alright, you're all set. Keglers at 8 pm, with a booth for 5!",
  "question": "According to the assistant's last message, is \"Keglers\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4ddccb8e78",
  "kind": "yes/no",
  "text": "Assistant: Ok. there is an initial inspection fee of $100 is this ok?\nCustomer: Yes\nAssistant: Ok appointment booked for 2/15 12pm for john smith. phone number 888-888-8888. 2018 Subaru wrx, hard start issue",
  "question": "According to the assistant's last message, is \"hard start issue\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdc1c3822c3",
  "kind": "yes/no",
  "text": "Customer: It's stalled on me a few times while at stoplights, it's pretty scary.\nAssistant: Okay, what is the car make and model, and year?\nCustomer: It's a 2003 Chrysler PT Cruiser.",
  "question": "In the customer's last message, does \"2003\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa54b86ae0e",
  "kind": "yes/no",
  "text": "Customer: Oh man! I totally forgot, I need to order pizza's for Benji's birthday party tonight. I'll order a few large pizza's from Town Pizza. Hi, Cheryl. I need you to order a few pizzas for Benji's birthday party tonight.",
  "question": "In the customer's last message, does \"Town Pizza\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7782a615c9",
  "kind": "yes/no",
  "text": "Customer: Hello Sara can you make a pick up order from Hungry Howies for me for dinner with the family tonight?",
  "question": "In the customer's last message, does \"Hungry Howies\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
