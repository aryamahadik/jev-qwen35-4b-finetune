# T07 redo2 extraction task T07-extract_g3h-918cfd16-004 (kind extract_g3h; read redo2-g3h)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_g3h-918cfd16-004.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 40 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "extraction". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: q3a5a42dc4c, q5d2e01e79a, q3d1b45c2c3, q06e160df95, qf43759698e, q30aa014e91, q59871ca0fb, q61cc38c2c5, q5c49109925, qef443defda, q25c094af59, q5fcfce1a52, q3d9690a6de, q4360ffd6a0, qa4a7fbd905, qb76163aeb0, q564605f8d8, q1092768867, qca5dfe4cfd, q3009869a53, qed983df395, qfde90b4c5f, q6e0e74a884, q0900dbed24, qefdf490c82, q0609869581, q746141f5ce, q700fca1cca, qd3381e852e, qc092a1064e, qd0f21bf976, q945df5a205, q2cbabe299c, q00a2a0c7c9, q99b1255915, q2da5a48cb2, q6a7ab49371, q7da1431e3f, q86b05ff5b1, q3304fd76ab.
- "extraction": one JSON object with every schema field name of the item, and no other name.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "q3a5a42dc4c", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}, ...]

Task kind: extract_g3h; read redo2-g3h; items: 40; outputs expected: 40.

## Instructions

TASK: FILL IN THE FIELDS OF ONE ADVERTISEMENT TEXT.

Each item has a "text" (a short advertisement; its fine print is one line that starts with a star, *) and a "schema"
(the fields to fill, each with a description and, for some, the choices allowed). Read the text on its own and fill
every field from the text only.

- "store": the name of the store that runs the advertisement, copied as written.
- a field ending in "_rule": copy one of its listed choices exactly. Use "absent" when the text states no rule of that
  kind.
- a field ending in "_bound": copy the value that the rule names, exactly as written in the text (a date, an amount, a
  category or a level name). Use null when the rule is absent.

Do not guess a value the text does not state. Do not correct spelling or change the wording. Judge each item on its own.

Output: one JSON array with exactly one object per item, keyed by the item's "qid":
[{"qid": "...", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}]
Use every schema field name exactly, and no other names. No text outside the JSON.
Write the whole answer with the Write tool to the ANSWER FILE named in your task file, and nowhere else.

## Items (40; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q3a5a42dc4c",
  "text": "Harborlight Goods brings you thoughtful, well-made essentials that feel right at home. Browse our selection and see what catches your eye. Our team is glad to help you find your favourite finds.\n*Excludes items with refurbished status. Minimum order subtotal: $25.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q5d2e01e79a",
  "text": "Hello neighbours, Birchwood Linens is delighted to share our new arrivals with you. Pop by the shop and say hi. Thanks for being part of our little community.\n*Covers the electronics product category only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q3d1b45c2c3",
  "text": "Subject: practical picks for fresh air\nHello there,\nWrenfield Outdoor helps you enjoy fresh air with dependable, down to earth equipment. Our lightweight picks and sturdy accessories suit everyday adventures. Pack a flask and a map, then head out for a stroll.\nHappy exploring,\n*Valid for orders placed on or before 17 February 2026. Valid only for items in the garden tools category.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q06e160df95",
  "text": "Subject: a soft note from our home to yours\nDear friend,\nThank you for visiting Cedarline Living. We are glad to share gentle ideas for a calm and cozy home, chosen with a patient eye. Our team hopes these pieces bring a little peace into your life.\nWith gratitude, the team\n*Valid for orders placed on or before 29 June 2026. Delivery to Hollin only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qf43759698e",
  "text": "Turn up the fun with Northvale Audio, where music lovers feel right at home. Let the tunes do the talking! Thanks for stopping by and sharing your playlist with us.\n*Excludes items with clearance status. Order by 12 May 2026 at the latest.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q30aa014e91",
  "text": "Welcome to Thistledown Supply, where calm design meets thoughtful choices. Take a relaxed moment to explore what we have prepared, and let quality speak for itself. Thank you for listening, and we appreciate your attention.\n*Excludes items with pre-order status. Valid for orders placed on or before 7 July 2026.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q59871ca0fb",
  "text": "Hey you, Copperleaf Kitchen is sending playful vibes your way! Come and say hello.\n*Valid for orders placed on or after 28 November 2026. Minimum order subtotal: $35.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q61cc38c2c5",
  "text": "Cozy comfort begins with gentle warmth and a soft, calm feeling. Kestrel Outfitters helps your family rest easy and share happy smiles.\n*Covers the bedding product category only. The order subtotal must be above $100.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q5c49109925",
  "text": "Hi from Wrenfield Outdoor. Pop in and see what we have ready for your trip ahead.\n*For Premier members and below.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qef443defda",
  "text": "Thanks for bringing a splash of colour home from Birchwood Linens.\nA gentle shake and a fluffy dry help it stay soft and happy.\nThen fold it neatly and enjoy the cozy moments ahead.\n*Minimum order subtotal: $100.00. Excludes delivery to Hollin.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q25c094af59",
  "text": "Welcome to Elmstead Emporium, where polished choices meet friendly service. Our experts are ready to guide you toward a beautifully chosen assortment. Thank you for trusting us, and enjoy your stay.\n*Items whose status is open box are excluded. The order subtotal must be above $75.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q5fcfce1a52",
  "text": "Juniper Gadgets brings quiet, refined tech to a calm, thoughtful home. Take a slow look as you browse.\n*Items whose status is open box are excluded. Delivery to Fallowmere only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q3d9690a6de",
  "text": "Thank you for choosing Harborlight Goods.\nCare for it gently with a soft cloth, and store it in a dry, sheltered place.\nSimple habits help it look its best for longer, and we are glad to be part of your routine.\n*Valid on orders over $100.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q4360ffd6a0",
  "text": "Hey there, this is Quaymoor Traders with a bit of playful magic for you. Our shelves are bursting with quirky finds and charming surprises, so pop in and let your senses wander. See you there!\n*Valid on orders of $25.00 or more. Order by 14 May 2026 at the latest.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qa4a7fbd905",
  "text": "Thank you for choosing Harborlight Goods. Dust it gently with a soft cloth and let it rest in a shady spot, away from damp. A little attention goes a long way, and it looks sharp for longer.\n*Order by 24 August 2026 at the latest.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qb76163aeb0",
  "text": "Subject: modern tech picks are in\nHi there,\nJuniper Gadgets has fresh tech, crisp design and a clever spirit to share. Browse what is new, find your fit, and enjoy the ride.\n*Excludes items with open box status. Delivery to Fallowmere only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q564605f8d8",
  "text": "Hi there, families! Come and see what is waiting for you at Elmstead Emporium.\nBring the little explorers along and let them look around our cheerful aisles.\nWe are happy to see you, and thank you for visiting with us.\n*Items whose status is final sale are excluded. Orders delivered to Arvale are excluded.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q1092768867",
  "text": "Hello from the team at Kestrel Outfitters, your friendly neighbourhood shop. We love chatting with regulars and helping folks find just the right pick. Drop in and say hello.\n*Covers the bedding product category only. The order subtotal must be above $100.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qca5dfe4cfd",
  "text": "Thank you for choosing Wrenfield Outdoor.\nCalm, careful attention helps your piece hold its beauty.\nWe appreciate your trust and wish you a peaceful life.\n*Excludes the pet supplies category.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q3009869a53",
  "text": "Rowanbrook Store brings you a refined selection for the modern home. Discover thoughtful pieces that add character to your kitchen, hallway and balcony. Explore with confidence, and let our experts help you choose with ease.\n*Items in the bedding product category are excluded.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qed983df395",
  "text": "Hi from Kestrel Outfitters, your neighbourly shop with a friendly welcome. Stop in for a chat and a browse.\n*Minimum order subtotal: $150.00. Excludes items with pre-order status.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qfde90b4c5f",
  "text": "Birchwood Linens brings refined comfort and tasteful design to the spaces you love. Our range is crafted with care, and we are confident you feel at ease. Thanks for exploring with us.\n*The order subtotal must be above $200.00. Order by 4 August 2026 at the latest.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q6e0e74a884",
  "text": "Subject: a practical update\nDear friend,\nBirchwood Linens has everyday bits and bobs for a tidy home.\nOur racks are easy to browse, with clear labels and friendly help nearby.\nThanks for stopping by, and we are grateful for your custom.\n*Valid on orders over $50.00. Valid only for items in the pet supplies category.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q0900dbed24",
  "text": "Thank you for choosing Kestrel Outfitters. Clean up messes gently with a soft cloth, and place it in a cozy spot. We hope your family enjoys it and shares cheerful laughs together.\n*Items whose status is final sale are excluded. Minimum order subtotal: $150.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qefdf490c82",
  "text": "Welcome to Birchwood Linens, where cozy textures make a home feel warm. We are glad you stopped by. Thank you for being part of our community.\n*Valid for orders placed on or after 12 July 2026. Delivery to Arvale only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q0609869581",
  "text": "Subject: Cedarline Living has fresh ideas for you\nHello friends,\nWe have been busy dreaming up a lovely new look for your home, and we are glad to share it with you. Thanks for stopping by, and enjoy a playful browse of our newest picks.\n*Valid only for orders delivered to Hollin. Valid for orders placed before 2 March 2026.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q746141f5ce",
  "text": "Brightwell Home has practical essentials for busy households. Take a look at what suits your space, read up on what it does, and pick what feels right for you. We make things simple and fair.\n*Valid for orders placed before 4 September 2026. Delivery to Fallowmere only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q700fca1cca",
  "text": "Subject: a warm hello with love\nDear friend,\nWelcome to Birchwood Linens. We are so happy you stopped by. We love sharing gentle ideas for a restful, cozy life. Please take a look around, and we are here with a friendly smile to help.\nThank you and warm regards, the team\n*Orders delivered to Brenmoor are excluded. Valid only for items in the bedding category.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qd3381e852e",
  "text": "Tidewell Supply here with practical bits for your home. Drop in, browse, and pick what suits you.\n*Items in the toys product category are excluded. Orders delivered to Fallowmere are excluded.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qc092a1064e",
  "text": "Hello and welcome to Elmstead Emporium, our warm little corner of the high street. Come in and enjoy a friendly chat with our helpful crew. We are so happy you are here, and we look forward to meeting you.\n*Delivery to Fallowmere only. Excludes items with refurbished status.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "qd0f21bf976",
  "text": "Subject: Fresh, modern picks\nHi there,\nOakhurst Interiors has clean shapes, bold textures and sharp ideas ready for you. Scroll and see what speaks to you. Thanks for stopping by, and we look forward to hearing from you.\n*Minimum order subtotal: $150.00. Valid only for items in the furniture category.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q945df5a205",
  "text": "Thanks for choosing Brightwell Home. We hope your new piece adds joy to your kids' routine. Clean it with a soft sponge and mild soap, then rinse it and let it air out.\n*Orders delivered to Fallowmere are excluded. Members at the Blue level or higher only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q2cbabe299c",
  "text": "Fernway Market has fresh arrivals waiting for you. Stop by, browse the newest picks and find your new favorite.\n*Excludes items with clearance status. Valid for orders placed before 10 November 2026.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q00a2a0c7c9",
  "text": "Welcome, and thank you for choosing Birchwood Linens.\nA little gentle care helps your piece stay soft and cozy.\nWe are so happy to have you with us.\n*The order subtotal must be above $100.00. Members at the Blue level or higher only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q99b1255915",
  "text": "Kestrel Outfitters has everyday staples for people who like to be prepared. Grab dependable basics for the path ahead. Simple, reliable choices make the journey smoother.\n*Valid for orders placed on or after 9 June 2026. The order subtotal must be above $100.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q2da5a48cb2",
  "text": "Subject: a quiet note on refined living\nDear friend,\nLarkspur Playthings presents a calm selection of refined pieces for thoughtful households.\nBrowse our carefully curated range at your own pace, and let the quality speak for itself.\nWe appreciate your trust and look forward to welcoming you back.\nWarm regards,\nThe team\n*Minimum order subtotal: $35.00. Delivery to Arvale only.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q6a7ab49371",
  "text": "Welcome to Rowanbrook Store, where thoughtful design meets quiet calm. Our spaces are meant to feel unhurried and refined, so take your pick at a gentle pace. We appreciate you joining us and look forward to sharing new ideas.\n*Members at the Platinum level or higher only. Minimum order subtotal: $150.00.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q7da1431e3f",
  "text": "Hello friends, welcome to Rowanbrook Store, the friendliest stop on the high street. We have cosy finds for grown-ups and kids alike. Pop in with the family and let our friendly team help you find a fun keepsake to take home.\n*Valid on orders of $50.00 or more.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q86b05ff5b1",
  "text": "Hi from Juniper Gadgets! Fun new gizmos are here for the family and friends.\n*Order by 23 March 2026 at the latest. Excludes items with final sale status.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 },
 {
  "qid": "q3304fd76ab",
  "text": "Birchwood Linens makes everyday living a little easier.\nPractical picks and sturdy weaves suit real life, so you get on with your plans.\nThanks for shopping with us.\n*Order by 18 May 2026 at the latest. For Green members and below.",
  "schema": [
   {
    "field": "store",
    "type": "name",
    "describe": "the store that runs the advertisement"
   },
   {
    "field": "region_rule",
    "type": "enum",
    "describe": "the delivery-region rule of the fine print: in = only that region, out = that region excluded, absent = no region rule",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "region_bound",
    "type": "category",
    "describe": "the value the region rule names, as written (null if absent)",
    "choices": [
     "Arvale",
     "Brenmoor",
     "Calderon",
     "Dunmere",
     "Eskarth",
     "Fallowmere",
     "Greyhaven",
     "Hollin"
    ]
   },
   {
    "field": "category_rule",
    "type": "enum",
    "describe": "the product-category rule: in = only that category, out = that category excluded, absent = none",
    "choices": [
     "in",
     "out",
     "absent"
    ]
   },
   {
    "field": "category_bound",
    "type": "category",
    "describe": "the value the category rule names, as written (null if absent)",
    "choices": [
     "bedding",
     "electronics",
     "furniture",
     "garden tools",
     "kitchenware",
     "pet supplies",
     "sports gear",
     "toys"
    ]
   },
   {
    "field": "status_rule",
    "type": "enum",
    "describe": "the price-status rule: out = items with that status excluded, absent = none",
    "choices": [
     "out",
     "absent"
    ]
   },
   {
    "field": "status_bound",
    "type": "category",
    "describe": "the value the status rule names, as written (null if absent)",
    "choices": [
     "clearance",
     "final sale",
     "open box",
     "pre-order",
     "refurbished",
     "regular price"
    ]
   },
   {
    "field": "date_rule",
    "type": "enum",
    "describe": "the order-date rule: le = on or before the date, lt = strictly before, ge = on or after, absent = none",
    "choices": [
     "le",
     "lt",
     "ge",
     "absent"
    ]
   },
   {
    "field": "date_bound",
    "type": "date",
    "describe": "the value the date rule names, as written (null if absent)"
   },
   {
    "field": "tier_rule",
    "type": "enum",
    "describe": "the membership rule: min = that level and above, max = that level and below, absent = none",
    "choices": [
     "min",
     "max",
     "absent"
    ]
   },
   {
    "field": "tier_bound",
    "type": "category",
    "describe": "the value the tier rule names, as written (null if absent)",
    "choices": [
     "Basic",
     "Black",
     "Blue",
     "Bronze",
     "Elite",
     "Gold",
     "Green",
     "Platinum",
     "Plus",
     "Premier",
     "Silver"
    ]
   },
   {
    "field": "spend_rule",
    "type": "enum",
    "describe": "the subtotal rule: ge = at least the amount, gt = strictly more, absent = none",
    "choices": [
     "ge",
     "gt",
     "absent"
    ]
   },
   {
    "field": "spend_bound",
    "type": "cents",
    "describe": "the value the spend rule names, as written (null if absent)"
   }
  ]
 }
]
```
