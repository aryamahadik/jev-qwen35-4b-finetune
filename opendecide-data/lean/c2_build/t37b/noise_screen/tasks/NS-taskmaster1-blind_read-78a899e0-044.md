# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-044 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-044.json

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
  "qid": "qa82751998f",
  "kind": "yes/no",
  "text": "Assistant: Okay great. What time will you be arriving?\nCustomer: 7:30 pm. I should be right on time.\nAssistant: Okay excellent. I have your reservation confirmed for 7:30 pm",
  "question": "According to the assistant's last message, is \"7:30 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfae0d187a4",
  "kind": "yes/no",
  "text": "Assistant: Yes, there are tickets left for the 7 P.M. IMAX showing, but not the 10 P.M.\nCustomer: That works then.\nAssistant: Alright, I have placed your order for 2 tickets to Hellboy at 7:00 P.M. at the Regal Cinemas in Mayfair. I am sending your tickets to your phone now.",
  "question": "According to the assistant's last message, is \"7:00 P.M\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9a7401b6e6",
  "kind": "yes/no",
  "text": "Assistant: Would you like whipped cream on top?\nCustomer: No, thank you.\nAssistant: Actually, they just ran out of skim milk. What would you like instead?",
  "question": "According to the assistant's last message, is \"skim milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q62b9257264",
  "kind": "yes/no",
  "text": "Customer: what are the names\nAssistant: the first one is passage to india and the second is indian cuisine\nCustomer: Let's go for passage to india and book me a table tonight for two near the window",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6567abce95",
  "kind": "yes/no",
  "text": "Customer: Assistant, What theaters are playing the movie US near me.\nAssistant: Malco Studio on the Square,Malco Paradiso Cinema Grill And IMAX,Malco Wolfchase Cinema Grill\nCustomer: Can I get tickets to US at Malco Wolfchase Cinema Grill in 3d",
  "question": "In the customer's last message, does \"Malco Wolfchase Cinema Grill\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0250ffd962",
  "kind": "yes/no",
  "text": "Assistant: There is a nice place in Staten Island . Taste of India . Cousy place with a good food. Should I ask if they have a table ?\nCustomer: Well , I would like to try a new place . Call and ask please.\nAssistant: Table for tomorrow after 6 is not available. Should we move it for later ?",
  "question": "According to the assistant's last message, is \"tomorrow after 6\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q23bf2dea99",
  "kind": "yes/no",
  "text": "Assistant: What about Luigi's on McPherson Church Road?\nCustomer: We've been there before, it's really good. What about 6:00 tomorrow with an outside table since the weather is going to be really nice.\nAssistant: They won't have outside seating because they have a large party booked.",
  "question": "According to the assistant's last message, is \"outside seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q630cc8ba44",
  "kind": "yes/no",
  "text": "Customer: An extra large please.\nAssistant: Sorry, they only have single slices, smalls and larges. Which one did you want?\nCustomer: The large then.",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa6317de721",
  "kind": "yes/no",
  "text": "Assistant: Same size?\nCustomer: Sure thing.\nAssistant: Ok, I've placed your order. One venti white chocolate mocha late, extra milk, extra sugar.",
  "question": "According to the assistant's last message, is \"white chocolate mocha late\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q56d481a288",
  "kind": "yes/no",
  "text": "Assistant: Okay, sure, let me find you a car.\nCustomer: Actually, can you request a Lux car for me?\nAssistant: Unfortunately, I do not see any Lux.",
  "question": "According to the assistant's last message, is \"Lux\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q80ee88dd35",
  "kind": "yes/no",
  "text": "Customer: I'd like to make a reservation at El Tiempo Cantina for tonight.\nAssistant: Okay, which location would you like?\nCustomer: The Westheimer location, please.",
  "question": "In the customer's last message, does \"Westheimer\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa5fb130dbe",
  "kind": "yes/no",
  "text": "Assistant: So, I have some bad new.\nCustomer: Well tell me!\nAssistant: It seems that Starbucks is out of the cinnamon sauce. What would you like to do?",
  "question": "According to the assistant's last message, is \"cinnamon sauce\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9e22879d3f",
  "kind": "yes/no",
  "text": "Customer: Yea I'll add whipped cream.\nAssistant: Got it. Anything else you would like to order?\nCustomer: Yes I'd like a grande cappuccino as well.",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8f4729328d",
  "kind": "yes/no",
  "text": "Customer: I'd like to order a pizza from Hungry Howies.",
  "question": "In the customer's last message, does \"Hungry Howies\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6e0c397c17",
  "kind": "yes/no",
  "text": "Customer: I'd like to buy tickets for Green Book",
  "question": "In the customer's last message, does \"Green Book\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe04077b838",
  "kind": "yes/no",
  "text": "Assistant: Perfect! I will call them back now.\nCustomer: That is late, but I really want to go there.\nAssistant: I called and have you booked for that 9 o'clock spot. I am sure it will be worth going late.",
  "question": "According to the assistant's last message, is \"9 o'clock\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q387b556e77",
  "kind": "yes/no",
  "text": "Customer: There's a Starbucks right around the corner. Let's go there.\nAssistant: Ok, great. What would you like to order?\nCustomer: A Cinnamon Cloud Macchiato.",
  "question": "In the customer's last message, does \"Cinnamon Cloud Macchiato\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9fb8cbb0d3",
  "kind": "yes/no",
  "text": "Assistant: Okay, can I get a name and phone number to contact you at?\nCustomer: Dany Turk, 555-555-5555\nAssistant: Got it, I've booked that in under Dany Turk and they will contact you at 555-555-5555 when the vehicle is ready",
  "question": "According to the assistant's last message, is \"Dany Turk\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7da8bc7819",
  "kind": "yes/no",
  "text": "Assistant: Ok in what time?\nCustomer: tonight would be the best.\nAssistant: Unfortunately 6:pm is all sold out. Would you like me to give you a reference?",
  "question": "According to the assistant's last message, is \"6:pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe145bf2839",
  "kind": "yes/no",
  "text": "Assistant: To confirm your order you would like a Grande Caramel Macchiato with 2% milk and a double shot of espresso from the Starbucks on Rt. 3 in Frederickburg. Is that correct?\nCustomer: That's correct.\nAssistant: Your drink has been ordered and will be ready for pickup at the Rt. 3 location in Fredericksburg. Your receipt will be sent to your phone via text message.",
  "question": "According to the assistant's last message, is \"Rt. 3 location in Fredericksburg\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd6da1914c1",
  "kind": "yes/no",
  "text": "Assistant: Sorry, US at Malco Wolfchase Cinema Grill is sold out in 3d and regular showings.\nCustomer: What about Malco Studio on the Square?\nAssistant: Checking, no 3d showings.",
  "question": "According to the assistant's last message, is \"3d\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q70ec721a29",
  "kind": "yes/no",
  "text": "Customer: Ok, no problem. Let me know when you're ready for my order!\nAssistant: Ok, I'm ready....\nCustomer: Large PAN pizza with Butter Crust. Toppings: Green ppr, BLK olive, Tomatoes, Onion, Sausage & XTRA CHEESE.",
  "question": "In the customer's last message, does \"Large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q15843187f4",
  "kind": "yes/no",
  "text": "Assistant: Ok, I have updated your order to a Venti Caramel Macchiato with whole milk with whipped cream on top.\nCustomer: Please confirm the whole order for me again.\nAssistant: Your Venti Caramel Macchiato with whole milk is on order at the 110 Donahue St Sausalito location and will be ready for pickup at 4pm. Your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"Caramel Macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q326f6685a5",
  "kind": "yes/no",
  "text": "Assistant: A large bacon and jalapenos?\nCustomer: That would be great.\nAssistant: I'm sorry but the local Imo's is out of jalapenos.",
  "question": "According to the assistant's last message, is \"jalapenos\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe70380a481",
  "kind": "yes/no",
  "text": "Assistant: They cannot estimate that at this time\nCustomer: Ok, please schedule\nAssistant: Thank you, you are reserved at Intelligent Auto Solutions tomorrow at 8 am under Peter 702-555-3434 for a 2015 Ford Focus for a air conditioning diagnostic for $100",
  "question": "According to the assistant's last message, is \"air conditioning diagnostic\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q12d4f7dc35",
  "kind": "yes/no",
  "text": "Customer: I will be in Naples florida for the weekend and need a nice place to have dinner.",
  "question": "In the customer's last message, does \"Naples florida\" give the location of the restaurant (city, area or address) for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb1547d95d8",
  "kind": "yes/no",
  "text": "Customer: Actually, I would like to have an extra pump of whipped cream on the top.\nAssistant: Extra whipped cream? Added that to the order. What size would you like this drink to be?\nCustomer: I would like a triple please.",
  "question": "In the customer's last message, does \"triple\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q48d6defedd",
  "kind": "yes/no",
  "text": "Customer: Just one other person.\nAssistant: Do you have a preferred theater?\nCustomer: The SouthSide Works Cinema looks nice.",
  "question": "In the customer's last message, does \"SouthSide Works Cinema\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8aca212b0d",
  "kind": "yes/no",
  "text": "Customer: Fuego is in Henderson, NV and Olive garden is on North Nellis blvd in Las Vegas, nv\nAssistant: How many people will be in your reservation?\nCustomer: there will be two of us",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q893bb57720",
  "kind": "yes/no",
  "text": "Assistant: What phone number can they contact you at?\nCustomer: 333-333-3333\nAssistant: Okay, I've scheduled your appointment at Intelligent Auto Solutions for 3:30 this afternoon. The inspection fee for a engine lurching is $100.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8254260326",
  "kind": "yes/no",
  "text": "Assistant: Please hold while I call them.\nCustomer: Ok.\nAssistant: So, it appears that they have NO free reservations at 7... but they might have a 7:30?",
  "question": "According to the assistant's last message, is \"7.\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5125f04436",
  "kind": "yes/no",
  "text": "Customer: Yes i am from new york city. any starbucks coffee shop available.\nAssistant: Yes, near by newyork. May I take your order?\nCustomer: Yes. I'd like the flat white order of coffee.",
  "question": "In the customer's last message, does \"flat white\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7888e8bc79",
  "kind": "yes/no",
  "text": "Customer: Reno, Nevada\nAssistant: What theater?\nCustomer: Century 16",
  "question": "In the customer's last message, does \"Century 16\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7af0854f8a",
  "kind": "yes/no",
  "text": "Assistant: Ok, I will schedule under John Smith. What is his phone number?\nCustomer: 000-000-0000\nAssistant: Perfect. I have your 2006 Galant scheduled at Intelligent Auto for today at 3:30pm",
  "question": "According to the assistant's last message, is \"Intelligent Auto\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6362cd47e2",
  "kind": "yes/no",
  "text": "Assistant: Ok any special requests?\nCustomer: Yes we'd also like a booth.\nAssistant: Ok I have you booked for May 1st at 5 in a booth at Bricco for two people.",
  "question": "According to the assistant's last message, is \"May 1st at 5\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q025675be28",
  "kind": "yes/no",
  "text": "Assistant: Let me check. They do have the Hawaiian pizza.\nCustomer: Great, please go ahead and order a large pizza for me.\nAssistant: No problem. They confirmed your order of a large Extramostbestest Hula Hawaiian pizza.",
  "question": "According to the assistant's last message, is \"Extramostbestest Hula Hawaiian pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7a9b1903e6",
  "kind": "yes/no",
  "text": "Assistant: Almond milk it is. I'm sorry, that is disappointing, but I think almond milk will be good too. I'm placing that order now.\nCustomer: That's ok, I know it's not your fault.\nAssistant: I appreciate your understanding. Your Venti Cinnamon Dolce Latte with almond milk and whipped cream will be ready shortly at the Starbucks on 21st and State Street in Salt Lake City. In just a moment, your mobile device should get a text message with your receipt. Let me know how the coffee turns out!",
  "question": "According to the assistant's last message, is \"Cinnamon Dolce Latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3b93ad5dd8",
  "kind": "yes/no",
  "text": "Customer: Fort Worth 76108 and I will look at the menu real quick.\nAssistant: Okay take your time no problem.\nCustomer: Okay I want a Black and White Mocha and a Blueberry scone.",
  "question": "In the customer's last message, does \"Black and White Mocha\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5e23439a59",
  "kind": "yes/no",
  "text": "Assistant: a medium pepperoni and sausage?\nCustomer: yes please\nAssistant: they don't have any pepperoni",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8fbcec3d2f",
  "kind": "yes/no",
  "text": "Customer: Hey, can you make an appointment right now for me to take in my car to the auto shop, Intelligent Auto Solutions? Maybe book online?",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbf8d20fa19",
  "kind": "yes/no",
  "text": "Customer: ok that would be great,\nAssistant: can i have the make, model and a year?\nCustomer: yes its Bmw 740il 1997",
  "question": "In the customer's last message, does \"Bmw 740il\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf450cb4dac",
  "kind": "yes/no",
  "text": "Customer: Get me the nice one, I'm old, I deserve it.\nAssistant: Ok, and what time do you want to be picked up?\nCustomer: As soon as possible, but I'm not done packing yet so I need another 30 minutes to get down stairs",
  "question": "In the customer's last message, does \"30 minutes\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5bafbd5a38",
  "kind": "yes/no",
  "text": "Assistant: Okay let me check on that\nCustomer: Sure\nAssistant: Looks like soy milk is not available what other option would you like?",
  "question": "According to the assistant's last message, is \"soy milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q341e05dedd",
  "kind": "yes/no",
  "text": "Assistant: Which type of ride would you like?\nCustomer: How much would a Lux ride be?\nAssistant: Sorry, the Lux ride is currently not available.",
  "question": "According to the assistant's last message, is \"Lux ride\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe670aec089",
  "kind": "yes/no",
  "text": "Customer: Hey Susan, can you order an Uber for me?\nAssistant: I can do that. Where do you need to be picked up?\nCustomer: Gordman's in Arnold Crossroads in Arnold, Mo. We all went shopping before the game.",
  "question": "In the customer's last message, does \"Gordman's in Arnold Crossroads in Arnold, Mo\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q521b731035",
  "kind": "yes/no",
  "text": "Customer: Hi, I'm looking for a place in Midtown that has good tacos.\nAssistant: I found Tacos A Go Go, Cyclone, and Saint Daine's.\nCustomer: Can you book a table for 4 outside at Tacos A Go Go for 5:30?",
  "question": "In the customer's last message, does \"5:30\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8cb25f903b",
  "kind": "yes/no",
  "text": "Assistant: What size?\nCustomer: Small, please.\nAssistant: They said they're out of mushrooms and garlic.",
  "question": "According to the assistant's last message, is \"mushrooms\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q74653b3b66",
  "kind": "yes/no",
  "text": "Customer: Sounds good. Can I book a table for tonight?\nAssistant: Yes, you can. What time would you like your reservation at?\nCustomer: 6:30 PM please.",
  "question": "In the customer's last message, does \"6:30 PM\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1ab13007fb",
  "kind": "yes/no",
  "text": "Assistant: Okay let me find a car for you\nCustomer: Thanks\nAssistant: Okay your ride will be there in fifteen minutes",
  "question": "According to the assistant's last message, is \"fifteen minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q67e5c27661",
  "kind": "yes/no",
  "text": "Customer: That sound nice, is it one of their sugar-bombs?\nAssistant: Not too bad, it's 260 calories for a Grande.\nCustomer: I can never remember, how big is a Grande.",
  "question": "In the customer's last message, does \"Grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
