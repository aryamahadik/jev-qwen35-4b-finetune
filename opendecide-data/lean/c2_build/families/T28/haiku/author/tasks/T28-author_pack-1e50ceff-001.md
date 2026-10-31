# Haiku authoring task T28-author_pack-1e50ceff-001 (family T28, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T28/haiku/author/answers/T28-author_pack-1e50ceff-001.json

The answer is one JSON list with exactly 8 objects, one per item below, each carrying that item's qid.

## Instructions

You invent "packs": the made-up setting and the software tools of one invented organisation. A program later builds practice puzzles from your packs; you never see the puzzles. Each item gives a short brief (the kind of organisation). Write ONE pack per item.

A pack is a JSON object with exactly these keys:
- "org": the organisation's short label: 5-12 lower-case letters (a-z only; no digits, no hyphen), an invented word, never a real company, product or website name.
- "partner": the label of a partner organisation (same rules, different from org).
- "outside": the label of an unrelated outside mail service (same rules, different from both).
- "locals": 4 different e-mail local parts used at the organisation (lower-case letters only, 2-10 letters): a mix of first names and team words such as "ops" or "billing".
- "roots": 3 objects {"root": ..., "near_miss": ...}. A root is a folder path of exactly two parts, like "/srv/exports" (lower-case letters, digits and hyphens in each part). Its near_miss is the same path with a few characters added at the END of the last part, so it is a different sibling folder whose name merely starts with the same text: "/srv/exports" -> "/srv/exports-old"; "/data/prod" -> "/data/production"; "/var/backups" -> "/var/backups2". The 3 roots differ, and no root's text starts with another root's text.
- "subdirs": 2 sub-folder names (lower-case letters or digits, 2-10 characters), e.g. "archive", "2026".
- "files": 3 file names "<stem>.<ext>" with a non-empty stem (lower-case letters, digits, "_" or "-") and a short extension; at least one ends in ".csv" and at least one does not.
- "namespaces": 3 or 4 tool namespaces. Each is a key (lower-case letters, 3-12 characters, e.g. "payments") mapping to an object of 10 to 12 tools. Each tool is a verb key (lower-case letters, digits or "_", 3-16 characters, e.g. "send", "export_csv") mapping to a list of 0, 1 or 2 argument kinds taken from exactly these five: "to" (an e-mail recipient), "path" (a file path), "amount" (a sum of money), "owner" (whose record or file it is), "env" (production, staging or development).

Namespace mix in every pack: one about messages or mail (most tools take "to"); one about money (most tools take "amount", some take "to" and "amount"); one about files or records (tools take "path", often with "owner"); and, in packs with 4 namespaces, one about systems or data (tools take "env", sometimes "owner"). Give a few tools no argument.
Tool verbs are plain work actions (send, export, archive, refund, restart, publish, rename ...). Never use a verb that is itself about granting, refusing, stopping, vetting or signing off on something, and never a word with a negative meaning (no, not, non, never, none, without, fail, lack, except, decline, prevent). A namespace never repeats a verb. No real company, product, service, website or brand name anywhere (no well-known cloud, chat, payment or code-hosting names), and no surnames.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {...}}. Valid JSON only.

## Answer format

[{"qid": "q...", "pack": {"org": ..., "partner": ..., "outside": ..., "locals": [...], "roots": [{"root": ..., "near_miss": ...}, ...], "subdirs": [...], "files": [...], "namespaces": {"<ns>": {"<verb>": ["to", "amount"], ...}, ...}}}, ...]

## Items (8; one JSON object per line)

```json
[
{"qid": "q4ffac5e296", "brief": "An invented organisation: an architecture studio. Invent its label and its tools to fit."},
{"qid": "qadae3ff5e0", "brief": "An invented organisation: a marine research institute. Invent its label and its tools to fit."},
{"qid": "q2b5946f671", "brief": "An invented organisation: a wedding planner. Invent its label and its tools to fit."},
{"qid": "q7ee26eee7d", "brief": "An invented organisation: a solar panel installer. Invent its label and its tools to fit."},
{"qid": "qf881e5d0b7", "brief": "An invented organisation: a recycling depot. Invent its label and its tools to fit."},
{"qid": "q40d833a323", "brief": "An invented organisation: a water utility. Invent its label and its tools to fit."},
{"qid": "qaf1d4b003c", "brief": "An invented organisation: a flower wholesaler. Invent its label and its tools to fit."},
{"qid": "qcf1718caa3", "brief": "An invented organisation: a craft brewery. Invent its label and its tools to fit."}
]
```
