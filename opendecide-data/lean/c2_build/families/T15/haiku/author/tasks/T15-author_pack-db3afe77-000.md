# Haiku authoring task T15-author_pack-db3afe77-000 (family T15, kind author_pack, pool names)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/author/answers/T15-author_pack-db3afe77-000.json

The answer is one JSON list with exactly 7 objects, one per item below, each carrying that item's qid.

## Instructions

You write lists of invented-person names for practice puzzles. Each item asks for one list. Write ONE list per item.

Rules (a program drops any name that breaks one):
1. First names and last names are ONE word each: letters only, first letter capital, the rest lower case, 3-10 letters (no hyphen, apostrophe, accent or space).
2. Draw from a wide range of languages and cultures; ordinary given names and family names only, never a famous person's full name.
3. Never a word that is also a common English word, a month or a weekday, a number word or a modal verb (no May, June, April, August, Will, Bill, Hope, Faith, Joy, Sunny, Rich, Summer, Winter, Autumn, Mark, Pat, Grant ...), and never a word that starts with No, Not or Non.
4. Inside one list every name differs.
5. Where the item asks for full names, write "First Last" (exactly two words, each following rule 1).

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "names": ["...", "..."]}. Valid JSON only.

## Answer format

[{"qid": "q...", "names": ["...", "..."]}, ...]

## Items (7; one JSON object per line)

```json
[
{"qid": "qfbac374746", "brief": "Write 40 different women's first names."},
{"qid": "qce01c99bf7", "brief": "Write 40 different family names (last names), unlike common English ones."},
{"qid": "qf2d241d773", "brief": "Write 30 different full names \"First Last\" for caseworkers, using first names that suit any gender."},
{"qid": "q811641f370", "brief": "Write 40 different men's first names."},
{"qid": "q407750743e", "brief": "Write 40 different family names (last names)."},
{"qid": "q942f92f237", "brief": "Write 40 different short first names for young children (3-6 letters), girls' and boys' names mixed."},
{"qid": "qbe994a3ea2", "brief": "Write 16 different first names that suit any gender."}
]
```
