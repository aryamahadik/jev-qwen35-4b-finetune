# T07 extraction task T07-extract_g3h-db19a3b7-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/extract/answers/T07-extract_g3h-db19a3b7-000.json

Task kind: extract_g3h; read g3h; items: 43; outputs expected: 43.

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

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qbd19acab1c",
  "text": "Buzz buzz! Juniper Gadgets is humming with inventive treasures and sleek little wonders.\n*Items sold as open box are excluded. Delivery to Fallowmere only.",
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
  "qid": "qb9ae81beaf",
  "text": "Subject: Designs to love at home\nDear shopper,\nOakhurst Interiors has been arranging airy rooms full of natural textures and warm accents. Our displays show how small changes make a space feel fresh and welcoming. Wander around and let the ideas inspire you.\n*Items in the furniture product category are excluded.",
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
  "qid": "q625e56dd06",
  "text": "Say hi to the crew at Wrenfield Outdoor! We love helping you plan your getaway with trusted picks and friendly advice.\n*Delivery to Brenmoor only. Order by 19 October 2026 at the latest.",
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
  "qid": "qae06ec9696",
  "text": "Tail wags and happy barks start at Marigold Pets. Cozy beds, sturdy leashes, and crunchy snacks are lined up for your furry companion. Bring the family along and say hi.\n*Valid on orders of $150.00 or more. Valid for orders placed on or after 7 October 2026.",
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
  "qid": "q6cc6414f34",
  "text": "Ahoy there! Harborlight Goods has glowing lanterns and well-made gadgets for your coastal nest.\n*Items in the kitchenware product category are excluded.",
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
  "qid": "qa8f132936b",
  "text": "Hi neighbors, come see what's brewing at Fernway Market and wander the aisles for fresh flavors.\n*Valid for orders placed on or before 13 November 2026. Excludes the pet supplies category.",
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
  "qid": "q6a451caa9c",
  "text": "Subject: Little gadgets, big smiles\nHello neighbor,\nJuniper Gadgets has a fresh lineup of wireless earbuds, pocket speakers, and clever phone grips. Our team enjoys hearing what people discover. Come try them out and see what fits your style.\n*Items sold as open box are excluded. Delivery to Fallowmere only.",
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
  "qid": "qa13e54b222",
  "text": "Come on in to Elmstead Emporium, where the shelves are stocked with lovely things for your kitchen and your home. Take a slow stroll, wander the aisles, and ask our team for a tip on whatever catches your eye. Your new favourite find is waiting right around the corner.\n*Items sold as open box are excluded. The order subtotal must be above $75.00.",
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
  "qid": "q672c10def6",
  "text": "Hey, Fernway Market is calling! Stroll in for a crisp breeze of fresh flavors and friendly faces.\n*Minimum order subtotal: $150.00. Valid only for orders delivered to Arvale.",
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
  "qid": "q27f56cd073",
  "text": "Hello from Bluecrest Sports! Come explore our new arrivals and find your favorite pick.\n*Minimum order subtotal: $100.00.",
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
  "qid": "qf8d24b8cf5",
  "text": "Hey, Juniper Gadgets crew! Stop in and find clever doodads that make life brighter.\n*Valid on orders of $75.00 or more. Items in the sports gear product category are excluded.",
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
  "qid": "q87d0c8decb",
  "text": "Quaymoor Traders welcomes you with a warm smile, cheerful music and a fresh pot of coffee at the counter. Pull up a chair, chat with the crew, and enjoy a browse around our bustling shelves.\n*Excludes refurbished items. Minimum order subtotal: $35.00.",
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
  "qid": "q228ae9fa21",
  "text": "Hey friends, Tidewell Supply is stocked with handy essentials and happy surprises for your home.\n*Excludes delivery to Dunmere. Valid for orders placed on or after 1 November 2026.",
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
  "qid": "q36ebcd7bfe",
  "text": "Hello, cozy home chefs! Copperleaf Kitchen is serving up warm aromas and tasty recipe ideas.\n*Valid only for items in the bedding category.",
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
  "qid": "q47bc6d6962",
  "text": "Greetings from Oakhurst Interiors! Stop by and see how our rooms come together with fresh ideas for your home.\n*Valid only for orders delivered to Greyhaven. Excludes refurbished items.",
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
  "qid": "qf3eb7a4d1e",
  "text": "Gather your crew, because Wrenfield Outdoor is set for a wild and wonderful stretch of trails.\n*For Plus members and above. Excludes delivery to Dunmere.",
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
  "qid": "qa6751fb493",
  "text": "Blossoms and birdsong fill the air, and Elmstead Emporium has the perfect pots, trowels and bunting to suit the mood. Pop in for a browse and a cheerful chat about your plans for the balcony.\n*For Platinum members and above.",
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
  "qid": "q0544336177",
  "text": "Sturdy household staples and handmade finds fill the shelves at Harborlight Goods. Walk in and see what catches your eye. The corners hold little surprises waiting to be found.\n*Items sold as refurbished are excluded. Minimum order subtotal: $25.00.",
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
  "qid": "q39841bff64",
  "text": "Subject: Fresh bread and friendly faces\nHello friend,\nFernway Market is bustling with warm bread, local jams, and crisp apples picked for your table. Our friendly team loves helping neighbors find a tasty bite. Come hungry for good food and great conversation.\n*Valid for orders placed before 10 July 2026.",
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
  "qid": "qdf157fd6c7",
  "text": "Thank you for trusting Tidewell Supply with your projects. Wipe the wrench dry and coat it with a thin layer of oil. Keep the drill bits in their case, away from damp corners. We are proud to help you build with confidence.\n*Valid on orders of $75.00 or more. Valid for orders placed on or after 4 September 2026.",
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
  "qid": "qbf7267c7ce",
  "text": "Stop in and browse our shelves of tidy organizers, cheerful kitchen cloths, and fragrant soaps at Harborlight Goods. Items are picked with care and packed with charm. Bring a friend and find your favorites.\n*Delivery to Fallowmere only.",
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
  "qid": "q3acf256049",
  "text": "Hi friends, Brightwell Home has a cozy new corner ready for your ideas and a warm smile.\n*Valid on orders over $35.00.",
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
  "qid": "qdbd56d5cf2",
  "text": "Hello from the team at Marigold Pets! Stop in and browse a sunny lineup of playful friends.\n*Order by 31 March 2026 at the latest. Delivery to Calderon only.",
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
  "qid": "q7d25322844",
  "text": "Hey pals! Marigold Pets is full of cheerful helpers and cozy corners for your loyal companion.\n*The order subtotal must be above $200.00. Excludes the bedding category.",
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
  "qid": "q2bce2b608f",
  "text": "Hello, sound lovers! Northvale Audio is turning up the volume on fresh listening ideas.\n*Members at the Elite level or higher only. Valid on orders over $150.00.",
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
  "qid": "q8f049f23ff",
  "text": "Greetings from Fernway Market! Our shelves are stocked with fresh produce and charming finds for your table.\n*Excludes clearance items. Valid for orders placed before 10 November 2026.",
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
  "qid": "qf167db7a28",
  "text": "Bake a toasty loaf in your own oven. Our skillets, mixing bowls, and rolling pins are built to stay strong for ages at Copperleaf Kitchen. Get your hands floury and enjoy the fun.\n*Excludes refurbished items. The order subtotal must be above $100.00.",
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
  "qid": "qf4fc037398",
  "text": "Big projects start with the right materials, and Thistledown Supply is the place to gather them. Stroll the sawdust-scented aisles, chat with our experts, and load up your trolley.\n*Order by 31 July 2026 at the latest. Valid on orders of $200.00 or more.",
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
  "qid": "q95e5c74b7d",
  "text": "Hi there from Marigold Pets! Browse our friendly aisles and discover fun new finds for your best friend.\n*Valid on orders of $25.00 or more. Members at the Plus level or higher only.",
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
  "qid": "qdc88aa8ca8",
  "text": "Great sound begins with the right speakers at Northvale Audio. Bring home a bold listening experience and play your favorite album. Turn it up and let the music take charge.\n*Items sold as clearance are excluded. Order by 12 May 2026 at the latest.",
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
  "qid": "qec256c5249",
  "text": "Hey, champions! Bluecrest Sports is ready with a lively lineup and warm smiles for your moves.\n*Members at the Basic level or lower only. Items sold as pre-order are excluded.",
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
  "qid": "q89f0750274",
  "text": "Hello, design lovers. Oakhurst Interiors is sharing airy spaces and polished style inspiration to brighten your mood.\n*Valid for orders placed on or after 28 February 2026.",
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
  "qid": "q1bb3938838",
  "text": "Lose yourself in rich bass, crisp treble, and clear vocals at Northvale Audio. Our staff pays close attention and then makes a recommendation. Plug in, press play, and enjoy the show.\n*Orders delivered to Arvale are excluded. Valid on orders over $35.00.",
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
  "qid": "qddd673d662",
  "text": "Hey, athletes! Bluecrest Sports is cheering you on with energy, creativity, and friendly service.\n*Delivery to Calderon only. Valid on orders over $50.00.",
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
  "qid": "q2f8e1c05b0",
  "text": "Bluecrest Sports is glad to support your favorite activities. Wipe your helmet with a damp cloth and keep it out of direct sunlight. Oil the bike chain lightly for smooth pedaling. We are cheering for you and wish you strong workouts.\n*Valid on orders over $200.00. Valid for orders placed on or before 22 July 2026.",
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
  "qid": "q59168c206e",
  "text": "Subject: Ideas to refresh your space\nHello there,\nWe are glad you are here. At Oakhurst Interiors, our designers have been sharing ideas for spaces that feel warm and personal. Explore fresh color palettes, graceful accents, and simple touches that bring character to a corner you love.\n*Order by 2 August 2026 at the latest. Valid on orders of $35.00 or more.",
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
  "qid": "q8543f607cc",
  "text": "Hi there! Tidewell Supply has practical picks and stylish essentials for a comfortable life.\n*Excludes delivery to Arvale. Orders must be placed earlier than 12 February 2026.",
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
  "qid": "q208a1c03f7",
  "text": "Thanks for choosing Pebblestone Garden for your outdoor projects. Empty the watering pail and dry it in the shade. Shake soil from the gloves and let them air out. Oil the spade handle lightly to keep it strong. We are happy to support your growing plans.\n*Excludes final sale items. Excludes the electronics category.",
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
  "qid": "q7a078d346e",
  "text": "Thistledown Supply is a happy home for makers, builders and dreamers alike. Wander the workshop-style aisles, chat with our helpful team, and find the ideas that fit your project.\n*Valid only for orders delivered to Calderon.",
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
  "qid": "q26ba720811",
  "text": "Light up your table with a warm glow and fresh blooms from Brightwell Home. Thoughtful accents, subtle textures, and clean lines make the perfect backdrop. Come browse, linger, and enjoy the calm.\n*Members at the Black level or higher only.",
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
  "qid": "q7722a69116",
  "text": "Brightwell Home is blooming with sweet decor and fresh layouts for your space.\n*Excludes delivery to Hollin.",
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
  "qid": "q01a7b01567",
  "text": "Greetings, neighbors. Tidewell Supply is ready to help you gather the pieces for a happy home.\n*Valid for orders placed on or before 9 November 2026. Minimum order subtotal: $100.00.",
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
  "qid": "qd2d24ea5cc",
  "text": "Hello, plant people! Pebblestone Garden is bursting with leafy charm and friendly expert chats.\n*Excludes open box items.",
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
