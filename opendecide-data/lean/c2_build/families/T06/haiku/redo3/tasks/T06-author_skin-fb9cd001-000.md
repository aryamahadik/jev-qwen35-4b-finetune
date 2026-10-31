# T06 redo3 authoring task T06-author_skin-fb9cd001-000 (kind author_skin)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo3/answers/T06-author_skin-fb9cd001-000.json

(The folder of that path is created by your write if it does not exist yet.)

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 15 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q71e93a01fe, qab961a53fa, q92a123be4f, q0ccad2dbf6, q4263eee34e, q16e9ca901e, q378a5acd70, qf3ef903ce2, q9f0156a3ab, qbbc6caca94, q1d786f570f, qee5be25f44, q4e5d2efe0a, q88db066536, qb9cba5553c.
- "text": one JSON string: the whole message or line (use \n for a line break).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one): [{"qid": "q71e93a01fe", "text": "<the text>"}, ...]

Task kind: author_skin; items: 15; outputs expected: 15.

## Instructions

You write short customer messages for a puzzle set about online shopping. A program fills in the facts later; you never see the puzzle, its question or its outcome. Each item gives a register (the kind of text), a tone and a hint. Write ONE message per item.

Every message uses exactly three placeholders, each exactly once, written exactly like this: {CUSTOMER} (the customer's full name), {STORE} (the online store's name) and the item they bought: write {a|ITEM} where the item needs "a" or "an" in front of it (the program picks the right one), or {ITEM} where no article goes in front of it (after "the" or "my", or as a field value). Never write "a" or "an" yourself right before a placeholder. Write no other placeholder and no other name.

The message only says that the customer wants to send the item back to the store, and that they bought it online (on the website, in the app or in the online shop). It says nothing else about the case.

Layout: one block of text with no blank line (single line breaks are fine where the register uses them); at most about sixty words. Never start with "Order record" or "Message added to the case", and never list order facts.

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

## Already taken (never repeat, and never copy closely, anything listed here)

Each entry is one JSON string (a line break inside a text is written \n).

### Messages already taken, register chat (35)
- "{CUSTOMER}: Hi, I bought my {ITEM} online at {STORE}. How do I send it back, please?"
- "{CUSTOMER}: Hello. I purchased {a|ITEM} through the online shop and I wish to return it.\nsupport: Welcome to {STORE} support. Please state your request."
- "{CUSTOMER}: Hi, where do I send {a|ITEM} back? I bought it online from {STORE}."
- "{CUSTOMER}: Please start the return, I bought {a|ITEM} online from {STORE} and I want to send it back.\nsupport: Thank you, I am on it."
- "support: Hello, this is {STORE} support. What is your question?\n{CUSTOMER}: Sorry to bother you, I bought {a|ITEM} online and I want to send it back. Please send me a return label."
- "{CUSTOMER}: Hi there, thanks a lot! I bought {a|ITEM} online from {STORE}, so please help me with the return, yay!"
- "{CUSTOMER}: Hello. I bought {a|ITEM} online from {STORE} and I want to send it back. How do I do that?"
- "{CUSTOMER}: Hello, I bought {a|ITEM} in the {STORE} app and want to send it back. Thanks!"
- "{CUSTOMER}: Hey there! I bought {a|ITEM} online from {STORE} and want to send it back, you are the best!"
- "{CUSTOMER}: Hello. I bought my {ITEM} online from {STORE} and wish to send it back. Kindly advise where to send it."
- "{CUSTOMER}: Please start the return for {a|ITEM} bought online from {STORE}."
- "{CUSTOMER}: Just send me a return label, I bought my {ITEM} online and want to send it back.\nsupport: Hello from {STORE}. Let me check that for you."
- "{CUSTOMER}: Hello {STORE}, sorry to bother you, and thank you for your kindness. Please help me with the return of {a|ITEM} I bought online."
- "{CUSTOMER}: Hiya! I bought {a|ITEM} online and I want to send it back. How do I do that?\nsupport: Hi there, {STORE} here, happy to help."
- "{CUSTOMER}: Hello {STORE}. I bought {a|ITEM} online and I want to send it back.\nsupport: Hello, thanks for your message."
- "{CUSTOMER}: Hello, thank you. I bought {a|ITEM} online from {STORE} and want to return it."
- "{CUSTOMER}: Hello, I bought {a|ITEM} online with {STORE} and I respectfully ask you to start the return."
- "{CUSTOMER}: I bought {a|ITEM} online at {STORE}. I want to send it back. Please send me a return label."
- "{CUSTOMER}: Thanks, {STORE}. I bought {a|ITEM} online and want to send it back, so please help me with the return.\nsupport: Hello, thanks for your message."
- "{CUSTOMER}: Sorry to ask, I bought {a|ITEM} online from {STORE} and I want to send it back. How do I do that?"
- "{CUSTOMER}: Hi {STORE}! I bought {a|ITEM} on your website and I want to send it back. Thanks a lot!"
- "{CUSTOMER}: Hello. I purchased {a|ITEM} online from {STORE} and want to return it."
- "{CUSTOMER}: Hello, I bought {a|ITEM} online from {STORE} and I want to send it back. Where do I send it? Thank you."
- "{CUSTOMER}: Hi there. I bought {a|ITEM} online from {STORE} and I am writing to ask for a return label.\nsupport: Thank you for writing in, I am glad to help."
- "{CUSTOMER}: Thank you, {STORE}! Please help with the return of {a|ITEM} I bought online, as I want to send it back."
- "{CUSTOMER}: Honestly, just tell me how to send {a|ITEM} back. I bought it online from {STORE}."
- "{CUSTOMER}: Sorry to bother you, I want to send back {a|ITEM} that I bought online.\nsupport: Hi there, {STORE} support here."
- "{CUSTOMER}: Hi there! I bought {a|ITEM} online and want to send it back to {STORE}. Thanks!"
- "{CUSTOMER}: I bought {a|ITEM} online and I want to send it back. Where do I send it?\nsupport: Hello, this is {STORE} support. Thank you for getting in touch."
- "{CUSTOMER}: Hello, I bought {a|ITEM} online from {STORE} and I want to send it back. Please start the return for me, thanks."
- "{CUSTOMER}: Hiya! I bought {a|ITEM} online from {STORE}, so please send me a return label, cheers!"
- "{CUSTOMER}: Thank you for your help. I bought {a|ITEM} online from {STORE} and I want to send it back, so please help me with the return.\nsupport: You are welcome, I am glad to assist."
- "{CUSTOMER}: Bought {a|ITEM} online. How do I send it back?\nsupport: Hi, {STORE} here."
- "{CUSTOMER}: Hi, I want to send {a|ITEM} back. I bought it online, so please just sort it out.\nsupport: Thanks for writing, this is {STORE}."
- "{CUSTOMER}: Hi {STORE} team, sorry to bother you. I bought {a|ITEM} online and want to return it.\nsupport: Hello, thanks for getting in touch."

### Messages already taken, register email (37)
- "Hello {STORE} team,\nI bought {a|ITEM} online and I want to send it back. Please send me a return label.\nThanks,\n{CUSTOMER}"
- "Hello {STORE} team,\nThank you. I bought {a|ITEM} online and I want to send it back, so please just help me.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nSorry to bother you. I bought {a|ITEM} online and want to send it back. How do I do that?\nBest wishes,\n{CUSTOMER}"
- "Hello {STORE} team,\nHope you are well! I bought {a|ITEM} online and want to send it back.\nThanks!\n{CUSTOMER}"
- "Hello {STORE} team,\nI am writing to send back {a|ITEM} that I purchased on your website.\nKind regards,\n{CUSTOMER}"
- "Hi {STORE} team,\nI bought {a|ITEM} online and I want to know where to send it back. Thanks.\nCheers,\n{CUSTOMER}"
- "Hello {STORE} team,\nI hope you are doing well. I bought {a|ITEM} on your app and I want to send it back, so please help me start the return. Thanks a lot for being so helpful!\nBest,\n{CUSTOMER}"
- "Hello {STORE} team,\nI am writing to ask for a return label. I want to send {a|ITEM} back, and I bought it online.\nKind regards,\n{CUSTOMER}"
- "Hi {STORE} team,\nThank you. I bought {a|ITEM} online and I want to send it back, so please help me with the return.\nThanks,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} on your website and I want to send it back. Please just reply with the steps for doing that.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nI am sorry to bother you, but I bought {a|ITEM} online and I want to send it back.\nThanks,\n{CUSTOMER}"
- "Hiya {STORE} team,\nGreat to be in touch! I bought {a|ITEM} online and I want to return it.\nCheers,\n{CUSTOMER}"
- "Hello {STORE} team,\nPlease tell me where to send the {ITEM} back. I bought it online on the website.\nBest regards,\n{CUSTOMER}"
- "Dear {STORE} team,\nI bought {a|ITEM} online and want to send it back. Please start the return for me. Thank you.\nBest regards,\n{CUSTOMER}"
- "Hello {STORE} team,\nHope you are doing well! I bought {a|ITEM} online and want to send it back, so please send me a return label. Thanks a lot!\nCheers,\n{CUSTOMER}"
- "Dear {STORE} team,\nThank you in advance for your help. I bought {a|ITEM} online and I am writing for help with sending it back.\nKind regards,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} online. How do I send it back?\nThanks,\n{CUSTOMER}"
- "Hi {STORE} team,\nI bought {a|ITEM} online and I want to send it back. Please just get on with it.\nThanks,\n{CUSTOMER}"
- "Dear {STORE} team,\nSorry to bother you. I bought {a|ITEM} online and I am writing to return it.\nThanks,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} online and want to send it back. Where do I send it? Thanks a lot!\nCheers,\n{CUSTOMER}"
- "Hello {STORE} team,\nPlease start the return of the {ITEM} I bought online from your website. Please let me know what to do.\nBest,\n{CUSTOMER}"
- "Hi {STORE} team,\nI bought {a|ITEM} online and want to send it back, so please send me a return label. Thank you!\nBest,\n{CUSTOMER}"
- "Hi {STORE} team,\nThanks a lot for your help! I bought {a|ITEM} online and want to send it back. Please help me with the return.\nThanks again,\n{CUSTOMER}"
- "Dear {STORE} team,\nI bought my {ITEM} online and wish to find out how to send it back.\nYours sincerely,\n{CUSTOMER}"
- "Dear {STORE} team,\nI bought my {ITEM} online and want to send it back.\nThanks,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} online and I want to send it back. Please get back to me about this.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nSorry to bother you, but where do I send {a|ITEM} back? I bought it online.\nThanks,\n{CUSTOMER}"
- "Hi {STORE} team,\nI bought {a|ITEM} from your website and I want to send it back. Please start the return for me, happy shopping!\nCheers,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} online and I want to send it back. Please send me a return label for it.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nThank you for your help. I bought {a|ITEM} online and want to send it back, so please assist me with the return.\nYours sincerely,\n{CUSTOMER}"
- "Dear {STORE} team,\nI am writing to return the {ITEM} that I bought online through your website. I wish to send it back to you.\nKind regards,\n{CUSTOMER}"
- "Hello {STORE} team,\nI bought {a|ITEM} online and I want to send it back.\nThanks,\n{CUSTOMER}"
- "Dear {STORE} team,\nI bought {a|ITEM} online and I want to send it back. Please just tell me where to send it.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nSorry for the bother, but please start the return of my {ITEM}. I bought it online and want to send it back.\nThanks,\n{CUSTOMER}"
- "Hi {STORE} team,\nHope you are doing great! I bought {a|ITEM} online and want to send it back.\nPlease send me a return label, thanks!\nCheers,\n{CUSTOMER}"
- "Hi {STORE} team,\nThank you for your support. I am writing to ask for help with the return of {a|ITEM} I bought online.\nRegards,\n{CUSTOMER}"
- "Hello {STORE} team,\nPlease tell me how to send back {a|ITEM} I bought on your website.\nThank you,\n{CUSTOMER}"

### Messages already taken, register yaml (37)
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: I wish to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nrequest: where do I send it back?"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: just start the return, please"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online website\nrequest: sorry to ask, I want to send it back, please send a return label"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nnote: bought online, thanks a lot for helping with the return!"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: how to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: please let me send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nnote: bought it in the app and want to return it, yay"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: I wish to send it back, please advise where to send it"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: please start the return"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nrequest: a return label, come on, please"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nnote: sorry to bother you, thank you for helping with the return"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nrequest: how to send it back, thanks"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: I want to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: return, please, thank you"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nrequest: hey, where do I send it back? Thanks!"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nrequest: send me a return label"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: thanks, please just help me send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nnote: sorry to ask, bought it online, how do I send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nnote: so happy to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\ntopic: return\nrequest: purchased on the website, wants to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: please tell me where to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: please start the return, thanks!"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nrequest: a return label"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: thanks, please help me with sending it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nrequest: just tell me how to send it back."
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nnote: sorry, I wish to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nnote: yay, I want to send it back!"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: where to send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: I want to send it back, please start the return."
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: app\nrequest: hi, I want to send it back and please send me a return label"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nnote: thank you for your help with the return"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: how do I send it back"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online shop\nrequest: I want to send it back, come on"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nrequest: sorry, I want to return it"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: website\nnote: bought online, happy to send it back, where do I send it?"
- "customer: {CUSTOMER}\nshop: {STORE}\nitem: {ITEM}\nchannel: online\nrequest: start the return for this purchase"

### Messages already taken, register transcript (22)
- "Agent: Hello, {STORE} customer desk here. What brings you here?\nCaller: Hello, my name is {CUSTOMER}. I bought it online.\nAgent: Certainly, let me help.\nCaller: Kindly send a return label, and I want to send my {ITEM} back."
- "Agent: Hello, you have reached {STORE}. Who am I speaking with?\nCaller: Hi, it is {CUSTOMER}! Thanks for taking my call.\nAgent: Happy to help. What is up?\nCaller: I bought {a|ITEM} online and I am hoping for help sending it back."
- "Agent: Hello, you have reached {STORE}.\nCaller: My name is {CUSTOMER}. I bought {a|ITEM} online and wish to send it back. How do I do that?"
- "Agent: Thanks for calling {STORE}, what is your request?\nCaller: I am {CUSTOMER}. I want to send {a|ITEM} back. I bought it online.\nAgent: Thank you for letting us know."
- "Agent: Thank you for calling {STORE}. Who am I speaking with?\nCaller: This is {CUSTOMER}. I bought {a|ITEM} online and I want to return it.\nAgent: Thank you. Please go on.\nCaller: I just want to send it back, please."
- "Agent: Hi there, this is the {STORE} help desk, lovely to hear from you.\nCaller: Hi, this is {CUSTOMER}. I bought {a|ITEM} online and I want to send it back, so please start the return for me, thanks!"
- "Agent: Hello, {STORE} here.\nCaller: My name is {CUSTOMER}. I bought {a|ITEM} online and I want a return label, please."
- "Agent: Hello, you have reached {STORE}. Go ahead.\nCaller: Thank you, this is {CUSTOMER}. I bought {a|ITEM} online, please help me with the return."
- "Agent: Hello, this is {STORE}, thanks for getting in touch.\nCaller: Hiya, it is {CUSTOMER}. I bought {a|ITEM} online and I want to send it back. How do I do that?\nAgent: Lovely, let me help you with that."
- "Agent: Hello, {STORE} speaking. Who am I speaking with?\nCaller: This is {CUSTOMER}. I bought {a|ITEM} online and I want to send it back.\nAgent: Thank you, I am happy to help you with that."
- "Agent: Thanks for calling {STORE}. What is your name?\nCaller: My name is {CUSTOMER}. I bought {a|ITEM} online and want to return it."
- "Agent: Thank you for calling {STORE}. Go ahead, please.\nCaller: Sorry to bother you, this is {CUSTOMER}. I bought {a|ITEM} online and I want you to start the return.\nAgent: Of course, I am happy to help."
- "Agent: Hello, thanks for calling {STORE}. Go ahead, please.\nCaller: Hi, this is {CUSTOMER}. I bought {a|ITEM} online and want to send it back. Please send me a return label, thanks a lot!"
- "Agent: Hello, you have reached the {STORE} help desk. What do you want to ask about?\nCaller: Hi, this is {CUSTOMER}. I bought {a|ITEM} online and I want to send it back. Thanks for your help with the return."
- "Agent: Hello, {STORE} support speaking. Who is calling?\nCaller: Hi, it is {CUSTOMER}. Sorry to call.\nAgent: Of course, go ahead.\nCaller: I bought my {ITEM} online and want to send it back. How do I do that, please?"
- "Agent: Hi, {STORE} here. Who do I have on the line?\nCaller: Hiya, lovely to chat! My name is {CUSTOMER}, and I bought {a|ITEM} online and want to send it back.\nAgent: Great, go on, please."
- "Agent: {STORE} speaking. What is your enquiry?\nCaller: This is {CUSTOMER}. I bought {a|ITEM} online and I wish to return it.\nAgent: Certainly, let us proceed."
- "Agent: Thanks for calling {STORE}. What is the call about?\nCaller: Hi, this is {CUSTOMER}. I bought {a|ITEM} online and want to send it back. Where do I send it?\nAgent: Happy to help with that."
- "Agent: Thank you for contacting {STORE}.\nCaller: Hi, this is {CUSTOMER}. I bought {a|ITEM} online and I want you to just start the return, please."
- "Agent: Thank you for calling {STORE}. Who am I speaking with?\nCaller: Hello, this is {CUSTOMER}. Sorry to bother you, I bought it online.\nAgent: Of course. Tell me what you want.\nCaller: Please send me a return label, I want to send my {ITEM} back."
- "Agent: You are through to {STORE}, lovely to hear from you.\nCaller: Hiya, I am {CUSTOMER}. Thanks a lot! I bought {a|ITEM} online and want to send it back, so please help me with the return.\nAgent: Brilliant, glad to help."
- "Agent: This is {STORE}, thank you for calling.\nCaller: My name is {CUSTOMER}. I bought {a|ITEM} online and want to send it back. How do I go about that?"

## Items (15; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q71e93a01fe",
  "brief": "Write a YAML contact record. Tone: polite and brief. Hint: the customer asks for a return label.",
  "register": "yaml",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "3-5 lines of block-style 'key: value' YAML with lower-case keys and plain values, for example 'customer: {CUSTOMER}'. Write the placeholders bare as values and use {ITEM}, never {a|ITEM}.",
   "Context keys only (customer, shop, item, channel, topic, request, note); never a key about dates, a reason, the condition, delivery, packaging, a policy or a status.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file."
  ]
 },
 {
  "qid": "qab961a53fa",
  "brief": "Write a short e-mail. Tone: formal. Hint: the customer says they bought it online and want to return it.",
  "register": "email",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A short e-mail on single lines (no blank line): a greeting line to the {STORE} team, 1-3 sentences, a sign-off word line and {CUSTOMER} on the last line.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q92a123be4f",
  "brief": "Write a phone-call transcript. Tone: formal. Hint: the customer asks where to send the item.",
  "register": "transcript",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'; the caller gives the name {CUSTOMER} once; the agent speaks for {STORE}.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q0ccad2dbf6",
  "brief": "Write a chat message. Tone: formal. Hint: the customer asks how to send the item back.",
  "register": "chat",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case).",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q4263eee34e",
  "brief": "Write a short e-mail. Tone: short and to the point. Hint: the customer asks where to send the item.",
  "register": "email",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A short e-mail on single lines (no blank line): a greeting line to the {STORE} team, 1-3 sentences, a sign-off word line and {CUSTOMER} on the last line.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q16e9ca901e",
  "brief": "Write a chat message. Tone: cheerful. Hint: the customer asks where to send the item.",
  "register": "chat",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case).",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q378a5acd70",
  "brief": "Write a phone-call transcript. Tone: friendly and chatty. Hint: the customer says they bought it online and want to return it.",
  "register": "transcript",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'; the caller gives the name {CUSTOMER} once; the agent speaks for {STORE}.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "qf3ef903ce2",
  "brief": "Write a chat message. Tone: polite and brief. Hint: the customer asks for a return label.",
  "register": "chat",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case).",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q9f0156a3ab",
  "brief": "Write a chat message. Tone: friendly and chatty. Hint: the customer thanks the store and asks for help with the return.",
  "register": "chat",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case).",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "qbbc6caca94",
  "brief": "Write a phone-call transcript. Tone: short and to the point. Hint: the customer asks the store to start the return.",
  "register": "transcript",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'; the caller gives the name {CUSTOMER} once; the agent speaks for {STORE}.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q1d786f570f",
  "brief": "Write a chat message. Tone: businesslike. Hint: the customer asks the store to start the return.",
  "register": "chat",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A chat message from the customer, or a chat excerpt of 2-3 lines 'speaker: message' where the customer line starts with '{CUSTOMER}:' and any other speaker is written 'support:' (lower case).",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "qee5be25f44",
  "brief": "Write a short e-mail. Tone: friendly and chatty. Hint: the customer simply states the wish to send the item back.",
  "register": "email",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A short e-mail on single lines (no blank line): a greeting line to the {STORE} team, 1-3 sentences, a sign-off word line and {CUSTOMER} on the last line.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 },
 {
  "qid": "q4e5d2efe0a",
  "brief": "Write a YAML contact record. Tone: formal. Hint: the customer asks how to send the item back.",
  "register": "yaml",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "3-5 lines of block-style 'key: value' YAML with lower-case keys and plain values, for example 'customer: {CUSTOMER}'. Write the placeholders bare as values and use {ITEM}, never {a|ITEM}.",
   "Context keys only (customer, shop, item, channel, topic, request, note); never a key about dates, a reason, the condition, delivery, packaging, a policy or a status.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file."
  ]
 },
 {
  "qid": "q88db066536",
  "brief": "Write a YAML contact record. Tone: friendly and chatty. Hint: the customer thanks the store and asks for help with the return.",
  "register": "yaml",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "3-5 lines of block-style 'key: value' YAML with lower-case keys and plain values, for example 'customer: {CUSTOMER}'. Write the placeholders bare as values and use {ITEM}, never {a|ITEM}.",
   "Context keys only (customer, shop, item, channel, topic, request, note); never a key about dates, a reason, the condition, delivery, packaging, a policy or a status.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file."
  ]
 },
 {
  "qid": "qb9cba5553c",
  "brief": "Write a phone-call transcript. Tone: polite and brief. Hint: the customer simply states the wish to send the item back.",
  "register": "transcript",
  "slots": {
   "CUSTOMER": "name",
   "ITEM": "name",
   "STORE": "name"
  },
  "rules": [
   "A phone-call transcript of 2-4 lines 'Agent: ...' / 'Caller: ...'; the caller gives the name {CUSTOMER} once; the agent speaks for {STORE}.",
   "Already taken: never repeat, and never copy closely, a message listed under your item's register in the 'Already taken' section of this file.",
   "Words that made a program throw away earlier messages: 'much' and 'bunch' (as in 'thanks so much' or 'a bunch of questions') and 'right' in any use (as in 'Right,' at the start of a reply, 'all right', 'right away'). Thank with 'thank you' or 'thanks' only."
  ]
 }
]
```
