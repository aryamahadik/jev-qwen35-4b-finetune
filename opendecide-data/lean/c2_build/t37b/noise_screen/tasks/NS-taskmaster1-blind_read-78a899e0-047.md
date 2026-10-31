# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-047 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-047.json

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
  "qid": "q1a0f2e5a1e",
  "kind": "yes/no",
  "text": "Customer: A medium.\nAssistant: Alright! What type of crust are you looking to get?\nCustomer: Just the standard garlic butter kind.",
  "question": "In the customer's last message, does \"standard garlic butter\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q37fbc57009",
  "kind": "yes/no",
  "text": "Customer: how about another movie\nAssistant: what other movie\nCustomer: is avengers, end game playing at that time",
  "question": "In the customer's last message, does \"avengers, end game\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6ee4d8c6c8",
  "kind": "yes/no",
  "text": "Customer: That's a bit late... so nothing earlier?\nAssistant: There's a spot at 6PM.\nCustomer: I suppose 8:30 would work, we could get a few cocktails before.",
  "question": "In the customer's last message, does \"8:30\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69f24c2519",
  "kind": "yes/no",
  "text": "Assistant: Whipped cream?\nCustomer: Yes please whipped cream.\nAssistant: Unfortunately they don't have any mocha cappuccino available.",
  "question": "According to the assistant's last message, is \"mocha cappuccino\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6c5a870718",
  "kind": "yes/no",
  "text": "Customer: Great, Bob's Auto Shop is fine.\nAssistant: Great, and what type of car will you be maintenance?\nCustomer: A 2000 Honda Odyssey.",
  "question": "In the customer's last message, does \"2000\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b195e1f69",
  "kind": "yes/no",
  "text": "Customer: Ok no cheese on the second pizza, but I want mushrooms and red onions.\nAssistant: What kind of crust did you want for that one?\nCustomer: Thins crust.",
  "question": "In the customer's last message, does \"Thins crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qef6faf1706",
  "kind": "yes/no",
  "text": "Customer: Hey Tanner! Could you get me two tickets for \"Us\" for tonight?\nAssistant: Of course. Two tickets for \"Us\", tonight at the Carmike theater, right?\nCustomer: Oh! No, actually I am actually in Jacksonville this week.",
  "question": "In the customer's last message, does \"Jacksonville\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd2212d6572",
  "kind": "yes/no",
  "text": "Customer: Starting location is Longhorn Steakhouse on Airport Blvd in Mobile, Alabama.\nAssistant: And which movie theater are you going to?\nCustomer: AMC Mobile 16 on Schillinger Road also in Mobile.",
  "question": "In the customer's last message, does \"AMC Mobile 16 on Schillinger Road\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcbff66e917",
  "kind": "yes/no",
  "text": "Customer: Hi [ASSISTANT], could you order a pizza from Pizza Rigazzi for my dinner date?",
  "question": "In the customer's last message, does \"Pizza Rigazzi\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q14d22ae10c",
  "kind": "yes/no",
  "text": "Assistant: I will order a large & use your Rewards Card\nCustomer: I will pick it up in 20 minutes\nAssistant: I'm sorry, they are out of whipped cream woud you like something else",
  "question": "According to the assistant's last message, is \"whipped cream\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdf8a2a358c",
  "kind": "yes/no",
  "text": "Assistant: How many passengers will be riding?\nCustomer: 2\nAssistant: OK, I have ordered you a Lyft XL to pick you both up at 11 am",
  "question": "According to the assistant's last message, is \"Lyft XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2f09638a13",
  "kind": "yes/no",
  "text": "Assistant: Okay, what would you like?\nCustomer: I want a Grande caramel frapuccino with an extra shot of espresso, and no whipped cream.\nAssistant: They seem to be out of caramel, would you like a different kind of frap?",
  "question": "According to the assistant's last message, is \"caramel\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q69e6b6059a",
  "kind": "yes/no",
  "text": "Customer: Yes, it is actually a bit scary.\nAssistant: OK. what is the specific problem.\nCustomer: Well, it is doing a couple things. First of all, it is pulling to the left when I hit the brake.",
  "question": "In the customer's last message, does \"pulling to the left when I hit the brake\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q845c69370b",
  "kind": "yes/no",
  "text": "Assistant: Intelligent Auto Solutions will close at 8:00 p.m. on Tuesday.\nCustomer: 4:30 will be perfect then.\nAssistant: Great. I'll schedule the appointment for 4:30 p.m. this Tuesday at Intelligent Auto Solutions. I have the vehicle listed as a 2007 Mazda 3 and the reason listed as an alternator/battery check. Your appointment will be saved under Daniel Craig at 555-8777.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q526f02d5c5",
  "kind": "yes/no",
  "text": "Assistant: All right. A large Paradise Pie pizza with a gluten free thin crust, add feta cheese, and pineapples, from Hide Away in North Little Rock. I've got you.\nCustomer: Thank you.\nAssistant: Hello there. I hate to inform you, but they are out of the gluten free crust as well as pineapples of all things.",
  "question": "According to the assistant's last message, is \"gluten free crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2e7ca8991a",
  "kind": "yes/no",
  "text": "Customer: BBQ gives me heartburn. Make it regular.\nAssistant: What type of crust?\nCustomer: I normally get normal crust, but let's do thin crust this time!",
  "question": "In the customer's last message, does \"thin crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf8cb216a25",
  "kind": "yes/no",
  "text": "Customer: What is the closest movie theatre that's playing The Lego Movie part 2?",
  "question": "In the customer's last message, does \"The Lego Movie part 2\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q090f056dab",
  "kind": "yes/no",
  "text": "Customer: Hi, I need an appointment scheduled at Intelligent Auto Solutions.\nAssistant: Hi. I'd be happy to assist you with scheduling your appointment. What is the make and model of your vehicle?\nCustomer: It is a Kia Optima.",
  "question": "In the customer's last message, does \"Kia Optima\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q15035deb44",
  "kind": "yes/no",
  "text": "Customer: Yes, that's the place. My buddy John works there.\nAssistant: Ok, I need the year, make, and model of your car.\nCustomer: It's a 2016 BMW 3 Series Sedan. Name is Howard Wolowitz and my number is 123-456-7890",
  "question": "In the customer's last message, does \"Howard Wolowitz\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbb60a3186a",
  "kind": "yes/no",
  "text": "Customer: I need to order a pizza from Chapos Pizzeria",
  "question": "In the customer's last message, does \"Chapos Pizzeria\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q18500bf99a",
  "kind": "yes/no",
  "text": "Assistant: I'll place your order now.\nCustomer: Thanks!\nAssistant: Bad news. They're currently out of pineapples, would you like to just get ham?",
  "question": "According to the assistant's last message, is \"pineapples\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q41526955b3",
  "kind": "yes/no",
  "text": "Customer: yes hun its very easy to find.\nAssistant: what size would you like?\nCustomer: please go ahead and grab me a tall today.",
  "question": "In the customer's last message, does \"tall\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9c77e6b586",
  "kind": "yes/no",
  "text": "Customer: Would next tuesday be available at 10 a.m.\nAssistant: Where at?\nCustomer: At Schmid'ts auto repair",
  "question": "In the customer's last message, does \"Schmid'ts auto repair\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q71923aec3a",
  "kind": "yes/no",
  "text": "Assistant: Yes they use organic honey there\nCustomer: Then go ahead and place the order\nAssistant: Your order is placed at the Starbucks in 5th Ave. The receipt will be sent to your phone shortly.",
  "question": "According to the assistant's last message, is \"5th Ave\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q276b7fb54e",
  "kind": "yes/no",
  "text": "Customer: I thought you would have this information John.\nAssistant: Sorry sir. All I know is that you have a Chevrolet Malibu.\nCustomer: Yes John. I have a Chevrolet Malibu LT and the year is 2018.",
  "question": "In the customer's last message, does \"2018\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1a12e0a32d",
  "kind": "yes/no",
  "text": "Customer: Hi, I'll need to schedule an appointment to repair my car.\nAssistant: I'll be glad to help. Which auto repair shop do you have in mind?\nCustomer: I use the Intelligent Auto Solutions please.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4f17a8ab87",
  "kind": "yes/no",
  "text": "Customer: I would like to be picked up from the Atlanta airport and driven to the Atlanta zoo.\nAssistant: When do you want to be picked up?\nCustomer: Today at 2:00 pm.",
  "question": "In the customer's last message, does \"2:00 pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5803559dc8",
  "kind": "yes/no",
  "text": "Customer: do you have booth\nAssistant: sorry sir not available\nCustomer: ok can you book at 8.30pm",
  "question": "In the customer's last message, does \"8.30pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdecb995bb0",
  "kind": "yes/no",
  "text": "Assistant: Perfect, and the name and number I should book it under?\nCustomer: John White, and put down my cell, 617-555-0123.\nAssistant: Ok great, I'm booking you at the sister location across town for 9:30am today, for your 2007 Toyota Yaris, I've noted that it stalls when you come up to a stop with the AC on, and booked under John White and left your cell, 617-555-0123.",
  "question": "According to the assistant's last message, is \"Toyota Yaris\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6b046bcb95",
  "kind": "yes/no",
  "text": "Customer: I would like to be picked up from my house.\nAssistant: Excellent, and when would you like to leave?\nCustomer: I would like to leave at 2 pm.",
  "question": "In the customer's last message, does \"2 pm\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9fa282a5da",
  "kind": "yes/no",
  "text": "Customer: Hello, I need help with my car.\nAssistant: I can help with that. Where would you like to take your car to?\nCustomer: Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb973255448",
  "kind": "yes/no",
  "text": "Customer: I want Italian food but I dont have a strong preference\nAssistant: So there are a lot of great restaurants near the area one of them Olive Garden and the other Pomodori Bistro & Wine Bar\nCustomer: Can you tell me about the menu options at Pomodori Bistro & Wine Bar",
  "question": "In the customer's last message, does \"Pomodori Bistro & Wine Bar\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q716f7de826",
  "kind": "yes/no",
  "text": "Assistant: There are showings in XD at 4:00pm, 7:00pm and 10:05pm at the century 25\nCustomer: oh cool, get me 2 tickets to the 7:00pm showing.\nAssistant: unfortunately it looks like the 7:00pm showing is sold out.",
  "question": "According to the assistant's last message, is \"7:00pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q22bda76d51",
  "kind": "yes/no",
  "text": "Customer: I need a couple of tickets for the movie What Men Want.\nAssistant: Ok. Do you have a theater location in mind?\nCustomer: Yes. I'd like to see if it is playing in Macon, Ga tonight?",
  "question": "In the customer's last message, does \"Macon, Ga\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc90907d21b",
  "kind": "yes/no",
  "text": "Customer: A pepperoni and pineapple pizza please!\nAssistant: What size pizza would you like?\nCustomer: A large pizza! Can we also get a 2 liter of Sprite?",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4bea491699",
  "kind": "yes/no",
  "text": "Assistant: For today, it's 1:15, 4:15, and 7:15.\nCustomer: I guess I'll have to settle for the 7:15 show. Oh, and I'd like to see it in 3D if possible.\nAssistant: I'll see what I can do. Okay, it says here that the Great Northern doesn't have any 3D theaters. Do you want to change theaters?",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q71f0f7b747",
  "kind": "yes/no",
  "text": "Assistant: To confirm, I've got one grande gingerbread latte with soy milk and extra whipped cream. Is that right?\nCustomer: Yes.\nAssistant: I have place the order and it will be ready for pickup shortly at the Starbucks on 1134 Lancaster Dr, Salem, Oregon.",
  "question": "According to the assistant's last message, is \"1134 Lancaster Dr, Salem, Oregon\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q08755fa0d8",
  "kind": "yes/no",
  "text": "Customer: I prefer the Alamo Drafthouse.\nAssistant: Which Alamo location do you prefer? Midtown or La Vista?\nCustomer: I prefer La Vista.",
  "question": "In the customer's last message, does \"La Vista\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf13cfc77d3",
  "kind": "yes/no",
  "text": "Assistant: Sorry, but the broccoli is not available as a topping.\nCustomer: Okay, then just a large sized pizza, extra thick stuffed crust, with garlic and mushrooms.\nAssistant: Okay, I placed an order for a large sized pizza, extra thick stuffed crust, and mushrooms and garlic.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf438d72df4",
  "kind": "yes/no",
  "text": "Customer: 5\nAssistant: What time would you like to make the reservation for?\nCustomer: 6pm and a table in the bar lounge if possible.",
  "question": "In the customer's last message, does \"6pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9103d210bd",
  "kind": "yes/no",
  "text": "Customer: I would like to schedule a diagnostic test on my car.",
  "question": "In the customer's last message, does \"diagnostic test\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1e5d940b5b",
  "kind": "yes/no",
  "text": "Customer: 9:40 one sounds good then.\nAssistant: How many seats do you need?\nCustomer: there's four of us.",
  "question": "In the customer's last message, does \"four\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0a9e27f7e7",
  "kind": "yes/no",
  "text": "Assistant: To confirm, you want a large BBQ chicken pizza for dinner tonight. Delivery or pick up?\nCustomer: Pick up.\nAssistant: Okay. I just ordered you a large BBQ chicken pizza for pick up.",
  "question": "According to the assistant's last message, is \"BBQ chicken pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd786a15f43",
  "kind": "yes/no",
  "text": "Assistant: When would you like to schedule the appointment?\nCustomer: Today if possible.\nAssistant: There is nothing available today. The first available appointment is tomorrow morning at 8am.",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcd749f7fb4",
  "kind": "yes/no",
  "text": "Customer: It is the front right tire.\nAssistant: What type of car?\nCustomer: It is a 2017 Ford Fiesta.",
  "question": "In the customer's last message, does \"Ford Fiesta\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q382dcdd9a5",
  "kind": "yes/no",
  "text": "Assistant: Anything else\nCustomer: That should do it.\nAssistant: Your order has been place for a grande Caffe Mocha extra hot with coconut milk and whipped cream",
  "question": "According to the assistant's last message, is \"whipped cream\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3d24b90fcd",
  "kind": "yes/no",
  "text": "Assistant: Same account as usual?\nCustomer: Yes please.\nAssistant: Ordered! Your order for a small Italian sausage and meatball pizza is going to be ready for pickup in 25 minutes.",
  "question": "According to the assistant's last message, is \"small\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q472172494b",
  "kind": "yes/no",
  "text": "Customer: REGAL CINEMAS GATEWAY 16, Austin, Texas\nAssistant: OK, where is the next destination?\nCustomer: COUNTER CULTURE, 2337 E Cesar Chavez St, Austin, TX 78702",
  "question": "In the customer's last message, does \"COUNTER CULTURE, 2337 E Cesar Chavez St, Austin, TX 78702\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q946dc3f67c",
  "kind": "yes/no",
  "text": "Assistant: what size and toppings\nCustomer: a tall with coconut milk with whipped cream on top\nAssistant: no coconut milk and the tall size is unavailable",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q57ac6cdf08",
  "kind": "yes/no",
  "text": "Customer: I want to see the wedding guest\nAssistant: What city?\nCustomer: South Kingstown",
  "question": "In the customer's last message, does \"South Kingstown\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
