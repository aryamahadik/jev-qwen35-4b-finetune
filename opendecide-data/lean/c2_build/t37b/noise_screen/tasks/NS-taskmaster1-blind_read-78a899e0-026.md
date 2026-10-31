# Replay noise screen blind read NS-taskmaster1-blind_read-78a899e0-026 (family NS-taskmaster1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/noise_screen/answers/NS-taskmaster1-blind_read-78a899e0-026.json

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
  "qid": "q89430ab187",
  "kind": "yes/no",
  "text": "Assistant: Thanks, what is the make, model and year?\nCustomer: It is a 2018 Toyota Cressida.\nAssistant: To recap, your appointment is tomorrow at 10:00AM and your full name is Jim Hanks and contact number is 482.573.6109 for a 2018 Toyota Cressida.",
  "question": "According to the assistant's last message, is \"Toyota Cressida\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qaa07c0b983",
  "kind": "yes/no",
  "text": "Assistant: I'm sorry sir, but we have no booth seating available at that time.\nCustomer: I will take a table for 4 people, please.\nAssistant: You are all set sir. I have booked a table for four for Tuesday evening, March 4th at 6:00PM.",
  "question": "According to the assistant's last message, is \"table\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qb1fc4bdfe4",
  "kind": "yes/no",
  "text": "Customer: Okay lets switch restaurants.\nAssistant: Which restaurant would you like\nCustomer: Sky Sushi which is next door and use the same info I gave you for tomorrow at 7pm for 4 inside.",
  "question": "In the customer's last message, does \"Sky Sushi\" give the name the reservation should be under for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qc7cafae906",
  "kind": "yes/no",
  "text": "Assistant: Next boss\nCustomer: OK let me know\nAssistant: Chief inform me that special pizza is not available",
  "question": "According to the assistant's last message, is \"special pizza\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2dc85ddfc6",
  "kind": "yes/no",
  "text": "Customer: 2018\nAssistant: What name should I give for the appointment?\nCustomer: Me, Jeff Powers.",
  "question": "In the customer's last message, does \"Jeff Powers\" give the name of the repair shop for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qe870240e17",
  "kind": "yes/no",
  "text": "Assistant: What time would you like the reservation?\nCustomer: 8 pm as I said.\nAssistant: They have no openings at 8 but there is one at 9. Would you like that?",
  "question": "According to the assistant's last message, is \"8\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q5c25368e7c",
  "kind": "yes/no",
  "text": "Customer: I'll pick Giulia.\nAssistant: At what time and for how many?\nCustomer: I'd like to book 6 PM on January 9th with seats for two.",
  "question": "In the customer's last message, does \"6 PM\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q56fa53cd71",
  "kind": "yes/no",
  "text": "Customer: Hi I want to order a Lyft ride.\nAssistant: Hi, where from and to would like to go?\nCustomer: I need to go from the airport to Virginia street 509",
  "question": "In the customer's last message, does \"Virginia street 509\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8cfc3f9958",
  "kind": "yes/no",
  "text": "Customer: I'm looking for a fresh seafood restaurant\nAssistant: In what city are you looking for a restaurant?\nCustomer: Malibu, CA",
  "question": "In the customer's last message, does \"Malibu, CA\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qedf94081d2",
  "kind": "yes/no",
  "text": "Assistant: Im sorry indoor seating is unavailable at 12:00pm.\nCustomer: What about outdoor seating?\nAssistant: Im sorry, outdoor seating is not offered at Ross Grill.",
  "question": "According to the assistant's last message, is \"outdoor seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0abfb35e74",
  "kind": "yes/no",
  "text": "Customer: I need to order some pizza\nAssistant: what pizza restaurant?\nCustomer: Joeys Pizzaeria!",
  "question": "In the customer's last message, does \"Joeys Pizzaeria\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q85ab8ac700",
  "kind": "yes/no",
  "text": "Customer: I need tickets for US?",
  "question": "In the customer's last message, does \"US\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qfffc07a1b3",
  "kind": "yes/no",
  "text": "Assistant: 6:00 and 9:00\nCustomer: Ok, I'll get two tickets for Captain Marvel in 3D at 6:00 at Pioneer Place Stadium 6 in Portland OR\nAssistant: The 6:00 showing is not in 3D",
  "question": "According to the assistant's last message, is \"3D\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qa5843813b9",
  "kind": "yes/no",
  "text": "Assistant: Yes it is.\nCustomer: Okay.\nAssistant: Okay your UberX from Main St to the nearest CVS is booked and will be there any minute.",
  "question": "According to the assistant's last message, is \"the nearest CVS\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q91c2996c39",
  "kind": "yes/no",
  "text": "Customer: Okay what about April 8th, the following Monday?\nAssistant: I'm sorry that is not available either.\nCustomer: Okay what other steakhouse so you recommend in Manhattan?",
  "question": "In the customer's last message, does \"Manhattan\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q8cc0de5402",
  "kind": "yes/no",
  "text": "Customer: Do you know where the movie Hellboy is playing?\nAssistant: Yes, it’s playing at AMC Theatres in Alpharetta.\nCustomer: Would you please book two tickets for me?",
  "question": "In the customer's last message, does \"two tickets\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q3f00755c07",
  "kind": "yes/no",
  "text": "Customer: Okay, I'll the 8:45 showing at How much do the tickets cost at Regal Union Square Stadium.\nAssistant: How many tickets do you want?\nCustomer: I need two tickets.",
  "question": "In the customer's last message, does \"two\" give the movie showtime for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qcdc3bbeec1",
  "kind": "yes/no",
  "text": "Assistant: So that is a large pan pizza with pepperoni and extra cheese as the two toppings?\nCustomer: Correct!\nAssistant: Okay, it seems like they are out of extra cheese.",
  "question": "According to the assistant's last message, is \"extra cheese.\" confirmed for the customer's pizza order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q61dde163ba",
  "kind": "yes/no",
  "text": "Customer: No that's too late, are there any regular seats?\nAssistant: No it's all sold out at that time. There are seats available for US, didn't you say you wanted to see that as well?\nCustomer: No not today. What about at the Forum 8? What do they have at 7:30",
  "question": "In the customer's last message, does \"Forum 8\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q86e7d0a631",
  "kind": "yes/no",
  "text": "Assistant: Alright. I will give them a call back to make sure that is still available.\nCustomer: Right on. Thanks for your help.\nAssistant: No problem. The reservation is confirmed for 7:45 tonight.",
  "question": "According to the assistant's last message, is \"7:45\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3f48f43547",
  "kind": "yes/no",
  "text": "Assistant: yes, it does.\nCustomer: great\nAssistant: I want to confirm, your appointment is Saturday at 10 am for an oil change for you 2012 Hyundai Sonata. The cost will be $22.85",
  "question": "According to the assistant's last message, is \"Hyundai Sonata\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0dbf560811",
  "kind": "yes/no",
  "text": "Customer: I need to schedule an appointment at Intelligent Auto Solutions\nAssistant: Great, I can help you with that. What seems to be the problem?\nCustomer: My car needs an oil change.",
  "question": "In the customer's last message, does \"oil change\" give the problem or service the car is being brought in for for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q095ab551dd",
  "kind": "yes/no",
  "text": "Assistant: I'm placing your order now.\nCustomer: Thanks.\nAssistant: Your drink has been ordered from the Starbucks on Grand in Laramie and will be ready in approximately 10 minutes.",
  "question": "According to the assistant's last message, is \"Grand in Laramie\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q7d41bb4030",
  "kind": "yes/no",
  "text": "Customer: I'd like a large\nAssistant: You mean venti?\nCustomer: Yes, a venti please.",
  "question": "In the customer's last message, does \"venti\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q11d132a833",
  "kind": "yes/no",
  "text": "Assistant: Any changes to it like the milk or anything?\nCustomer: Almond milk instead of 2%. Oh and see if they can add extra caramel drizzle\nAssistant: I’m trying to order but they are out of almond milk. I know you sometimes get coconut and I asked, they are out of that too.",
  "question": "According to the assistant's last message, is \"almond milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf494f36347",
  "kind": "yes/no",
  "text": "Customer: We need a reservation for four.\nAssistant: I have a table for four available at 7:00, if you would just give me your name.\nCustomer: My last name is Foster. Thank you for the reservation",
  "question": "In the customer's last message, does \"Foster\" give the name of the restaurant for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q541725fec8",
  "kind": "yes/no",
  "text": "Assistant: Do you want to order anything else?\nCustomer: No, thank you, just the coffee.\nAssistant: Okay, your coffee has been ordered at the College Avenue and will be ready in 5 minutes. You will get a text receipt on your cell phone.",
  "question": "According to the assistant's last message, is \"College Avenue\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q2a81b56699",
  "kind": "yes/no",
  "text": "Customer: Hey, I'm hungry. Can we get some chow?\nAssistant: Yeah of course. What'd you have in mind?\nCustomer: I feel like pizza. Let's go for Pizza Hut",
  "question": "In the customer's last message, does \"Pizza Hut\" give the location of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qa7f2d59d6a",
  "kind": "yes/no",
  "text": "Assistant: Okay, what is the make, model and year of your car?\nCustomer: It is a Hyundai Elantra 2010.\nAssistant: Okay, I have booked you for 6 pm tonight for your Hyundai Elantra 2010..",
  "question": "According to the assistant's last message, is \"Hyundai Elantra\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qfa3c7fdac7",
  "kind": "yes/no",
  "text": "Customer: We'd like tickets for the 9:00 showing. The others are too late.\nAssistant: And how many tickets would you like?\nCustomer: Just two please.",
  "question": "In the customer's last message, does \"two\" give the number of tickets for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q387eea51e5",
  "kind": "yes/no",
  "text": "Customer: It makes a strange noise when I turn it on.\nAssistant: Okay, where do you want to take your vehicle to?\nCustomer: Intelligent Auto Solutions.",
  "question": "In the customer's last message, does \"Intelligent Auto Solutions\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q36ed931d7d",
  "kind": "yes/no",
  "text": "Customer: The one you can't pronounce right. OBVI. I can embrace my latina side\nAssistant: oh of course i don't know how I could have even guessed the first option. Um what size would you want your coffee?\nCustomer: Go venti or go home (assistants name)",
  "question": "In the customer's last message, does \"venti\" give the size of the drink for this coffee order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qac2f542f53",
  "kind": "yes/no",
  "text": "Assistant: Alright let me check.\nCustomer: Sounds good\nAssistant: They actually do not have outside seating currently.",
  "question": "According to the assistant's last message, is \"outside seating\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q143113c95b",
  "kind": "yes/no",
  "text": "Customer: Hi I would like to know how much a pizza is?\nAssistant: Hi I would be happy to help you. Which location would you be picking your food up at?\nCustomer: The one on Main street in Center City.",
  "question": "In the customer's last message, does \"Main street in Center City\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q69e7c4803e",
  "kind": "yes/no",
  "text": "Assistant: Not at this location\nCustomer: Alright go ahead and reserve the tickets.\nAssistant: Alright, I've reserved two Adult tickets for you for Spiderman: Into the Spierverse in Standard Cinema at the Lake Theater Classic Cinema for the 9:45 showing. Is that correct.",
  "question": "According to the assistant's last message, is \"9:45\" confirmed for the customer's movie ticket order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0e2bf55ac6",
  "kind": "yes/no",
  "text": "Assistant: Great. I'll book it right now.\nCustomer: Perfect.\nAssistant: It appears there are no Select cars currently available.",
  "question": "According to the assistant's last message, is \"Select\" confirmed for the customer's ride booking?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q3b486484d4",
  "kind": "yes/no",
  "text": "Customer: Hi, I want to see Captain Marvel with a friend.\nAssistant: Where do you want to see Captain Marvel?\nCustomer: In Prescott, Arizona.",
  "question": "In the customer's last message, does \"Prescott, Arizona\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qabafdbb6c7",
  "kind": "yes/no",
  "text": "Customer: I'm at the Capitol Lounge, at 229 Pennsylvania Ave SE, Washington DC.\nAssistant: Ok, and where is your home?\nCustomer: I live at 2000 N ST NW, near DuPont Circle.",
  "question": "In the customer's last message, does \"2000 N ST NW, near DuPont Circle\" give the destination (where the ride should drop the customer off) for this ride booking?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd93a5e0022",
  "kind": "yes/no",
  "text": "Assistant: No, that is all they need. Should I submit the appointment request?\nCustomer: Yes, go ahead and submit it. Just let me know if any sooner appointments come up. Otherwise the 6pm slot will work just fine.\nAssistant: Alright. You are all booked! It will be this evening at 6pm for your Subaru Impreza 2013 at the Intelligent Auto Solutions.",
  "question": "According to the assistant's last message, is \"Intelligent Auto Solutions\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q0f439a8d82",
  "kind": "yes/no",
  "text": "Customer: Hmm those are some good choices that I have heard of\nAssistant: Well Marvel is at 6::00 pm, Bumble be at 7 and Avengers at 10:00 pm\nCustomer: My favorite choice would be the Avengers, but I hav to go with something earlier",
  "question": "In the customer's last message, does \"Avengers\" give the name of the movie theater for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qaae94d0b54",
  "kind": "yes/no",
  "text": "Assistant: No problem. Let me check.\nCustomer: Take your time.\nAssistant: Allgauer's confirmed that they have a table with all your requested choices.",
  "question": "According to the assistant's last message, is \"Allgauer's\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qf53b718784",
  "kind": "yes/no",
  "text": "Assistant: I did not know you had an estate in Atherton.\nCustomer: I inherited it from my grandfather last year. I prefer the climate there, instead of my other estate in Lafayette.\nAssistant: Very good. Your appointment has been confirmed for 2 p.m. today at the shop, where they will inspect your 2018 Bentley Mulsanne for the \"check engine light\" issue.",
  "question": "According to the assistant's last message, is \"Bentley Mulsanne\" confirmed for the customer's car repair appointment?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "qc4905929f8",
  "kind": "yes/no",
  "text": "Customer: It is a 2017 model.\nAssistant: What style?\nCustomer: It is a hatchback",
  "question": "In the customer's last message, does \"hatchback\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q50bf378e24",
  "kind": "yes/no",
  "text": "Assistant: There's a table available at 6pm\nCustomer: Great, let's book it\nAssistant: I have reserved a table for you at Nodoguro at 6pm",
  "question": "According to the assistant's last message, is \"Nodoguro\" confirmed for the customer's restaurant reservation?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q43cfd1bfcd",
  "kind": "yes/no",
  "text": "Customer: I think it's like metal to metal. It's loud.\nAssistant: May I have your name and your contact number?\nCustomer: It's Jane Smith, my number is 615-555-1232",
  "question": "In the customer's last message, does \"Jane Smith\" give the customer's own name for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q6fd9bd2775",
  "kind": "yes/no",
  "text": "Customer: Hey Eric, I want to take my boyfriend out to dinner tonight. Can you please help with reservations?\nAssistant: Sure, what are you thinking?\nCustomer: He's been wanting to go to LB Steak. Can you please book at table for tonight at 7pm for two?",
  "question": "In the customer's last message, does \"two\" give the time of the reservation for this restaurant reservation?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qdc0cd431ff",
  "kind": "yes/no",
  "text": "Customer: sounds ood\nAssistant: which movie?\nCustomer: I'd like to see captain marvel",
  "question": "In the customer's last message, does \"captain marvel\" give the title of the movie for this movie ticket order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "q4b3c5df57f",
  "kind": "yes/no",
  "text": "Assistant: What kind of milk?\nCustomer: Soy.\nAssistant: Oh, I was hoping you wouldn't say that. They just ran out of soy milk this morning.",
  "question": "According to the assistant's last message, is \"soy milk\" confirmed for the customer's coffee order?",
  "definitions": "- yes: The assistant's last message confirms this value as booked, ordered, scheduled or available for the customer's transaction.\n- no: The assistant's last message says this value is unavailable, sold out, full, not offered or cannot be done, even if it offers an alternative or confirms other parts of the order."
 },
 {
  "qid": "q8ef1aad8c5",
  "kind": "yes/no",
  "text": "Customer: It's a Ford.\nAssistant: Ok. Next, can you tell me the model of your car?\nCustomer: It's a Fusion.",
  "question": "In the customer's last message, does \"Fusion\" give the make or model of the vehicle for this car repair appointment?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 },
 {
  "qid": "qd78239422e",
  "kind": "yes/no",
  "text": "Customer: I would like to order a pizza from Blue Line pizza for dinner with my family tonight.",
  "question": "In the customer's last message, does \"Blue Line pizza\" give the name of the pizza place for this pizza order?",
  "definitions": "- yes: The quoted phrase in the customer's last message refers to exactly the detail named in the question, even if the customer mentions it to rule it out or change it.\n- no: The quoted phrase states a different detail of the order (for example the destination rather than the pickup point, or the party size rather than the time), so it does not give the detail named."
 }
]
