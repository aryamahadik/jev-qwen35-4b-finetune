# T06 redo2 authoring task T06-author_freeform-8ad80f22-001 (kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo2/answers/T06-author_freeform-8ad80f22-001.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 30 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: qdbf35ce787, q614445d1a9, q6681f8a94b, q64403223a2, q0dbcfb50e0, qf152f01427, q4d33c0dbc8, q8d6234a037, qef2fb086e8, q4c74907910, q8c2ee6dd85, q7f2ca0c0e3, qc924bcacc9, qcf962cabb3, q339557dbbe, q167ed14bc9, q3726df85af, qe81fff59e6, qb6a86bbea0, qd7f8c3be21, q0ce95fd48d, qebc7bedf13, q6b935e903d, q80069dc0c5, qbb35769ad9, qd372821c38, q9a2fa9982c, q1bdfce0385, q0ecc2d7400, qbaa5ee28b0.
- "text": one JSON string: the whole message (use \n for a line break).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one): [{"qid": "qdbf35ce787", "text": "<the message>"}, ...]

Task kind: author_freeform; items: 30; outputs expected: 30.

## Instructions

You write short customer messages for a puzzle set about online shopping. Each item gives a register, a tone and three facts: CUSTOMER (the customer's full name), ITEM (what they bought) and STORE (the online store). Write ONE message per item, in which the customer says they want to send the item back to the store and that they bought it online (on the website, in the app or in the online shop). Nothing else about the case.

Fact rules (a program copies the three values out of your message letter by letter, and throws away any message in which a value is changed):
A. Write the CUSTOMER, ITEM and STORE values exactly as given, each at least once: every word of the value, in the same order, with the same spelling and the same capitals. Never shorten a value, never leave out a word of it, never make it plural and never put another word in its place: if ITEM is "electric toothbrush", write "the electric toothbrush", never "the toothbrush" or "the brush". Write "the" or "my" right before the item, never "a" or "an"; after its first mention, call the item "it". Never describe the item or say what kind of goods it is.
B. The customer's name appears only as the whole CUSTOMER value (first and last name together). Never write the first name alone or the last name alone, anywhere: also not in a greeting and also not in a reply from the support side (write "Hello" or "Hello there", never "Hello" followed by a first name). No other person's name, company name, brand or product name.
C. One block of text with no blank line (single line breaks are fine where the register uses them); at most about seventy words.
D. The word rules below apply to YOUR OWN words only. They never apply to the three values, which you always copy whole, whatever words they contain.
E. Thanks and greetings: use only "thank you", "thanks", "hello", "hi" or "dear". Never write "so much", "very much", "a bunch", "a lot", "good morning", "good afternoon" or "good evening".

Hard word rules (a program rejects any text that breaks one):
1. No digits, number words or ordinals (one, two, first, second, half, single, double, twice, pair, couple), no dates, times, months or weekdays, no currency or percent signs, no e-mail or web addresses, no domain names, no codes that mix letters and digits.
2. No time words: today, tonight, tomorrow, yesterday, now, soon, later, earlier, recently, currently, already, yet, next, last, past, ago, day, week, month, weekend, morning, evening, night, daily, immediately, quick, quickly, time, period, window, deadline.
3. Nothing about why the item goes back and nothing about its condition: no words such as wrong, damaged, cracked, scratched, torn, working, stopped, issue, problem, quality, mistake, changed, mind, fit, size, colour, unwanted, repair, replace, warranty, guarantee.
4. Nothing about delivery or the parcel: no words such as delivered, delivery, arrived, came, received, parcel, package, locker, neighbour, courier, shipping, collected, picked up, doorstep, dispatch.
5. Nothing about packaging or seals: no words such as seal, sealed, wrapper, wrapping, box, packaging, opened, unopened, tag, unused.
6. Nothing about money, rights or rules: no words about money coming back, paying, cash, vouchers, credit notes, exchanges, compensation, what anyone is due or deserves, rights, rules, policies, terms, laws, notices or signs, promises or claims. Never say whether the return will work out, and never speak about lateness or timeliness.
7. No quantity or quantifier words: all, every, each, some, any, none, both, either, neither, only, always, never, often, usually, several, few, many, much, more, most, less, least, another, extra, whole, entire, total.
8. No modal words: must, may, might, can, could, should, shall, will, would, need, able, have to, has to, allowed, permitted, required, optional (write "I want to send it back", "please help me with the return", "I am writing to return ..."). Avoid contractions such as I'd and I'll.
9. No hedges: maybe, perhaps, probably, likely, seems, appears, think, believe, guess, assume, suspect, almost, roughly.
10. No status or outcome words: approved, accepted, confirmed, pending, completed, done, processed, open, opened, closed, active, valid, settled, ok, okay, cancel, cancelled.
11. No logic words: if, unless, except, otherwise, instead, regardless, provided, excluding.
12. No negation of any kind: not, n't (don't, can't, isn't ...), no, never, nothing, nobody, nowhere, without, cannot, lack, fail, hardly.
13. No capital letter except at the start of a sentence, of a line, or right after a colon, and in the placeholders or names you are given (write "the help desk", never "the Help Desk"; no acronyms; "I" is fine).

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the message>"}. Use \n for line breaks inside the text. Every message must differ from every other message you write.

## Items (30; answer every item, keyed by its qid)

```json
[
 {
  "qid": "qdbf35ce787",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Paloma Ortega",
   "ITEM": "table fan",
   "STORE": "Pebblestone Beauty"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q614445d1a9",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Farid Castellano",
   "ITEM": "coffee grinder",
   "STORE": "Northvale Audio"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q6681f8a94b",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Marisol Bergstrom",
   "ITEM": "bluetooth speaker",
   "STORE": "Pebblestone Beauty"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q64403223a2",
  "brief": "Write a short formal letter in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Celine Dufresne",
   "ITEM": "desk lamp",
   "STORE": "Orchard Lane Florists"
  },
  "rules": [
   "A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a closing line and the CUSTOMER name on the last line.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q0dbcfb50e0",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: businesslike.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Rhea Takahashi",
   "ITEM": "wall clock",
   "STORE": "Cedarline Living"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qf152f01427",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Oskar Fujimoto",
   "ITEM": "face serum",
   "STORE": "Cedarline Living"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q4d33c0dbc8",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Umar Vasquez",
   "ITEM": "meal kit",
   "STORE": "Northvale Audio"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q8d6234a037",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: cheerful.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Darius Jaramillo",
   "ITEM": "name-printed mug",
   "STORE": "Orchard Lane Florists"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qef2fb086e8",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: apologetic.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Elena Halvorsen",
   "ITEM": "wireless earbud set",
   "STORE": "Cedarline Living"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q4c74907910",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: cheerful.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Marisol Nakashima",
   "ITEM": "table fan",
   "STORE": "Bluecrest Sports"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q8c2ee6dd85",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: formal.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Paloma Dufresne",
   "ITEM": "bluetooth speaker",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q7f2ca0c0e3",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Wes Castellano",
   "ITEM": "rain jacket",
   "STORE": "Lumenor Electronics"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qc924bcacc9",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Chiara Nakashima",
   "ITEM": "tailored blazer",
   "STORE": "Kestrel Outfitters"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qcf962cabb3",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Kalinda Takahashi",
   "ITEM": "fresh flower bouquet",
   "STORE": "Fernway Market"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q339557dbbe",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: businesslike.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Isla Ortega",
   "ITEM": "engraved cutting board",
   "STORE": "Copperleaf Kitchen"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q167ed14bc9",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Oskar Rasmussen",
   "ITEM": "hair clipper",
   "STORE": "Kestrel Outfitters"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q3726df85af",
  "brief": "Write a short formal letter in which the customer wants to send the item back. Tone: businesslike.",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Yusuf Sorensen",
   "ITEM": "electric toothbrush",
   "STORE": "Copperleaf Kitchen"
  },
  "rules": [
   "A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a closing line and the CUSTOMER name on the last line.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qe81fff59e6",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Soren Ekwueme",
   "ITEM": "custom portrait canvas",
   "STORE": "Lumenor Electronics"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qb6a86bbea0",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: formal.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Talia Bergstrom",
   "ITEM": "bluetooth speaker",
   "STORE": "Tidewell Supply"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qd7f8c3be21",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Bram Halvorsen",
   "ITEM": "phone case",
   "STORE": "Kestrel Outfitters"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q0ce95fd48d",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: apologetic.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Talia Kowalczyk",
   "ITEM": "board game",
   "STORE": "Lumenor Electronics"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qebc7bedf13",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Leon Ekwueme",
   "ITEM": "face serum",
   "STORE": "Kestrel Outfitters"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q6b935e903d",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Leon Petrakis",
   "ITEM": "hair clipper",
   "STORE": "Harborlight Goods"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q80069dc0c5",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: businesslike.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Bram Rasmussen",
   "ITEM": "table fan",
   "STORE": "Bluecrest Sports"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qbb35769ad9",
  "brief": "Write a short formal letter in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Niamh Kowalczyk",
   "ITEM": "engraved watch",
   "STORE": "Kestrel Outfitters"
  },
  "rules": [
   "A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a closing line and the CUSTOMER name on the last line.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qd372821c38",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Darius Takahashi",
   "ITEM": "tailored blazer",
   "STORE": "Tidewell Supply"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q9a2fa9982c",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: formal.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Isla Dufresne",
   "ITEM": "engraved watch",
   "STORE": "Harborlight Goods"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q1bdfce0385",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: businesslike.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Kalinda Jaramillo",
   "ITEM": "cheese hamper",
   "STORE": "Harborlight Goods"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q0ecc2d7400",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: cheerful.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Farid Nakashima",
   "ITEM": "kettle",
   "STORE": "Lumenor Electronics"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qbaa5ee28b0",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: formal.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Chiara Fujimoto",
   "ITEM": "name-printed mug",
   "STORE": "Pebblestone Beauty"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 }
]
```
