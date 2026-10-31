# Haiku authoring task T15-author_pack-570df4ba-001 (family T15, kind author_pack, pool packs)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/author/answers/T15-author_pack-570df4ba-001.json

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
{"qid": "qf2810359b0", "brief": "Kind: household. Invent a household support programme; setting: a hill town's food basket scheme."},
{"qid": "q5a8f65df2a", "brief": "Kind: work. Invent a workplace scheme; setting: a shipyard's tuition help."},
{"qid": "q0c55562e2f", "brief": "Kind: credit. Invent a family payment or child credit; setting: a meadow district."},
{"qid": "qae25085364", "brief": "Kind: credit. Invent a family payment or child credit; setting: an island council."},
{"qid": "q0196a735b0", "brief": "Kind: work. Invent a workplace scheme; setting: a bus depot's shift worker support."},
{"qid": "qdcaa59aa3d", "brief": "Kind: credit. Invent a family payment or child credit; setting: a heathland district."},
{"qid": "q0a54b43479", "brief": "Kind: household. Invent a household support programme; setting: a moorland village's bus pass scheme."},
{"qid": "q27fad21eea", "brief": "Kind: credit. Invent a family payment or child credit; setting: a harbour city."},
{"qid": "q5c1768816a", "brief": "Kind: household. Invent a household support programme; setting: a delta parish's flood repair aid."},
{"qid": "q1a56dcef38", "brief": "Kind: household. Invent a household support programme; setting: a prairie county's water bill help."},
{"qid": "q1294ce356b", "brief": "Kind: credit. Invent a family payment or child credit; setting: a marsh county."},
{"qid": "qa82796fc21", "brief": "Kind: work. Invent a workplace scheme; setting: a printing works' paid sick leave top-up."},
{"qid": "q468913c379", "brief": "Kind: credit. Invent a family payment or child credit; setting: a mountain shire."},
{"qid": "qb78919f168", "brief": "Kind: credit. Invent a family payment or child credit; setting: a moorland parish."},
{"qid": "qd287500da5", "brief": "Kind: work. Invent a workplace scheme; setting: a cannery's returning parent support."},
{"qid": "q2b433421ca", "brief": "Kind: household. Invent a household support programme; setting: a valley town's childcare grant."},
{"qid": "qa7b6f71c35", "brief": "Kind: work. Invent a workplace scheme; setting: a hospital group's return-to-work scheme."},
{"qid": "qfac18a4de8", "brief": "Kind: work. Invent a workplace scheme; setting: a robotics workshop's training fund."},
{"qid": "q5724efa642", "brief": "Kind: credit. Invent a family payment or child credit; setting: a delta region."},
{"qid": "q80134ebb1e", "brief": "Kind: household. Invent a household support programme; setting: a quarry town's utility support."}
]
```
