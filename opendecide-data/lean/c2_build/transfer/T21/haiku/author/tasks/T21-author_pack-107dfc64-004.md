# Haiku authoring task T21-author_pack-107dfc64-004 (family T21, kind author_pack)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/haiku/author/answers/T21-author_pack-107dfc64-004.json

Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.
The answer is one JSON list with exactly 8 objects, one per item below, each carrying that item's qid. Inside JSON strings, write a line break as \n and a double quote as \".

## Instructions

You invent "packs": the made-up names behind one invented line of business that signs contracts with other organisations. A program later builds reading puzzles from your packs; you never see the puzzles. Each item gives a short brief (the line of business). Write ONE pack per item.

A pack is a JSON object with exactly these two keys:
- "agreements": 4 different agreement names. Each is one or two capitalised invented words, then one or two lower-case words for the kind of deal, then the word "agreement", for example "Oatfield licence agreement", "Harbor Lantern supply agreement", "Gallowhill hosting agreement". Letters, spaces, hyphens and apostrophes only.
- "parties": 6 different invented organisation names, each 2-3 words, every word capitalised, for example "Brindle Foods", "Corran Rail", "Upland Water Board". Letters, spaces, hyphens and apostrophes only. Never use the word "agreement" in a party name.

Word rules for every name (a program rejects a pack that breaks one):
1. No digits, no number words or ordinals (one, two, first, second, half, double, single, dozen ...).
2. No word about claims, contracts or their terms: cap, limit, liability, claim, clause, notice, term, cause, schedule, definitions, dispute, court, tribunal, carve, waiver, indemnity, and none of these words: breach, confidentiality, secret, privacy, data, protection, leak, intellectual, property, patent, copyright, trademark, infringement, late, delay, delivery, shipment, defective, faulty, goods, fees, invoice, payment, unpaid, injury, accident, harm, damage, fire, flood, security, incident, hack, negligence, careless, misconduct, deliberate, fraud, subcontractor, contractor, supplier, vendor, mistake, error, ordinary, gross, wilful, personal, duties.
3. No word that judges or reports a state or an outcome: approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, closed, active, settled, resolved, outstanding, breached, waived, granted, ok, okay, fine, good, bad, strong, weak, safe, risky, win, lose.
4. No word about time or frequency: daily, weekly, monthly, yearly, annual, morning, evening, night, early, last, next, new, old, now, today.
5. No negative word: not, no, non, never, none, without, nothing, lack, un- words such as "unpaid".
6. No modal or quantity word: may, must, can, will, should, need, able, all, every, each, any, some, both, only, more, most, many, few, extra, total, whole, full, maximum, minimum, main, general.
7. Invent everything: no real company, brand, product, town, street or famous person, and none of the example names above. No name of a pack may contain another name of the same pack (for example a party "Oatfield" beside "Oatfield licence agreement").

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"agreements": [...], "parties": [...]}}. Valid JSON only. Every pack must differ from every other pack you write.

## Answer format

[{"qid": "q...", "pack": {"agreements": ["...", "...", "...", "..."], "parties": ["...", "...", "...", "...", "...", "..."]}}, ...]

## Items (8; answer every item once, keyed by its qid)

```json
[
{"qid": "q080cc349b8", "brief": "An invented line of business: a hotel group. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "qaf174433c6", "brief": "An invented line of business: a water utility. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "q8920ffd809", "brief": "An invented line of business: a dairy cooperative. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "q79a3a6f8e4", "brief": "An invented line of business: a flower grower. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "qaf29bb5c3b", "brief": "An invented line of business: a regional airport operator. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "q7ae84e2005", "brief": "An invented line of business: a fishing cooperative. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "q16183f4458", "brief": "An invented line of business: a tram network. Invent the names of its agreements and of the organisations it deals with, to fit it."},
{"qid": "q9614623cb3", "brief": "An invented line of business: a city parks department. Invent the names of its agreements and of the organisations it deals with, to fit it."}
]
```
