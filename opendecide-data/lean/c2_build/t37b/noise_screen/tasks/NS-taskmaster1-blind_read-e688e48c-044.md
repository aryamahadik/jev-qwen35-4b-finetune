# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-044 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-044.json

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
  "qid": "q43731acf5b",
  "kind": "yes/no",
  "text": "Assistant: 6:00 and 9:00\nCustomer: Ok, I'll get two tickets for Captain Marvel in 3D at 6:00 at Pioneer Place Stadium 6 in Portland OR\nAssistant: The 6:00 showing is not in 3D",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q74735eea36",
  "kind": "yes/no",
  "text": "Customer: I'd like to order pickup from the Domino's on 876 Geary Street in San Francisco, California\nAssistant: Sounds good, what kind of pizzas would you like?\nCustomer: I'd like to order one large MeatZZa pizza and a Pacific Veggie of the same size",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qab997a8d01",
  "kind": "yes/no",
  "text": "Customer: Hi I need a ride asap from Ontario to Rancho Cucamonga",
  "question": "In the customer's last message, does \"Ontario\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q74b7cbb5ce",
  "kind": "yes/no",
  "text": "Customer: Hey, can you please make an appointment with a shop for me for my car?\nAssistant: Of course, which car are we talking about?\nCustomer: The 2014 Nissan Altima.",
  "question": "In the customer's last message, does \"2014\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q281599ccdc",
  "kind": "yes/no",
  "text": "Assistant: Okay that showing is IMAX 2D is that okay or did you want to change?\nCustomer: Oh, cool! No you can still purchase those I thought they would have been sold out of those showings by now.\nAssistant: Oh gosh. I spoke too soon. That IMAX2D showing is already sold out. They have one at 6:00pm did you want to change it to that showing?",
  "question": "According to the assistant's last message, is \"IMAX2D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qba3db89806",
  "kind": "yes/no",
  "text": "Assistant: Who would you like to pick your party up.\nCustomer: Lets do a Lyft ride XL ride.\nAssistant: Let me check, there are no Lyft XL rides currently available in your area.",
  "question": "According to the assistant's last message, is \"Lyft XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4b1a0e537f",
  "kind": "yes/no",
  "text": "Customer: Hello Bob. I would like to watch Captain Marvel at the theater. Could you please reserve the movie for me\nAssistant: Well I sure can. What city are do you want?\nCustomer: Sierra Vista",
  "question": "In the customer's last message, does \"Sierra Vista\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q92ba20e7d9",
  "kind": "yes/no",
  "text": "Customer: I want an Iced white chocolate mocha\nAssistant: Did you want a grande, tall?\nCustomer: I'll take a grande",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf8f79ea700",
  "kind": "yes/no",
  "text": "Assistant: All right, sounds good. I'm placing the reservation now.\nCustomer: Read it back to me when you're finished.\nAssistant: All right, all set. You have a booth reservation for two people on Thursday at 8.",
  "question": "According to the assistant's last message, is \"booth\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2d49a9a1b5",
  "kind": "yes/no",
  "text": "Customer: Okay, I'll have something else.\nAssistant: Okay, what shall I order for you instead?\nCustomer: A Blonde Vanilla Latte.",
  "question": "In the customer's last message, does \"Blonde Vanilla Latte\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q86ce790e06",
  "kind": "yes/no",
  "text": "Customer: No, are there any tickets available for Captive State?\nAssistant: Yes, it is available. The showtimes for that movie are 7:30, 8:00 and 9pm\nCustomer: 8pm works for me",
  "question": "In the customer's last message, does \"8pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5c7319b3a7",
  "kind": "yes/no",
  "text": "Customer: Yes, a black and white mocha\nAssistant: Sure. What size.\nCustomer: I'll take a grande.",
  "question": "In the customer's last message, does \"grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3a3bf50c72",
  "kind": "yes/no",
  "text": "Assistant: Same time, place, and seating, outside, Thursday 8PM?\nCustomer: Yes\nAssistant: They also don't have seating outside at that time, but they do have tables inside. Should we go with that or find another place?",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q88d0198cf8",
  "kind": "yes/no",
  "text": "Assistant: How many tickets will you need?\nCustomer: 2, please\nAssistant: Perfect, 2 tickets have been purchased for the 8 P.M. showing of Us at the AMC Classic. I will send the tickets to your phone.",
  "question": "According to the assistant's last message, is \"AMC Classic\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q964fef9303",
  "kind": "yes/no",
  "text": "Assistant: What time is best for you?\nCustomer: Either 4 or 6 pm.\nAssistant: I'm sorry, but it looks like the 4:10 and the 6:10 pm showings are sold out.",
  "question": "According to the assistant's last message, is \"6:10 pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q034a68d24c",
  "kind": "yes/no",
  "text": "Customer: Friday April 5th at 7pm.\nAssistant: How many people should I set the reservation for?\nCustomer: For 5 people please.",
  "question": "In the customer's last message, does \"5\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q07048bf663",
  "kind": "yes/no",
  "text": "Customer: I want a Cinnamon Dolce Latte, please.\nAssistant: Sorry, they said they're out of the dolce syrup that goes in that drink right now. Do you want to try something else?\nCustomer: Yes, that's fine. In that case, I'll just go with an Iced Caffe Mocha.",
  "question": "In the customer's last message, does \"Iced Caffe Mocha\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q99b0febb60",
  "kind": "yes/no",
  "text": "Customer: Nothing, black\nAssistant: Will that be all?\nCustomer: No, how about also two small hot chocolates",
  "question": "In the customer's last message, does \"small\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe71016b1a5",
  "kind": "yes/no",
  "text": "Customer: That sounds fine.\nAssistant: Would you like the same time?\nCustomer: Yes, I'd like a booth for two at 8 p.m. tomorrow",
  "question": "In the customer's last message, does \"two\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q510c738ad0",
  "kind": "yes/no",
  "text": "Assistant: tomorrow 1 PM is available, shall I make this appointment?\nCustomer: yes\nAssistant: your appointment is scheduled at Intelligent Auto Solutions tomorrow 1PM for Toyota Rav4 2017 your estimated cost is $200",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb9547e7f54",
  "kind": "yes/no",
  "text": "Customer: Thats the one\nAssistant: Ok what is your order?\nCustomer: I want a grande cappuchino",
  "question": "In the customer's last message, does \"cappuchino\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb1eae27dc8",
  "kind": "yes/no",
  "text": "Assistant: No problem, I'll order it right now.\nCustomer: Awesome, thanks!\nAssistant: Your drink is on order at the Starbucks in Guntesrville. Your order will ready shortly and your receipt will be texted to your phone.",
  "question": "According to the assistant's last message, is \"Guntesrville\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4bb287c9e5",
  "kind": "yes/no",
  "text": "Customer: Yes, and can you also check if they offer a nice selection of desserts?\nAssistant: Certainly, I see now that there is a booth available by the window.\nCustomer: Wonderful! Is it available at 6:00?",
  "question": "In the customer's last message, does \"6:00\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q717f18371f",
  "kind": "yes/no",
  "text": "Customer: I'd like to buy tickets to Glass.\nAssistant: What city would you like to see it in?\nCustomer: Long Beach",
  "question": "In the customer's last message, does \"Long Beach\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe594354aa0",
  "kind": "yes/no",
  "text": "Customer: Hey! I'm driving and I need you to make an appointment for my car.\nAssistant: Okay, where at?\nCustomer: Make it at the auto repair shop called Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0064d89179",
  "kind": "yes/no",
  "text": "Assistant: Yes, there will be an extra charge for the topping change. Anything else?\nCustomer: Can I have stuffed crust for the other pizza?\nAssistant: No, I'm sorry stuffed crust is not available.",
  "question": "According to the assistant's last message, is \"stuffed crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe904b19d9e",
  "kind": "yes/no",
  "text": "Customer: Is there an extra charge?\nAssistant: No.\nCustomer: Extra thick, then.",
  "question": "In the customer's last message, does \"Extra thick\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2d7dcf6e82",
  "kind": "yes/no",
  "text": "Assistant: Gotcha. I placed the order.\nCustomer: Can you read it back to me?\nAssistant: Your venti latte macchiato with almond milk and honey will be ready in 10 minutes at the Starbucks across the street.",
  "question": "According to the assistant's last message, is \"across the street\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9096a77d83",
  "kind": "yes/no",
  "text": "Assistant: Let me check and see what available time we have.\nCustomer: Sure, take your time.\nAssistant: Upon checking, it looks like 11 a.m. is not available. Is 10:30 a.m. okay?",
  "question": "According to the assistant's last message, is \"11 a.m\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qac17d4d3d0",
  "kind": "yes/no",
  "text": "Assistant: I got the perfect seats! They are $14.79 each, if that okay?\nCustomer: You can' sneak me in as a child can you? I'm kidding. That is fine.\nAssistant: I ordered 2 tickets for Escape at 9:20pm at the AMC Phipps Plaza 14 Seats B6 and B7.",
  "question": "According to the assistant's last message, is \"Escape\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q89437157dd",
  "kind": "yes/no",
  "text": "Assistant: Are there any other specific request before I look for the reservation?\nCustomer: Actually yes, could you find out if the establishment has high chair for kids.\nAssistant: Let's see, the restaurant does have a high chair for kids, but unfortunately all reservations for 7pm are fully booked. Will you like to consider other times?",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4c2c577886",
  "kind": "yes/no",
  "text": "Customer: Oh shoot hold on let me look at the user guide\nAssistant: okay no hurry\nCustomer: alright it is a chevy malibu",
  "question": "In the customer's last message, does \"chevy malibu\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qea492df6a2",
  "kind": "yes/no",
  "text": "Customer: Is the cinnamon dolce lattes available?\nAssistant: Yes it is.\nCustomer: Ok I will take a tall cinnamon dolce latte with almond milk.",
  "question": "In the customer's last message, does \"tall\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfdb030cbed",
  "kind": "yes/no",
  "text": "Assistant: Okay. One moment while I book that for you.\nCustomer: okay, thanks.\nAssistant: No problem, your ride has been booked for 3pm for 4 people.",
  "question": "According to the assistant's last message, is \"3pm\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q08052300fc",
  "kind": "yes/no",
  "text": "Customer: Hello, can you please order me some tickets to Missing Link?\nAssistant: I'd be happy to do that for you. What theater would you like me to order the tickets from?\nCustomer: The WestWind Drive-in in Glendale, Arizona, please.",
  "question": "In the customer's last message, does \"WestWind Drive-in\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbd631dbc1f",
  "kind": "yes/no",
  "text": "Assistant: Okay, I will ask for a short delay.\nCustomer: Use my Visa to pay.\nAssistant: Got it. I've ordered the car and confirmed the fee of $34.37.",
  "question": "According to the assistant's last message, is \"$34.37\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q785aa07f90",
  "kind": "yes/no",
  "text": "Assistant: They have that. Still want a Venti with extra caramel drizzle?\nCustomer: No, can you make it Grande size… definitely still want the extra caramel drizzle though!\nAssistant: Got it. Your Grande Caramel Macchiato with soy milk and extra caramel drizzle was ordered under your account. It’s at the Starbucks on Main St.",
  "question": "According to the assistant's last message, is \"Caramel Macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2699080516",
  "kind": "yes/no",
  "text": "Assistant: Do you want extra cheese or topping?\nCustomer: I want to add banana peppers\nAssistant: Oh, looks like they're out of banana peppers, are green peppers ok?",
  "question": "According to the assistant's last message, is \"banana peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q68103c3d7b",
  "kind": "yes/no",
  "text": "Customer: Great, please go ahead and order a large Pepperoni pizza for me.\nAssistant: No problem. They confirmed your order of a large Pepperoni pizza.\nCustomer: Excellent. Please pay them from my account with Pizza Hut.",
  "question": "In the customer's last message, does \"Pizza Hut\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q85f01c11ea",
  "kind": "yes/no",
  "text": "Customer: Hey! Can you call Intelligent Auto Solutions and make an appointment for me?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1fd2efa968",
  "kind": "yes/no",
  "text": "Assistant: Which option do prefer?\nCustomer: Am okay with uber XL\nAssistant: Uber XL goes for $23.27 to Hell's kitchen but unfortunately it is not available.",
  "question": "According to the assistant's last message, is \"Uber XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc2ab3316a3",
  "kind": "yes/no",
  "text": "Customer: The car when turned on makes a sound along it's fan belt. It has me worried when I hear it.\nAssistant: That seems like it can be a significant issue. What is your car brand?\nCustomer: I am using a Toyota.",
  "question": "In the customer's last message, does \"Toyota\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q92757abfb9",
  "kind": "yes/no",
  "text": "Customer: Hi, can you help me get ticket to Dumbo?",
  "question": "In the customer's last message, does \"Dumbo\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4365742896",
  "kind": "yes/no",
  "text": "Customer: For sure. Please enter my information, I have a 2010 Chevy Tahoe\nAssistant: Ok, got it.\nCustomer: Also, they will want my name and number. Please enter it under Jane Doe and use my home number 999-999-9999",
  "question": "In the customer's last message, does \"Jane Doe\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa605503d02",
  "kind": "yes/no",
  "text": "Customer: Hey can you do me a favor a order me a pizza from Pats?",
  "question": "In the customer's last message, does \"Pats\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q692d7cdf05",
  "kind": "yes/no",
  "text": "Assistant: Okay, one moment\nCustomer: Alright\nAssistant: Okay, I've booked your Uber for 5pm.",
  "question": "According to the assistant's last message, is \"5pm\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q12dd023234",
  "kind": "yes/no",
  "text": "Customer: The account is under my name, phone number 999-999-9999. Let me know when you're ready for my vehicle information\nAssistant: Ok, I have your account pulled up. And your vehicle info?\nCustomer: I have a 2018 GMC Yukon",
  "question": "In the customer's last message, does \"2018\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcf92b5e592",
  "kind": "yes/no",
  "text": "Customer: Hey there! My car is making a funny noise, can you schedule to have it looked at?\nAssistant: Same place as usual?\nCustomer: Intelligent Auto Solutions, yes.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4b1250272c",
  "kind": "yes/no",
  "text": "Customer: My car is leaking a lot of oil and shaking on the highway.\nAssistant: That sounds pretty dangerous, what make and model is it?\nCustomer: 2007 Saturn ES",
  "question": "In the customer's last message, does \"2007\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q67ecd609dd",
  "kind": "yes/no",
  "text": "Customer: Just one other person.\nAssistant: Do you have a preferred theater?\nCustomer: The SouthSide Works Cinema looks nice.",
  "question": "In the customer's last message, does \"SouthSide Works Cinema\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
