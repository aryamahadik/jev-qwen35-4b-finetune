# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-018 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-018.json

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
  "qid": "q73f3fad7f2",
  "kind": "yes/no",
  "text": "Customer: That is later than I would like to go as I have to drive back to Louisville tonight.\nAssistant: I've noticed that the Movie Tavern at Brannon Crossing has a 6:20pm time for $13.50 ticket price.\nCustomer: Hamburg Pavillion is rather far from where we are having dinner. See if US is playing at the Kentucky Theatre tonight.",
  "question": "In the customer's last message, does \"Kentucky Theatre\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3a8069ed36",
  "kind": "yes/no",
  "text": "Customer: I want to order a pizza from Jets.\nAssistant: Great place to come, I can help! What location?\nCustomer: The one in Rivergate.",
  "question": "In the customer's last message, does \"Rivergate\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3cdf7380b0",
  "kind": "yes/no",
  "text": "Assistant: Where are you located?\nCustomer: I'm at the Grand Budapest Hotel in Lawrence.\nAssistant: I'm sorry, there isn't an UberX available in your area at the moment. Would you like a different car type?",
  "question": "According to the assistant's last message, is \"UberX\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q38f123913f",
  "kind": "yes/no",
  "text": "Customer: i am really craving a pizza from domino's for our dinner tonight!\nAssistant: That does sound really good which one are you thinking of?\nCustomer: lets go with the one on east kearney street, there dough is the best",
  "question": "In the customer's last message, does \"east kearney street\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q32949e32c3",
  "kind": "yes/no",
  "text": "Customer: Hello i would like some information on getting a tune up for my 2017 chevy cruise.",
  "question": "In the customer's last message, does \"chevy cruise\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe9a066e8e5",
  "kind": "yes/no",
  "text": "Assistant: Ok Sam, let me check that out.\nCustomer: Fine, and I'll take an extra large and put some extra cheese on that too.\nAssistant: Sorry Sammy, Brother's Pizzeria is out of the Hawaiin pizza choice tonight.",
  "question": "According to the assistant's last message, is \"Brother's Pizzeria\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7155390e47",
  "kind": "yes/no",
  "text": "Customer: Okay, how about soy milk?\nAssistant: They have that. Still want a Venti with extra caramel drizzle?\nCustomer: No, can you make it Grande size… definitely still want the extra caramel drizzle though!",
  "question": "In the customer's last message, does \"Grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6e4df70e2f",
  "kind": "yes/no",
  "text": "Customer: hey tom its me dick\nAssistant: hey dick what can i do for you?\nCustomer: My car is pulling to the left when i am in motion.",
  "question": "In the customer's last message, does \"car is pulling to the left when i am in motion\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcf535be62f",
  "kind": "yes/no",
  "text": "Assistant: Let me see what's available\nCustomer: Thanks\nAssistant: Unfortunately, there is nothing available for 6:30 pm",
  "question": "According to the assistant's last message, is \"6:30 pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1e4c98cd9c",
  "kind": "yes/no",
  "text": "Assistant: Sure let me call them\nCustomer: Perfect!\nAssistant: Sorry, El Pasco cant accomodate 100 people",
  "question": "According to the assistant's last message, is \"El Pasco\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q22289608b8",
  "kind": "yes/no",
  "text": "Customer: I need an Uber XL, please.\nAssistant: Okay, where are you located and where will you be going?\nCustomer: Im located at the mall, I need to get dropped off at the airport.",
  "question": "In the customer's last message, does \"airport\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa151de2c09",
  "kind": "yes/no",
  "text": "Assistant: They're at 2302B Nesconset Highway in Stony Brook.\nCustomer: Okay, got it. I just wrote that down.\nAssistant: Perfect. I just put the order in. You're confirmed for one large pizza with anchovy and kalamata olives. It'll be ready for pickup in 25 minutes. Your receipt will go directly to your cell phone by text message.",
  "question": "According to the assistant's last message, is \"kalamata olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9311775933",
  "kind": "yes/no",
  "text": "Customer: I would like for you to purchase tickets to the movie Glass",
  "question": "In the customer's last message, does \"Glass\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4d418d164b",
  "kind": "yes/no",
  "text": "Assistant: Okay, I will get on that immediately.\nCustomer: Thank you Renee.\nAssistant: Hello, Mr. John Doe, I called in your order, but they don't have any italian sausage, but they do have beef sausage.",
  "question": "According to the assistant's last message, is \"italian sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qee0c32df17",
  "kind": "yes/no",
  "text": "Assistant: Perfect, It looks like it's going to be about $25 to get everyone to Megan's house. Since you live right down the road it shouldn't cost too much more. I'll get it set up for you now.\nCustomer: Great! Tell them to hurry, these girls are getting rowdy.\nAssistant: They are on the way, should be to you in four minutes.",
  "question": "According to the assistant's last message, is \"four minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q22101ee689",
  "kind": "yes/no",
  "text": "Assistant: Yes, that is available. Can I get the name for the reservation\nCustomer: Smithers\nAssistant: Very good. You're all set. Smithers, table for 5 with a high chair has been reserved at the Olive Garden at the Bridgeton location",
  "question": "According to the assistant's last message, is \"Olive Garden\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q870815ab52",
  "kind": "yes/no",
  "text": "Customer: I think everyone likes Italian - - a really good Italian place. We're going to spend some time there.\nAssistant: What about Luigi's on McPherson Church Road?\nCustomer: We've been there before, it's really good. What about 6:00 tomorrow with an outside table since the weather is going to be really nice.",
  "question": "In the customer's last message, does \"6:00\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q42259cfd3a",
  "kind": "yes/no",
  "text": "Customer: Hey, I'm looking to make a reservation at a seafood restaurant. Can you recommend anything in downtown Pittsburgh, PA?",
  "question": "In the customer's last message, does \"downtown Pittsburgh, PA\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf0b8ca2cf0",
  "kind": "yes/no",
  "text": "Assistant: Be sure to check your text messages as I will be sending over the order details and tickets.\nCustomer: I will be sure to keep my cell phone in my pocket. We will be taking a limo to the show from a retaurant.\nAssistant: Ok, we are all set. I have four tickets booked for Westshore 14 at 8:30 p.m.",
  "question": "According to the assistant's last message, is \"8:30 p.m\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q559d56348d",
  "kind": "yes/no",
  "text": "Assistant: I see. I will make the request then.\nCustomer: Just make sure it's from Sonoma County, and leave a phone number so they can contact you if they have any questions.\nAssistant: Ok, I've reserved a window table for 4 at 7 o'clock on Valentines day. I've also noted your dietary request and asked that 2 bottles of Sonoma County Pinot Noir be chilled prior to your arrival.",
  "question": "According to the assistant's last message, is \"window table\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd8c5229ce4",
  "kind": "yes/no",
  "text": "Customer: Schedule an appointment with Intelligent Auto Solutions\nAssistant: say the purpose for the appointment\nCustomer: Car is making noise when it is run at high speed",
  "question": "In the customer's last message, does \"Car is making noise when it is run at high speed\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q77481509f6",
  "kind": "yes/no",
  "text": "Customer: Hello, can you please order me a car?\nAssistant: Yes, where are you located and where are you going?\nCustomer: I am at Ford Field, I would like to go to Birmingham.",
  "question": "In the customer's last message, does \"Ford Field\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0986086204",
  "kind": "yes/no",
  "text": "Customer: And for a car with a car seat?\nAssistant: You are looking at 46.07.\nCustomer: Last estimate request for best price from MSG to Leo's in Garden City.",
  "question": "In the customer's last message, does \"MSG\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3f301a6730",
  "kind": "yes/no",
  "text": "Assistant: I don't see any tables available outside by the water. Would you like to sit somewhere else?\nCustomer: Just anywhere outside then is fine. Are there any available?\nAssistant: Sorry, I don't see any outside tables.",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q75883f6d17",
  "kind": "yes/no",
  "text": "Customer: Ok, thanks.\nAssistant: Sorry, they said they're out of espresso at the moment. Did you want anything else?\nCustomer: Sure, just get me a tall regular coffee",
  "question": "In the customer's last message, does \"tall\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1d65ab607a",
  "kind": "yes/no",
  "text": "Assistant: Any other specifications?\nCustomer: That should do it.\nAssistant: Okay, only one problem. They are out of Soy milk.",
  "question": "According to the assistant's last message, is \"Soy milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfd1eee795d",
  "kind": "yes/no",
  "text": "Customer: yes I am\nAssistant: Okay, and what would you like to see?\nCustomer: I was thinking Captain Marvel",
  "question": "In the customer's last message, does \"Captain Marvel\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q18f22ecf4c",
  "kind": "yes/no",
  "text": "Assistant: Ok, I'll get that ordered up for you. Now to be sure, that's a large hawaiian, pineapple and ham.\nCustomer: Correct, thanks. You have the number and details you need.\nAssistant: Yes, calling now. Oh, they didn't get the shipment of ham in so the Hawaiian is not available today. Second choice?",
  "question": "According to the assistant's last message, is \"Hawaiian\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q02b42958c0",
  "kind": "yes/no",
  "text": "Assistant: Will that be all for your order.\nCustomer: Yeah that is all, can you please repeat my order?\nAssistant: Your order is a medium caramel macchiato with almond milk, a small Americano, and a small cappucino with almond milk.",
  "question": "According to the assistant's last message, is \"caramel macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4fbc784475",
  "kind": "yes/no",
  "text": "Customer: Intelligent auto solutions\nAssistant: Ok.. What make and model car do you have?\nCustomer: Prius, Toyota 2016",
  "question": "In the customer's last message, does \"2016\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2161ff907d",
  "kind": "yes/no",
  "text": "Assistant: Okay I have placed the order and paid for it with your online accont. You should receive a receipt via text shortly.\nCustomer: Thank you, when will it be ready?\nAssistant: The pizzas will be ready for pick up in 25 minutes at Uno on Grand Street.",
  "question": "According to the assistant's last message, is \"Uno\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa9fa00add9",
  "kind": "yes/no",
  "text": "Customer: Make it extra large.\nAssistant: Alright, how about crust type, thin or thick?\nCustomer: Thin of course.",
  "question": "In the customer's last message, does \"Thin\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4f567a97eb",
  "kind": "yes/no",
  "text": "Customer: Yes, please.\nAssistant: Alright, I have one table booked at Ostra, April 9th at 7PM. Four people two children, one highchair, outside.\nCustomer: Yes. Thank you so much. It will be under my name Mathius Levens",
  "question": "In the customer's last message, does \"Mathius Levens\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q909cfb6fd5",
  "kind": "yes/no",
  "text": "Customer: I'd like to order pizza from Dominoes\nAssistant: Sure, what is the location of the store?\nCustomer: It's located on 1234 Fake Street, Fakeville",
  "question": "In the customer's last message, does \"1234 Fake Street, Fakeville\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q218bfebb27",
  "kind": "yes/no",
  "text": "Customer: Is Pizza Hut currently open?",
  "question": "In the customer's last message, does \"Pizza Hut\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q65b0036553",
  "kind": "yes/no",
  "text": "Customer: I will need two tickets.\nAssistant: Is there anything else?\nCustomer: Yes, the AMC RAINBOW PROMENADE 10 location has reserved seating, see if you can get the reserved seating for either showtime.",
  "question": "In the customer's last message, does \"AMC RAINBOW PROMENADE 10\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2e3a04a041",
  "kind": "yes/no",
  "text": "Customer: What is the difference in price between a medium and a large?\nAssistant: There is a $2 difference.\nCustomer: I will just take a large then.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q605f49184e",
  "kind": "yes/no",
  "text": "Customer: I need to order a pizza for pick up at Papa johns",
  "question": "In the customer's last message, does \"Papa johns\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe13a131cb5",
  "kind": "yes/no",
  "text": "Customer: Sure. What?\nAssistant: We need the make and model as well as your phone number. Should I give your cell or home?\nCustomer: Give my cell 858-322-1118 and my Honda CRV RKW881",
  "question": "In the customer's last message, does \"Honda CRV RKW881\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q25f6862f59",
  "kind": "yes/no",
  "text": "Customer: I need to make an appointment for my car. The fan isn't working when I turn on the A/C. Can you go to Intelligent Auto Solutions site and set up a time for me?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9d0ac42ce9",
  "kind": "yes/no",
  "text": "Customer: Yes.\nAssistant: And where are you going to?\nCustomer: Red Robin at Arrowhead",
  "question": "In the customer's last message, does \"Red Robin at Arrowhead\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf3ced7b92d",
  "kind": "yes/no",
  "text": "Customer: I'm planning to have dinner for two at a french restaurant, do you have any suggestions?",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0d9f8ebb68",
  "kind": "yes/no",
  "text": "Assistant: Okay, how many people are in your party?\nCustomer: 4 people in total.\nAssistant: I'm sorry, but a regular ride is not big enough to accommodate your party.",
  "question": "According to the assistant's last message, is \"regular\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0b2b6358fe",
  "kind": "yes/no",
  "text": "Customer: I'd like a grande Americano from Starbucks",
  "question": "In the customer's last message, does \"grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q098dd6fce9",
  "kind": "yes/no",
  "text": "Assistant: sure thing, what would you like to get?\nCustomer: Id like a medium specialty pizza with everything on it. the works\nAssistant: Ok, we got you. However, we just ran out of sausage, can we substitute another meat for you?",
  "question": "According to the assistant's last message, is \"sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6f323f0a51",
  "kind": "yes/no",
  "text": "Assistant: OK I am ordering it now.\nCustomer: Thank you, this is gonna be great!\nAssistant: Whoa! No red onions, and no garlic crust it says here.",
  "question": "According to the assistant's last message, is \"garlic crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q508f40690a",
  "kind": "yes/no",
  "text": "Assistant: What size?\nCustomer: Trenta\nAssistant: They don't have trenta lids is that ok?",
  "question": "According to the assistant's last message, is \"trenta\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6a231281b5",
  "kind": "yes/no",
  "text": "Customer: P. I. A. C. I.\nAssistant: Ok, Piaci. And is that in Fort Bragg, South Carolina? I'm not seeing one listed.\nCustomer: No, up north in Fort Bragg, California. I'm not going that far for pizza.",
  "question": "In the customer's last message, does \"up north in Fort Bragg, California\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4f288e865c",
  "kind": "yes/no",
  "text": "Customer: yes\nAssistant: with pepperoni, tomatoes, canadian bacon extra cheese and mushrooms\nCustomer: yes, dont forget deep dish",
  "question": "In the customer's last message, does \"deep dish\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb0846ebee6",
  "kind": "yes/no",
  "text": "Assistant: Okay, let me confirm this.\nCustomer: Thanks so much!\nAssistant: You're welcome! Your appointmetont is confirmed for today 04/15/2019 at 2:00pm at Intelligent Auto Solutions. You are getting your turning signal repaired. The fee will be $100.00. There could/will be additional charges depending on your auto repair.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
