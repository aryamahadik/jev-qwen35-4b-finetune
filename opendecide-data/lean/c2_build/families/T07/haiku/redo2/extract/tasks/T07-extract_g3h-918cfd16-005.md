# T07 redo2 extraction task T07-extract_g3h-918cfd16-005 (kind extract_g3h; read redo2-g3h)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_g3h-918cfd16-005.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 40 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "extraction". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: q1f625eceab, qd6732150cf, qb4e1369354, q63fcbb396a, q2b2ecc30a3, qa837b18cf4, q46ff6749f5, q063501a5b3, qbb283d90cd, q6e98712693, qb1c949da1e, q9db5e01ca8, q2656a7de99, qf046855d2c, q8057525c9d, q8ad490d758, qe5f89cc054, q3e7dc6a47a, q4077c7ea3b, q1b1bf46186, q95d3c521ec, qcf91677354, qfb30fdd042, q17feb19dbc, q33316b44ad, q8fed0d0a41, q9ea2baa927, q763999b9b6, q66d62f3063, q34f7000c11, q3c44677a16, qd9fbd8b13d, qdee0c0fd6a, qe45ab321c4, qb369579e54, qb91aebfd25, qc76164474b, q986bcfb078, qd5ed627cf0, q047cf179de.
- "extraction": one JSON object with every schema field name of the item, and no other name.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "q1f625eceab", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}, ...]

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
  "qid": "q1f625eceab",
  "text": "Subject: simple, sensible ideas for home\nDear friend,\nThanks for reading. At Marigold Pets we focus on simple, sensible ideas that make routine tasks easier. We are happy to help you find what suits your home, and we are glad to answer your questions.\nSincerely, the team\n*The order subtotal must be above $200.00. Delivery to Dunmere only.",
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
  "qid": "qd6732150cf",
  "text": "Thank you for choosing Birchwood Linens for your family home.\nGentle care helps your piece stay soft and cozy for the people you love.\nThanks for trusting us, and we are glad you are here.\n*The order subtotal must be above $100.00. Members at the Blue level or higher only.",
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
  "qid": "qb4e1369354",
  "text": "Brightwell Home here: sharp new arrivals, quick picks and slick ideas for your space. Step in and browse the newest finds.\n*For Premier members and above. Valid for orders placed on or before 29 September 2026.",
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
  "qid": "q63fcbb396a",
  "text": "Quick hello from Bluecrest Sports, where momentum meets style. Dive in and see what is fresh.\n*Members at the Basic level or lower only. Excludes items with pre-order status.",
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
  "qid": "q2b2ecc30a3",
  "text": "Hello there, and welcome to Rowanbrook Store. We are so pleased you stopped by, and we hope you feel at home as you look around. Take your pick, say hello to our friendly crew, and let us help make your visit a happy experience.\n*Valid for orders placed on or after 4 June 2026.",
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
  "qid": "qa837b18cf4",
  "text": "Hello from your neighbourhood helpers at Birchwood Linens!\nWe love seeing familiar faces and sharing fresh ideas for your home.\nPop in and say hello, we are glad to chat.\n*Excludes delivery to Fallowmere. Order by 14 June 2026 at the latest.",
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
  "qid": "q46ff6749f5",
  "text": "Subject: A little fun is brewing at Copperleaf Kitchen\nDear friend,\nOur playful mood is in full swing, and we hope it finds you smiling.\nPop in, browse the cheerful corners, and enjoy a bit of cheer.\nThank you for being such good company.\n*Excludes the electronics category. Delivery to Hollin only.",
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
  "qid": "q063501a5b3",
  "text": "Thank you for choosing Tidewell Supply.\nSimple care helps your piece look sharp and feel great.\nThanks for being with us, we are glad you are here.\n*Excludes delivery to Eskarth. Minimum order subtotal: $35.00.",
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
  "qid": "qbb283d90cd",
  "text": "Subject: a quiet welcome from our team\nDear friend,\nThank you for stopping by Bluecrest Sports. We appreciate your trust, and we are glad to share thoughtful ideas for the path ahead. Our team has made these pieces with care, so your steps feel steady and smooth.\nWarm regards, the team\n*Order by 21 April 2026 at the latest.",
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
  "qid": "q6e98712693",
  "text": "Subject: a warm welcome from our little corner of the world\nHello and welcome,\nPebblestone Garden is delighted to share ideas for calm, cozy living. Our team loves helping you create a welcoming space. Thank you for being here with us.\n*Excludes items with final sale status. For Green members and below.",
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
  "qid": "qb1c949da1e",
  "text": "Welcome to Quaymoor Traders, where good taste meets a friendly face. Browse our carefully chosen range and find what suits your home just right. Step in, wander the shelves, and let our team help you pick the perfect piece.\n*Valid on orders of $25.00 or more. Order by 14 May 2026 at the latest.",
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
  "qid": "q9db5e01ca8",
  "text": "Fresh ideas move fast, and Juniper Gadgets moves right along with you. Sharp design, clever features and simple setup, ready for your big adventure.\n*Valid on orders of $150.00 or more. Order by 20 August 2026 at the latest.",
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
  "qid": "q2656a7de99",
  "text": "Harborlight Goods brings a calm, refined touch to modern living. Our pieces are chosen with care and crafted with thought. Relax and enjoy a quiet, elegant feel.\n*Excludes items with refurbished status. Minimum order subtotal: $25.00.",
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
  "qid": "qf046855d2c",
  "text": "Subject: practical picks for your home\nDear friend,\nCedarline Living has practical picks for real life at home.\nBrowse the shelves, compare what suits your space, and choose with confidence.\nOur team is happy to answer questions, big or small.\nThanks for reading, and we hope to see you again.\nWarm regards,\nThe team\n*Valid for orders placed on or before 29 June 2026. Delivery to Hollin only.",
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
  "qid": "q8057525c9d",
  "text": "Hi from Juniper Gadgets, your neighbourhood shop with friendly faces. Pop in and say hello, we are happy to chat.\n*Order by 23 March 2026 at the latest. Excludes items with final sale status.",
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
  "qid": "q8ad490d758",
  "text": "Subject: a quiet note on refined essentials\nHello there,\nWrenfield Outdoor curates refined pieces for people who enjoy a slower pace. Our selection is thoughtful and well made. Enjoy the calm of fresh air.\n*Minimum order subtotal: $50.00. Members at the Blue level or higher only.",
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
  "qid": "qe5f89cc054",
  "text": "Thank you for choosing Marigold Pets.\nGentle care helps your piece look refined for longer.\nDab it softly with a cloth and let it air dry in a calm spot.\n*Excludes delivery to Calderon. Valid for orders placed on or before 26 March 2026.",
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
  "qid": "q3e7dc6a47a",
  "text": "Subject: a sharper approach to cooking and hosting\nHello there,\nCopperleaf Kitchen is pleased to present a refined assortment built for confident hosts and calm, well-run gatherings. Our newest arrivals combine practical design with lasting quality, and we are proud to share them with you. Thank you for choosing us as part of your routine.\nWarm regards,\n*Valid only for orders delivered to Fallowmere. Valid for orders placed from 2 May 2026 onward.",
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
  "qid": "q4077c7ea3b",
  "text": "Welcome to Rowanbrook Store, where a quiet sense of style is ready for you. Take a leisurely walk around the displays, and let calm surroundings and refined craft speak for themselves. Thanks for visiting, we appreciate your company.\n*Excludes items with open box status. Valid only for orders delivered to Arvale.",
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
  "qid": "q1b1bf46186",
  "text": "Tech fun is buzzing around here. Juniper Gadgets has playful picks that make tech feel like pure fun. Come say hello and see what catches your eye.\n*Valid on orders of $150.00 or more. Order by 20 August 2026 at the latest.",
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
  "qid": "q95d3c521ec",
  "text": "Thank you for choosing Wrenfield Outdoor. Great journeys deserve careful attention, so give your pack a quick dust when it has seen tough use, then let it dry fully and store it. Thanks for trusting us, and we are glad to support your adventures ahead.\n*Excludes items with final sale status. Valid on orders over $35.00.",
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
  "qid": "qcf91677354",
  "text": "Thanks for choosing Kestrel Outfitters for your outdoor plans.\nA quick dab when it gets muddy is easy.\nLet it dry in a shady corner and fold it neatly.\nEnjoy your outings, from our family to yours.\n*Valid on orders of $50.00 or more. Orders must be placed earlier than 14 January 2026.",
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
  "qid": "qfb30fdd042",
  "text": "Refined sound and sharp style meet at Northvale Audio.\nOur team is confident about the picks we make.\nCome and hear it for yourself.\n*Excludes items with clearance status. Order by 12 May 2026 at the latest.",
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
  "qid": "q17feb19dbc",
  "text": "Thank you for choosing Copperleaf Kitchen.\nConfident care helps your piece look refined and feel sturdy.\nWe appreciate your trust and look forward to hearing how it goes.\n*Members at the Premier level or higher only. Valid on orders of $200.00 or more.",
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
  "qid": "q33316b44ad",
  "text": "Thank you for welcoming Pebblestone Garden into your life. Care for your piece with a gentle clean and careful handling, and it stays sharp. We are proud to be part of your story.\n*Items whose status is final sale are excluded. Excludes the electronics category.",
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
  "qid": "q8fed0d0a41",
  "text": "Thanks for choosing Oakhurst Interiors. Dust it lightly with a soft cloth and move it away from direct sunlight. A little routine care goes a long way.\n*Excludes the bedding category. Valid on orders of $50.00 or more.",
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
  "qid": "q9ea2baa927",
  "text": "Thank you for choosing Brightwell Home. We are proud to share a little warmth with you. For easy upkeep, dust it lightly, dry it well, and enjoy the moments indoors.\n*Covers the kitchenware product category only. Excludes delivery to Brenmoor.",
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
  "qid": "q763999b9b6",
  "text": "Welcome to Pebblestone Garden, where warm hearts and fresh ideas meet. Come sit, chat, and find a cozy home for your favourite things. We are thankful for our visitors.\n*Valid on orders of $150.00 or more. Orders delivered to Brenmoor are excluded.",
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
  "qid": "q66d62f3063",
  "text": "Subject: sharper training, simpler routines\nHello there,\nBluecrest Sports gives athletes a confident edge with dependable, well-tested equipment. Build a steady routine, then push a little harder when you are ready. Our team is here to support your progress.\n*Members at the Elite level or higher only. Valid only for orders delivered to Hollin.",
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
  "qid": "q34f7000c11",
  "text": "Subject: a warm welcome from Marigold Pets\nHi friends,\nWe are so happy to have you here. Your companions deserve gentle, cozy comforts, and we love sharing fresh ideas that make home life easier.\n*Order by 31 January 2026 at the latest. The order subtotal must be above $50.00.",
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
  "qid": "q3c44677a16",
  "text": "Elmstead Emporium has treasures waiting to make you smile. Pop by and wander the aisles. Have a lovely browse and enjoy the fun.\n*Items whose status is open box are excluded. The order subtotal must be above $75.00.",
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
  "qid": "qd9fbd8b13d",
  "text": "Subject: Larkspur Playthings has fresh new ideas for play\nHi there,\nOur newest lineup is sharp, playful and made to be used again and again. Shop the look, grab your favourites, and enjoy the fun.\n*Items whose status is clearance are excluded.",
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
  "qid": "qdee0c0fd6a",
  "text": "Subject: Bluecrest Sports has practical picks for your plans\nHi there,\nWe have dependable essentials for the activities you love, and our staff are glad to guide you to the right fit. Drop by for a look and see what suits your plans.\n*Members at the Platinum level or higher only.",
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
  "qid": "qe45ab321c4",
  "text": "Hi folks, it is Thistledown Supply with a little sunshine for your spirits. Our shelves are full of tiny treasures and cheerful surprises. Hop on in, have a wander, and see what makes you giggle!\n*For Premier members and below.",
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
  "qid": "qb369579e54",
  "text": "Hi from Oakhurst Interiors! Come see our cosy family corner and say hello.\n*Valid only for orders delivered to Greyhaven. Items whose status is refurbished are excluded.",
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
  "qid": "qb91aebfd25",
  "text": "Bluecrest Sports brings dependable equipment for the way you train. Built for performance, our range feels confident underfoot. Step up your routine and push your boundaries.\n*Valid only for items in the bedding category. Valid on orders of $100.00 or more.",
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
  "qid": "qc76164474b",
  "text": "Copperleaf Kitchen is sharp, simple, and ready to inspire your cooking. Scroll the newest picks and find a favourite that clicks. Fast, clean curves and bold design make the choice easy.\n*Orders must be placed earlier than 23 March 2026. The order subtotal must be above $50.00.",
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
  "qid": "q986bcfb078",
  "text": "Hello, and warm welcome to Rowanbrook Store. We are delighted to have you here, and we hope your visit feels cozy and friendly. Take a leisurely look around, and please ask our team about your questions.\n*Valid on orders of $50.00 or more.",
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
  "qid": "qd5ed627cf0",
  "text": "Hello, and thanks for dropping by Rowanbrook Store. We are a down-to-earth crew who love simple, honest service. Take a look around and ask us your questions. Thanks for listening, and see you at the counter.\n*Valid for orders placed on or after 4 June 2026.",
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
  "qid": "q047cf179de",
  "text": "Thank you for bringing Cedarline Living into your home. Give your piece a soft cloth and a little affection, and it stays cheerful with you. We are so glad you chose us, and we hope it makes you smile for ages.\n*Valid for orders placed before 13 April 2026.",
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
