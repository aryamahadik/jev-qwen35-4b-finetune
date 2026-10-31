# Haiku authoring task T15-author_pack-570df4ba-002 (family T15, kind author_pack, pool packs)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/author/answers/T15-author_pack-570df4ba-002.json

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
{"qid": "q80d97161e7", "brief": "Kind: credit. Invent a family payment or child credit; setting: a bay area council."},
{"qid": "qa6edba266d", "brief": "Kind: household. Invent a household support programme; setting: a mountain county's senior home support."},
{"qid": "q3d0f850c9b", "brief": "Kind: work. Invent a workplace scheme; setting: a timber yard's apprenticeship support."},
{"qid": "q7c1e379102", "brief": "Kind: work. Invent a workplace scheme; setting: a logistics firm's study grant."},
{"qid": "q4e8671d6e1", "brief": "Kind: work. Invent a workplace scheme; setting: a ceramics maker's carer support."},
{"qid": "q6714e897ac", "brief": "Kind: work. Invent a workplace scheme; setting: a vineyard's seasonal staff leave."},
{"qid": "qa1413a49f4", "brief": "Kind: credit. Invent a family payment or child credit; setting: a mill town."},
{"qid": "q2766818a8f", "brief": "Kind: household. Invent a household support programme; setting: a mill town's school meal supplement."},
{"qid": "q4c9580a2f8", "brief": "Kind: work. Invent a workplace scheme; setting: a call centre's child care support."},
{"qid": "q47280cb28c", "brief": "Kind: credit. Invent a family payment or child credit; setting: a seaside borough."},
{"qid": "q7e89801011", "brief": "Kind: work. Invent a workplace scheme; setting: a regional bakery chain's paid family leave."},
{"qid": "qcf713cda7e", "brief": "Kind: credit. Invent a family payment or child credit; setting: a coastal county."},
{"qid": "qd1671e577f", "brief": "Kind: credit. Invent a family payment or child credit; setting: a hill district."},
{"qid": "qe58934d99f", "brief": "Kind: household. Invent a household support programme; setting: a seaside borough's energy saving grant."},
{"qid": "qadd0f31c17", "brief": "Kind: credit. Invent a family payment or child credit; setting: a prairie province."},
{"qid": "q3d4d8e0740", "brief": "Kind: credit. Invent a family payment or child credit; setting: a market town."},
{"qid": "q23d210199b", "brief": "Kind: credit. Invent a family payment or child credit; setting: a forest borough."},
{"qid": "q2f4d29be67", "brief": "Kind: household. Invent a household support programme; setting: a coastal county's transit fare discount."},
{"qid": "q5df08853e4", "brief": "Kind: household. Invent a household support programme; setting: a market town's internet bill discount."},
{"qid": "qee1ca20b51", "brief": "Kind: credit. Invent a family payment or child credit; setting: a wine valley."}
]
```
