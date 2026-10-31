# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-028 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-028.json

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
  "qid": "qda875a67b6",
  "kind": "yes/no",
  "text": "Customer: I'd like an iced skinny cinnamon dolce latte.\nAssistant: What size would you like that to be?\nCustomer: Let's go with a venti today.",
  "question": "In the customer's last message, does \"venti\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q779a345f9f",
  "kind": "yes/no",
  "text": "Customer: I want to buy some movie tickets to see Glass in theaters please.",
  "question": "In the customer's last message, does \"Glass\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3f7cac6d8c",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to make an auto appointment at Intelligent Auto Solutions, please\nAssistant: Sure. I can help you with that. What type of car do you have?\nCustomer: I have a 2018 Kia Sportage",
  "question": "In the customer's last message, does \"2018\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3ff23b1a41",
  "kind": "yes/no",
  "text": "Assistant: Great, I will place your order at the Starbucks in downtown Oakland.\nCustomer: Perfect.\nAssistant: Your order for a grande latte with 2% milk and vanilla, served hot, from the downtown Oakland Starbucks has been placed. Your order will be ready for pick up shortly and the receipt will be sent via text to your mobile device.",
  "question": "According to the assistant's last message, is \"grande\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q900afb84ca",
  "kind": "yes/no",
  "text": "Customer: I was really hoping for this afternoon. I'm afraid I may have a bad gasket.\nAssistant: They said they can probably get to it this afternoon, but they're not sure if they can have it done today if it's a gasket.\nCustomer: Ask for Fred. I've dealt with him in the past. Tell him you're talking to Mitch Donahue. He'll remember me.",
  "question": "In the customer's last message, does \"Mitch Donahue\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qed2353b41d",
  "kind": "yes/no",
  "text": "Assistant: They have 5pm, 6:30pm, 8pm.\nCustomer: Make it for 8pm.\nAssistant: Actually, there is no 8pm available, only 5pm & 6:30pm.",
  "question": "According to the assistant's last message, is \"8pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc6d1b9400a",
  "kind": "yes/no",
  "text": "Customer: Hello, I need a pizza ordered for a small party tonight.\nAssistant: Okay, where would you like me to order from?\nCustomer: Brooklyn Pizza, upper Peach Ave.",
  "question": "In the customer's last message, does \"upper Peach Ave\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q612ddee02e",
  "kind": "yes/no",
  "text": "Customer: Yeah, I remember now.\nAssistant: What would you like to order\nCustomer: I want a large specialty pizza, thin crust, the one with chicken and barbeque sauce",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4af7983861",
  "kind": "yes/no",
  "text": "Customer: No thank you.\nAssistant: The closest showtime is 8:20pm and another at 9:00pm. Which one do you prefer?\nCustomer: 8:20 pm",
  "question": "In the customer's last message, does \"8:20 pm\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0e298c86bf",
  "kind": "yes/no",
  "text": "Customer: Ill take one in the mall this time.\nAssistant: How many tickets are you going to be getting?\nCustomer: I want 4 tickets.",
  "question": "In the customer's last message, does \"4\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q949135d303",
  "kind": "yes/no",
  "text": "Assistant: For which showing would you like these two tickets?\nCustomer: The ten thirty showing, please.\nAssistant: I'm sorry, there is no ten thirty showing. They do have a seven thirty showing, though.",
  "question": "According to the assistant's last message, is \"ten thirty\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc50be945fc",
  "kind": "yes/no",
  "text": "Assistant: unfortunately they don't have any reservations available for a party of 8 at 7pm\nCustomer: I'm not having any luck\nAssistant: I'm afraid not. i checked for 6:30 as well as 7:30 but neither were available.",
  "question": "According to the assistant's last message, is \"6:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q419559c4f6",
  "kind": "yes/no",
  "text": "Customer: sigh, okay how about just a caramel frap?\nAssistant: okay, i see that\nCustomer: Ok good, I would like that, still grande and still coconut milk sub",
  "question": "In the customer's last message, does \"grande\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qab131aadcf",
  "kind": "yes/no",
  "text": "Customer: Get me the large.\nAssistant: What kind of crust do want with it?\nCustomer: I want the crunchy thin crust.",
  "question": "In the customer's last message, does \"crunchy thin\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7bba1bc2a7",
  "kind": "yes/no",
  "text": "Customer: Ok And what are the current ratings for each restaurant?\nAssistant: Orange Hill has 4.4 stars out 5 and The Ranch has 4.6 out of 5\nCustomer: Ok, I would like to schedule reservations for Orange Hill.",
  "question": "In the customer's last message, does \"Orange Hill\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9ba2b909b8",
  "kind": "yes/no",
  "text": "Customer: 2007 Dodge Dynasty\nAssistant: Okay, and what are you bringing it in for?\nCustomer: Tune up",
  "question": "In the customer's last message, does \"Tune up\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd03cbd163c",
  "kind": "yes/no",
  "text": "Customer: Hello, can you help me buy movie tickets for Hellboy? I am going to watch a movie with my friend.\nAssistant: Sure, which location do you prefer?\nCustomer: I want Cinemark Tinseltown at North Aurora.",
  "question": "In the customer's last message, does \"Cinemark Tinseltown\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qaf7ab2b059",
  "kind": "yes/no",
  "text": "Customer: Large.\nAssistant: Ok, what kind of crust would you like?\nCustomer: Hand-tossed crust.",
  "question": "In the customer's last message, does \"Hand-tossed crust\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0fb470a3a6",
  "kind": "yes/no",
  "text": "Assistant: Got it. So that’s one over XL from AC Hotel to farmhouse bar?\nCustomer: Yes!\nAssistant: OK your ride will be on his way in 5 minutes",
  "question": "According to the assistant's last message, is \"5 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q49961a97e7",
  "kind": "yes/no",
  "text": "Customer: No, that's okay, do they have thin or pan crust?\nAssistant: Yes, both of those are available\nCustomer: I'll have it with the pan crust then.",
  "question": "In the customer's last message, does \"pan crust\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb07e7d0f59",
  "kind": "yes/no",
  "text": "Customer: That's too bad! Actually then, I don't want to see it in IMAX at all. It's not necessary. Let's just watch it normally.\nAssistant: Is the 1:15 time going to work for you still?\nCustomer: Yes. 2 tickets for Us at 1:15.",
  "question": "In the customer's last message, does \"Us\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q619faef11b",
  "kind": "yes/no",
  "text": "Customer: Hello i would like some information on an uber ride from my home to the mall then to the grocery store then back home.",
  "question": "In the customer's last message, does \"mall\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdf4be2fc11",
  "kind": "yes/no",
  "text": "Assistant: What size?\nCustomer: Grande.\nAssistant: Okay...It looks like they're out of soy milk, is 2% okay?",
  "question": "According to the assistant's last message, is \"soy milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf5ecc559f2",
  "kind": "yes/no",
  "text": "Assistant: So you want the heart shaped pizza with bruschetta fresh tomato, fresh mozzarella, and spinach?\nCustomer: That is correct.\nAssistant: Your total comes to $11.26 your order has been placed and will be ready for pickup in 25 minutes at 6965 E Broad St, Columbus, OH.",
  "question": "According to the assistant's last message, is \"6965 E Broad St, Columbus, OH\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q647d4ff03b",
  "kind": "yes/no",
  "text": "Assistant: All right, sounds good. I'm placing the reservation now.\nCustomer: Read it back to me when you're finished.\nAssistant: All right, all set. You have a booth reservation for two people on Thursday at 8.",
  "question": "According to the assistant's last message, is \"booth\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb09fa033d0",
  "kind": "yes/no",
  "text": "Customer: It's a 2015 Ford F150.\nAssistant: Okay. What contact details do you want me to put down?\nCustomer: James Johnson and for my phone number put 416-423-9500.",
  "question": "In the customer's last message, does \"James Johnson\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9cdb30d213",
  "kind": "yes/no",
  "text": "Customer: Hey sally i would like to order 2 pizza's from luigis on main street in town.",
  "question": "In the customer's last message, does \"main street in town\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2e65218c82",
  "kind": "yes/no",
  "text": "Assistant: The Chase bank card?\nCustomer: Yes, that one.\nAssistant: Order has been placed. One extra large all meats hand tossed pizza for delivery.",
  "question": "According to the assistant's last message, is \"extra large\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1a7b8ccb78",
  "kind": "yes/no",
  "text": "Customer: Is it possible to get in at 8 pm?\nAssistant: I'm afraid there are no reservations available at that time.\nCustomer: Ok, what about 8:30?",
  "question": "In the customer's last message, does \"8:30\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q65b542c6c8",
  "kind": "yes/no",
  "text": "Customer: No, let me try Scheme Resteraunt and Bar\nAssistant: Okay what location would you like to try?\nCustomer: The one on North 7th Street in Salina, Ks please",
  "question": "In the customer's last message, does \"North 7th Street in Salina, Ks\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd360cbc2e5",
  "kind": "yes/no",
  "text": "Customer: Hey can you set up an appointment at Intelligent Auto Solutions?\nAssistant: I sure can. What kind of car are you bringing in?\nCustomer: A 1999 Honda Accord",
  "question": "In the customer's last message, does \"1999\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe9d350ac34",
  "kind": "yes/no",
  "text": "Customer: I'd like to order a pizza from Pizza Hut.\nAssistant: Which Pizza Hut are you going to order from.\nCustomer: The Pizza Hut on Alondra Blvd, Downey.",
  "question": "In the customer's last message, does \"Pizza Hut\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbc3e0ddbbb",
  "kind": "yes/no",
  "text": "Assistant: Like, do you want any extra sugar, espresso shots, flavor pumps, anything like that?\nCustomer: Oh, no. Just the almond milk.\nAssistant: Hmmm... so it says they're out of almond milk. Do you want a different kind of milk?",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd19a9546aa",
  "kind": "yes/no",
  "text": "Customer: That is unfortunate.\nAssistant: Yes, it really is.\nCustomer: Well, how about Yellow Flamingo. Can you see if the have anything available for tonight?",
  "question": "In the customer's last message, does \"Yellow Flamingo\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1b35cfee9f",
  "kind": "yes/no",
  "text": "Customer: Oh shoot hold on let me look at the user guide\nAssistant: okay no hurry\nCustomer: alright it is a chevy malibu",
  "question": "In the customer's last message, does \"chevy malibu\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcaa4259815",
  "kind": "yes/no",
  "text": "Customer: At the AMC Promenade 24\nAssistant: How many tickets am I booking?\nCustomer: I need two tickets",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3780451a0e",
  "kind": "yes/no",
  "text": "Customer: Yes, you will need my vehicle information, are you ready?\nAssistant: Yes, go ahead\nCustomer: It is a 2010 GMC Yukon XL",
  "question": "In the customer's last message, does \"2010\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q46a8d7236a",
  "kind": "yes/no",
  "text": "Assistant: Let me check. Before I put the information in what car are you driving?\nCustomer: I am on the 2006 Chevrolet Impala. Just use my name John Smith and my personal cell (555) 555 - 5555.\nAssistant: Alright. Thanks so much, let's see...they're actually all booked up for Wednesday. Would you like to try Thursday?",
  "question": "According to the assistant's last message, is \"Wednesday\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q585345d8ff",
  "kind": "yes/no",
  "text": "Customer: Its a Hyundai.\nAssistant: I will also need model, year and color.\nCustomer: It's an Elantra, 2006 and it's silver.",
  "question": "In the customer's last message, does \"Elantra\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q079d669d18",
  "kind": "yes/no",
  "text": "Assistant: Ok I will add that to your order.\nCustomer: Can I get it soon?\nAssistant: Yes the order has been placed at the Starbucks on Cedar and Ashlan to get a Venti Caramel Brulee latte. You want it with extra whip cream, almond milk, chocolate sauce, and with an added espresso shot. I also have a caffe mocha grande hot. Your receipt will be in your email.",
  "question": "According to the assistant's last message, is \"Cedar and Ashlan\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc16ec4563b",
  "kind": "yes/no",
  "text": "Customer: Giant Foods on Cradlerock Way in Columbia\nAssistant: What time would you like to be picked up?\nCustomer: In a half hour",
  "question": "In the customer's last message, does \"half hour\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q03f9a67e7d",
  "kind": "yes/no",
  "text": "Customer: I want a cafe latte\nAssistant: Ok great. What size do you want?\nCustomer: I would like a tall size.",
  "question": "In the customer's last message, does \"tall\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3b2d39211d",
  "kind": "yes/no",
  "text": "Assistant: They have that. Still want a Venti with extra caramel drizzle?\nCustomer: No, can you make it Grande size… definitely still want the extra caramel drizzle though!\nAssistant: Got it. Your Grande Caramel Macchiato with soy milk and extra caramel drizzle was ordered under your account. It’s at the Starbucks on Main St.",
  "question": "According to the assistant's last message, is \"Caramel Macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf8172dddfa",
  "kind": "yes/no",
  "text": "Assistant: Ok. I will go ahead and book two tickets for you for tonight.\nCustomer: great\nAssistant: The tickets are booked for tonight at the Frank Theatre at 4:20 on 3D.",
  "question": "According to the assistant's last message, is \"Frank Theatre\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb289eca539",
  "kind": "yes/no",
  "text": "Customer: I would like to get two tickets to see \"Fighting with my Family\" tonight.\nAssistant: Ok. Where would you like to see the movie?\nCustomer: Burlington, Vermont",
  "question": "In the customer's last message, does \"Burlington, Vermont\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa0f1473e06",
  "kind": "yes/no",
  "text": "Customer: Kindly Confirm to me how urgent the appointment can be approved because I have morning meetings tommorow and I will need the car.\nAssistant: Before I confirm that provide me with your full details for booking\nCustomer: Johnstone Williams, phone number 2434542422",
  "question": "In the customer's last message, does \"Johnstone Williams\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe64b295b23",
  "kind": "yes/no",
  "text": "Customer: Please go to the Intelligent Auto Solutions website and book an appointment for me.\nAssistant: Which car are you taking in?\nCustomer: The 2018 Subaru Outlander.",
  "question": "In the customer's last message, does \"Subaru Outlander\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc0404ad6e1",
  "kind": "yes/no",
  "text": "Customer: I'm near the basketball stadium.\nAssistant: Okay, what would you like?\nCustomer: I'd like a cafe latte large.",
  "question": "In the customer's last message, does \"cafe latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q447adae52f",
  "kind": "yes/no",
  "text": "Customer: Lexus IS 250 and the year is 2015.\nAssistant: Should I just give your name and number?\nCustomer: Yes, schedule it under my name, Mike and give my cell phone number 818-555-1234.",
  "question": "In the customer's last message, does \"Mike\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q244827d05e",
  "kind": "yes/no",
  "text": "Customer: 7:30's good.\nAssistant: Ok, is it just you?\nCustomer: No. Me and a friend, so we need two tickets.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
