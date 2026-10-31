# Haiku REDO-2 task T36-author_freeform-602ca5b9-000 (family T36, kind author_freeform): 10 item(s), 2 candidate texts each

Read this whole file. Do not open, list, search or write any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/haiku/redo2/answers/T36-author_freeform-602ca5b9-000.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 10 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "texts" (a list of exactly 2 different strings: 2 alternative texts for that item, each complete on its own and each following every rule below; write \n for a line break and \" for a double quote in a string).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys. Every item answered once.

Literal example of the required shape:

[
  {"qid": "q9bdd0f857e", "texts": ["<text A>", "<text B>"]},
  ...
]

How the texts are used: a program checks each text against the rules below in the order you wrote them and keeps the first text that passes every check; the others are thrown away. So every text must follow every rule, and the texts of one item must be clearly different from each other.

## Instructions

You are writing short text pieces for a test set about software projects and the external packages they depend on. Invent everything: never copy text from real projects, packages, companies, people or websites. Write in English. Make every text clearly different from every other text in this file (structure, opening, length, word choice). Each item below has a qid and the details of what to write; the answer is one object per item as in the contract above.

TASK: for each item write 2 alternative short free-form documents in the item's register (style notes below) in which the maintainer of a software project writes about, or is mentioned in connection with, a look at the project's dependency on an external package. A program prints the package's details after your document; your document only sets the scene and adds no fact of its own.
Facts: each item gives two facts (PERSON = the maintainer's full name, PROJECT = the project's name). Use EACH fact value at least once, copied exactly character for character: never shorten, split, re-case or abbreviate it, and never use a first name alone. Every other person is unnamed (a colleague, the team, a reviewer), and nobody else maintains the project or is called a maintainer. Refer to the package only as "the package", "the library" or "this dependency", never by a name.
Maintainer statement (required): each document says in plain words that PERSON maintains PROJECT, with both values written in full, exactly as given, as part of that statement (shapes in the redo note).
Register styles: changelog: a draft changelog entry: a heading line, then one or two bullet lines starting with "- " | lockfile_comment: a comment block at the top of a lock or manifest file: one to three lines, each starting with "# "
Length: 40-120 words. Plain text with line breaks where the register needs them; no empty line.
Hard rules (a document that breaks one is thrown away):
1. Apart from the two fact values: no digits, no number words (billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero; also as part of a hyphenated word), no dates, months or weekdays, no codes or ids (no word that mixes letters and digits), no web or e-mail addresses, no currency or percent signs.
2. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
3. No other names of people, companies, products, places or teams.
4. Say nothing about versions or version numbers, version ranges, operators or symbols, release stages (test builds, release candidates, nightly builds and the like), whether any version is acceptable, suitable, approved or safe, which version gets picked or used, moving to another version, or how new or old anything is; use no word that ranks versions by age or by order. Never hint at any answer: the text only sets the scene for a look at the project's dependency on the package.
5. Capital letters only at the start of a sentence, a line, a list item or a label, in the two fact values, and for CI, PR, QA and API.
6. None of the reserved words in the redo note below.
Follow each item's form for variety. Before writing, check every document: the maintainer statement is there; both fact values appear verbatim; no digit; no number word; no negation; no reserved word.

## Redo note

REDO NOTE (added for this second redo; every rule above still holds). Earlier documents for these items were thrown away. Avoid each cause:
A. The maintainer statement was missing (nearly every item). A later reader is asked who maintains the project and copies that name only when the document says so in words. So each document contains one plain statement that PERSON maintains PROJECT, with both values written in full in that statement. Shapes that work (put the item's own values where <PERSON> and <PROJECT> stand): "<PERSON>, who maintains <PROJECT>, ..."; "<PROJECT> is maintained by <PERSON>."; "<PERSON>, the maintainer of <PROJECT>, ..."; "As maintainer of <PROJECT>, <PERSON> ..."; in a log line "project=<PROJECT> maintainer=<PERSON>"; in a ticket a "Project: <PROJECT>" line and a "Maintainer: <PERSON>" line. A document that says only that PERSON asked for, opened, owns, leads, signed, thanked or was assigned the review is thrown away. Nobody else in the document maintains the project or is called a maintainer; every other person stays unnamed. Vary where the statement sits and how it is phrased.
B. A number word, above all "third" in "third-party" (write "external package" or "imported package"), and words such as "one" (also in "no one"), "first" and "second" (as in a first look or a second pair of eyes) and "half". The check reads every part of a hyphenated word.
C. Reserved words. The check throws away a document that uses any of these kinds of words, in any form (with -s, -ed, -ing and the like):
  - words that judge whether something agrees with, suits, corresponds to or is admitted by a requirement, a rule or a limit, and words for being able to work together with something or for backing it;
  - the everyday verb and noun for getting together with people (a get-together of the team): they are spelled like a reserved word, so write "sync", "call", "catch-up", "planning session" or "review session";
  - place words for being in the interior of something, in a region bounded by a limit, or beyond its edge: write plain position words such as "in", "at", "for", "across", "around", "near";
  - words about letting something into a group or keeping it out of one;
  - words about putting software onto a machine, and words for settling a question (write "look into", "work through", "go over");
  - comparison words for height, rank or age: the -er and -est forms of high, low, new and old, and the -est form of late;
  - words about how steady software is, about changes that harm its users, about moving software to a different level, and the names of early test stages of software.
Before you write the file, read each document once more against hard rules 1-6 and this note.

## Items (10; one JSON object per line)

```json
[
{"qid": "q9bdd0f857e", "brief": "Form: a short reply in an ongoing conversation. Write 2 alternative documents.", "register": "changelog", "facts": {"PERSON": "Oskar Lind", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the changelog register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q9a757cb721", "brief": "Form: a hand-over note from a teammate to a colleague. Write 2 alternative documents.", "register": "lockfile_comment", "facts": {"PERSON": "Oskar Lind", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the lockfile_comment register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q2dc66a38b4", "brief": "Form: a hand-over note from a teammate to a colleague. Write 2 alternative documents.", "register": "changelog", "facts": {"PERSON": "Oskar Lind", "PROJECT": "Quarrytop Wiki"}, "rules": ["use each fact value verbatim at least once", "write in the changelog register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q1fc01597bc", "brief": "Form: a quick, informal write-up. Write 2 alternative documents.", "register": "lockfile_comment", "facts": {"PERSON": "Beatriz Soto", "PROJECT": "Quarrytop Wiki"}, "rules": ["use each fact value verbatim at least once", "write in the lockfile_comment register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qdc59645438", "brief": "Form: a message with a little background on why the dependency is being looked at. Write 2 alternative documents.", "register": "lockfile_comment", "facts": {"PERSON": "Beatriz Soto", "PROJECT": "Quarrytop Wiki"}, "rules": ["use each fact value verbatim at least once", "write in the lockfile_comment register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qd7020b0198", "brief": "Form: a quick, informal write-up. Write 2 alternative documents.", "register": "changelog", "facts": {"PERSON": "Priya Hallam", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the changelog register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q1cb22039e1", "brief": "Form: a message that thanks the team. Write 2 alternative documents.", "register": "changelog", "facts": {"PERSON": "Oskar Lind", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the changelog register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qf401385da9", "brief": "Form: a tidy note in short paragraphs. Write 2 alternative documents.", "register": "lockfile_comment", "facts": {"PERSON": "Beatriz Soto", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the lockfile_comment register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qfe949073cd", "brief": "Form: a short reply in an ongoing conversation. Write 2 alternative documents.", "register": "lockfile_comment", "facts": {"PERSON": "Beatriz Soto", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the lockfile_comment register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q1548c4f6fd", "brief": "Form: a tidy note in short paragraphs. Write 2 alternative documents.", "register": "changelog", "facts": {"PERSON": "Priya Hallam", "PROJECT": "Brackenfold Hub"}, "rules": ["use each fact value verbatim at least once", "write in the changelog register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]}
]
```
