# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-001 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-001.json

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
  "qid": "q941f3720ba",
  "kind": "yes/no",
  "text": "Customer: Hi. Can you please help me book an appointment to get my car fixed?\nAssistant: Sure! What shop do you want to take it to?\nCustomer: Intelligent Auto Solutions on Main Street.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe848c0471f",
  "kind": "yes/no",
  "text": "Customer: I was thinking a jumbo thin slice pizza.\nAssistant: They only do small, medium, or large and it's regular crust.\nCustomer: Oh, okay. How about a large? With extra cheese!",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q94a4ffbe82",
  "kind": "yes/no",
  "text": "Customer: in the afternoon\nAssistant: there is an appointment available the day after tomorrow at 4 pm\nCustomer: that sounds good, can you also add in a wheel alignment for me",
  "question": "In the customer's last message, does \"wheel alignment\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q49ef80625f",
  "kind": "yes/no",
  "text": "Customer: The front headlight needs replaced and fender has damage.\nAssistant: Okay can I have the year, make & model of your vehicle?\nCustomer: It's a 1977 Ford Maverick.",
  "question": "In the customer's last message, does \"1977\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0ec9b73916",
  "kind": "yes/no",
  "text": "Customer: It seems like something just came up and I will not be able to leave the restaurant for another hour.\nAssistant: Okay, so what time would you like me to arrange the trip.\nCustomer: Arrange the trip for 9pm pickup.",
  "question": "In the customer's last message, does \"9pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbbd845e974",
  "kind": "yes/no",
  "text": "Customer: I want a golden caffe latte.\nAssistant: What size would you like?\nCustomer: Better make it a medium.",
  "question": "In the customer's last message, does \"medium\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc4d4e19f59",
  "kind": "yes/no",
  "text": "Assistant: $10 each.\nCustomer: Use my account to order them.\nAssistant: Alright, your tickets for The Lego Movie 2 at 7PM tonight at Cinemark Mall St. Matthews have been ordered.",
  "question": "According to the assistant's last message, is \"Cinemark Mall St. Matthews\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfd18cb7cf2",
  "kind": "yes/no",
  "text": "Customer: I want the thick crust.\nAssistant: You mean deep dish?\nCustomer: Yes! That's it. Deep dish.",
  "question": "In the customer's last message, does \"Deep dish\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe7765ef305",
  "kind": "yes/no",
  "text": "Customer: I need you to let them know that my 2014 Chevrolet Malibu has been pulling to the left when I''m driving.\nAssistant: Okay. Do you have a certain time you want to make the appointment for?\nCustomer: Yes. Tomorrow morning would be the best. Give them my name: Julie McMahon and phone number 307-555-5555 also",
  "question": "In the customer's last message, does \"Julie McMahon\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q571c23f68d",
  "kind": "yes/no",
  "text": "Customer: Lisa can you call Uber for me and see if they have a Uber Pool available to take me from Union square to the children's interactive museum Please\nAssistant: Sure, you want me to call Uber for you and get a Pool ride from Union Square to the Children's interactive museum\nCustomer: Yes, please, and I will need the pick up time to be at 2:00 pm",
  "question": "In the customer's last message, does \"2:00 pm\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q00c00e05c2",
  "kind": "yes/no",
  "text": "Assistant: Do you want to order anything else?\nCustomer: One Blueberry Muffin would be great.\nAssistant: Ok, your order is on Blueberry Muffin, Caramel Brulee Latte tall, with 2% milk and whipped cream.",
  "question": "According to the assistant's last message, is \"Caramel Brulee Latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q68aac653da",
  "kind": "yes/no",
  "text": "Customer: Yes, please.\nAssistant: Ok, when do you want to go?\nCustomer: Make it for this upcoming Saturday at 6PM. Two people. I would like patio seating.",
  "question": "In the customer's last message, does \"6PM\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbcd4f128a4",
  "kind": "yes/no",
  "text": "Assistant: Okay, sounds good. I'm going to give them a call now.\nCustomer: Thank you.\nAssistant: Bad news, they don't have pepperoni.",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf666f3b254",
  "kind": "yes/no",
  "text": "Assistant: Ok perfect. Ordering now.\nCustomer: Ok thank you.\nAssistant: Bad news. They're out of artichokes today. Delivery didn't come in.",
  "question": "According to the assistant's last message, is \"artichokes\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q21bc5ec0ff",
  "kind": "yes/no",
  "text": "Customer: no, that's too late, how about The Antique Rose?\nAssistant: They can't seat 8 at all Friday night.\nCustomer: What about The French Hen?",
  "question": "In the customer's last message, does \"The French Hen\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa1b8552e3b",
  "kind": "yes/no",
  "text": "Customer: I would like to take my son to watch a movie tonight.\nAssistant: That sounds like a blast! What movie did you have in mind?\nCustomer: Well we really would like to see Captain Marvel. He is also a little interested in watching the new Dumbo movie.",
  "question": "In the customer's last message, does \"Dumbo\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q451626fb35",
  "kind": "yes/no",
  "text": "Customer: Are there any BBQ restaurants near me?\nAssistant: Where are you looking to find a restaurant?\nCustomer: Rochester, NY",
  "question": "In the customer's last message, does \"Rochester, NY\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe1f2880c32",
  "kind": "yes/no",
  "text": "Customer: i would like you to order a Caramel Cloud Macchiato from starbucks please",
  "question": "In the customer's last message, does \"Caramel Cloud Macchiato\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7823dd1074",
  "kind": "yes/no",
  "text": "Assistant: what name do you want to use for the appointment\nCustomer: bond, contact number 6666666\nAssistant: the appointment is set for 4 pm today as you wanted at intelligent auto solution, the estimated fee for windshild replacement is 2000",
  "question": "According to the assistant's last message, is \"intelligent auto solution\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe9970ad9b0",
  "kind": "yes/no",
  "text": "Customer: I need to be taken to JFK airport.\nAssistant: When do you want to be picked up?\nCustomer: I will be ready in fifteen minutes from now.",
  "question": "In the customer's last message, does \"fifteen minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7ec5841133",
  "kind": "yes/no",
  "text": "Assistant: How about Cowboy Star? When would you like to come in?\nCustomer: This Saturday at 8 PM\nAssistant: Unfortunately, this Saturday we don't have anything at 8 PM",
  "question": "According to the assistant's last message, is \"8 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa82b3983cb",
  "kind": "yes/no",
  "text": "Assistant: The pacific veggie pizza contains:Roasted red peppers, fresh baby spinach, fresh onions, fresh mushrooms, tomatoes, black olives, feta, provolone, and mozzarella. confirm?\nCustomer: confirmed.\nAssistant: they seem to be all out of black olives at the moment.",
  "question": "According to the assistant's last message, is \"black olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9d5f897438",
  "kind": "yes/no",
  "text": "Customer: I need to get an oil change next week.\nAssistant: Which car needs the oil change?\nCustomer: I would like to get the oil change on my 2014 BMW M3",
  "question": "In the customer's last message, does \"2014\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q32737ef1b3",
  "kind": "yes/no",
  "text": "Assistant: okay what toppings\nCustomer: pepperoni and ham\nAssistant: sorry ham is not available",
  "question": "According to the assistant's last message, is \"ham\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q568618829d",
  "kind": "yes/no",
  "text": "Assistant: I will check again for you\nCustomer: Great thank you\nAssistant: Unfortunately sir firebirds is still not available",
  "question": "According to the assistant's last message, is \"firebirds\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0a29f53b76",
  "kind": "yes/no",
  "text": "Customer: I need to see about an Uber\nAssistant: I can help you. Where are you going from and to?\nCustomer: I am at SFO and need a ride to the Fairmont.",
  "question": "In the customer's last message, does \"Fairmont\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1ae26eb309",
  "kind": "yes/no",
  "text": "Customer: Good evening. I'd like to order a pizza tonight.\nAssistant: Yes, sir. Where would you like to order from?\nCustomer: I think we'll try Sonny's tonight.",
  "question": "In the customer's last message, does \"Sonny's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf2cbe0134b",
  "kind": "yes/no",
  "text": "Assistant: OK. What would you like to order?\nCustomer: Can I get a deep dish pizza with Spinach and Goat Cheese?\nAssistant: Auggie's Pizzeria does not have Goat Cheese.",
  "question": "According to the assistant's last message, is \"Goat Cheese\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcc422a21d1",
  "kind": "yes/no",
  "text": "Customer: what is the showtimes of the movie\nAssistant: that was having three showtimes 10.15 pm, 10.00 pm, and 10.20 pm\nCustomer: Ok Book my tickets on 10.15 pm show",
  "question": "In the customer's last message, does \"10.15 pm\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0bd25dc540",
  "kind": "yes/no",
  "text": "Customer: I would like a Golden Cold Brew Fog Latte\nAssistant: What size?\nCustomer: Large, please",
  "question": "In the customer's last message, does \"Large\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd74186e5b6",
  "kind": "yes/no",
  "text": "Customer: Yes, that's kind of disappointing but OK.\nAssistant: And lastly, ticket prices. Tickets for the PM showings are 12.50 per person.\nCustomer: That's fine, and can you get tickets for four adults?",
  "question": "In the customer's last message, does \"four\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2ef733b914",
  "kind": "yes/no",
  "text": "Assistant: What contact information would you like me to provide?\nCustomer: Please provide may cellphone number 919-905-9000 under Brett Carmichael\nAssistant: Great. Looks like the initial estimate for the appointment is $150 and I have you confirmed for today at 6PM.",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q64abcb8f7c",
  "kind": "yes/no",
  "text": "Assistant: Is there any information I should add to the reservation note?\nCustomer: It is my friend's birthday.\nAssistant: Got it. Your reservation for 4 people at 6:45pm at Tamarind Tree on 2/28 is confirmed.",
  "question": "According to the assistant's last message, is \"Tamarind Tree\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q78e734604b",
  "kind": "yes/no",
  "text": "Customer: My car engine light just came on telling me I need to have my car scheduled for an appointment. Can you schedule the appointment with Intelligent Auto Solutions?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q52ff202b6c",
  "kind": "yes/no",
  "text": "Assistant: Yes. Sandwiches and Burgers and Wings, etc\nCustomer: Okay. Can you book me for dinner there on the 26th at 6PM?\nAssistant: Yes, but outdoor seating is not available for 6pm?",
  "question": "According to the assistant's last message, is \"outdoor seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe291f972b6",
  "kind": "yes/no",
  "text": "Customer: Get me two tickets for Hellboy tonight.\nAssistant: What city were you thinking of watching the movie?\nCustomer: My friend lives in Orange, I think they have an AMC theater over there can you look up the address.",
  "question": "In the customer's last message, does \"AMC theater\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q334e2c33f9",
  "kind": "yes/no",
  "text": "Assistant: Confirming you want one large single crust hawaiian pizza, for pickup from Oley's Highway 24 location in about 25 minutes.\nCustomer: Confirmed.\nAssistant: OK. I have completed this order. It will be ready for pickup in about 25 minutes at the Highway 24 location.",
  "question": "According to the assistant's last message, is \"Highway 24\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa03563891e",
  "kind": "yes/no",
  "text": "Customer: Hello, I'd like you to order me an Uber.\nAssistant: Where will you need to be picked up and where will you be heading?\nCustomer: I'm at work in Charlotte and would like to go to the Cinemark in Matthews.",
  "question": "In the customer's last message, does \"Cinemark in Matthews\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc9fa3c8923",
  "kind": "yes/no",
  "text": "Customer: Hey Amanda, I'm having some issues with my car on my way to work today can you make me an appointment with the shop?\nAssistant: I absolutely can! Which shop do you prefer?\nCustomer: I went to Intelligent Auto Solutions last time and they did a wonderful job can you see if there are any openings today?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdc95bda9df",
  "kind": "yes/no",
  "text": "Customer: MKE International Airport.\nAssistant: Where will you be going to?\nCustomer: The Up & Under Pub on East Brady Street in Milwaukee.",
  "question": "In the customer's last message, does \"The Up & Under Pub on East Brady Street in Milwaukee\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q80f5982233",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry, the first available seating is at 9pm\nCustomer: Take that then\nAssistant: I've set up your reservation at The Pirani for a party of 4 at 9pm on Thursday.",
  "question": "According to the assistant's last message, is \"The Pirani\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0403b90e82",
  "kind": "yes/no",
  "text": "Customer: Hello, can you book a table for me for this Friday night?\nAssistant: Sure, which restaurant do you prefer?\nCustomer: Royal Buffet at Hoffman Estates.",
  "question": "In the customer's last message, does \"Hoffman Estates\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcb5303bc8f",
  "kind": "yes/no",
  "text": "Customer: Then let me order a Cinnamon Shortbread Creme, grande sized with whole milk.\nAssistant: Okay, is there anything else you would like to order?\nCustomer: Also, can I get a grande Triple Mocha Frappucino, with whole milk.",
  "question": "In the customer's last message, does \"Triple Mocha Frappucino\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q016a482348",
  "kind": "yes/no",
  "text": "Assistant: Ok, are their any special requests for this reservation?\nCustomer: No thank you.\nAssistant: Sorry it looks like 5pm is all booked, would you be interested in another time slot?",
  "question": "According to the assistant's last message, is \"5pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8817b5be2b",
  "kind": "yes/no",
  "text": "Assistant: Let me go and check.\nCustomer: Thanks\nAssistant: I cannot do 1:30, but there is a 2:00 would that work?",
  "question": "According to the assistant's last message, is \"1:30\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd510dbb143",
  "kind": "yes/no",
  "text": "Assistant: Will that be a large pizza?\nCustomer: Yes, of course.\nAssistant: They are out of sausage. Would you like something else.",
  "question": "According to the assistant's last message, is \"sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q772aec2d40",
  "kind": "yes/no",
  "text": "Assistant: Please confirm that you accept the initial inspection fee of $100\nCustomer: Confirmed.\nAssistant: You are confirmed for 9:30am drop off tomorrow with a $100 inspection fee.",
  "question": "According to the assistant's last message, is \"9:30am\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6c3bac4d3c",
  "kind": "yes/no",
  "text": "Assistant: We have soy, and coconut milk.\nCustomer: Is soy milk available?\nAssistant: Im sorry, soy is unavailable.",
  "question": "According to the assistant's last message, is \"soy\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2a5ccc3bcb",
  "kind": "yes/no",
  "text": "Customer: How about this Saturday at 7 pm?\nAssistant: I'm sorry, it seems like they're all booked at that time.\nCustomer: How about 6 pm?",
  "question": "In the customer's last message, does \"6 pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb7192e5abf",
  "kind": "yes/no",
  "text": "Customer: I'd like to buy tickets for The Lego Movie 2 tonight please",
  "question": "In the customer's last message, does \"The Lego Movie 2\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
