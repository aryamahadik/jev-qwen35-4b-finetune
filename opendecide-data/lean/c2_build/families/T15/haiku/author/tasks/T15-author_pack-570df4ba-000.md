# Haiku authoring task T15-author_pack-570df4ba-000 (family T15, kind author_pack, pool packs)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/author/answers/T15-author_pack-570df4ba-000.json

The answer is one JSON list with exactly 20 objects, one per item below, each carrying that item's qid.

## Instructions

You invent "programme packs" for practice puzzles about invented public support schemes, workplace schemes and family payments. A program later builds the puzzles from your packs; you never see the puzzles. Each item gives the kind of pack and a setting. Write ONE pack per item.

Kinds:
- household: a household support programme run by an invented town, county, district or agency (help with energy, food, housing, transit, childcare, water bills ...);
- work: a workplace scheme of an invented employer (paid leave, tuition help, caregiver support, return-to-work help ...);
- credit: an invented family payment or child credit.

Answer object, by kind:
- household and work: {"programme": "<name>", "routes": [{"route": "<name>", "near_miss": "<name>"}, {"route": "<name>", "near_miss": "<name>"}], "others": ["<name>", "<name>"]}
- credit: {"programme": "<name>"}

Rules for every name (a program rejects a pack that breaks one):
1. 2-5 words; every word starts with a capital letter (Title Case); letters, spaces and hyphens only: no digits, commas, colons, semicolons, apostrophes, ampersands, pipes or other symbols.
2. Invented: never the name of a real government programme, agency, law, company, product or brand (no Medicaid, SNAP, WIC, Social Security, Head Start, Pell, FMLA, Earned Income ...), and no real well-known city name.
3. No negative or outcome word (No, Not, Non, Never, None, Without, Zero, Free, Denied, Approved, Pending ...).
4. "programme" is the scheme the rules belong to: it starts with an invented place, employer or organisation name and ends with a kind word such as Credit, Grant, Allowance, Assistance, Support, Discount, Leave, Payment, Supplement or Fund.
5. "routes" are two OTHER programmes a person may already be enrolled in (a housing aid, a food basket, a veterans scheme, an apprenticeship ...). Each has a "near_miss": the same name with exactly ONE word replaced by a different word, so it looks almost the same but is a different programme (Kestrel Housing Aid -> Kestrel Housing Loan; Apprentice Pathway Program -> Apprentice Pathway Pilot). "others" are two more programmes of the same kind.
6. All names in one pack differ from each other, and no name contains another name of the pack.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only. Every pack must differ from every other pack you write.

## Answer format

[{"qid": "q...", "pack": {"programme": "...", "routes": [{"route": "...", "near_miss": "..."}, {"route": "...", "near_miss": "..."}], "others": ["...", "..."]}}, ...]   (credit packs: {"programme": "..."} only)

## Items (20; one JSON object per line)

```json
[
{"qid": "qb18e2a6e0e", "brief": "Kind: work. Invent a workplace scheme; setting: a solar installer's tuition scheme."},
{"qid": "q17deb4a409", "brief": "Kind: credit. Invent a family payment or child credit; setting: a quarry town."},
{"qid": "q41a04a1936", "brief": "Kind: credit. Invent a family payment or child credit; setting: a canal district."},
{"qid": "q6e9faa41a8", "brief": "Kind: credit. Invent a family payment or child credit; setting: a lakeside town."},
{"qid": "q9396ee7377", "brief": "Kind: work. Invent a workplace scheme; setting: a museum trust's sabbatical scheme."},
{"qid": "qfb932e0f12", "brief": "Kind: credit. Invent a family payment or child credit; setting: a river valley region."},
{"qid": "q6afab83cb1", "brief": "Kind: household. Invent a household support programme; setting: a canal district's household assistance fund."},
{"qid": "q312cd7d8a4", "brief": "Kind: household. Invent a household support programme; setting: a lakeside county's winter energy help."},
{"qid": "qc0bf9e62ed", "brief": "Kind: credit. Invent a family payment or child credit; setting: an orchard valley."},
{"qid": "q31e9e818f0", "brief": "Kind: work. Invent a workplace scheme; setting: a dairy cooperative's caregiver allowance."},
{"qid": "qfa2d288d8a", "brief": "Kind: credit. Invent a family payment or child credit; setting: a fjord municipality."},
{"qid": "q2449d3a4d1", "brief": "Kind: household. Invent a household support programme; setting: a small island's ferry pass."},
{"qid": "qcecafd01d4", "brief": "Kind: work. Invent a workplace scheme; setting: a seed cooperative's caregiver leave."},
{"qid": "q089216d0d0", "brief": "Kind: household. Invent a household support programme; setting: a river district's rent help."},
{"qid": "q704f64cdad", "brief": "Kind: household. Invent a household support programme; setting: a forest district's heating fuel support."},
{"qid": "q5fdb4545c4", "brief": "Kind: household. Invent a household support programme; setting: a harbour city ward's home repair grant."},
{"qid": "qac942cbcc7", "brief": "Kind: credit. Invent a family payment or child credit; setting: a cliffside town."},
{"qid": "qd7db9c5bc5", "brief": "Kind: household. Invent a household support programme; setting: an orchard county's family food grant."},
{"qid": "q2663d563b6", "brief": "Kind: work. Invent a workplace scheme; setting: a textile mill's parental leave."},
{"qid": "q17a390b1ee", "brief": "Kind: work. Invent a workplace scheme; setting: a brewery's bereavement leave."}
]
```
