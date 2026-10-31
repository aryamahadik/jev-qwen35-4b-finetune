# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-051 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-051.json

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
  "qid": "q72d11a0dd7",
  "kind": "yes/no",
  "text": "Assistant: Do you want whipped cream on it?\nCustomer: Oh yeah.\nAssistant: Unfortunately, whole milk is not available.",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd800fa3ad9",
  "kind": "yes/no",
  "text": "Customer: Yes that is fine, is there anything before 6pm\nAssistant: Yes, I see two showtimes for 1:10 pm and 3:45 pm. How many tickets are you looking for?\nCustomer: I need two tickets and I think I will go with the 3:45 showing",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q33cc9be56b",
  "kind": "yes/no",
  "text": "Assistant: Ok, at what time?\nCustomer: I need the reservation for 7pm\nAssistant: 7pm is not available, please request a different time",
  "question": "According to the assistant's last message, is \"7pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf209f517ea",
  "kind": "yes/no",
  "text": "Assistant: Not necessary, I already have it on file.\nCustomer: Ok great.\nAssistant: Ok, your drink is on order at the Starbucks on South Westlake Boulevard and will be ready for pickup shortly. Your receipt will be sent to your mobile device via text message.",
  "question": "According to the assistant's last message, is \"South Westlake Boulevard\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1f4b201f03",
  "kind": "yes/no",
  "text": "Assistant: Ok. No problem.\nCustomer: Thanks.\nAssistant: Bad news. They don't have any chicken. Anything else you want?",
  "question": "According to the assistant's last message, is \"chicken\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbb9a659800",
  "kind": "yes/no",
  "text": "Assistant: Are you planning on watching the movie in 3D, Imax, or Standard?\nCustomer: I want to buy tickets for a standard showing.\nAssistant: At the moment, no tickets are available for Shazam today, for a standard showing.",
  "question": "According to the assistant's last message, is \"Shazam\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc5038b7665",
  "kind": "yes/no",
  "text": "Assistant: What time do you want to see the movie?\nCustomer: At 7:00pm\nAssistant: They don't have a 7:00 showing. The closest available time is 8:00pm.",
  "question": "According to the assistant's last message, is \"7:00\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q11f732fc51",
  "kind": "yes/no",
  "text": "Customer: Uber\nAssistant: Is that the Courtyard by Marriott Downtown?\nCustomer: No, it's the Nashville Marriott at Vanderbilt University",
  "question": "In the customer's last message, does \"the Nashville Marriott at Vanderbilt University\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc8448b06ee",
  "kind": "yes/no",
  "text": "Assistant: Unfortunately, they cannot accommodate you at 6pm. Would you like to try a different time?\nCustomer: Yes, please ask if they can seat us at 6:30pm.\nAssistant: I'm sorry, 6:30pm is not available either.",
  "question": "According to the assistant's last message, is \"6:30pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcdf317c9af",
  "kind": "yes/no",
  "text": "Customer: It's a 2009 Chevy Corvette\nAssistant: Ok, and what kind of problem is it having?\nCustomer: I think the clutch is slipping",
  "question": "In the customer's last message, does \"clutch is slipping\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q125f4098fa",
  "kind": "yes/no",
  "text": "Assistant: Your order is for one venti size Black and White Mocha with 1% milk and whipped cream from the Starbucks on Castro St in Mountain View.\nCustomer: Yes thats it.\nAssistant: An order has been placed at the Starbucks on Castro St in Mountain View, for one venti Black and White Mocha with 1% milk and whipped cream,",
  "question": "According to the assistant's last message, is \"Black and White Mocha\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7d1fbace79",
  "kind": "yes/no",
  "text": "Assistant: I can seat 4 at 6:30 PM.\nCustomer: That will work. I'll take it.\nAssistant: Okay, your table for four has been reserved at Parma for 6:30 PM tonight.",
  "question": "According to the assistant's last message, is \"Parma\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q85911d102f",
  "kind": "yes/no",
  "text": "Customer: Jackie Olson, and 431-777-6431\nAssistant: Thank you. I have real time access to the auto repair shop's interface so let me see what is available.\nCustomer: I really need to get into the shop asap. My car is overheating and I won't be able to drive it like this for long.",
  "question": "In the customer's last message, does \"overheating\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q49e7c6069c",
  "kind": "yes/no",
  "text": "Customer: Hi [ASSISTANT], could you order a pizza from Pizza Rigazzi for my dinner date?",
  "question": "In the customer's last message, does \"Pizza Rigazzi\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2cf49f1062",
  "kind": "yes/no",
  "text": "Assistant: how many tickets?\nCustomer: two please let's go to the regal theatre\nAssistant: the regal is saying the are sold out both shows. Would you like something different?",
  "question": "According to the assistant's last message, is \"the regal\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q32c7c1e86b",
  "kind": "yes/no",
  "text": "Assistant: Hazelnut is still in stock. Would you like this flavor?\nCustomer: Yes please.\nAssistant: Great, your vente hazelnut latte with almond milk is confirmed at the Kendall Square Starbucks.",
  "question": "According to the assistant's last message, is \"hazelnut latte\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q78f60aa853",
  "kind": "yes/no",
  "text": "Customer: I want some pizzas, two of them\nAssistant: Where do you want them from?\nCustomer: Pizza Hut, in Demoines, Iowa on 7th street.",
  "question": "In the customer's last message, does \"Demoines, Iowa on 7th street\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcb878f7a11",
  "kind": "yes/no",
  "text": "Assistant: Okay, hang on and I'll order\nCustomer: Thank you\nAssistant: Sorry, but they don't have any 2% today",
  "question": "According to the assistant's last message, is \"2%\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdab6b9177a",
  "kind": "yes/no",
  "text": "Assistant: Mikuni is close to you and is popular, does that work?\nCustomer: Sure, can you make me a reservation for 3/31 at 5pm for 6 people?\nAssistant: Mikuni has no available reservations for that day. Want me to try another day?",
  "question": "According to the assistant's last message, is \"Mikuni\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3bef9a6ec2",
  "kind": "yes/no",
  "text": "Customer: Hi Kim\nAssistant: Hello\nCustomer: Can you please book a reservation at Pasta Too for two on Saturday, July 4th?",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q2cc7c9812a",
  "kind": "yes/no",
  "text": "Customer: I could really go for a Cinnamon Cloud Macchiato. Could you order one for me?\nAssistant: Yes of course. How would you like it?\nCustomer: I want a a Grande with coconut milk and extra cinnamon syrup.",
  "question": "In the customer's last message, does \"Grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6fb737b1b7",
  "kind": "yes/no",
  "text": "Customer: Two tickets\nAssistant: What time would you like to see the movie?\nCustomer: 8pm would be great",
  "question": "In the customer's last message, does \"8pm\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfd5dd3a5a6",
  "kind": "yes/no",
  "text": "Customer: Hey, I need to get my car brought into the mechanics.\nAssistant: OK. What seems to be the problem?\nCustomer: It's making a weird noise whenever I stop at traffic stops. I'll pull up for a few seconds and it'll start. It's a 2016 Ford Fiesta ST.",
  "question": "In the customer's last message, does \"Ford Fiesta ST\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qff1fa25dc2",
  "kind": "yes/no",
  "text": "Assistant: Looks like 8:30 PM works as well! Did you want me to book this?\nCustomer: Yes, please!\nAssistant: Okay! 8:30 PM is booked!",
  "question": "According to the assistant's last message, is \"8:30 PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q366cfd57e3",
  "kind": "yes/no",
  "text": "Customer: I want the one in Center City Philadelphia\nAssistant: ok how many people\nCustomer: It is for four people.",
  "question": "In the customer's last message, does \"four\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8d94f4d81e",
  "kind": "yes/no",
  "text": "Assistant: Okay, let me confirm this.\nCustomer: Thanks so much!\nAssistant: You're welcome! Your appointmetont is confirmed for today 04/15/2019 at 2:00pm at Intelligent Auto Solutions. You are getting your turning signal repaired. The fee will be $100.00. There could/will be additional charges depending on your auto repair.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb6e01e6639",
  "kind": "yes/no",
  "text": "Assistant: PABU Izakaya is closer.\nCustomer: Okay, see if a table is available at PABU Izakaya on March 4th at 6:30 p.m. for 2 people, outside if possible.\nAssistant: Unfortunately, there are no tables available outside at that time.",
  "question": "According to the assistant's last message, is \"outside\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8418b17968",
  "kind": "yes/no",
  "text": "Assistant: what type of pizza would you like\nCustomer: I want the Hawaiian pizza but I would like to exchange the ham for sausage\nAssistant: sorry sausage is not an option, is there something else you would like instead",
  "question": "According to the assistant's last message, is \"sausage\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf90d132c74",
  "kind": "yes/no",
  "text": "Assistant: There will be a fee for the inspection of the mechanical problem.\nCustomer: That is fine, thanks for your help.\nAssistant: You're all set with an appointment for Thursday at eight a.m., for the 2011 Dodge Nitro, tune up, inspection of check engine light, Evan Phillips dropping off, and we have 33-991-0000 as the contact number to reach you. The inspection fee will be fifty dollars. Have a great day!",
  "question": "According to the assistant's last message, is \"tune up, inspection of check engine light\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe0af7d2e59",
  "kind": "yes/no",
  "text": "Customer: I'd like to see a movie.\nAssistant: Of course! What can I do for you?\nCustomer: I wanted to see Aquaman, is that possible?",
  "question": "In the customer's last message, does \"Aquaman\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8d7904bb86",
  "kind": "yes/no",
  "text": "Customer: I need to make a car repair appointment with Intelligent Auto Solutions\nAssistant: Ok what's the year, make, and model of you car\nCustomer: A 2011 Dodge Caliber",
  "question": "In the customer's last message, does \"2011\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe767a9acd4",
  "kind": "yes/no",
  "text": "Customer: Is there any deals on oi changes?\nAssistant: No not at this time.\nCustomer: Okay I'll take an oil change as well",
  "question": "In the customer's last message, does \"oil change\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcf6de64035",
  "kind": "yes/no",
  "text": "Customer: I'm good with an Uber Pool.\nAssistant: Got it. What time do you want to be picked up?\nCustomer: I need to be picked up at 2:45.",
  "question": "In the customer's last message, does \"2:45\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qeef7729642",
  "kind": "yes/no",
  "text": "Customer: Yes, Intelligent Auto Solutions.\nAssistant: Okay, I have their number saved already. Whats going on?\nCustomer: It is for my 2009 Mercury Mariner.",
  "question": "In the customer's last message, does \"2009\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q664ef29911",
  "kind": "yes/no",
  "text": "Customer: Hightstown NJ\nAssistant: I see two in Hightstown, which one ?\nCustomer: The one on Route 130.",
  "question": "In the customer's last message, does \"Route 130\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q7eda9930cb",
  "kind": "yes/no",
  "text": "Assistant: Would you like to order anything else today?\nCustomer: No, just the pizza.\nAssistant: Sorry sir, it turns out we've run out of pineapple tonight. Would you like to replace it with a different topping?",
  "question": "According to the assistant's last message, is \"pineapple\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2b767982a6",
  "kind": "yes/no",
  "text": "Customer: 666-666-6666\nAssistant: What type of car is this for?\nCustomer: A 2018 Chrysler 300.",
  "question": "In the customer's last message, does \"2018\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3fe68b8b90",
  "kind": "yes/no",
  "text": "Assistant: It does not appear to be.\nCustomer: Do they have any 3D showtimes left?\nAssistant: It doesn't look like they're showing it in 3d tomorrow.",
  "question": "According to the assistant's last message, is \"3d\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q82fe182465",
  "kind": "yes/no",
  "text": "Customer: Hey Caroline, I would like to get tickets to see Shazam tonight.\nAssistant: ok, where would you like to go to see it\nCustomer: I am thinking about the Frank Theatre.",
  "question": "In the customer's last message, does \"Frank Theatre\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q12ef6762e9",
  "kind": "yes/no",
  "text": "Assistant: They're at 2302B Nesconset Highway in Stony Brook.\nCustomer: Okay, got it. I just wrote that down.\nAssistant: Perfect. I just put the order in. You're confirmed for one large pizza with anchovy and kalamata olives. It'll be ready for pickup in 25 minutes. Your receipt will go directly to your cell phone by text message.",
  "question": "According to the assistant's last message, is \"kalamata olives\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qdf1f6f825b",
  "kind": "yes/no",
  "text": "Customer: Hey, would you be able to get me tickets to a movie?\nAssistant: Sure. Where did you want to go?\nCustomer: Los Angeles area theater.",
  "question": "In the customer's last message, does \"Los Angeles area\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q783a5e46da",
  "kind": "yes/no",
  "text": "Assistant: Any whipped cream or other flavors?\nCustomer: No I just want the espresso and almond milk. I'm a purist.\nAssistant: All good. The order is placed. It will be ready at Springwood Rd in 10.",
  "question": "According to the assistant's last message, is \"Springwood Rd in 10\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc8a7156fc3",
  "kind": "yes/no",
  "text": "Customer: oh my. What about a sausage and pepperoni extra cheese?\nAssistant: thin crust for that one as well?\nCustomer: no hand tossed",
  "question": "In the customer's last message, does \"hand tossed\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q37aa620d08",
  "kind": "yes/no",
  "text": "Customer: AMC 30\nAssistant: What time is best for you?\nCustomer: 7 PM",
  "question": "In the customer's last message, does \"7 PM\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q51fad86739",
  "kind": "yes/no",
  "text": "Customer: im at target from imola\nAssistant: alright to drop at where?\nCustomer: target plaza",
  "question": "In the customer's last message, does \"target plaza\" give the pickup location (where the ride starts) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q55169b092f",
  "kind": "yes/no",
  "text": "Assistant: Great what milk do you want with it?\nCustomer: Whole milk please.\nAssistant: Ok well it looks like the whole milk actually is not available right now.",
  "question": "According to the assistant's last message, is \"whole milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd32d03b07f",
  "kind": "yes/no",
  "text": "Customer: I'd like to book an appoint at Intelligent Auto Solutions\nAssistant: Sure, what is the make, model, and year of your vehicle?\nCustomer: Ford Focus 2014",
  "question": "In the customer's last message, does \"2014\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q032a80a20b",
  "kind": "yes/no",
  "text": "Assistant: I'm showing at 6:30 pm or at 8 pm.\nCustomer: 8 pm will do.\nAssistant: Okay, I have booked a booth for two at Hikata on Saturday at 8 pm.",
  "question": "According to the assistant's last message, is \"Hikata\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2570859a60",
  "kind": "yes/no",
  "text": "Customer: The shop I go to is only open on Saturday, so let's try for Saturday, March 30.\nAssistant: O.k. You would like an appointment for this Saturday, March 30.\nCustomer: That is correct. Call Jim at Intelligent Auto Solutions and ask for a morning appointment.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q15ed6333aa",
  "kind": "yes/no",
  "text": "Customer: Anaheim Gardenwalk\nAssistant: How long are you willing to wait? What type of ride?\nCustomer: 10 mins and UberX`",
  "question": "In the customer's last message, does \"10 mins\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
