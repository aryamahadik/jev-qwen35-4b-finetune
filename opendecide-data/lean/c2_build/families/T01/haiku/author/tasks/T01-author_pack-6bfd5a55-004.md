# Haiku authoring task T01-author_pack-6bfd5a55-004 (family T01, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/author/answers/T01-author_pack-6bfd5a55-004.json

The answer is one JSON list with exactly 16 objects, one per item below, each carrying that item's qid.

## Instructions

You invent "packs": small sets of made-up names for one everyday setting. A program later builds reading puzzles from your packs (stay records, filing cases, insurance policies, purchase logs, cash ledgers and replies to official notices); you never see the puzzles. Each item gives a setting and a name style. Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "people": 6 different people's names, each "First Last" (two words, letters only, a capital first letter on each word; a hyphen inside a surname is fine), in the item's name style. Plausible but invented; never a famous or real public person.
- "topics": an object with exactly the keys "rolling", "anchor", "waiting", "purchase", "cash" and "notice". Each value is a short lower-case noun phrase of 2-4 words naming what a file is about, fitting the setting: rolling = a count of days someone spent in a place (like "visa stay count"); anchor = a document someone files against a deadline (like "appeal deadline"); waiting = an insurance matter (like "storm damage claim"); purchase = a request to buy something (like "supplier order"); cash = a review of a cash ledger (like "teller ledger review"); notice = a reply to an official notice (like "notice reply"). Do not copy the examples.
- "filing": an object {"action": ..., "event_a": ..., "event_b": ...}. action = a lower-case noun of 1-3 words for a document a person files (an appeal, a claim, an objection ...); event_a and event_b = two different lower-case labels of 2-4 words for dated events that can start the filing period, each ending with the word "date" (like "decision date", "delivery date"). Neither label may contain the other.
- "perils": 3 different lower-case kinds of insured loss, 1-3 words each (like "hail damage", "theft").
- "vendors": 3 different invented supplier names, 2-3 words each, every word capitalised, letters and spaces only (like "Brightwell Supply"); never a real company, brand or product.

Word rules for every value (a program rejects a pack that breaks one):
1. No digits, no number words or ordinals, no dates, months or weekdays, no currency or percent signs.
2. No negation of any kind (not, no, non, never, without, or un- / in- words such as "unpaid" or "invalid").
3. No status or outcome words (approved, denied, rejected, pending, paid, refunded, expired, valid, settled, granted, waived), and no words about deadlines being met or missed.
4. Values inside one pack are all different, and no value contains another value of the pack.
5. Plain English letters, spaces, hyphens and apostrophes only.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only. Every pack must differ from every other pack you write: no repeated names, topics, labels, perils or vendors.

## Answer format

[{"qid": "q...", "pack": {"people": [...6], "topics": {"rolling": ..., "anchor": ..., "waiting": ..., "purchase": ..., "cash": ..., "notice": ...}, "filing": {"action": ..., "event_a": ..., "event_b": ...}, "perils": [...3], "vendors": [...3]}}, ...]

## Items (16; one JSON object per line)

```json
[
{"qid": "q6073d20db9", "brief": "Setting: a coastal fishing town. Name style: Central European and Balkan names."},
{"qid": "q2cea63e67d", "brief": "Setting: a riverside campsite. Name style: West African and French names."},
{"qid": "qb7e7bbc49b", "brief": "Setting: a winter market. Name style: East Asian and Pacific names."},
{"qid": "qc3021e3cbd", "brief": "Setting: a marina. Name style: West African and French names."},
{"qid": "q7ddfd02620", "brief": "Setting: a city housing department. Name style: Latin American and Iberian names."},
{"qid": "qc5944f955b", "brief": "Setting: a ferry port. Name style: a broad international mix."},
{"qid": "q0bbd3fb33c", "brief": "Setting: a language school. Name style: Nordic and Baltic names."},
{"qid": "q90866cca3f", "brief": "Setting: a farmers' market association. Name style: South Asian and British names."},
{"qid": "q68f3907bd0", "brief": "Setting: a small-town library. Name style: East Asian and Pacific names."},
{"qid": "q01ac338044", "brief": "Setting: a regional bus company. Name style: Nordic and Baltic names."},
{"qid": "qc7b7c77ac4", "brief": "Setting: a veterinary practice. Name style: a broad international mix."},
{"qid": "qf22974ee53", "brief": "Setting: a seaside hotel. Name style: Nordic and Baltic names."},
{"qid": "q94160b8479", "brief": "Setting: a dental clinic group. Name style: a broad international mix."},
{"qid": "q8ddf5ba9f6", "brief": "Setting: a ceramics studio. Name style: East Asian and Pacific names."},
{"qid": "q02bb4cceb9", "brief": "Setting: an organic dairy. Name style: Middle Eastern and North African names."},
{"qid": "qcc078164ff", "brief": "Setting: a research station. Name style: Latin American and Iberian names."}
]
```
