# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-005 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-005.json

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
  "qid": "q698cebff7d",
  "kind": "yes/no",
  "text": "Customer: No thanks, I'll skip that today.\nAssistant: Ok, I've put in an order for a Cinnamon Dolce Latte, sugar free syrup, almond milk, and no whipped cream. What size?\nCustomer: A tall please.",
  "question": "In the customer's last message, does \"tall\" give the drink being ordered for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdccce0e0d9",
  "kind": "yes/no",
  "text": "Customer: Oh, yes, how about half green olives and half mushrooms as well?\nAssistant: Sounds good. Which pizza place were you thinking?\nCustomer: Pizza Hut on 7th Ave.",
  "question": "In the customer's last message, does \"7th Ave\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf654616cc6",
  "kind": "yes/no",
  "text": "Assistant: No problem, two tickets right?\nCustomer: Yes.\nAssistant: Okay, they confirmed two tickets are available for Dumbo 3D at 6:30 tonight.",
  "question": "According to the assistant's last message, is \"Dumbo\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qda6a3a70f3",
  "kind": "yes/no",
  "text": "Customer: do you have free coffe?\nAssistant: yes a complimentary coffe for our customers\nCustomer: my car model is toyota camry",
  "question": "In the customer's last message, does \"toyota camry\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qf862ec5124",
  "kind": "yes/no",
  "text": "Customer: Hello, I'm Terry Garcia and I'm calling to reserve two tickets to see the movie \"Shazam\" for tonight.",
  "question": "In the customer's last message, does \"Shazam\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc55a3b4787",
  "kind": "yes/no",
  "text": "Assistant: Would you like anything else?\nCustomer: Nope\nAssistant: Unfortunately, they are out of olives and onions.",
  "question": "According to the assistant's last message, is \"onions\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb2c6d410a9",
  "kind": "yes/no",
  "text": "Assistant: It's about thirty dollars for an entree each.\nCustomer: Hmm, not bad. I think my partner will be happy.\nAssistant: I'm sure they will be. Reservations for Pastabilities, tonight at 7 PM for two people in a private corner are confirmed!",
  "question": "According to the assistant's last message, is \"private corner\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q484173da01",
  "kind": "yes/no",
  "text": "Assistant: 9 pm or 6:45 pm.\nCustomer: Let's do 6:45 pm.\nAssistant: Great. You're confirmed at Buddhakan for tonight at 6:45 pm for 6 people.",
  "question": "According to the assistant's last message, is \"tonight at 6:45 pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q988fc8e596",
  "kind": "yes/no",
  "text": "Customer: I need to book an appointment for my truck.\nAssistant: Okay, and where would you like me to book this appointment?\nCustomer: At Intelligent Auto Solutions",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa78c55bddc",
  "kind": "yes/no",
  "text": "Assistant: OK, how about tomorrow at 8am?\nCustomer: Yes, perfect!\nAssistant: Ok you are all set for tomorrow at 8am to get your tire checked out",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q14914e732f",
  "kind": "yes/no",
  "text": "Assistant: It's $6.45\nCustomer: Okay, order that for me.\nAssistant: Okay, the order has been placed at the 12015 Harbor Blvd, Garden Grove, CA 92840 location. It will be ready for pickup shortly and your receipt will be sent to your cellphone via text message.",
  "question": "According to the assistant's last message, is \"12015 Harbor Blvd, Garden Grove, CA 92840\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfaff60c62b",
  "kind": "yes/no",
  "text": "Customer: I want to take the clients out to a good steakhouse\nAssistant: Well, Ruth’s Chris and. Orton’s Are good choices\nCustomer: Good, let’s make it Morton’s",
  "question": "In the customer's last message, does \"Morton’s\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6e688cb236",
  "kind": "yes/no",
  "text": "Assistant: Okay. I'll give a call and see if anything is available.\nCustomer: Sounds good.\nAssistant: They don't have a 6 o'clock. The earliest they have is 7.",
  "question": "According to the assistant's last message, is \"6 o'clock\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3f7c657451",
  "kind": "yes/no",
  "text": "Customer: Actually, I prefer the WAV ride\nAssistant: No problem, I will schedule that for you. How soon do you need to be picked up?\nCustomer: In about 45 minutes.",
  "question": "In the customer's last message, does \"45 minutes\" give the time the customer needs to arrive at the destination for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8d4cd6b6de",
  "kind": "yes/no",
  "text": "Customer: I need an appointment setup with Intelligent Auto Solutions\nAssistant: Okay what is the nature of your problem?\nCustomer: My car is shaking a lot",
  "question": "In the customer's last message, does \"My car is shaking a lot\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9c06ccc0b9",
  "kind": "yes/no",
  "text": "Customer: Yes, please.\nAssistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.",
  "question": "In the customer's last message, does \"Hyundai Elantra\" give the model year of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q553dfb405b",
  "kind": "yes/no",
  "text": "Customer: 235 555-1212\nAssistant: And what is the reason for the appointment?\nCustomer: The trunk keeps flying open.",
  "question": "In the customer's last message, does \"The trunk keeps flying open\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdfde63f66e",
  "kind": "yes/no",
  "text": "Customer: 2006\nAssistant: great! your 2006 ford explorer will be seen at intelligent auto solutions at 11:15am today. What name and phone number should I put down?\nCustomer: Annie smith and 555-555-5555.",
  "question": "In the customer's last message, does \"Annie smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q86966769cc",
  "kind": "yes/no",
  "text": "Assistant: Would you like to confirm your appointment?\nCustomer: Yes, please.\nAssistant: Appointment with Intelligent Auto Solutions set for today at 3pm, costing $75. Confirmed.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qea444c85ef",
  "kind": "yes/no",
  "text": "Assistant: What type of crust?\nCustomer: stuffed crust if that's possible\nAssistant: They do not have stuffed crust at this place, that's pizza hut",
  "question": "According to the assistant's last message, is \"stuffed crust\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7e47bbe958",
  "kind": "yes/no",
  "text": "Customer: Really? Anything later in the afternoon? I am flexible about the time.\nAssistant: Yes, they do have an outdoor table for 10 available at 3pm. Do you want that reservation?\nCustomer: Yes, 3pm is also a great time for an early afternoon dinner celebration.",
  "question": "In the customer's last message, does \"3pm\" give the number of people in the party for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q685a57c20a",
  "kind": "yes/no",
  "text": "Assistant: Alright, I went ahead and scheduled the appointment for you.\nCustomer: Can you go over the details?\nAssistant: Your car's breaks aren't working as they should. The appointment is at 10am tomorrow. There will be an initial inspection fee of 20 dollars.",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qcb1ed289ed",
  "kind": "yes/no",
  "text": "Customer: I did, thanks. Is it playing around 6 pm tonight?\nAssistant: Unfortunately, no. There's a screening at 5:30 and another at 7.\nCustomer: Darn. Ok, 7:30 pm it is then.",
  "question": "In the customer's last message, does \"7:30 pm\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q28113f507d",
  "kind": "yes/no",
  "text": "Assistant: Okay I will order now.\nCustomer: Thanks.\nAssistant: Pizza Hut informed me they are out of pepperoni. Is there something else I can replace it with?",
  "question": "According to the assistant's last message, is \"pepperoni\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q73bcd52710",
  "kind": "yes/no",
  "text": "Assistant: I think so, let me double-check....yes, that'll be fine.\nCustomer: All right, so I want a large supreme, with extra black olives and red peppers.\nAssistant: I'm sorry, red peppers are not an option. They have green. Will that be ok?",
  "question": "According to the assistant's last message, is \"red peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q084c0b3a96",
  "kind": "yes/no",
  "text": "Assistant: What would you like to order?\nCustomer: I'd like a medium caramel macchiato, with coconut milk.\nAssistant: I am sorry, coconut milk is not offered as a option for this location?",
  "question": "According to the assistant's last message, is \"coconut milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7a107cbc33",
  "kind": "yes/no",
  "text": "Assistant: Thanks, let me reserve that for you.\nCustomer: Ok.\nAssistant: Ok You are all set, see you at 8am at Intelligent Auto SOlutions I will text you the information. Thank you for calling.",
  "question": "According to the assistant's last message, is \"Intelligent Auto SOlutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q72b45d4b82",
  "kind": "yes/no",
  "text": "Assistant: I just checked and they don't have any tables available for that time.\nCustomer: Hm, how about 7:30.\nAssistant: Unfortunately, they are fully booked that night from 6 until 8:30. Shall I keep trying?",
  "question": "According to the assistant's last message, is \"6 until 8:30\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf17e5b941b",
  "kind": "yes/no",
  "text": "Customer: This evening at 7 pm.\nAssistant: How many?\nCustomer: Four people.",
  "question": "In the customer's last message, does \"Four\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4ec8537822",
  "kind": "yes/no",
  "text": "Customer: What's the cost?\nAssistant: 2 out of 4 dollar signs on Yelp.\nCustomer: Ok, do they have an opening for 2 between 6pm and 7pm?",
  "question": "In the customer's last message, does \"2\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qee6867cd85",
  "kind": "yes/no",
  "text": "Assistant: Which type of car you are looking\nCustomer: I need a uberXL\nAssistant: Sure , I have booked an UberXL for you from zoo to metro station today at 5PM",
  "question": "According to the assistant's last message, is \"metro station\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q9b525b7eb6",
  "kind": "yes/no",
  "text": "Customer: Yes\nAssistant: What is your car model\nCustomer: Mercedes E320",
  "question": "In the customer's last message, does \"Mercedes E320\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q9bbfbd6605",
  "kind": "yes/no",
  "text": "Customer: The 2017 Volkwagen Tiguan.\nAssistant: Okay, got it. What is the problem?\nCustomer: Something is up with the tires, one keeps losing air.",
  "question": "In the customer's last message, does \"Something is up with the tires, one keeps losing air.\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3178a95f64",
  "kind": "yes/no",
  "text": "Assistant: there is no 8PM show for Standard , your options are 6PM or 7PM please choose one\nCustomer: 7 PM\nAssistant: 7 PM show there are not enough seats available , do you want to check 6PM show",
  "question": "According to the assistant's last message, is \"7 PM\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q72cdb54a52",
  "kind": "yes/no",
  "text": "Assistant: Approximately 6 minutes.\nCustomer: Ok, go ahead and schedule it.\nAssistant: I have reserved your UberX for tonight at 6:30. You can check the status on your phone.",
  "question": "According to the assistant's last message, is \"UberX\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc5c0776b47",
  "kind": "yes/no",
  "text": "Customer: We will take that one.\nAssistant: What name do you want me to put this under?\nCustomer: You can put it under the name Alex.",
  "question": "In the customer's last message, does \"Alex\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q1d1bd5a8dd",
  "kind": "yes/no",
  "text": "Assistant: You got it. So that's one large BBQ chicken, and one large sausage and pepper, is that correct?\nCustomer: Yes that's correct\nAssistant: I'm so sorry, we are all out of peppers. Is there a different topping you prefer for the sausage pizza?",
  "question": "According to the assistant's last message, is \"peppers\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qe24e812717",
  "kind": "yes/no",
  "text": "Customer: Yes, that's the one.\nAssistant: What is the year, make and the model of your car?\nCustomer: It's 2013 Toyota Camry.",
  "question": "In the customer's last message, does \"Toyota Camry\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3bb6a37aee",
  "kind": "yes/no",
  "text": "Assistant: Let me check OpenTable for you, how many people will be attending?\nCustomer: Two people\nAssistant: I've checked OpenTable for Modern Love in Brooklyn, there are no openings available Friday at 6pm for two people, would you like to try another time?",
  "question": "According to the assistant's last message, is \"6pm\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q67c278e360",
  "kind": "yes/no",
  "text": "Assistant: There are no appointments available for today.\nCustomer: OK, tomorrow then.\nAssistant: There are no appointments open for tomorrow, the first available is Monday at 8am",
  "question": "According to the assistant's last message, is \"tomorrow\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf35620abf1",
  "kind": "yes/no",
  "text": "Customer: No, the service there has gotten really poor. I've been meaning to visit the new Alamo theater that just opened. Are there any tickets there for 8 p.m. tonight?\nAssistant: Let me see.... no but there is one at 7:30. Is that okay with you?\nCustomer: Sure, that works. How much are two tickets?",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qebbcd33f56",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza from Eno's in dallas.",
  "question": "In the customer's last message, does \"Eno's\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6852a0f32c",
  "kind": "yes/no",
  "text": "Customer: No, just the bacon and pineapple, please.\nAssistant: And what size did you want for this pizza?\nCustomer: Give me a large.",
  "question": "In the customer's last message, does \"large\" give the size of the pizza for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q721261eadc",
  "kind": "yes/no",
  "text": "Assistant: What is the name and number you would like me to put it under\nCustomer: Rico Suave 777-777-7777\nAssistant: Ok. Appointment booked for today at 4pm. Contact information is Rico Suave 777-777-7777. The diagnostics fee will be $100 to check out all the warning lights",
  "question": "According to the assistant's last message, is \"check out all the warning lights\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3e71041b86",
  "kind": "yes/no",
  "text": "Assistant: Okay. I will have it delivered to your house with the credit card you have on file.\nCustomer: Okay.\nAssistant: Hello. The Papa John's store says that they are out of onions. Would you like to choose a different topping?",
  "question": "According to the assistant's last message, is \"onions\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0d270b276b",
  "kind": "yes/no",
  "text": "Assistant: Are you planning on watching the movie in 3D, Imax, or Standard?\nCustomer: I want to buy tickets for a standard showing.\nAssistant: At the moment, no tickets are available for Shazam today, for a standard showing.",
  "question": "According to the assistant's last message, is \"Shazam\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf0810bd230",
  "kind": "yes/no",
  "text": "Customer: That’s too late. How about Saturday at 6:45?\nAssistant: I’m looking at Saturday. The only times are 8:00 and 9:30.\nCustomer: Those won’t work at all. Can we try for a table at Din Tai Fung in Century City?",
  "question": "In the customer's last message, does \"Century City\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q05b26c26ee",
  "kind": "yes/no",
  "text": "Customer: Hi! Can you place an order at Pizza Bella, please?",
  "question": "In the customer's last message, does \"Pizza Bella\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6f8484133d",
  "kind": "yes/no",
  "text": "Customer: Flint, Michigan\nAssistant: Okay, and what company would you like to book the appointment for?\nCustomer: Belle Tire",
  "question": "In the customer's last message, does \"Belle Tire\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q144702d8aa",
  "kind": "yes/no",
  "text": "Customer: Hi, I want to go see a movie tonight, can you help me with that?\nAssistant: Absolutely, what would you like to see?\nCustomer: I want to see Captain Marvel.",
  "question": "In the customer's last message, does \"Captain Marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
