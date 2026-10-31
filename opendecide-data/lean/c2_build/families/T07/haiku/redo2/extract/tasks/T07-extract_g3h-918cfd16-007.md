# T07 redo2 extraction task T07-extract_g3h-918cfd16-007 (kind extract_g3h; read redo2-g3h)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_g3h-918cfd16-007.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 8 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "extraction". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: q7de52e8ac6, q5ceaefc7c3, qe1185bcd36, qe181b7a645, qca1281d0bb, qf84ba048cc, qd4673866e7, qb8463c4083.
- "extraction": one JSON object with every schema field name of the item, and no other name.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "q7de52e8ac6", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}, ...]

Task kind: extract_g3h; read redo2-g3h; items: 8; outputs expected: 8.

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

## Items (8; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q7de52e8ac6",
  "text": "Subject: Thoughtful selections from Copperleaf Kitchen\nDear friend,\nWe are proud of the pieces we have chosen for you. Our edit is crisp, polished, and easy to explore.\nThank you for putting your trust in us.\nWith best wishes\n*Excludes the electronics category. Delivery to Hollin only.",
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
  "qid": "q5ceaefc7c3",
  "text": "Subject: warm greetings from our friendly team\nHi there,\nWelcome to Northvale Audio, where we love helping you find the sound that feels just right. Our team is here to listen to what you enjoy and share ideas that fit your home.\n*Valid for orders placed on or before 10 July 2026. Members at the Plus level or higher only.",
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
  "qid": "qe1185bcd36",
  "text": "Thanks for picking Copperleaf Kitchen, and welcome to a happy little routine of care. Buff your piece gently with a soft cloth and a bit of attention, and it stays shiny and cheerful. We are so glad to be part of your home.\n*Members at the Premier level or higher only. Valid on orders of $200.00 or more.",
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
  "qid": "qe181b7a645",
  "text": "Subject: a warm welcome from our happy corner\nHello friend,\nLarkspur Playthings is delighted to share an assortment of cheerful ideas for curious little minds and grown-up hearts alike. We are so glad you stopped by. Thank you for being part of our story, and we look forward to seeing what you discover.\nWith love,\n*Valid only for orders delivered to Calderon. Order by 27 August 2026 at the latest.",
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
  "qid": "qca1281d0bb",
  "text": "Thanks for trusting Brightwell Home with your piece.\nA little gentle care helps it stay lovely and easy to love.\nWe are glad to have you as a neighbour.\n*Orders delivered to Fallowmere are excluded. Members at the Blue level or higher only.",
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
  "qid": "qf84ba048cc",
  "text": "Marigold Pets here with fresh, useful ideas for your home. Thanks for being part of our circle, and enjoy browsing.\n*The order subtotal must be above $35.00. Excludes items with refurbished status.",
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
  "qid": "qd4673866e7",
  "text": "Fast and fresh, Tidewell Supply is ready to fuel your plans. Swing by and see what is new.\n*Excludes delivery to Calderon. Items in the garden tools product category are excluded.",
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
  "qid": "qb8463c4083",
  "text": "Subject: simple ways to enjoy better sound\nHello there,\nNorthvale Audio helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 10 July 2026. Members at the Plus level or higher only.",
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
