# T06 redo2 authoring task T06-author_freeform-8ad80f22-000 (kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo2/answers/T06-author_freeform-8ad80f22-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 31 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: qa994f07aa7, q119a657f2c, q7f038cd5ee, q4526c740d5, qdccaaec2d3, qd061a057c4, qa72c922bab, q3fb510d174, q756e0b5714, qfb6b1b16e4, q0428556688, qda97659a24, qbff77b97b1, qbadd542a45, q9ca5b66ee1, q57201930a6, qfc14d21c5c, qcc15222b79, qfcc7a0106f, q25aaca3896, qa25c95ff5c, q5ec623323c, q01ea9223d5, q9986b4dfe7, q52816e79d9, q915a702ea2, q4c887e1aac, q3ac5f042dc, q6ad90c9b62, qc3fdc21c4b, q66d3a3d850.
- "text": one JSON string: the whole message (use \n for a line break).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one): [{"qid": "qa994f07aa7", "text": "<the message>"}, ...]

Task kind: author_freeform; items: 31; outputs expected: 31.

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

## Items (31; answer every item, keyed by its qid)

```json
[
 {
  "qid": "qa994f07aa7",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: apologetic.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Jonas Moreau",
   "ITEM": "kettle",
   "STORE": "Fernway Market"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q119a657f2c",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: formal.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Niamh Vasquez",
   "ITEM": "engraved cutting board",
   "STORE": "Bluecrest Sports"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q7f038cd5ee",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Jonas Achebe",
   "ITEM": "coffee grinder",
   "STORE": "Copperleaf Kitchen"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q4526c740d5",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Bastian Ortega",
   "ITEM": "razor cartridge pack",
   "STORE": "Cedarline Living"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qdccaaec2d3",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Zelda Ekwueme",
   "ITEM": "rain jacket",
   "STORE": "Copperleaf Kitchen"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qd061a057c4",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: apologetic.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Rhea Gallagher",
   "ITEM": "desk lamp",
   "STORE": "Orchard Lane Florists"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qa72c922bab",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Yusuf Gallagher",
   "ITEM": "swimsuit",
   "STORE": "Harborlight Goods"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q3fb510d174",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Aditi Bergstrom",
   "ITEM": "electric toothbrush",
   "STORE": "Fernway Market"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q756e0b5714",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Amara Sorensen",
   "ITEM": "meal kit",
   "STORE": "Orchard Lane Florists"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qfb6b1b16e4",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Vera Fujimoto",
   "ITEM": "swimsuit",
   "STORE": "Northvale Audio"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q0428556688",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: cheerful.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Wes Lindgren",
   "ITEM": "yoga mat",
   "STORE": "Copperleaf Kitchen"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qda97659a24",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Dmitri Castellano",
   "ITEM": "rain jacket",
   "STORE": "Bluecrest Sports"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qbff77b97b1",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: cheerful.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Umar Halvorsen",
   "ITEM": "cheese hamper",
   "STORE": "Tidewell Supply"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qbadd542a45",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Quentin Achebe",
   "ITEM": "hair clipper",
   "STORE": "Orchard Lane Florists"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q9ca5b66ee1",
  "brief": "Write a short formal letter in which the customer wants to send the item back. Tone: formal.",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Farid Fujimoto",
   "ITEM": "desk lamp",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a closing line and the CUSTOMER name on the last line.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q57201930a6",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: cheerful.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Hiro Iwu",
   "ITEM": "board game",
   "STORE": "Northvale Audio"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qfc14d21c5c",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Ximena Achebe",
   "ITEM": "monogrammed towel set",
   "STORE": "Tidewell Supply"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qcc15222b79",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Quentin Jaramillo",
   "ITEM": "face serum",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qfcc7a0106f",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: businesslike.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Celine Moreau",
   "ITEM": "kettle",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q25aaca3896",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: businesslike.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Zelda Moreau",
   "ITEM": "yoga mat",
   "STORE": "Pebblestone Beauty"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qa25c95ff5c",
  "brief": "Write a short formal letter in which the customer wants to send the item back. Tone: cheerful.",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Vera Rasmussen",
   "ITEM": "electric toothbrush",
   "STORE": "Lumenor Electronics"
  },
  "rules": [
   "A short formal letter on single lines (no blank line): 'Dear' + the STORE name, 1-2 sentences, a closing line and the CUSTOMER name on the last line.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q5ec623323c",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: apologetic.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aditi Kowalczyk",
   "ITEM": "swimsuit",
   "STORE": "Bluecrest Sports"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q01ea9223d5",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: cheerful.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dmitri Lindgren",
   "ITEM": "yoga mat",
   "STORE": "Pebblestone Beauty"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q9986b4dfe7",
  "brief": "Write a support ticket in which the customer wants to send the item back. Tone: apologetic.",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Amara Iwu",
   "ITEM": "birthday cake",
   "STORE": "Cedarline Living"
  },
  "rules": [
   "A support ticket: 2-3 short 'field: value' lines and 1-2 sentences.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q52816e79d9",
  "brief": "Write a short e-mail in which the customer wants to send the item back. Tone: polite and brief.",
  "register": "email",
  "facts": {
   "CUSTOMER": "Hiro Sorensen",
   "ITEM": "backpack",
   "STORE": "Harborlight Goods"
  },
  "rules": [
   "A short e-mail on single lines: a greeting line, 1-3 sentences and a sign-off line with the CUSTOMER name.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q915a702ea2",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: businesslike.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Ximena Iwu",
   "ITEM": "custom portrait canvas",
   "STORE": "Fernway Market"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q4c887e1aac",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: formal.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Greta Vasquez",
   "ITEM": "razor cartridge pack",
   "STORE": "Fernway Market"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q3ac5f042dc",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: slightly impatient.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Greta Lindgren",
   "ITEM": "wireless earbud set",
   "STORE": "Tidewell Supply"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q6ad90c9b62",
  "brief": "Write a chat message in which the customer wants to send the item back. Tone: formal.",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Elena Petrakis",
   "ITEM": "razor cartridge pack",
   "STORE": "Northvale Audio"
  },
  "rules": [
   "A chat message thread of 1-3 short lines 'speaker: message'; the customer speaks under the CUSTOMER name; any other speaker is 'support'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "qc3fdc21c4b",
  "brief": "Write a phone-call transcript in which the customer wants to send the item back. Tone: friendly and chatty.",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Soren Petrakis",
   "ITEM": "monogrammed towel set",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 },
 {
  "qid": "q66d3a3d850",
  "brief": "Write a service-desk note in which the customer wants to send the item back. Tone: short and to the point.",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Bastian Gallagher",
   "ITEM": "wireless earbud set",
   "STORE": "Brightwell Home"
  },
  "rules": [
   "A service-desk note of 2-3 sentences written by store staff about the customer's message.",
   "Copy CUSTOMER, ITEM and STORE whole, letter for letter (every word of each value); name the customer only by the whole CUSTOMER value; after the first mention, call the item 'it'."
  ]
 }
]
```
