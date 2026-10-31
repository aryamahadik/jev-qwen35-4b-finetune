# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-019 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-019.json

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
  "qid": "q9894495ab7",
  "kind": "yes/no",
  "text": "Customer: And basil on everything\nAssistant: Oh right the basil, yeah\nCustomer: And its an extra large",
  "question": "In the customer's last message, does \"extra large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd90ae53f9b",
  "kind": "yes/no",
  "text": "Assistant: Great! Give me a few seconds to book your appointment.\nCustomer: Thank you!\nAssistant: Already! You're all set. I have booked an appointment for you at 10:30 in the morning. If the service is not covered, there will be a minimum fee for this service.",
  "question": "According to the assistant's last message, is \"10:30 in the morning\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7e58b93ee1",
  "kind": "yes/no",
  "text": "Customer: I'm near the basketball stadium.\nAssistant: Okay, what would you like?\nCustomer: I'd like a cafe latte large.",
  "question": "In the customer's last message, does \"cafe latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q784dfdddc7",
  "kind": "yes/no",
  "text": "Customer: David, I need you to make travel arrangements to get me around town tomorrow.\nAssistant: I will be happy to take of that. What is the first place you will need transportation from and where will you be going to?\nCustomer: I need transportation from the office to the Opryland Hotel for a business luncheon.",
  "question": "In the customer's last message, does \"the office\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3facb4b031",
  "kind": "yes/no",
  "text": "Customer: No problem, I'll wait.\nAssistant: I have found Bob's Auto Shop with an opening on Wednesday.\nCustomer: Great, Bob's Auto Shop is fine.",
  "question": "In the customer's last message, does \"Bob's Auto Shop\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd870b33b68",
  "kind": "yes/no",
  "text": "Customer: Hi, I want to order an Uber.\nAssistant: From where to where?\nCustomer: I want to get picked up at Port Authority in New York City and dropped off at Lincoln Center in New York City.",
  "question": "In the customer's last message, does \"Port Authority in New York City\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc98516212a",
  "kind": "yes/no",
  "text": "Customer: I'll be in San Jose for a work meeting and driving home to San Francisco will be too late, so let's do San Jose\nAssistant: Okay. Any preference in theatre?\nCustomer: I'd like to watch it at Eastridge tonight at 8pm, regular seating.",
  "question": "In the customer's last message, does \"Eastridge\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdfb7b8da8c",
  "kind": "yes/no",
  "text": "Assistant: Can you tell me which seats you would like to reserve for the showing?\nCustomer: I have a preference for as close to the screen as possible, but not the closest row. What seats are available at the moment?\nAssistant: Only seat G7 has been reserved for the Wednesday 10:30 am showing, all other seats are currently available.",
  "question": "According to the assistant's last message, is \"10:30 am\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2e1c6415f7",
  "kind": "yes/no",
  "text": "Assistant: Superb! Can I book UberX for you?\nCustomer: That's great with me.\nAssistant: Excellent. I have UberX at $32.70 confirmed.",
  "question": "According to the assistant's last message, is \"$32.70\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0730004159",
  "kind": "yes/no",
  "text": "Customer: How about from Peets on Broadway?\nAssistant: Ok. Do you want a Latte or Mocha or Macchiato or Expresso?\nCustomer: I think I'll go for a Latte, iced.",
  "question": "In the customer's last message, does \"Latte\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qefd4ca4fd5",
  "kind": "yes/no",
  "text": "Assistant: would you like me to reserve a booth or a table\nCustomer: we will be needing a table please\nAssistant: ok the table is unavailable that day. i can change the time or would you like a booth?",
  "question": "According to the assistant's last message, is \"table\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb7aca41d15",
  "kind": "yes/no",
  "text": "Assistant: I will, it is done\nCustomer: thank you\nAssistant: you are welcome, your appointment is at 3 today for noises and slower than normal acceleration as well as a full check up",
  "question": "According to the assistant's last message, is \"today\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q65a331a54a",
  "kind": "yes/no",
  "text": "Assistant: Do you have any special requests?\nCustomer: We need a high chair and a booth.\nAssistant: There are tables available for seven people at the Kicking Kangaroo tonight at 7:00 with a high chair. But, there are no booths available at that time. Would you like a different time?",
  "question": "According to the assistant's last message, is \"booths\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb6bef6a2ff",
  "kind": "yes/no",
  "text": "Assistant: Got it. What time would you like me to make the reservation for?\nCustomer: I would like to make the reservation for 8PM on Thursday.\nAssistant: Ok. I just checked with the restaurant and there is no tables available at 8PM on Thursday.",
  "question": "According to the assistant's last message, is \"8PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q718d6c7184",
  "kind": "yes/no",
  "text": "Customer: Get me two tickets for Hellboy tonight.\nAssistant: What city were you thinking of watching the movie?\nCustomer: My friend lives in Orange, I think they have an AMC theater over there can you look up the address.",
  "question": "In the customer's last message, does \"AMC theater\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0abe7edd63",
  "kind": "yes/no",
  "text": "Assistant: okay what toppings\nCustomer: pepperoni and ham\nAssistant: sorry ham is not available",
  "question": "According to the assistant's last message, is \"ham\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q78044431f4",
  "kind": "yes/no",
  "text": "Customer: I was thinking Chinese or Mexican.\nAssistant: What city are you located in?\nCustomer: Port Huron, Michigan",
  "question": "In the customer's last message, does \"Port Huron, Michigan\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q60ee889643",
  "kind": "yes/no",
  "text": "Assistant: Sure, where would you like your pizza from?\nCustomer: How about Marzonnis? Are they open on Monday evenings?\nAssistant: Im sorry, Marzonnis is closed on Mondays. Is there another pizza place you like?",
  "question": "According to the assistant's last message, is \"Marzonnis\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q64dfade71e",
  "kind": "yes/no",
  "text": "Customer: I want to see Glass, i'm bringing a friend\nAssistant: okay, so you want two tickets?\nCustomer: yeah, two",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q51ed798f8b",
  "kind": "yes/no",
  "text": "Assistant: No problem, is there anything else I can help you with?\nCustomer: Yes, can you see if they can change the oil while it's there. Then, everything will be good to go.\nAssistant: Ok, so you're all set to drop off your 2012 Subaru WRX at Intelligent Auto Solutions, 11:00 AM, and will be charged $120 diagnostic fee and $47 for the oil change.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbad8b72352",
  "kind": "yes/no",
  "text": "Assistant: No, they don't serve chicken.\nCustomer: Then we will go to Saha.\nAssistant: They can't take you at 7:00. Can you do 7:30?",
  "question": "According to the assistant's last message, is \"7:00\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa2c228e89f",
  "kind": "yes/no",
  "text": "Assistant: How about Thistle Lodge Beachfront Restaurant?\nCustomer: That sounds good. Book a table for 4, with a view of the water for Wednesday the 23rd at 7pm\nAssistant: They don't have any reservations left for 7pm for Wednesday night, how about another time?",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7f2631939b",
  "kind": "yes/no",
  "text": "Customer: Yeah, you wouldn't expect this from a truck that only has 40,000 miles.\nAssistant: Ok. I am on their website right now and they are asking for the vehicle information.\nCustomer: Yeah of course, it is a Dodge Ram 1500 2013.",
  "question": "In the customer's last message, does \"Dodge Ram 1500\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q64f460cc75",
  "kind": "yes/no",
  "text": "Assistant: Let me check.\nCustomer: Thanks.\nAssistant: They have a booth available on Friday, but it's not at 6pm. It's at 8pm",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1359cac2d9",
  "kind": "yes/no",
  "text": "Customer: It's a Subaru Legacy Outback 2008.\nAssistant: Okay. And what is the reason for scheduling the service appointment?\nCustomer: The transmission fluid is leaking badly and I have to fill it every morning.",
  "question": "In the customer's last message, does \"The transmission fluid is leaking badly\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q87064bc03a",
  "kind": "yes/no",
  "text": "Assistant: Do you have any special requests?\nCustomer: I'll take a spot of espresso.\nAssistant: Okay. Unfortunately 2% milk is not available",
  "question": "According to the assistant's last message, is \"2% milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5e0ce195bd",
  "kind": "yes/no",
  "text": "Assistant: All of Joe's tables are wheelchair accessible.\nCustomer: Great! Please make the reservation.\nAssistant: You have a confirmed reservation for 2 by the water at 7pm tonight.",
  "question": "According to the assistant's last message, is \"by the water\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5eac3be2c2",
  "kind": "yes/no",
  "text": "Customer: No! But I've heard it's good.\nAssistant: There is a 7:20 of Captain Marvel at Alamo Drafthouse.\nCustomer: Great, book two seats to that.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q5277b09330",
  "kind": "yes/no",
  "text": "Assistant: Your welcome is there anything else that I can help you with?\nCustomer: Yes. I changed my mind and I decided that I really don't want pepperoni, I would like a spinich topping instead of the pepperoni.\nAssistant: Not a problem. I will change pepperoni to spinich. Is there anything else that I can help you with?",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4992f7c149",
  "kind": "yes/no",
  "text": "Customer: There is a nail in the tire im going to need it changed\nAssistant: okay name and phone number they need\nCustomer: okay danielle ziker best number is my cell 455-788-9879",
  "question": "In the customer's last message, does \"danielle ziker\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q56b76cf32f",
  "kind": "yes/no",
  "text": "Assistant: Great I'll put that order right in.\nCustomer: Thank You!\nAssistant: Alright, all set. Your drink is ordered and will be ready for pick up at the West Lafayette starbucks. A receipt will be sent to your cell phone.",
  "question": "According to the assistant's last message, is \"West Lafayette\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q44f2009d94",
  "kind": "yes/no",
  "text": "Customer: 9:40 one sounds good then.\nAssistant: How many seats do you need?\nCustomer: there's four of us.",
  "question": "In the customer's last message, does \"four\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qaecadd4dd4",
  "kind": "yes/no",
  "text": "Assistant: Great! What milk do you want?\nCustomer: Whole milk. It gives that richness, you know?\nAssistant: Agreed, but they don't seem to have Whole. Is 2% fine?",
  "question": "According to the assistant's last message, is \"Whole\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe744540f9e",
  "kind": "yes/no",
  "text": "Customer: Yes, please.\nAssistant: Alright, I have one table booked at Ostra, April 9th at 7PM. Four people two children, one highchair, outside.\nCustomer: Yes. Thank you so much. It will be under my name Mathius Levens",
  "question": "In the customer's last message, does \"Mathius Levens\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc7badb70e6",
  "kind": "yes/no",
  "text": "Assistant: Right away, sir. What time and seating arrangements do you desire?\nCustomer: Ah, for tonight, obviously, let's say 7:30, indoor booth, for two people.\nAssistant: Thank you, sir. This should just take a few moments. Oh, dear. It appears that no indoor seating is available at the time you have requested.",
  "question": "According to the assistant's last message, is \"indoor\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q953582a6d8",
  "kind": "yes/no",
  "text": "Customer: Let me see.. what about Long Horn Steakhouse?\nAssistant: Yes, it looks like they still have a few tables available!\nCustomer: Great! Go ahead and book a table for 4",
  "question": "In the customer's last message, does \"4\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc65a3840f3",
  "kind": "yes/no",
  "text": "Assistant: Okay, is that all.\nCustomer: Yes, that will work\nAssistant: Okay, Your order will be for a grade Vanilla Late with coconut milk and extra vanilla",
  "question": "According to the assistant's last message, is \"extra vanilla\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3b6281d5b4",
  "kind": "yes/no",
  "text": "Customer: I would like to order pizza from Ray's Pizza.",
  "question": "In the customer's last message, does \"Ray's Pizza\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q43d503b320",
  "kind": "yes/no",
  "text": "Customer: I want to order a pizza from pizza hut.",
  "question": "In the customer's last message, does \"pizza hut\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7935319291",
  "kind": "yes/no",
  "text": "Assistant: I see they have a 4:30 or 7:15 showing, the 6pm must be popular, it's sold out.\nCustomer: Oh dear, ok, how about the 7:15\nAssistant: Ok, I can do the 7:15 but 3D is not available.",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q64b13ded74",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry, the first available seating is at 9pm\nCustomer: Take that then\nAssistant: I've set up your reservation at The Pirani for a party of 4 at 9pm on Thursday.",
  "question": "According to the assistant's last message, is \"The Pirani\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qce00022d9c",
  "kind": "yes/no",
  "text": "Assistant: Sure. Anything else?\nCustomer: No, that's it. Oh, make sure it's 2% milk, if they ask.\nAssistant: I'm sorry, apparently they're out of the caramel syrup for the caramel macchiato. Do you want a different latte?",
  "question": "According to the assistant's last message, is \"caramel macchiato\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q210b8f78b6",
  "kind": "yes/no",
  "text": "Assistant: What time would you like it booked for?\nCustomer: I'd like it at 7.\nAssistant: Hmm. It looks like they are booked full for 7, but they have an opening at 8 for 4 people.",
  "question": "According to the assistant's last message, is \"7\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q4073ab7198",
  "kind": "yes/no",
  "text": "Assistant: And the phone you want to use?\nCustomer: 15552550896\nAssistant: Got it. That's 2003 Chevy Cavalier, at 5pm today. This is confirmed.",
  "question": "According to the assistant's last message, is \"2003\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfaeb0ed4d2",
  "kind": "yes/no",
  "text": "Customer: Hi, Can I get a Caramel Macchiato, please?",
  "question": "In the customer's last message, does \"Caramel Macchiato\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qbfa62a082f",
  "kind": "yes/no",
  "text": "Customer: I want to go see How To Train Your Dragon 3.\nAssistant: What location would you like to see the movie at?\nCustomer: Elder Theater, Jackson Center Ohio.",
  "question": "In the customer's last message, does \"Jackson Center Ohio\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf7e25eb523",
  "kind": "yes/no",
  "text": "Customer: I need two.\nAssistant: Which showing do you prefer?\nCustomer: I want the 1:30 pm showing.",
  "question": "In the customer's last message, does \"1:30 pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa775c1500b",
  "kind": "yes/no",
  "text": "Assistant: How about Cowboy Star? When would you like to come in?\nCustomer: This Saturday at 8 PM\nAssistant: Unfortunately, this Saturday we don't have anything at 8 PM",
  "question": "According to the assistant's last message, is \"8 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3f06876a2a",
  "kind": "yes/no",
  "text": "Assistant: What type of milk would you like?\nCustomer: Can I have almond milk?\nAssistant: Im sorry, almond milk is unavailable?",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc81073620e",
  "kind": "yes/no",
  "text": "Assistant: Checking... Yes, Pagoda has tables available. Any other requests?\nCustomer: No, just make it for two people.\nAssistant: OK... I have made a reservation for two people at 8 p.m. Wednesday at Pagoda. The request is for a booth.",
  "question": "According to the assistant's last message, is \"Pagoda\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
