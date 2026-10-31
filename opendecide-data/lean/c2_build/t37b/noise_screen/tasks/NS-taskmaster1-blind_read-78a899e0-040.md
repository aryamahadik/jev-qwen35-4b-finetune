# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-040 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-040.json

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
  "qid": "q415293c90c",
  "kind": "yes/no",
  "text": "Customer: Is it extra for extra cheese?\nAssistant: Yes, it costs $1 more for extra cheese.\nCustomer: And what about getting a Stuffed Crust?",
  "question": "In the customer's last message, does \"Stuffed Crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf3e017676a",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry. I see that Mexico Lindo has no available tables at 8pm. Would you like to try another time?\nCustomer: Yes try for 7:30pm\nAssistant: I'm sorry Mexico Lindo has no tables available for tomorrow at 7:30. Would you like to try another time?",
  "question": "According to the assistant's last message, is \"7:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa22073a206",
  "kind": "yes/no",
  "text": "Customer: Hi Bob, are you busy? I want to take a friend to go see Pet Sematary tonight at The Grand in Conroe.",
  "question": "In the customer's last message, does \"The Grand\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc69025c7c4",
  "kind": "yes/no",
  "text": "Assistant: Do you want me to book it?\nCustomer: Yes please.\nAssistant: Okay, I just booked you two reserved seats for 7:30pm for Hellboy tonight. The tickets are going to be sent to your phone.",
  "question": "According to the assistant's last message, is \"Hellboy\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7f8e4a63ee",
  "kind": "yes/no",
  "text": "Assistant: I am now making the booking for you.\nCustomer: Okay.\nAssistant: They confirmed your booking. Please arrive no later than 7 a.m. tomorrow morning at the auto shop.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q58aed76038",
  "kind": "yes/no",
  "text": "Assistant: Any toppings?\nCustomer: Nope.\nAssistant: Sorry, it seems whole milk is out.",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q662a230fd5",
  "kind": "yes/no",
  "text": "Assistant: Sure, I'll go ahead and sort that out for you now.\nCustomer: Awesome.\nAssistant: Hi, so it seems Missing Link isn't playing at this theater, would you like to try a different theater?",
  "question": "According to the assistant's last message, is \"Missing Link\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5198940607",
  "kind": "yes/no",
  "text": "Customer: I'd like to buy tickets for Aquaman",
  "question": "In the customer's last message, does \"Aquaman\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1c79f112e3",
  "kind": "yes/no",
  "text": "Customer: Thanks! Anything else needed?\nAssistant: Yes, actually. Do you want the High St. or Kansas Ave. location?\nCustomer: I want the High St.",
  "question": "In the customer's last message, does \"High St.\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2ba14d767b",
  "kind": "yes/no",
  "text": "Customer: Yes of course.\nAssistant: What do you want to order?\nCustomer: We'll do that 2 large pizza special with them, one pepperoni and one chicken bbq.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa5148df318",
  "kind": "yes/no",
  "text": "Assistant: Great. Could I get your first and last name?\nCustomer: Yes. Michael Brown.\nAssistant: Okay, Mr. Brown, I have you booked for 4 people at the Hill Country BBQ for 730 pm.",
  "question": "According to the assistant's last message, is \"4 people\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe45fdc1d6e",
  "kind": "yes/no",
  "text": "Customer: Iced, please.\nAssistant: Ok, what size Iced Caramel Machiatto would you like?\nCustomer: A Grande, please.",
  "question": "In the customer's last message, does \"Grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3839f0eccf",
  "kind": "yes/no",
  "text": "Assistant: And when were you wanting to bring it in?\nCustomer: I'd like to bring it in by 2pm today if I can.\nAssistant: A 2pm appointment is not available, but there is one for 3:30pm. Is that okay?",
  "question": "According to the assistant's last message, is \"2pm\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q891e283029",
  "kind": "yes/no",
  "text": "Customer: i need to try and get my car in to Intelligent Auto Solutions asap\nAssistant: ok what seems to be the problem\nCustomer: well my car is making a loud clunk when i turn",
  "question": "In the customer's last message, does \"my car is making a loud clunk when i turn\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qff30c3cd93",
  "kind": "yes/no",
  "text": "Assistant: I hope so!\nCustomer: Sure is, it consists of Rich espresso and house-made chocolate sauce rendezvous with creamy steamed milk under a blanket of fresh whipped cream.\nAssistant: Ok. So your Caffe Mocha is confirmed at your requested location: DC—Navy Yard 1115 New Jersey Avenue SE Washington, DC 20003. Your receipt is available shortly. One more thing; your receipt will be sent to your mobile device via text message",
  "question": "According to the assistant's last message, is \"DC—Navy Yard 1115 New Jersey Avenue SE Washington, DC 20003\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q80186606e0",
  "kind": "yes/no",
  "text": "Assistant: Absolutely. I'll request your Lyft now. To confirm, you're being picked up at 85 West Street and going to Madison Square Garden at Four Pennsylvania Plaza. You wish to be left at the west side of the building on Eighth Avenue.\nCustomer: You got it. Hey Darcy, you ever been to a dog show?\nAssistant: No, Ms. Carmody. I did see \"Best in Show\" once though. Okay, your Lyft has been ordered and will arrive in approximately six minutes.",
  "question": "According to the assistant's last message, is \"six minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc2e69a8065",
  "kind": "yes/no",
  "text": "Customer: Medium\nAssistant: What crust do you prefer?\nCustomer: Thick please.",
  "question": "In the customer's last message, does \"Thick\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q41a673fabc",
  "kind": "yes/no",
  "text": "Customer: I'll be in town.\nAssistant: Okay, let's see. It's play at The Drafthouse and IMAX.\nCustomer: Ohh, IMAX. How much are those tickets?",
  "question": "In the customer's last message, does \"IMAX\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0de97d9965",
  "kind": "yes/no",
  "text": "Customer: I don't think I have that much time Linda.\nAssistant: Why not?\nCustomer: My brakes are really squealing now, I don't think I could risk the interstate. I'm afraid I would crash and die in a fiery wreck.",
  "question": "In the customer's last message, does \"My brakes are really squealing now\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2a06f8a0c0",
  "kind": "yes/no",
  "text": "Customer: Intelligent Auto Solutions, please.\nAssistant: OK cool. I need some quick info. What vehicle, name, and number?\nCustomer: The vehicle is a 2015 Ford Ranger. Put it under the name Jason Bash. My phone number is 123-456-7890.",
  "question": "In the customer's last message, does \"2015\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q72cedd5bd3",
  "kind": "yes/no",
  "text": "Assistant: Any toppings should I add?\nCustomer: Just ask to put extra cheese and mushroom.\nAssistant: I am sorry , but Grandma is sold out . Is there any other pizza you would like to have?",
  "question": "According to the assistant's last message, is \"Grandma\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q53c8cd230a",
  "kind": "yes/no",
  "text": "Customer: My car has had a hard time starting lately, Can you make me a car appointment?\nAssistant: Yes what kind of car is it?\nCustomer: It is a 2018 subaru wrx",
  "question": "In the customer's last message, does \"2018\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q14410ba4b3",
  "kind": "yes/no",
  "text": "Customer: Hello I would like to get a uber please.\nAssistant: Sure! Where are we picking you up from and dropping you off at?\nCustomer: Trattoria Stella, 1200 W Eleventh St, Traverse City, MI and I would like to go toView Nightclub at West Bay Beach Resort, 615 E Front St, Traverse City, MI",
  "question": "In the customer's last message, does \"Trattoria Stella, 1200 W Eleventh St, Traverse City, MI\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2f03ec7266",
  "kind": "yes/no",
  "text": "Customer: I would like to know the Menu for Starbucks\nAssistant: The menu at starbucks is : Cappuccino Caramel Brulée Latte Seasonal offering Caramel Macchiato Cherry Mocha Chestnut Praline Latte Seasonal offering Cinnamon Dolce Latte Cinnamon Shortbread Latte Cordusio Eggnog Latte Seasonal offering Espresso Espresso Con Panna Espresso Macchiato Espresso Macchiato Flat White Gingerbread Latte Seasonal offering Iced Black and White Mocha Seasonal offering Iced Caffè Americano Iced Caffè Latte Iced Caffè Mocha Iced Caramel Brulée Latte Iced Caramel Macchiato Iced Cherry Mocha Iced Chestnut Praline Latte Seasonal offering Iced Cinnamon Dolce Latte Iced Cinnamon Shortbread Latte Iced Cold Foam Cappuccino Iced Cordusio Iced Eggnog Latte Seasonal offering Iced Gingerbread Latte Seasonal offering Iced Juniper Latte Iced Latte Macchiato Iced Peppermint Mocha Seasonal offering Iced Peppermint White Chocolate Mocha Seasonal offering Iced Pumpkin Spice Chai Latte Iced Pumpkin Spice Latte Iced Salted Caramel Mocha Iced Skinny Cinnamon Dolce Latte Iced Skinny Mocha Iced Starbucks Blonde® Juniper Latte Iced Starbucks® Blonde Vanilla Bean Coconutmilk Latte Iced Starbucks® Blonde Black and White Mocha Seasonal offering Iced Starbucks® Blonde Caffè Americano Iced Starbucks® Blonde Caffè Latte Iced Starbucks® Blonde Caramel Brulée Latte Iced Starbucks® Blonde Chestnut Praline Latte Iced Starbucks® Blonde Cinnamon Shortbread Latte Iced Starbucks® Blonde Cold Foam Cappuccino\nCustomer: Ok, thats a lot of options, I want a Cappachino Venti",
  "question": "In the customer's last message, does \"Venti\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb4fa9bd853",
  "kind": "yes/no",
  "text": "Assistant: Do you want whipped cream?\nCustomer: No I don't.\nAssistant: OK. Your drink will be ready to collect at 55th Street in 15 minutes.",
  "question": "According to the assistant's last message, is \"55th Street\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf0e04316c7",
  "kind": "yes/no",
  "text": "Assistant: AMC Phipps and CineBistro are both nearby.\nCustomer: AMC Phipps then. Do they have 3D options?\nAssistant: Sorry, the movie Us does not have any 3D viewings at AMC Phipp.",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc486a010c9",
  "kind": "yes/no",
  "text": "Customer: I'd like to book an appointment at Intelligent Auto Solutions.\nAssistant: Okay. What seems to be the problem?\nCustomer: There's a crack in my rear windshield.",
  "question": "In the customer's last message, does \"crack in my rear windshield.\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa0cc224e56",
  "kind": "yes/no",
  "text": "Customer: I need you to order some pizza from Pizza Hut.\nAssistant: Which one do you want me to order from?\nCustomer: The one in Macon.",
  "question": "In the customer's last message, does \"Macon\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4f4fa76017",
  "kind": "yes/no",
  "text": "Customer: Yes, try for the 10:10pm showing if it's not available at 7:30.\nAssistant: How many tickets?\nCustomer: I will need two tickets.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q18afdb0963",
  "kind": "yes/no",
  "text": "Assistant: anything else?\nCustomer: tomato\nAssistant: They are out of tomato",
  "question": "According to the assistant's last message, is \"tomato\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6ca5cf19ae",
  "kind": "yes/no",
  "text": "Assistant: Ok. there is an initial inspection fee of $100 is this ok?\nCustomer: Yes\nAssistant: Ok appointment booked for 2/15 12pm for john smith. phone number 888-888-8888. 2018 Subaru wrx, hard start issue",
  "question": "According to the assistant's last message, is \"hard start issue\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q02c3f641bb",
  "kind": "yes/no",
  "text": "Customer: Great anything else?\nAssistant: keep your speed to a steady pace.\nCustomer: Fine. Tell them it is a 2004 Chevy Trailblazer with a 4.2 litre",
  "question": "In the customer's last message, does \"2004\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3e61e4ebab",
  "kind": "yes/no",
  "text": "Customer: I would like to watch the movie in Seattle.\nAssistant: Sure, which movie theater?\nCustomer: At the Regal Cinemas Meridian 16.",
  "question": "In the customer's last message, does \"Regal Cinemas Meridian 16\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qeddb01c9ed",
  "kind": "yes/no",
  "text": "Assistant: For 4 tickets, it will be $55.\nCustomer: Alright book it for me please.\nAssistant: I have booked 4 tickets of Spiderman: Into the Spiderverse for 8:00pm. The tickets will be sent to your phone.",
  "question": "According to the assistant's last message, is \"Spiderman: Into the Spiderverse\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2e7acf575f",
  "kind": "yes/no",
  "text": "Customer: Good morning Justin,I would like you to help make me buy some tickets for a movie.\nAssistant: Good morning madam, Where would you like me to buy the ticket?\nCustomer: AMC Empire 25 New York",
  "question": "In the customer's last message, does \"AMC Empire 25\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q624e27e532",
  "kind": "yes/no",
  "text": "Customer: Hey Donna can you buy me two movie tickets to see Captain Marvel?\nAssistant: Sure Turker, what theater do you want to see it at?\nCustomer: I want to try out the AMC Dine in theater at the Rio in Gaithersburg.",
  "question": "In the customer's last message, does \"Rio in Gaithersburg\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3f6df11a3e",
  "kind": "yes/no",
  "text": "Assistant: How many people?\nCustomer: A table for 4.\nAssistant: Okay. Landmarc is now reserved. Table of 4 at 8pm on Friday 22",
  "question": "According to the assistant's last message, is \"4\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe0d395e89b",
  "kind": "yes/no",
  "text": "Assistant: Yes, it does. I'll pass along that information.\nCustomer: Perfect. I think I'll make my flight.\nAssistant: They are on the way. They should be at your location in 2 minutes and you should have the details on your phone.",
  "question": "According to the assistant's last message, is \"2 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd4187ae977",
  "kind": "yes/no",
  "text": "Assistant: Okay, it looks like there aren't any tables available. Is there another time that works for you?\nCustomer: Sure, what about 6:30?\nAssistant: Sorry, looks like 6:30 is fully booked too.",
  "question": "According to the assistant's last message, is \"6:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q824dc6837e",
  "kind": "yes/no",
  "text": "Assistant: Okay, and I assume that you want the largest size since your family will be sharing this?\nCustomer: That's correct.\nAssistant: Alright, I've ordered you one large two topping pizza with pepperoni and canadian bacon. The crust is thin and crispy without any flavor.",
  "question": "According to the assistant's last message, is \"canadian bacon\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6604500ac7",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza from Papa Johns",
  "question": "In the customer's last message, does \"Papa Johns\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q866409133f",
  "kind": "yes/no",
  "text": "Customer: Today\nAssistant: OK. For what time?\nCustomer: 9 PM",
  "question": "In the customer's last message, does \"9 PM\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc040478dfe",
  "kind": "yes/no",
  "text": "Customer: I need to go to 141 Divisadero Street.\nAssistant: Ok, that's 141 Divisadero Street in San Francisco, correct?\nCustomer: Right, 141 Divisadero Street in SF.",
  "question": "In the customer's last message, does \"141 Divisadero Street in SF\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd2b2624b90",
  "kind": "yes/no",
  "text": "Assistant: What time?\nCustomer: 3pm today.\nAssistant: Okay, there are not two tickets available to see Shazam! at 3:00 at the Cinemark Sugarhouse today. Would you like a different time?",
  "question": "According to the assistant's last message, is \"3:00\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qda80fccf73",
  "kind": "yes/no",
  "text": "Customer: can you book me a couple movie tickets for tonight?\nAssistant: sure thing, which theater did you want to go to?\nCustomer: i think Crest Theater in Sacramento will be best",
  "question": "In the customer's last message, does \"Sacramento\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qba241ff2e9",
  "kind": "yes/no",
  "text": "Customer: the second will be all meat with a stuffed crust well done.\nAssistant: ok, got it.\nCustomer: the third pizza is vegetarian with a thin crust.",
  "question": "In the customer's last message, does \"thin crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qca3c1dd2d1",
  "kind": "yes/no",
  "text": "Assistant: Ok so it looks like they also have a balcony table. Would you like to give that a try?\nCustomer: No thanks. I think its supposed to rain.\nAssistant: Oh yea,good call. So your all set for this evening at 7pm for 5 people at the Fishermans Warf in Norfolk.",
  "question": "According to the assistant's last message, is \"5\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdbbe0378e4",
  "kind": "yes/no",
  "text": "Assistant: No, they have drivers available. Do you want this charged to your personal account or business account?\nCustomer: This should be charged to my business account.\nAssistant: Uber XL is on the way. You can check your phone for updates and receipt.",
  "question": "According to the assistant's last message, is \"Uber XL\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5d6ad4497a",
  "kind": "yes/no",
  "text": "Assistant: i sure can, is there anything else that i can order for you?\nCustomer: no i think thats it\nAssistant: ok great i have your nonfat caramel frapp with extra whip extra caramel ordered at the dewey and madison starbucks",
  "question": "According to the assistant's last message, is \"caramel frapp\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3598af44a4",
  "kind": "yes/no",
  "text": "Customer: Is Pizza Man open late?",
  "question": "In the customer's last message, does \"Pizza Man\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
