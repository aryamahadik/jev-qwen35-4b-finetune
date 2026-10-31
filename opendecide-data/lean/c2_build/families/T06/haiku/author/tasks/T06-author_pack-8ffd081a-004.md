# Haiku authoring task T06-author_pack-8ffd081a-004 (family T06, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/author/answers/T06-author_pack-8ffd081a-004.json

The answer is one JSON list with exactly 6 objects, one per item below, each carrying that item's qid.

## Instructions

You invent "packs": the made-up setting of one invented online store. A program later builds practice puzzles about shopping from your packs; you never see the puzzles. Each item gives a brief (the kind of store). Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "store": the store's name: 2 or 3 words, each starting with a capital letter, letters only (no digits, "&", apostrophe or hyphen), an invented name that is not a real company, brand or website, for example "Brightwell Home".
- "goods": an object with exactly these four keys, each a list of different item names the store sells:
  - "standard": 5 ordinary manufactured items (for example "desk lamp", "rain jacket", "board game");
  - "custom": 3 items made to the buyer's own specification: engraved, monogrammed, printed with a chosen name or photo, or made to measure (for example "engraved watch", "pair of made-to-measure curtains");
  - "perishable": 3 food or flower items that spoil within days (for example "box of pastries", "fresh flower bouquet", "cheese hamper");
  - "hygiene": 3 items sold in a protective hygiene seal (for example "electric toothbrush", "face serum", "swimsuit", "wireless earbud set").
  Item names: lower case, 1-5 words, letters, spaces and hyphens only; a plain noun phrase that reads right after "a" or "an" and after "the" (write "pair of hiking boots" or "set of mixing bowls", never a bare plural); no brand, no digits, no quantity or size words, no colour, and no word about the item's condition or quality.
- "customers": 6 invented customer names, each "First Last" (two capitalised words, letters only), from varied backgrounds; no famous people.
- "jurisdiction": the name of an invented country or region: one capitalised word of 5-10 letters, letters only, not a real place (for example "Valdoria").

The store's goods fit its brief. No name or item contains the words not, no, none, never or nothing. Never use words about an item being damaged, worn, used or spoiled. Every store, item, customer and jurisdiction must differ from every other one you write.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only.

## Answer format

[{"qid": "q...", "pack": {"store": "...", "goods": {"standard": [5 names], "custom": [3], "perishable": [3], "hygiene": [3]}, "customers": [6 names], "jurisdiction": "..."}}, ...]

## Items (6; one JSON object per line)

```json
[
{"qid": "qd439daf429", "brief": "An invented online store: a mountain lodge store. Its range includes all four kinds of goods the pack asks for."},
{"qid": "qc167266966", "brief": "An invented online store: a picnic and outdoor dining store. Its range includes all four kinds of goods the pack asks for."},
{"qid": "qd31c72d6a1", "brief": "An invented online store: a hiking and trail store. Its range includes all four kinds of goods the pack asks for."},
{"qid": "qdd1a5ae864", "brief": "An invented online store: an audio and gadget store with a snack bar. Its range includes all four kinds of goods the pack asks for."},
{"qid": "qf24e29330d", "brief": "An invented online store: a travel goods store. Its range includes all four kinds of goods the pack asks for."},
{"qid": "qa9cd06d586", "brief": "An invented online store: a fitness and nutrition store. Its range includes all four kinds of goods the pack asks for."}
]
```
