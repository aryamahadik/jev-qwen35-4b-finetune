# Haiku REDO-2 task T36-author_freeform-b8eb33e1-001 (family T36, kind author_freeform): 15 item(s), 2 candidate texts each

Read this whole file. Do not open, list, search or write any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/haiku/redo2/answers/T36-author_freeform-b8eb33e1-001.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 15 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "texts" (a list of exactly 2 different strings: 2 alternative texts for that item, each complete on its own and each following every rule below; write \n for a line break and \" for a double quote in a string).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys. Every item answered once.

Literal example of the required shape:

[
  {"qid": "qb93c1d4047", "texts": ["<text A>", "<text B>"]},
  ...
]

How the texts are used: a program checks each text against the rules below in the order you wrote them and keeps the first text that passes every check; the others are thrown away. So every text must follow every rule, and the texts of one item must be clearly different from each other.

## Instructions

You are writing short text pieces for a test set about software projects and the external packages they depend on. Invent everything: never copy text from real projects, packages, companies, people or websites. Write in English. Make every text clearly different from every other text in this file (structure, opening, length, word choice). Each item below has a qid and the details of what to write; the answer is one object per item as in the contract above.

TASK: for each item write 2 alternative short free-form documents in the item's register (style notes below) in which the maintainer of a software project writes about, or is mentioned in connection with, a look at the project's dependency on an external package. A program prints the package's details after your document; your document only sets the scene and adds no fact of its own.
Facts: each item gives two facts (PERSON = the maintainer's full name, PROJECT = the project's name). Use EACH fact value at least once, copied exactly character for character: never shorten, split, re-case or abbreviate it, and never use a first name alone. Every other person is unnamed (a colleague, the team, a reviewer), and nobody else maintains the project or is called a maintainer. Refer to the package only as "the package", "the library" or "this dependency", never by a name.
Maintainer statement (required): each document says in plain words that PERSON maintains PROJECT, with both values written in full, exactly as given, as part of that statement (shapes in the redo note).
Register styles: ci_log: one or two pipeline log lines made of key=value pairs or bracketed fields (no timestamps, no numbers) | dep_pr_review: a review comment on a pull request that touches the project's dependencies: one to three sentences | dep_ticket: a ticket written as plain "Field: value" lines (such as Summary, Owner, Component, Notes) | dep_wiki: a short paragraph from the project's internal wiki page about its external packages | dev_chat: a team-chat message: one to three short chat lines | issue: an issue-tracker post: a short title line, then a body of one to three sentences | maintainer_email: an e-mail: an optional "Subject:" line, a greeting, a short body and a sign-off | release_notes: a short passage from the project's release-preparation notes: a heading line and one or two lines
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

## Items (15; one JSON object per line)

```json
[
{"qid": "qb93c1d4047", "brief": "Form: a message with a little background on why the dependency is being looked at. Write 2 alternative documents.", "register": "maintainer_email", "facts": {"PERSON": "Tomas Ferreira", "PROJECT": "Gallowhill Portal"}, "rules": ["use each fact value verbatim at least once", "write in the maintainer_email register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qd42ace627c", "brief": "Form: a hand-over note from a teammate to a colleague. Write 2 alternative documents.", "register": "maintainer_email", "facts": {"PERSON": "Ravi Anand", "PROJECT": "Harbor Lantern"}, "rules": ["use each fact value verbatim at least once", "write in the maintainer_email register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q4d248d3561", "brief": "Form: a message with a little background on why the dependency is being looked at. Write 2 alternative documents.", "register": "dep_pr_review", "facts": {"PERSON": "Tomas Ferreira", "PROJECT": "Fellside Planner"}, "rules": ["use each fact value verbatim at least once", "write in the dep_pr_review register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qcf7f5dfa87", "brief": "Form: a slightly rambling explanation. Write 2 alternative documents.", "register": "dep_pr_review", "facts": {"PERSON": "Aiko Brandt", "PROJECT": "Harbor Lantern"}, "rules": ["use each fact value verbatim at least once", "write in the dep_pr_review register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qaf31e236eb", "brief": "Form: a tidy note in short paragraphs. Write 2 alternative documents.", "register": "dep_ticket", "facts": {"PERSON": "Lena Whitcombe", "PROJECT": "Pinecrest Tracker"}, "rules": ["use each fact value verbatim at least once", "write in the dep_ticket register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qe656246e68", "brief": "Form: a short reply in an ongoing conversation. Write 2 alternative documents.", "register": "dev_chat", "facts": {"PERSON": "Mira Castell", "PROJECT": "Oatfield Studio"}, "rules": ["use each fact value verbatim at least once", "write in the dev_chat register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qb6f0f59b72", "brief": "Form: a short reply in an ongoing conversation. Write 2 alternative documents.", "register": "dep_wiki", "facts": {"PERSON": "Lena Whitcombe", "PROJECT": "Spokewright Shop"}, "rules": ["use each fact value verbatim at least once", "write in the dep_wiki register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q625b248431", "brief": "Form: a slightly rambling explanation. Write 2 alternative documents.", "register": "ci_log", "facts": {"PERSON": "Ravi Anand", "PROJECT": "Westerby Archive"}, "rules": ["use each fact value verbatim at least once", "write in the ci_log register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qde2a97a74f", "brief": "Form: a message with a little background on why the dependency is being looked at. Write 2 alternative documents.", "register": "dep_wiki", "facts": {"PERSON": "Tomas Ferreira", "PROJECT": "Spokewright Shop"}, "rules": ["use each fact value verbatim at least once", "write in the dep_wiki register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q1d37ded893", "brief": "Form: a tidy note in short paragraphs. Write 2 alternative documents.", "register": "dep_wiki", "facts": {"PERSON": "Dana Okafor", "PROJECT": "Fellside Planner"}, "rules": ["use each fact value verbatim at least once", "write in the dep_wiki register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "q65d79856d5", "brief": "Form: a message with a little background on why the dependency is being looked at. Write 2 alternative documents.", "register": "issue", "facts": {"PERSON": "Lena Whitcombe", "PROJECT": "Spokewright Shop"}, "rules": ["use each fact value verbatim at least once", "write in the issue register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qb026a5b360", "brief": "Form: a note that sets out what the reader is asked to look at. Write 2 alternative documents.", "register": "dep_pr_review", "facts": {"PERSON": "Tomas Ferreira", "PROJECT": "Pinecrest Tracker"}, "rules": ["use each fact value verbatim at least once", "write in the dep_pr_review register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qe400026fab", "brief": "Form: a note that sets out what the reader is asked to look at. Write 2 alternative documents.", "register": "issue", "facts": {"PERSON": "Aiko Brandt", "PROJECT": "Westerby Archive"}, "rules": ["use each fact value verbatim at least once", "write in the issue register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qe08843a0cb", "brief": "Form: a note that sets out what the reader is asked to look at. Write 2 alternative documents.", "register": "release_notes", "facts": {"PERSON": "Tomas Ferreira", "PROJECT": "Fellside Planner"}, "rules": ["use each fact value verbatim at least once", "write in the release_notes register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]},
{"qid": "qc548231213", "brief": "Form: a tidy note in short paragraphs. Write 2 alternative documents.", "register": "dev_chat", "facts": {"PERSON": "Dana Okafor", "PROJECT": "Harbor Lantern"}, "rules": ["use each fact value verbatim at least once", "write in the dev_chat register (style notes in the instructions)", "say in plain words that PERSON maintains PROJECT (redo note A)"]}
]
```
