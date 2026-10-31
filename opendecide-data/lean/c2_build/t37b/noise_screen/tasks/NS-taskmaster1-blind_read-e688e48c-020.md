# Replay noise screen blind read NS-taskmaster1-blind_read-e688e48c-020 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-e688e48c-020.json

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
  "qid": "qd7e89d588b",
  "kind": "yes/no",
  "text": "Customer: I'd like to get a large pizza.\nAssistant: Got it! Would you like deep dish, hand tossed or a specialty crust?\nCustomer: I'd like to get a deep dish, please.",
  "question": "In the customer's last message, does \"deep dish\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q807790cf8b",
  "kind": "yes/no",
  "text": "Customer: 9:50\nAssistant: OK, is it just you or are you bringing guests?\nCustomer: I need 2 tickets.",
  "question": "In the customer's last message, does \"2\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q25c7ffb4ee",
  "kind": "yes/no",
  "text": "Assistant: There is a showing at 1:00pm, 3:15pm, and 5:30pm.\nCustomer: I'll like the 3:15pm showing.\nAssistant: The 3:15pm showing is sold out. Would you like to go book for another time?",
  "question": "According to the assistant's last message, is \"3:15pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qba5df6c4fd",
  "kind": "yes/no",
  "text": "Assistant: I'll place your order now.\nCustomer: Thanks!\nAssistant: Bad news. They're currently out of pineapples, would you like to just get ham?",
  "question": "According to the assistant's last message, is \"pineapples\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbd9a159056",
  "kind": "yes/no",
  "text": "Assistant: a medium pepperoni and sausage?\nCustomer: yes please\nAssistant: they don't have any pepperoni",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3a920f7c26",
  "kind": "yes/no",
  "text": "Assistant: Okay, I will check.\nCustomer: Thank you.\nAssistant: John, I booked you a reservation for service on tomorrow.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf58136a98f",
  "kind": "yes/no",
  "text": "Assistant: Ok. I will go ahead and book two tickets for you for tonight.\nCustomer: great\nAssistant: The tickets are booked for tonight at the Frank Theatre at 4:20 on 3D.",
  "question": "According to the assistant's last message, is \"Frank Theatre\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qda8eb60788",
  "kind": "yes/no",
  "text": "Customer: Yes. That sound great.\nAssistant: Could you tell me the name and your address you would like to reserve this appointment under?\nCustomer: Ryan Hardwick. I live at 725 Main Street in Bolingbrooke, Illinois.",
  "question": "In the customer's last message, does \"Ryan Hardwick\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q0598d8028e",
  "kind": "yes/no",
  "text": "Assistant: Okay. Would you like whipped cream on that?\nCustomer: Yes, with a sprinkle of cinnamon on top.\nAssistant: I'm sorry, they are currently out of White Chocolate Mochas and whole milk. Is there something else you would like?",
  "question": "According to the assistant's last message, is \"White Chocolate Mochas\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q383175693d",
  "kind": "yes/no",
  "text": "Customer: Is there availability before 8:00pm\nAssistant: Yes, at 4pm.\nCustomer: Is outdoor seating available at 8:00pm",
  "question": "In the customer's last message, does \"8:00pm\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3772cfb284",
  "kind": "yes/no",
  "text": "Assistant: What would you like to order?\nCustomer: I'd like a medium caramel macchiato, with coconut milk.\nAssistant: I am sorry, coconut milk is not offered as a option for this location?",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb2294e93d1",
  "kind": "yes/no",
  "text": "Customer: Oh, yes, how about half green olives and half mushrooms as well?\nAssistant: Sounds good. Which pizza place were you thinking?\nCustomer: Pizza Hut on 7th Ave.",
  "question": "In the customer's last message, does \"7th Ave\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q248392b2e2",
  "kind": "yes/no",
  "text": "Customer: Sure. It is a 2010 Toyota Highlander.\nAssistant: Got it. Now for your contact information?\nCustomer: Ramon Jaworski and my number is 323-743-0035",
  "question": "In the customer's last message, does \"Ramon Jaworski\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3302a619c2",
  "kind": "yes/no",
  "text": "Assistant: OK, if that's it, I will place your order and get right back to you.\nCustomer: Yes, thank you!\nAssistant: Well they said they are out of Tomatoes and Bell Peppers, do you want a replacement or to just leave them off?",
  "question": "According to the assistant's last message, is \"Tomatoes\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9f106d2ad1",
  "kind": "yes/no",
  "text": "Assistant: ok, how soon will you get there? i want to make sure you order is hot when you get there\nCustomer: in about 5 minutes im driving\nAssistant: ok. unfortunally this location is out of blonde cappucino at the moment. would you like something else?",
  "question": "According to the assistant's last message, is \"blonde cappucino\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe55f4d34e9",
  "kind": "yes/no",
  "text": "Assistant: I am now making the booking for you.\nCustomer: Okay.\nAssistant: They confirmed your booking. Please arrive no later than 7 a.m. tomorrow morning at the auto shop.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf709c0a0b2",
  "kind": "yes/no",
  "text": "Assistant: What kind of milk would you like with that?\nCustomer: Id like to get it with coconut milk.\nAssistant: They are out of coconut milk at this location.",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q29cd0aa149",
  "kind": "yes/no",
  "text": "Assistant: Would you like all the same requests?\nCustomer: yes\nAssistant: Okay, its all set then! You have a reservation for GATO tomorrow evening at 7pm for 5 seats by the window.",
  "question": "According to the assistant's last message, is \"GATO\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1b8c144932",
  "kind": "yes/no",
  "text": "Assistant: It doesn't look like you would be able to order food from those seats, would you like me to check food prices for you?\nCustomer: No, that's okay. I'll just order when I get there.\nAssistant: So, I have ordered seats A1, A2, and A3 for March 28th at 6:45pm for a total of $33.22.",
  "question": "According to the assistant's last message, is \"6:45pm\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q892582eae5",
  "kind": "yes/no",
  "text": "Assistant: How many are riding?\nCustomer: Just 1\nAssistant: OK, I've booked you a Lyft XL that will pick you up in 20 minutes at The Walton Arts Center.",
  "question": "According to the assistant's last message, is \"20 minutes\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q1613d29ebf",
  "kind": "yes/no",
  "text": "Assistant: Ok, I'll call you back.\nCustomer: Thanks\nAssistant: I confirmed that order of a large Bar-B-Que Pizza that will be ready for you to pickup in about 25 minutes.",
  "question": "According to the assistant's last message, is \"Bar-B-Que Pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qd9097763ce",
  "kind": "yes/no",
  "text": "Customer: Can you please stop at Starbucks for some coffee on your way back?\nAssistant: Yeah sure, what would you like? I'll go to the one on the corner.\nCustomer: I'll have a grande americano with two raw sugars and cream.",
  "question": "In the customer's last message, does \"americano\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q96bb1e3977",
  "kind": "yes/no",
  "text": "Customer: I'd like to eat on the patio.\nAssistant: Bialy's doesn't have any 7pm reservations for patio dining.\nCustomer: Check if they can seat us at 7:30 instead.",
  "question": "In the customer's last message, does \"7:30\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qec73d52264",
  "kind": "yes/no",
  "text": "Customer: 2018\nAssistant: Okay i got it.\nCustomer: Also please tell them my name is Joanna Lohnes and my number is 357-5484",
  "question": "In the customer's last message, does \"Joanna Lohnes\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe0e3286b7b",
  "kind": "yes/no",
  "text": "Customer: Yeah, let's delete that pizza and start over\nAssistant: Ok. What do you want on that pizza?\nCustomer: Let's get a medium ham and pineapple instead",
  "question": "In the customer's last message, does \"medium\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf3882c9152",
  "kind": "yes/no",
  "text": "Customer: okay I am free tomorrow at 12:00\nAssistant: perfect, they have an opening then!\nCustomer: okay, my car is a maserati",
  "question": "In the customer's last message, does \"maserati\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qac2009d223",
  "kind": "yes/no",
  "text": "Customer: Pickup, please.\nAssistant: Great, what can I get for you today?\nCustomer: I'd like a large Hawaiian pizza with extra pineapples, please.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qac1c9e209f",
  "kind": "yes/no",
  "text": "Customer: Please make reservations for an Italian dinner for two tonight at 7 p.m. at The Villa.\nAssistant: The Villa isn't available at 7 p.m. tonight.\nCustomer: Please try 8:30 p.m.",
  "question": "In the customer's last message, does \"8:30 p.m.\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q10e39857d0",
  "kind": "yes/no",
  "text": "Customer: 5678223687\nAssistant: Thanks for the info Ma'am Jen. Can I get your order pls?\nCustomer: I would like a large chicken supreme pizza",
  "question": "In the customer's last message, does \"large\" give the type of crust for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3fb2e313ee",
  "kind": "yes/no",
  "text": "Customer: Pizza Hut\nAssistant: What pizza would you like to order?\nCustomer: Large pan pizza with green pepper, onion and olives.",
  "question": "In the customer's last message, does \"Large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb824a59237",
  "kind": "yes/no",
  "text": "Customer: Barbuto\nAssistant: What time?\nCustomer: 7 pm please.",
  "question": "In the customer's last message, does \"7 pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q511b291efe",
  "kind": "yes/no",
  "text": "Customer: The Avengers 3D at 9:15 pm for two.\nAssistant: Upon checking, it looks like the 3D at 9:15 is already sold out but we have 2D still available at 10:30 which has more free seats. Is that alright?\nCustomer: I don't mind 2D and 10:30 is good.",
  "question": "In the customer's last message, does \"10:30\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa9cd2d5e25",
  "kind": "yes/no",
  "text": "Customer: I want to order a couple of pizzas from Marcos.",
  "question": "In the customer's last message, does \"Marcos\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd6bc1ff52b",
  "kind": "yes/no",
  "text": "Customer: Hi assistant, I need a ride from my house to the movie theater.",
  "question": "In the customer's last message, does \"my house\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q704bc7027c",
  "kind": "yes/no",
  "text": "Assistant: Okay, let me check. Take your time.\nCustomer: Take your time.\nAssistant: Sorry, the Supreme pizza is out of stock today. Do you want to order something else?",
  "question": "According to the assistant's last message, is \"Supreme pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q6994de92d9",
  "kind": "yes/no",
  "text": "Assistant: Ok, let me get back with them.\nCustomer: Thanks again!\nAssistant: Ok, all set. They reserved a table for you by the fire pit inside at 5pm",
  "question": "According to the assistant's last message, is \"5pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5a620bf2fd",
  "kind": "yes/no",
  "text": "Customer: Sounds good. I'll take that, thanks.\nAssistant: Okay. How many tickets do you need?\nCustomer: 2 please",
  "question": "In the customer's last message, does \"2\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qb0e7523ed1",
  "kind": "yes/no",
  "text": "Customer: Hi, I'd like to buy a ticket for The Upside.\nAssistant: Ok. Booking a ticket. What city and state?\nCustomer: Silver Spring, MD",
  "question": "In the customer's last message, does \"Silver Spring, MD\" give the location of the theater (city, neighbourhood or address) for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf3826932d6",
  "kind": "yes/no",
  "text": "Customer: Las Vegas.\nAssistant: What movie theatre do you prefer?\nCustomer: You can book them at the Regal Summerlin Luxury 5.",
  "question": "In the customer's last message, does \"Regal Summerlin Luxury 5\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q54c084bb72",
  "kind": "yes/no",
  "text": "Assistant: Give me a second to get all of this reserved.\nCustomer: Sure, thanks.\nAssistant: Unfortunately, Holdfast is completely booked for the entire weekend.",
  "question": "According to the assistant's last message, is \"Holdfast\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q924513467b",
  "kind": "yes/no",
  "text": "Assistant: No problem. Just a second.\nCustomer: Take your time.\nAssistant: Okay, they confirmed your order of four grande cappuccino with nonfat milk.",
  "question": "According to the assistant's last message, is \"nonfat milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbdbc6fee9e",
  "kind": "yes/no",
  "text": "Customer: I need to be at Bakersfield by 7:00.\nAssistant: From the pick-up location, Bakersfield is 14 minutes away by car. I can call the UberX at 6:30.\nCustomer: Make it 6:15 so that I have some time to spare.",
  "question": "In the customer's last message, does \"6:15\" give the pickup time for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd81fc0b78f",
  "kind": "yes/no",
  "text": "Customer: Okay. Also have them bring me home too.\nAssistant: Okay. What times will that be?\nCustomer: About 11 PM from the BJC.",
  "question": "In the customer's last message, does \"11 PM\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc01086fe09",
  "kind": "yes/no",
  "text": "Assistant: And finally, do you want your tickets sent to your mobile device, or do you want them sent to the will call window at the movie theater?\nCustomer: I want them sent to will call at the movie theater.\nAssistant: Okay. Your ticket purchase has been made for two tickets to 'Us' at Burlington AMC Movie Theater on Saturday at 11:15am. Your receipt will be sent to your mobile device. Your tickets will be waiting for you at the will call window.",
  "question": "According to the assistant's last message, is \"Saturday at 11:15am\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q76e40cd9a8",
  "kind": "yes/no",
  "text": "Customer: The one on GWU's campus. On H St. 2130 H St NW\nAssistant: Ok. What size should I order?\nCustomer: A grande size",
  "question": "In the customer's last message, does \"grande\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6af69125f4",
  "kind": "yes/no",
  "text": "Assistant: CRAVE features an outdoor patio, while Luna di Luna is indoor only.\nCustomer: The weather's pretty terrible anyways today. Can you book me a reservation at Luna di Luna for three people, preferably a booth, and after nine PM tonight?\nAssistant: I'm sorry, but the restaurant closes very close to nine PM. Would you like to eat earlier? I see an opening at seven PM.",
  "question": "According to the assistant's last message, is \"nine PM\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q70eb4388b8",
  "kind": "yes/no",
  "text": "Assistant: $15.99. Then the rest of the charge is from tax.\nCustomer: That is fine. Please book them right away.\nAssistant: Ok, your tickets are now officially booked for the Aquaman movie at AMC DINE-IN Block 37 in Chicago. You have 2 tickets for a total price of $34.32. Your show will start at 10:50. Don't forget your tickets are for B2 and B3.",
  "question": "According to the assistant's last message, is \"$34.32\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qbe2c9ed1d5",
  "kind": "yes/no",
  "text": "Customer: Assistant, What theaters are playing the movie US near me.\nAssistant: Malco Studio on the Square,Malco Paradiso Cinema Grill And IMAX,Malco Wolfchase Cinema Grill\nCustomer: Can I get tickets to US at Malco Wolfchase Cinema Grill in 3d",
  "question": "In the customer's last message, does \"Malco Wolfchase Cinema Grill\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q60617dacde",
  "kind": "yes/no",
  "text": "Customer: Have them pick me up at 15744 Goldenwest St, Huntington Beach, CA 92647\nAssistant: Okay, and where to do want them to take you?\nCustomer: I need them to drop me off at 2800, E Observatory Rd, Los Angeles, CA 90027",
  "question": "In the customer's last message, does \"2800, E Observatory Rd, Los Angeles, CA 90027\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd7dde17723",
  "kind": "yes/no",
  "text": "Assistant: What can I get for you today?\nCustomer: I would like a large royal feast Pizza.\nAssistant: Okay, I am sorry to inform you but they are currently out of bacon for the Royal Feast Pizza. Would it be okay if they left off the begin?",
  "question": "According to the assistant's last message, is \"bacon\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 }
]
