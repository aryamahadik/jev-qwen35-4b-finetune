# T07 redo2 extraction task T07-extract_g3h-918cfd16-002 (kind extract_g3h; read redo2-g3h)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/extract/answers/T07-extract_g3h-918cfd16-002.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 40 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "extraction". No other keys.
- "qid": copy the item's qid exactly. The qids of this task: q5eb3d3677e, qf8fcca5a31, q0331ee8c40, q7b43012cfe, q2f5056827d, qc16cffe36e, q9d51ee37df, q9e04cbfd68, q1a53761ba9, qc847618767, q43f88e6e38, qafb94c8c92, q8043fd4cc3, q7f4c586bc3, qfa604f43d7, q6ebaeb20d8, q7eac68dafc, qcfc78148d7, qd7d765e234, q23a57b01ee, q14eac6d787, q755f96541e, q4954ce14d7, q44d192b3e6, q168d760344, qa7d5744c4f, q2e384c7b4c, q3be6a82c88, q433890fe98, q4cd0d22268, qc60976824e, qc6c63199e9, qa08914bb1b, q5d08f86c35, q11481853a6, qf24d648791, q368fe2fba2, q47269bff22, qe7c32cd0a6, qa18f66b480.
- "extraction": one JSON object with every schema field name of the item, and no other name.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
Literal shape: [{"qid": "q5eb3d3677e", "extraction": {"store": "...", "region_rule": "...", "region_bound": null, ...}}, ...]

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
  "qid": "q5eb3d3677e",
  "text": "Hi neighbours, it is Copperleaf Kitchen here with fresh ideas for your cooking. Pop by and say hello, we love to see friendly faces.\n*Order by 3 August 2026 at the latest. The order subtotal must be above $100.00.",
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
  "qid": "qf8fcca5a31",
  "text": "Subject: a warm welcome to fresh air\nDear friend,\nWelcome to Wrenfield Outdoor, where we love helping people step outside with confidence.\nOur team is glad to share sturdy essentials for your adventures ahead.\nWe appreciate you stopping by, and we hope your path feels bold and easy.\nWarm regards,\nThe friendly crew\n*Valid for orders placed from 19 February 2026 onward. Minimum order subtotal: $35.00.",
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
  "qid": "q0331ee8c40",
  "text": "Thanks for welcoming Juniper Gadgets into your home, neighbour. To care for your product, dust it gently with a soft, dry cloth and place it in a calm, tidy spot. Caring for it is easy, and we are happy to chat with you. Thanks for being part of our small-shop family.\n*Members at the Plus level or lower only. Valid for orders placed on or before 23 May 2026.",
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
  "qid": "q7b43012cfe",
  "text": "Bluecrest Sports is made for happy adventures with the family. Stroll in and enjoy a cheerful browse with your kids. Bring the crew and make it a fun trip.\n*Covers the pet supplies product category only. Valid for orders placed on or before 18 March 2026.",
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
  "qid": "q2f5056827d",
  "text": "Hello neighbours, a little note from Larkspur Playthings.\nWe love seeing familiar faces pop in to browse our shelves.\nThank you for being part of our small corner of town.\nWe are glad you are here.\n*Valid for orders placed on or after 9 May 2026.",
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
  "qid": "qc16cffe36e",
  "text": "Rowanbrook Store is confident and proud of its range. Step inside for thoughtful finds, carefully chosen for you. Craftsmanship shows in the corners.\n*Excludes items with open box status. Valid only for orders delivered to Arvale.",
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
  "qid": "q9d51ee37df",
  "text": "Welcome to Rowanbrook Store. Take a calm look at our thoughtful ideas for a quiet and comfortable home. We appreciate you stopping by, and we are glad to help you find a lovely piece for your space.\n*Items in the bedding product category are excluded.",
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
  "qid": "q9e04cbfd68",
  "text": "Thanks for choosing Harborlight Goods! Give your piece a little love with a gentle clean and a soft cloth. We are delighted you are here, and we hope it brings a smile to your face.\n*Members at the Blue level or lower only.",
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
  "qid": "q1a53761ba9",
  "text": "Hello, neighbours! It is lovely to see you at Quaymoor Traders.\nOur little shop is run with heart, and we know you by name.\nDo pop in and say hi.\n*Orders delivered to Calderon are excluded. Excludes items with final sale status.",
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
  "qid": "qc847618767",
  "text": "Marigold Pets has calm, thoughtful picks for your loyal companions. Browse at your leisure and find a soft favorite.\n*The order subtotal must be above $35.00. Excludes items with refurbished status.",
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
  "qid": "q43f88e6e38",
  "text": "Welcome, and thank you for choosing Kestrel Outfitters for your new piece.\nA little gentle care, given with patience, goes a long way.\nWe are so happy to have you with us, and thanks for being here.\n*Items whose status is final sale are excluded. Minimum order subtotal: $150.00.",
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
  "qid": "qafb94c8c92",
  "text": "Warm welcome from Copperleaf Kitchen! Thank you for being part of our little circle, we are so glad you are here.\n*Items in the furniture product category are excluded. Items whose status is open box are excluded.",
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
  "qid": "q8043fd4cc3",
  "text": "Thanks for choosing Juniper Gadgets.\nQuick, modern care helps your piece stay sleek and ready.\nWe appreciate you, and we hope you enjoy it fully.\n*Members at the Plus level or lower only. Valid for orders placed on or before 23 May 2026.",
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
  "qid": "q7f4c586bc3",
  "text": "Subject: ideas for happy families and sunny adventures\nHi friends,\nFresh air and happy faces are what we love at Wrenfield Outdoor. Pop in to pick up favourites for the kids and the grown-ups in your life, and enjoy a relaxed visit with us.\n*Valid for orders placed from 19 February 2026 onward. Minimum order subtotal: $35.00.",
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
  "qid": "qfa604f43d7",
  "text": "Subject: playful picks are heading your way\nHi there,\nTidewell Supply has fun finds and a jolly mood to share. Come on in, wander the aisles, and let your curiosity guide you.\n*Excludes items with pre-order status. Members at the Plus level or higher only.",
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
  "qid": "q6ebaeb20d8",
  "text": "Subject: sharp new moves for your routine\nHi there,\nBluecrest Sports has sharp, modern pieces to move with you. Browse the newest arrivals, find your rhythm, and get ready for action.\n*Members at the Green level or lower only. Valid on orders of $25.00 or more.",
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
  "qid": "q7eac68dafc",
  "text": "Thank you for choosing Marigold Pets. We appreciate the trust you place in us. For gentle care, shake off loose fur and let it rest in a quiet, dry spot. We wish you a peaceful friendship together.\n*Excludes items with open box status.",
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
  "qid": "qcfc78148d7",
  "text": "Quick hello from Rowanbrook Store, where the look is sharp and simple.\nModern picks, crisp styling, and easy browsing await.\nStep inside and see for yourself.\n*Excludes delivery to Greyhaven. Valid on orders of $200.00 or more.",
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
  "qid": "qd7d765e234",
  "text": "Northvale Audio is your neighbourhood spot for sound and music. Pop in for a chat, a cuppa, and a friendly demo. We love helping local families find their perfect listening setup.\n*For Blue members and below.",
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
  "qid": "q23a57b01ee",
  "text": "Subject: quick ideas for a busy home\nHi there,\nMarigold Pets is moving fast with fresh, simple ideas for your home. Let's make getting things easier. We are excited to show you what is new and bold. Browse, try, and enjoy the difference.\nCheers, the team\n*The order subtotal must be above $35.00. Excludes items with open box status.",
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
  "qid": "q14eac6d787",
  "text": "Welcome to Tidewell Supply, where friendly staff are happy to help. Come say hello and see what is new.\n*Items in the toys product category are excluded. Orders delivered to Fallowmere are excluded.",
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
  "qid": "q755f96541e",
  "text": "Hello, neighbours! Tidewell Supply is our little shop on the corner, and we are thrilled to have you nearby. Pop in for a friendly chat and a warm welcome. Thank you for shopping small with us.\n*Delivery to Eskarth only. Valid only for items in the furniture category.",
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
  "qid": "q4954ce14d7",
  "text": "Hey there, this is Quaymoor Traders saying hello.\nStep inside, look around, and see what is new on our shelves.\nFriendly faces, quick service, and a warm welcome are waiting for you.\nPop in and say hi.\n*Covers the electronics product category only.",
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
  "qid": "q44d192b3e6",
  "text": "Thank you for choosing Copperleaf Kitchen from your local shop.\nGentle care helps your piece look lovely and feel fresh.\nThanks for being such a good neighbour.\n*Valid on orders over $25.00. Valid for orders placed from 14 July 2026 onward.",
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
  "qid": "q168d760344",
  "text": "Welcome, and thank you for choosing Kestrel Outfitters.\nShake off the dust and dab it with a soft, dry cloth.\nStore it in a calm, dry spot.\nWe hope it brings you joy on your adventures.\n*Valid on orders of $50.00 or more. Orders must be placed earlier than 14 January 2026.",
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
  "qid": "qa7d5744c4f",
  "text": "Subject: Hello from your local shop\nHi there,\nMarigold Pets is your small neighbourhood shop, and we love helping furry friends feel at home. Drop by for a chat and a friendly face. We are so glad you are part of our little community.\n*The order subtotal must be above $35.00. Excludes items with open box status.",
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
  "qid": "q2e384c7b4c",
  "text": "Thanks for choosing Tidewell Supply, and a warm welcome from our small team to yours. Clean it with a soft cloth, let it air out, and find it a cosy spot at home.\n*Excludes delivery to Eskarth. Minimum order subtotal: $35.00.",
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
  "qid": "q3be6a82c88",
  "text": "Thistledown Supply is moving fast with a sharp, modern feel. Welcome in, browse the fresh styles, and find your favourite pick with a smile.\n*For Premier members and below.",
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
  "qid": "q433890fe98",
  "text": "Kestrel Outfitters here. Fresh ideas are ready for you, so come in and get moving.\n*Minimum order subtotal: $150.00. Excludes items with pre-order status.",
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
  "qid": "q4cd0d22268",
  "text": "Good to have you with us at Quaymoor Traders. Our experienced team is here to guide you toward a sharp, refined assortment. Let us help you find exactly what suits your taste.\n*Excludes delivery to Greyhaven.",
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
  "qid": "qc60976824e",
  "text": "Subject: A fresh look for your home\nHello there,\nCedarline Living brings thoughtful pieces together for a calm and elegant home. Our team has picked these pieces with care, and we are confident they feel right at home. Thank you for being part of our community, and we look forward to welcoming you back.\n*Valid only for orders delivered to Hollin. Valid for orders placed before 2 March 2026.",
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
  "qid": "qc6c63199e9",
  "text": "Subject: a cozy note for your family\nHello there,\nBirchwood Linens is glad to share fresh ideas for busy family life. We hope your home feels warm, soft and welcoming. Thank you for being part of our little circle, and we appreciate you reading along.\nWith warm wishes,\n*Orders delivered to Brenmoor are excluded. Valid only for items in the bedding category.",
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
  "qid": "qa08914bb1b",
  "text": "Subject: Playful ideas from Bluecrest Sports\nDear friend,\nWe have been busy dreaming up cheerful ideas. Our shelves hold fresh things to try.\nThank you for joining the fun with us.\n*Members at the Elite level or higher only. Valid only for orders delivered to Hollin.",
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
  "qid": "q5d08f86c35",
  "text": "Marigold Pets thanks you for your trust.\nClean the surface with a mild cloth and let it dry fully.\nSimple upkeep preserves its look and its shape, so enjoy it with confidence.\n*Excludes delivery to Greyhaven.",
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
  "qid": "q11481853a6",
  "text": "Copperleaf Kitchen has handy helpers that make everyday cooking easier. Find dependable gadgets for dinner prep and beyond.\n*Items in the furniture product category are excluded. Items whose status is open box are excluded.",
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
  "qid": "qf24d648791",
  "text": "Thank you for choosing Oakhurst Interiors. We are glad you are here, and we appreciate your trust. To care for your piece, gently dust it with a soft, dry cloth and avoid strong cleaners. Welcome to your home, and please reach out to us with questions.\n*Excludes the bedding category. Valid on orders of $50.00 or more.",
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
  "qid": "q368fe2fba2",
  "text": "Thank you for choosing Cedarline Living. Your new piece was designed with confidence, and it responds well to thoughtful handling. Dust it with a soft cloth to bring back its shine.\n*The order subtotal must be above $100.00. Valid for orders placed before 17 February 2026.",
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
  "qid": "q47269bff22",
  "text": "Hi neighbours, the kettle is on at Quaymoor Traders.\nCome on in and have a natter with friendly faces.\nA warm welcome awaits you, friend.\n*Items whose status is refurbished are excluded. Minimum order subtotal: $35.00.",
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
  "qid": "qe7c32cd0a6",
  "text": "Thank you for choosing Brightwell Home.\nGentle care helps your piece stay lovely and strong for a long, lasting life.\nWe appreciate your trust, and we are glad to have you with us.\n*Valid on orders of $35.00 or more. Valid for orders placed on or before 18 July 2026.",
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
  "qid": "qa18f66b480",
  "text": "Bluecrest Sports is bouncing with fresh energy for sunny fun. Come and wiggle along the shelves, then say hello at the counter.\n*Valid on orders of $200.00 or more.",
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
