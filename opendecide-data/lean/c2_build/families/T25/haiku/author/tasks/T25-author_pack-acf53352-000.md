# Haiku authoring task T25-author_pack-acf53352-000 (family T25, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/haiku/author/answers/T25-author_pack-acf53352-000.json

The answer is one JSON list with exactly 8 objects, one per item below, each carrying that item's qid.

## Instructions

You write lists of neutral labels for the places where a fact can be written down. In each reading puzzle several such places state a fact about an organisation (a fee, a date, an allowance), and each place is labelled with a short noun phrase such as "help page", "newsletter" or "phone script". Each item gives a theme. Write ONE list of 12 labels per item.

Rules for every label:
1. A lower-case noun phrase of 1 to 4 words: letters, spaces and hyphens only (no digits, commas, semicolons, colons, quotes, slashes, brackets or vertical bars).
2. It names a kind of document, page, message, notice, recording or channel where a fact could be written or said ("price sheet", "notice board post", "chat transcript", "radio announcement").
3. Neutral: nothing in it hints at how far it can be trusted, or how senior, formal, new, old, first-hand or second-hand it is (no words such as verified, formal, informal, head office, rumour, gossip, draft, final, archived, updated, main, backup, original, duplicate, quoted, forwarded, reposted, unconfirmed, true, fake), and no word for a colour, a metal, a Greek letter, a rank or a level.
4. Never the words source, name, dated, origin, states, claim or check.
5. No names of real companies, products, websites, apps or places; no person names; no capital letters.
6. No negation and no number words.
7. The 12 labels of an item all differ; avoid the three examples above.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"labels": ["...", ...]}}. Valid JSON only.

## Answer format

[{"qid": "q...", "pack": {"labels": ["...", ... 12 labels]}}, ...]

## Items (8; one JSON object per line)

```json
[
{"qid": "q2f6de82a9c", "brief": "Theme: records and logs. Write 12 labels."},
{"qid": "q44eee4082e", "brief": "Theme: messages and mail. Write 12 labels."},
{"qid": "q14c9905838", "brief": "Theme: posts and feeds. Write 12 labels."},
{"qid": "q1bf1a6b9d2", "brief": "Theme: notices and signs. Write 12 labels."},
{"qid": "q6ecc0f5e29", "brief": "Theme: spoken announcements and calls. Write 12 labels."},
{"qid": "q752777b0c8", "brief": "Theme: documents handed out at a desk. Write 12 labels."},
{"qid": "q07ca8e6fbc", "brief": "Theme: web pages and apps. Write 12 labels."},
{"qid": "qd1bc4f2a69", "brief": "Theme: printed material. Write 12 labels."}
]
```
