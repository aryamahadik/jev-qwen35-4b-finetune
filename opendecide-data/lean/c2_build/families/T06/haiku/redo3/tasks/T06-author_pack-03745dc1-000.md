# T06 redo3 authoring task T06-author_pack-03745dc1-000 (kind author_pack)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo3/answers/T06-author_pack-03745dc1-000.json

(The folder of that path is created by your write if it does not exist yet.)

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 5 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "pack". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q725202ead7, q6d0e2d0234, qa8dd9cb3b1, q6793f649a5, qe339f16ffb.
- "pack": one JSON object with exactly four keys: "store" (a string), "goods" (an object with exactly the keys "standard" (a list of 5 strings), "custom" (a list of 3), "perishable" (a list of 3) and "hygiene" (a list of 3)), "customers" (a list of 6 strings) and "jurisdiction" (a string). Every value follows the instructions below.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a double quote as \".
Literal example of the shape (angle brackets stand for what you write; the qid shown is the first real one): [{"qid": "q725202ead7", "pack": {"store": "<store name>", "goods": {"standard": ["<item>", "<item>", "<item>", "<item>", "<item>"], "custom": ["<item>", "<item>", "<item>"], "perishable": ["<item>", "<item>", "<item>"], "hygiene": ["<item>", "<item>", "<item>"]}, "customers": ["<First Last>", "<First Last>", "<First Last>", "<First Last>", "<First Last>", "<First Last>"], "jurisdiction": "<jurisdiction>"}}, ...]

Task kind: author_pack; items: 5; outputs expected: 5.

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

## Already taken (never repeat, and never copy closely, anything listed here)

Each entry is one JSON string (a line break inside a text is written \n).

### Stores already used (38)
- "Marrowdale Home"
- "Carrowell Emporium"
- "Sorrelmere Pantry"
- "Tinselwick Parties"
- "Vellmora Wellness"
- "Bramblecot Nursery"
- "Stonefall Outfitters"
- "Kettlecrumb Bakehouse"
- "Quillmere Campus"
- "Fennick Apothecary"
- "Brinehollow Trading"
- "Pinecrest Trailhouse"
- "Thistlemoor Atelier"
- "Whiskerfold Home"
- "Quellan Tea Kitchen"
- "Brindlewood Acres"
- "Sunstring Revelry"
- "Ferrovox Audio Bar"
- "Pennyfold Stationery"
- "Mellowbrook Linens"
- "Quarrymoor Nutrition"
- "Pearlhollow Registry"
- "Bramblecourt Flowers"
- "Ferrowby Cheese House"
- "Corvane Trailworks"
- "Quillmere Shores"
- "Tallowgate Kitchen"
- "Puddlecrest Toys"
- "Tallowmere Table"
- "Thornmoss Grooming"
- "Lanternwick Market"
- "Lumenwick Home"
- "Ravenmoor Cycles"
- "Lyrewind Gifts"
- "Brackwell Summit"
- "Cordelle Corner"
- "Mirrowmere Lodge"
- "Dunmere Provisions"

### Jurisdictions already used (38)
- "Brelunia"
- "Tarsenia"
- "Cromandy"
- "Orlevia"
- "Istraven"
- "Lumeria"
- "Ostrenia"
- "Corvane"
- "Solvane"
- "Kestria"
- "Drevonia"
- "Miravel"
- "Brevonia"
- "Quintara"
- "Brelmoria"
- "Velmora"
- "Dorlanth"
- "Brindolt"
- "Maldrine"
- "Tavimor"
- "Quelmara"
- "Quiveran"
- "Quellisia"
- "Thalmar"
- "Dravenco"
- "Veltharia"
- "Ellarion"
- "Auredia"
- "Mirovane"
- "Hesmarin"
- "Wessalind"
- "Serrundo"
- "Iskarvia"
- "Corvania"
- "Keltharn"
- "Tavrinth"
- "Velmara"
- "Kestrovia"

## Items (5; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q725202ead7",
  "brief": "An invented online store: a travel goods store. Its range includes all four kinds of goods the pack asks for. Check your pack before you answer, because a program throws away the whole pack for any of these: (1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a customer name that is not exactly two words, each with a capital first letter followed only by lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the 'Already taken' section of this file or that another pack of yours uses."
 },
 {
  "qid": "q6d0e2d0234",
  "brief": "An invented online store: a camping store. Its range includes all four kinds of goods the pack asks for. Check your pack before you answer, because a program throws away the whole pack for any of these: (1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a customer name that is not exactly two words, each with a capital first letter followed only by lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the 'Already taken' section of this file or that another pack of yours uses."
 },
 {
  "qid": "qa8dd9cb3b1",
  "brief": "An invented online store: an art and craft store. Its range includes all four kinds of goods the pack asks for. Check your pack before you answer, because a program throws away the whole pack for any of these: (1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a customer name that is not exactly two words, each with a capital first letter followed only by lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the 'Already taken' section of this file or that another pack of yours uses."
 },
 {
  "qid": "q6793f649a5",
  "brief": "An invented online store: a vintage-style home store. Its range includes all four kinds of goods the pack asks for. Check your pack before you answer, because a program throws away the whole pack for any of these: (1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a customer name that is not exactly two words, each with a capital first letter followed only by lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the 'Already taken' section of this file or that another pack of yours uses."
 },
 {
  "qid": "qe339f16ffb",
  "brief": "An invented online store: a college town store. Its range includes all four kinds of goods the pack asks for. Check your pack before you answer, because a program throws away the whole pack for any of these: (1) an item name that ends with the letter s unless the name contains the word 'of' or ends with 'ss' or 'us' (so not 'trellis', 'canvas' or 'nail clippers'; 'pair of nail clippers' is fine); (2) a customer name that is not exactly two words, each with a capital first letter followed only by lower-case letters (so not 'MacRae', not 'O'Brien'); (3) a store name or jurisdiction that is in the 'Already taken' section of this file or that another pack of yours uses."
 }
]
```
