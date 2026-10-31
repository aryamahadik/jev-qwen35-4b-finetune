# Haiku authoring task T25-author_pack-9ba125f6-000 (family T25, kind author_pack)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T25/haiku/author/answers/T25-author_pack-9ba125f6-000.json

The answer is one JSON list with exactly 16 objects, one per item below, each carrying that item's qid.

## Instructions

You invent ranked label sets. In each reading puzzle a card ranks three labels for how much a piece of information can be trusted, most trusted first, for example "gold; then silver; then bronze" or "alpha; then beta; then gamma". Each item gives a theme. Write ONE set per item: three different labels in order, most trusted first.

Rules:
1. Each label is one lower-case word of 3 to 10 letters (a-z only).
2. The three labels belong together as a family drawn from the item's theme. Some sets may have an everyday order that matches the ranking (gold, silver, bronze); others have no everyday order at all (blue, green, grey). Never give a set whose everyday order runs the other way.
3. Never a word about trust, quality, truth, age or authority itself (no trusted, sure, verified, good, bad, true, false, best, worst, new, old, senior), no negation, no number words or ordinals, no names of real companies or products, and never the words source, name, dated, origin, states, claim or check.
4. Every set differs from every other set you write, no label appears in two of your sets, and none repeats the examples above.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "pack": {"ranks": ["<most trusted>", "<middle>", "<least trusted>"]}}. Valid JSON only.

## Answer format

[{"qid": "q...", "pack": {"ranks": ["...", "...", "..."]}}, ...]

## Items (16; one JSON object per line)

```json
[
{"qid": "qd009b043a6", "brief": "Theme: gemstones."},
{"qid": "q5f26e1163d", "brief": "Theme: trees."},
{"qid": "q85fbb9cec1", "brief": "Theme: musical instruments."},
{"qid": "qf766e7133f", "brief": "Theme: planets."},
{"qid": "qaa67016ef3", "brief": "Theme: fabrics."},
{"qid": "q274e706a15", "brief": "Theme: sizes."},
{"qid": "q92ad7345fd", "brief": "Theme: letters of an old alphabet."},
{"qid": "qd5bd0a6807", "brief": "Theme: metals."},
{"qid": "qfae7b8a896", "brief": "Theme: birds."},
{"qid": "qb542a407b6", "brief": "Theme: flowers."},
{"qid": "qd8205dd8d3", "brief": "Theme: seasons."},
{"qid": "qa9401235f1", "brief": "Theme: spices."},
{"qid": "qe2607547a9", "brief": "Theme: colours."},
{"qid": "q4da11490d4", "brief": "Theme: weather."},
{"qid": "q93c2ec38f5", "brief": "Theme: stones."},
{"qid": "q70c817e29b", "brief": "Theme: rivers."}
]
```
