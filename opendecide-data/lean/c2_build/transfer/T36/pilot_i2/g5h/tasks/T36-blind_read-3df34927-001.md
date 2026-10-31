# G5-H blind read T36-blind_read-3df34927-001 (family T36)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/pilot_i2/g5h/answers/T36-blind_read-3df34927-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q3c39680201",
  "kind": "choice",
  "text": "Subject: Hearth Saddle dependency look\nHello team,\nLukas Brandt maintains Hearth Saddle, and the planning sync has asked for a short look at how the code uses the external package.\nI would like the review session to go over the calls that reach into it, and to highlight the ones that matter most.\nThanks,\nA colleague\n\npackage.json of the project:\n{\"name\": \"hearth-saddle\", \"dependencies\": {\"cornice-hold\": \">=18.21.8 <19.0.0\"}}\n\nPublished versions of cornice-hold:\n| version |\n|---|\n| 18.21.9 |\n| 19.3.8 |\n| 18.21.8-alpha |\n| 18.26.7 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed cornice-hold version is the highest that meets the range?",
  "options": [
   "None of the listed versions meets the range",
   "18.26.7",
   "18.21.9"
  ]
 },
 {
  "qid": "qb7fe9788f9",
  "kind": "yes/no",
  "text": "Spindle Counter is maintained by Ottilie Brandt, who keeps the list of external packages tidy.\nThe reminder sending code relies on an external package, and that is the part we want to look at.\nWe want to check how it starts, what it calls, and how its errors show up in the logs.\n\nDeclared specifiers for gallerytally in project spindle-counter (Python packaging style): ==7.18.*\n\nPublished versions of gallerytally: 7.20.8.post3, 7.18.8a1, 7.28.0, 7.20.8, 7.18.7.post3, 7.18.0\nVersion under review: 7.20.8",
  "question": "Is version 7.20.8 of gallerytally not meeting the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd75a29bd97",
  "kind": "choice",
  "text": "Subject: note on berthledger\nDear Tavita Sefo,\nI hope you are well. I am writing with notes on the external packages in Sedgehollow Moorings, particularly on how the package is used across our codebase. Thank you in advance for your thoughts when you have a moment.\nWith thanks,\nthe maintainer\n\nDeclared specifiers for berthledger in project sedgehollow-moorings (Python packaging style): <=9.27.3\n\nPublished versions of berthledger: 9.29.2, 9.27.1.post1, 9.30.1, 9.28.3.post2, 10.21.1, 9.27.7",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed berthledger version does the resolver install, if any?",
  "options": [
   "None of the listed versions meets the range",
   "9.27.1.post1",
   "9.28.3.post2"
  ]
 },
 {
  "qid": "qb0e1fbf348",
  "kind": "choice",
  "text": "Preparation notes for the Crank Ledger release\nWith gratitude to Hana Kobayashi, the notes record the elevation-map package and its direct imports in careful detail.\n\nDeclared range for elevation-map in project crank-ledger (npm style): >=0.7.7 <0.8.0\n\nPublished versions of elevation-map: 0.10.0, 0.7.5, 2.6.7, 0.6.8, 1.9.9, 0.7.7-rc.2",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUsing the declared range of elevation-map, which listed version is the highest that the resolver installs?",
  "options": [
   "0.6.8",
   "None of the listed versions meets the range",
   "2.6.7"
  ]
 },
 {
  "qid": "q39f5a296fe",
  "kind": "yes/no",
  "text": "[CI] [owner=Lerato Dube] [target=hymnal-layout] [project=Carrowdell Vale] note team wants a word before merge\n\nDeclared specifiers for hymnal-layout in project carrowdell-vale (Python packaging style): ~=9.8.8\n\nPublished versions of hymnal-layout: 9.8.9, 9.8.8rc1, 9.8.9.post3, 9.8.8, 9.8.8.post3\nVersion under review: 9.8.8rc1",
  "question": "Would hymnal-layout at version 9.8.8rc1 fail to meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd44d3a86d8",
  "kind": "yes/no",
  "text": "Thank you, team: Mallet Pantry Rota release prep\nGideon Mensah maintains Mallet Pantry Rota, and thanks go to all who helped look into the external package. The sync write-ups made the work easy to follow, and the review session went well, so the release can carry on with a clear picture of this dependency.\n\nDeclared range for pallet-sorter in project mallet-pantry-rota (npm style): >=2.6.3-beta.2 <=2.7.0\n\nPublished versions of pallet-sorter: 2.6.1, 2.10.3, 3.0.2, 2.7.5, 2.6.3-beta.2, 2.6.3\nVersion under review: 2.10.3",
  "question": "Across the published versions of pallet-sorter, is version 2.10.3 not meeting the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q3f8028d536",
  "kind": "choice",
  "text": "Background on the external package. Wanjiru Kamau maintains Mallet Pantry Rota, and the team wanted a careful look at how the external package is used on the product pages. Most calls come from the catalog view, which is where the slow pages were reported.\n\nDeclared specifiers for pallet-sorter in project mallet-pantry-rota (Python packaging style): >=8.22.0, <9.0\n\nPublished versions of pallet-sorter: 9.2.0, 7.37.9, 8.26.4, 9.34.4, 8.20.8",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUnder these rules, which listed version of pallet-sorter does the resolver install?",
  "options": [
   "9.34.4",
   "None of the listed versions meets the range",
   "8.26.4"
  ]
 },
 {
  "qid": "q741949642e",
  "kind": "choice",
  "text": "[scan] kind=direct-deps hit=cable-chart workspace=Thistle Fennel by=Anand Iyer step=read-through\n\nDeclared specifiers for cable-chart in project thistle-fennel (Python packaging style): >6.6, <7.0\n\nPublished versions of cable-chart: 6.6, 7.4, 6.4, 6.5, 5.1, 7.0, 7.2",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUsing the declared range of cable-chart, which listed version is the highest that the resolver installs?",
  "options": [
   "6.6",
   "6.5",
   "6.4",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qdce51d6650",
  "kind": "yes/no",
  "text": "Priya Raghavan, the chainring-bin package is yours to look after in Quenbar Spanner from here on.\nI left my notes in the folder, so take a look when you get a minute.\n\nDeclared specifiers for chainring-bin in project quenbar-spanner (Python packaging style): ~=2.9a1\n\nPublished versions of chainring-bin: 2.10, 3.7, 2.8, 2.10b2, 1.2, 2.7\nVersion under review: 2.10",
  "question": "Where chainring-bin is concerned, does version 2.10 fail to meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q23c0354a25",
  "kind": "yes/no",
  "text": "staffindex thread again, sigh. Ngozi Eke is on it. Bradawl Folio side is idle and waiting for that.\n\nDeclared range for staffindex in project bradawl-folio (npm style): 3.9.x || 5.13.0 - 5.14.8\n\nPublished versions of staffindex: 3.9.3, 3.19.1, 3.9.1, 5.13.2, 5.15.0\nVersion under review: 5.13.2",
  "question": "Where staffindex is concerned, does version 5.13.2 fail to meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q3fcaf6e8a7",
  "kind": "choice",
  "text": "Passing the review of this pull request along. The mailing-roll package change touches our dependencies for Carrowdell Vale, so Lerato Dube takes it from here.\n\npackage.json of the project:\n{\"name\": \"carrowdell-vale\", \"dependencies\": {\"mailing-roll\": \"6.0.x\"}}\n\nPublished versions of mailing-roll:\n| version |\n|---|\n| 5.7.6 |\n| 7.5.4 |\n| 6.1.0 |\n| 6.0.3 |\n| 3.3.1 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPut simply, what is the top listed version of mailing-roll the resolver takes under these rules, if any?",
  "options": [
   "None of the listed versions meets the range",
   "6.0.3",
   "3.3.1"
  ]
 },
 {
  "qid": "qd21d2c0d03",
  "kind": "choice",
  "text": "Prepping the release for Pan Ration Tally, the notes are taking shape.\nRohan Desai flagged the kcal-table package in our draft and it deserves a closer read.\n\nDeclared range for kcal-table in project pan-ration-tally (npm style): ~0.3.2\n\nPublished versions of kcal-table: 0.1.2, 0.4.4, 0.5.1, 0.3.0, 0.1.3, 0.2.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nCould you tell which listed kcal-table version the resolver would install, if any?",
  "options": [
   "0.1.2",
   "0.1.3",
   "None of the listed versions meets the range",
   "0.5.1"
  ]
 },
 {
  "qid": "q40c7baf57e",
  "kind": "yes/no",
  "text": "Hi team,\nPassing the hewnsight work in Gimlet Matinee over to you. The notes are in the team folder and you know where the files live.\nThanks,\nRuairi Calloway\n\nDeclared range for hewnsight in project gimlet-matinee (npm style): >13.0.1-rc.1 <14.0.0\n\nPublished versions of hewnsight: 14.1.1, 13.0.1-rc.2, 13.1.2, 14.0.0, 16.6.3\nVersion under review: 13.0.1-rc.2",
  "question": "Would the declared range of hewnsight be met by version 13.0.1-rc.2?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb80bdcb558",
  "kind": "yes/no",
  "text": "What: mossfeed\nWhere: Fernhollow Tour tree\nContact: Hugo Saldana\nTodo: read the tree and write it up.\n\nDeclared specifiers for mossfeed in project fernhollow-tour (Python packaging style): ~=4.23\n\nPublished versions of mossfeed: 3.10, 5.0, 4.28, 4.23rc1, 4.25, 4.23.post3, 5.37\nVersion under review: 4.23.post3",
  "question": "Taking every line of the rules into account, does version 4.23.post3 meet the declared range of mossfeed?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q0e9ee32734",
  "kind": "choice",
  "text": "Hey there,\nSo the period-slot package has been on my mind, mostly because the team keeps asking about it. Chalk Register has come a long way and it is lovely to see people care so deeply.\nWarmly,\nJonah Abernathy\n\nDeclared range for period-slot in project chalk-register (npm style): 5.x\n\nPublished versions of period-slot: 4.1.3, 6.7.1, 6.0.0, 6.3.3, 5.8.2, 6.0.6, 3.8.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version of period-slot would the resolver install under these rules, if any, given the declared range?",
  "options": [
   "None of the listed versions meets the range",
   "3.8.3",
   "5.8.2"
  ]
 },
 {
  "qid": "q60f8b8f549",
  "kind": "yes/no",
  "text": "Prep notes, Rivet Loft\nNaledi Mahlangu asks a colleague to take a look at the routeplan package before the notes are final.\n\nDeclared range for routeplan in project rivet-loft (npm style): ^2.4.8-alpha.3\n\nPublished versions of routeplan: 4.7.7, 2.5.0, 3.2.0, 2.3.9\nVersion under review: 2.5.0",
  "question": "Is version 2.5.0 of routeplan not meeting the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd6f081b349",
  "kind": "choice",
  "text": "[scan] kind=direct-deps hit=refuge-slot workspace=Hearth Saddle by=Lukas Brandt step=read-through\n\nDeclared range for refuge-slot in project hearth-saddle (npm style): 0.5.5 - 0.8.4\n\nPublished versions of refuge-slot: 0.9.0, 0.7.0, 0.5.5-rc.1, 2.7.5, 0.5.4, 1.0.5",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith its declared range in mind, which listed version of refuge-slot will the resolver install?",
  "options": [
   "0.9.0",
   "None of the listed versions meets the range",
   "0.7.0"
  ]
 },
 {
  "qid": "qf7b332dbcd",
  "kind": "yes/no",
  "text": "Subject: Fresh look at the plate-register package\nHi Ngozi Eke,\nMind taking a look at how Bradawl Folio leans on it? My notes are below, and my reading of them feels a bit tangled. Eyes from a colleague are welcome. Thanks in advance.\nBest,\nthe maintainer\n\nDeclared range for plate-register in project bradawl-folio (npm style): ^19.9.4 || =0.0.13\n\nPublished versions of plate-register: 20.1.0, 19.10.4, 1.4.12, 19.8.5\nVersion under review: 20.1.0",
  "question": "Is version 20.1.0 of plate-register outside the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6b5dbcedf4",
  "kind": "choice",
  "text": "Title: dependency review round for brake-stock\nReviewer: Priya Raghavan\nScope: Quenbar Spanner manifest, reviewed in this round\nNotes: logged alongside the other packages in the same sweep.\n\nDeclared range for brake-stock in project quenbar-spanner (npm style): =20.0.2\n\nPublished versions of brake-stock: 20.0.2-rc.1, 19.0.3, 20.0.1, 17.6.2, 20.0.4-alpha.3, 20.0.2, 20.4.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUnder these rules, which listed version of brake-stock does the resolver install?",
  "options": [
   "20.0.2",
   "19.0.3",
   "20.4.3",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q5efa301000",
  "kind": "yes/no",
  "text": "Subject: note on chapterloom\nDear Dorin Pavlescu,\nI hope you are well. I am writing with notes on the external packages in Ysmere Cove, particularly on how the package is used across our codebase. Thank you in advance for your thoughts when you have a moment.\nWith thanks,\nthe maintainer\n\nDeclared range for chapterloom in project ysmere-cove (npm style): 0.0.3 - 0.3.2\n\nPublished versions of chapterloom: 3.0.2, 0.3.1, 0.3.2, 0.1.2, 0.2.1, 0.0.4, 0.0.3\nVersion under review: 0.1.2",
  "question": "Does the version under review, 0.1.2, meet the declared range of chapterloom?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd5c300abc8",
  "kind": "choice",
  "text": "[pipeline] stage=dependency-audit | repo=Fir Cairn Route | pkg=trail-tiles | owner=Elif Arslan | note=still_learning_the_codebase\n\nDeclared range for trail-tiles in project fir-cairn-route (npm style): >=20.24.11 <21.0.0\n\nPublished versions of trail-tiles: 20.25.39, 20.24.11, 20.24.12, 20.24.11-beta.2, 20.24.13, 20.24.13-alpha.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nFor trail-tiles, which listed version would the resolver end up with?",
  "options": [
   "20.24.11",
   "20.25.39",
   "20.24.12",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q13c6c99774",
  "kind": "yes/no",
  "text": "This PR touches the bunk-ledger package in Hearth Saddle, which we have been side-stepping for ages.\nBackground: the team has grown a lot since the project began, so Lukas Brandt knows the history best.\n\npackage.json of the project:\n{\"name\": \"hearth-saddle\", \"dependencies\": {\"bunk-ledger\": \"^5.4.10\"}}\n\nPublished versions of bunk-ledger:\n| version |\n|---|\n| 6.0.0 |\n| 5.14.12 |\n| 5.3.20 |\n| 5.9.29 |\n| 4.2.32 |\n| 5.4.10 |\nVersion under review: 6.0.0",
  "question": "Based on the card, does 6.0.0 fail to meet the range declared for bunk-ledger?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6092522ed4",
  "kind": "choice",
  "text": "Subject: note on refuge-slot\nDear Thandiwe Mokoena,\nI hope you are well. I am writing with notes on the external packages in Hearth Saddle, particularly on how the package is used across our codebase. Thank you in advance for your thoughts when you have a moment.\nWith thanks,\nthe maintainer\n\nDeclared specifiers for refuge-slot in project hearth-saddle (Python packaging style): <=5.4.17\n\nPublished versions of refuge-slot: 5.4.0a1, 5.3.20, 5.5a1, 5.4.21",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPut simply, what is the top listed version of refuge-slot the resolver takes under these rules, if any?",
  "options": [
   "5.4.21",
   "None of the listed versions meets the range",
   "5.3.20"
  ]
 },
 {
  "qid": "q6c5d91f6ee",
  "kind": "yes/no",
  "text": "Deps part, rel prep\nhandled by Dariusz Kowal, lines cover the berth-calendar package and its use in Murrelet Kelp.\n\nDeclared range for berth-calendar in project murrelet-kelp (npm style): >=3.2.0 <3.3.0\n\nPublished versions of berth-calendar: 2.7.2, 3.2.0-rc.1, 3.2.0, 3.3.0, 3.2.8, 6.7.1\nVersion under review: 3.2.0",
  "question": "Does 3.2.0 of berth-calendar meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1a21380af5",
  "kind": "yes/no",
  "text": "[pipeline] stage=dependency-audit | repo=Corvellan Perch | pkg=birdsong-cache | owner=Ambrose Tilley | note=still_learning_the_codebase\n\nDeclared range for birdsong-cache in project corvellan-perch (npm style): >=9.2.9 <9.3.0\n\nPublished versions of birdsong-cache:\n| version |\n|---|\n| 9.3.1 |\n| 8.9.8 |\n| 9.2.9 |\n| 9.2.10 |\n| 9.2.8 |\n| 9.6.7 |\n| 9.0.0 |\nVersion under review: 8.9.8",
  "question": "birdsong-cache declares a range, and does version 8.9.8 meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q166d824fcc",
  "kind": "yes/no",
  "text": "Going through the cohort-matrix package as part of the dependency sweep for Chalk Register.\nJonah Abernathy has the notes, so shout when you see it.\n\npyproject.toml of the project:\n[project]\nname = \"chalk-register\"\ndependencies = [\n  \"cohort-matrix >=6.3.8, !=6.4, <6.8\",\n]\n\nPublished versions of cohort-matrix:\n| version |\n|---|\n| 6.3.4 |\n| 6.3.9.post1 |\n| 6.6.0 |\n| 6.3.7 |\n| 6.1.7 |\nVersion under review: 6.6.0",
  "question": "Based on the card, does 6.6.0 fail to meet the range declared for cohort-matrix?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qbeb9a0fe19",
  "kind": "choice",
  "text": "Question about the plate-register package\nWe have leaned on this package since Bradawl Folio got going, and the team keeps circling back to it. Raised by Dara Ashdown, who is keen to hear what the rest of the crew says.\n\nDeclared range for plate-register in project bradawl-folio (npm style): >=4.17.10-rc.1 <5.0.0\n\nPublished versions of plate-register: 3.19.14, 7.24.26, 2.38.0, 4.16.14, 5.36.25, 5.0.3, 4.17.10",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version of plate-register would the resolver install under these rules, if any, given the declared range?",
  "options": [
   "7.24.26",
   "4.17.10",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qf75e87a560",
  "kind": "yes/no",
  "text": "[ci] job=external-package-check project=Pan Ration Tally maintainer=Rohan Desai owner=the reviewers\n[ci] reason=start-up timing of the external package looked odd in the pipeline run, so reviewers were asked to go over it before this change lands, and the timing data sits in the job log.\n\nDeclared specifiers for portion-map in project pan-ration-tally (Python packaging style): ==9.24.*\n\nPublished versions of portion-map: 9.24.2.post3, 9.24.0.post2, 9.22.6, 9.24.5, 9.24.5.post2, 9.24.2\nVersion under review: 9.22.6",
  "question": "Did the version 9.22.6 land outside the declared range set by portion-map?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q22a002ae9a",
  "kind": "yes/no",
  "text": "Regular dependency review, item for Crank Ledger\nThe bearing-lane package turned up on the list during the regular pass. Hana Kobayashi agreed to write up the findings for the group.\n\nDeclared range for bearing-lane in project crank-ledger (npm style): ~2.13.7\n\nPublished versions of bearing-lane: 0.22.8, 2.13.7, 2.14.7, 2.11.7\nVersion under review: 2.14.7",
  "question": "Is it true that version 2.14.7 does not meet the declared range of bearing-lane?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q24942198d1",
  "kind": "yes/no",
  "text": "[step=dependency_review] project=Mallet Pantry Rota package=pallet-sorter reviewer=Gideon Mensah state=in_progress\n\nDeclared specifiers for pallet-sorter in project mallet-pantry-rota (Python packaging style): >=4.28, !=4.29.0, <4.32\n\nPublished versions of pallet-sorter: 4.28, 5.0, 4.29.2, 4.30, 4.31\nVersion under review: 5.0",
  "question": "Under these rules, does the version 5.0 of pallet-sorter meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6d3eb2ecfe",
  "kind": "choice",
  "text": "Release prep\nGimlet Matinee is maintained by Ewa Lindqvist. Before the cut, the external package used for reminder emails needs a look at its start-up cost, and the reviewers should go over the logs from the pipeline run on the main branch.\n\nDeclared range for chalkline-grid in project gimlet-matinee (npm style): ^3.9.1 || ~6.23.18-beta.2\n\nPublished versions of chalkline-grid: 6.23.19, 3.9.3, 3.10.0, 6.23.18-alpha.3, 3.9.1-alpha, 3.31.12",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWould you kindly indicate which listed version of chalkline-grid the resolver installs under these rules?",
  "options": [
   "6.23.19",
   "3.31.12",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qae0611bf26",
  "kind": "choice",
  "text": "Hi team,\nPassing the plumage-atlas work in Corvellan Perch over to you. The notes are in the team folder and you know where the files live.\nThanks,\nSaoirse Quinlan\n\nDeclared specifiers for plumage-atlas in project corvellan-perch (Python packaging style): >=7.23.2, <7.26\n\nPublished versions of plumage-atlas: 7.26.3, 8.13.2, 7.21.3, 7.22.1, 6.35.2",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version of plumage-atlas, from its listed set, gets installed by the resolver, if any?",
  "options": [
   "7.21.3",
   "7.26.3",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q0289a52fae",
  "kind": "yes/no",
  "text": "refuge-slot. External package. Used by the Hearth Saddle build. Contact for questions: Thandiwe Mokoena. Review when touched.\n\nDeclared specifiers for refuge-slot in project hearth-saddle (Python packaging style): ==9.9.*\n\nPublished versions of refuge-slot: 9.7.10, 9.9.24a1, 9.19.34, 9.11.10, 9.9.24\nVersion under review: 9.19.34",
  "question": "By these rules, would 9.19.34 of refuge-slot lie outside the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd70399a596",
  "kind": "yes/no",
  "text": "Touches the macro-sum entry in Pan Ration Tally's manifest. Lock churn too. Reason? Asked by Rohan Desai.\n\nDeclared specifiers for macro-sum in project pan-ration-tally (Python packaging style): <=9.1\n\nPublished versions of macro-sum: 9.1, 9.3, 10.4, 9.1.post2, 9.3.post2\nVersion under review: 10.4",
  "question": "Can version 10.4 of macro-sum be said to meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q5a7757017b",
  "kind": "choice",
  "text": "Release prep\nTarnhollow Corpus is maintained by Valentina Ortiz. Before the cut, the external package used for reminder emails needs a look at its start-up cost, and the reviewers should go over the logs from the pipeline run on the main branch.\n\nDeclared range for gloss-ring in project tarnhollow-corpus (npm style): ^18.27.1\n\nPublished versions of gloss-ring: 20.30.3, 18.5.2, 17.31.3, 19.1.0, 18.25.2, 16.31.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich highest listed version of gloss-ring meets the declared range, if any?",
  "options": [
   "17.31.3",
   "None of the listed versions meets the range",
   "16.31.3",
   "20.30.3"
  ]
 },
 {
  "qid": "qa5a4094f6f",
  "kind": "yes/no",
  "text": "Summary: request for a careful review of the gauge-convert package\nOwner: Anand Iyer\nComponent: Thistle Fennel dependencies\nNotes: please take the matter in good order at your convenience.\n\nDeclared specifiers for gauge-convert in project thistle-fennel (Python packaging style): >8.3.7a1, <9.0\n\nPublished versions of gauge-convert: 8.1.8, 8.6.8, 8.4.7, 8.4.0b2, 8.3.11, 8.3.7a1, 8.3.7.post1\nVersion under review: 8.4.7",
  "question": "Is 8.4.7 falling outside the range of gauge-convert?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q49ede71302",
  "kind": "choice",
  "text": "Subject: handover for the external package review\nHi there,\nPassing my part of the external package review over to you. Tomasz Brenek, who maintains Mirrask Platter, wants a look at how long the package takes to start on each run. The log lines for that sit in the shared folder. Go over them before anything else, then check the pipeline timings with the reviewers.\nCheers,\nyour teammate\n\nDeclared specifiers for dressing-lattice in project mirrask-platter (Python packaging style): <=0.20\n\nPublished versions of dressing-lattice: 0.22, 1.22, 0.19, 0.18, 0.20a1, 0.20",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGoing by the card, which listed version of dressing-lattice would be picked as highest that meets the range?",
  "options": [
   "0.20",
   "0.22",
   "0.19",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q33d8372ff0",
  "kind": "yes/no",
  "text": "Subject: Fresh look at the chalkline-grid package\nHi Ruairi Calloway,\nMind taking a look at how Gimlet Matinee leans on it? My notes are below, and my reading of them feels a bit tangled. Eyes from a colleague are welcome. Thanks in advance.\nBest,\nthe maintainer\n\npackage.json of the project:\n{\"name\": \"gimlet-matinee\", \"dependencies\": {\"chalkline-grid\": \"~3.3.0 || >=4.7.2 <5.0.0\"}}\n\nPublished versions of chalkline-grid:\n| version |\n|---|\n| 4.17.2 |\n| 4.8.2 |\n| 5.3.0 |\n| 4.7.3 |\nVersion under review: 4.7.3",
  "question": "Regarding chalkline-grid, does version 4.7.3 meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- Parts separated by spaces must all hold.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qc514aaa91f",
  "kind": "choice",
  "text": "Quick ping from Rahul Venkatesan: the plotqueue package is on the list for Spade Roster.\nDrop a line when you are free.\n\npackage.json of the project:\n{\"name\": \"spade-roster\", \"dependencies\": {\"plotqueue\": \">0.0.9 <1.0.0\"}}\n\nPublished versions of plotqueue:\n| version |\n|---|\n| 1.9.8 |\n| 0.0.9 |\n| 1.3.9 |\n| 3.3.9 |\n| 1.0.0 |\n| 1.0.4 |\n| 1.1.7 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith these rules applied to plotqueue, which listed version would the resolver settle on, if any?",
  "options": [
   "None of the listed versions meets the range",
   "1.3.9",
   "3.3.9",
   "1.1.7"
  ]
 },
 {
  "qid": "q8c7a2131a2",
  "kind": "yes/no",
  "text": "Subject: dependency page for Tessemere Rota\nHi team,\nWanted to flag a gap on the page about how we use the airwave-list package. Please take a look when things calm down.\nThanks,\nJoaquin Ruelas\n\nDeclared specifiers for airwave-list in project tessemere-rota (Python packaging style): >=9.24.5, <9.28\n\nPublished versions of airwave-list: 9.25.5, 9.34.5, 9.23.6, 9.24.9\nVersion under review: 9.24.9",
  "question": "airwave-list: would version 9.24.9 meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q3111adb234",
  "kind": "yes/no",
  "text": "Release prep: Brevlin Exchange dependency look\nOskar Lindahl maintains Brevlin Exchange. The external package came up while the planning sync was going over the release list, and the calls it reaches for are being traced by the team, so a look in the review session is the plan.\n\npackage.json of the project:\n{\"name\": \"brevlin-exchange\", \"dependencies\": {\"seedling-tally\": \"~0.3.20\"}}\n\nPublished versions of seedling-tally:\n| version |\n|---|\n| 0.4.0 |\n| 0.3.11 |\n| 0.3.22 |\n| 0.3.22-beta.2 |\n| 0.13.18 |\nVersion under review: 0.3.11",
  "question": "On this card, does version 0.3.11 of seedling-tally meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa84f323a6a",
  "kind": "yes/no",
  "text": "Summary: review of the external package for Quoin Stanza\nProject: Quoin Stanza\nMaintainer: Maeve Dunphy\nComponent: reporting\nOwner: the reviewers\nMaeve Dunphy maintains Quoin Stanza, and the external package in the reporting code reads the export settings at start-up.\nSome exported reports come out with the wrong label, so the reviewers should go over that part.\nPlease look at the parsing path and the logs for it, then post what you find in the thread.\n\nDeclared specifiers for leading-grid in project quoin-stanza (Python packaging style): ==1.8.*\n\nPublished versions of leading-grid: 1.8.2, 0.8.8, 1.8.2.post3, 1.12.4\nVersion under review: 1.12.4",
  "question": "Is 1.12.4 falling outside the range of leading-grid?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qfe60fa5dc0",
  "kind": "choice",
  "text": "quick background on the package thing: Mehmet Yildiz maintains Ostrain Glaze, and the planning sync flagged the external package again\nso we want a short sync on which code paths lean on it\nbring the import list and whatever you have on the calls\n\nDeclared range for ramp-schedule in project ostrain-glaze (npm style): 2.1.2 - 2.4.2\n\nPublished versions of ramp-schedule: 1.0.1, 2.1.1, 2.5.3, 2.1.4-beta.2",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version does the resolver install from the listed ramp-schedule versions?",
  "options": [
   "1.0.1",
   "2.5.3",
   "2.1.1",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qb3bbe36d16",
  "kind": "choice",
  "text": "Where bunk-ledger shows up in Hearth Saddle\nI am still getting to know the codebase. Apologies for the basic questions. Please walk Lukas Brandt through how it is used across the project when there is a moment.\n\npyproject.toml of the project:\n[project]\nname = \"hearth-saddle\"\ndependencies = [\n  \"bunk-ledger >=8.12.0, !=8.13, <8.14\",\n]\n\nPublished versions of bunk-ledger: 8.12.6.post1, 8.10.9, 8.12.7, 8.12.4",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWould you kindly indicate which listed version of bunk-ledger the resolver installs under these rules?",
  "options": [
   "None of the listed versions meets the range",
   "8.12.7",
   "8.10.9"
  ]
 },
 {
  "qid": "q9965a5bdbb",
  "kind": "choice",
  "text": "[ci] job=external-package-check project=Crank Ledger maintainer=Hana Kobayashi owner=the reviewers\n[ci] reason=start-up timing of the external package looked odd in the pipeline run, so reviewers were asked to go over it before this change lands, and the timing data sits in the job log.\n\nDeclared range for elevation-map in project crank-ledger (npm style): >13.24.5 <=14.0.0\n\nPublished versions of elevation-map: 16.12.6, 13.24.7-alpha, 13.24.5, 13.24.5-beta, 13.25.4",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nOf the listed versions, which is the highest meeting the declared range of elevation-map, if any?",
  "options": [
   "None of the listed versions meets the range",
   "13.24.5",
   "13.25.4"
  ]
 },
 {
  "qid": "qac0fe33377",
  "kind": "yes/no",
  "text": "Hand-over: the glaze-sheet thread in Ostrain Glaze\nBogdan Stoica had started tracing where the package shows up across our manifests. Please carry that trace forward and note what you find for whoever takes this on, since my calendar is full.\n\nDeclared range for glaze-sheet in project ostrain-glaze (npm style): ^9.25.6\n\nPublished versions of glaze-sheet: 9.25.6-rc.2, 9.25.7, 9.25.6, 9.28.5, 8.15.5\nVersion under review: 9.25.6",
  "question": "Across the published versions of glaze-sheet, is version 9.25.6 not meeting the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa640b4f73b",
  "kind": "yes/no",
  "text": "Hi Ottilie Brandt,\nHere is a quick heads-up on the housekeeping list for Spindle Counter. I am looking at the gallerytally package entry, noting where it lives in the repo. Let me know your thoughts when you get the chance.\nCheers,\nthe maintainer\n\npackage.json of the project:\n{\"name\": \"spindle-counter\", \"dependencies\": {\"gallerytally\": \"7.3.7\"}}\n\nPublished versions of gallerytally:\n| version |\n|---|\n| 7.3.7 |\n| 6.6.7 |\n| 8.7.7 |\n| 7.4.9 |\nVersion under review: 7.4.9",
  "question": "Across the card, does version 7.4.9 fail to meet the declared range that gallerytally specifies?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q98f93b660a",
  "kind": "choice",
  "text": "Spade Roster is maintained by Rahul Venkatesan. If you are picking up the external package section from me, here is where things stand: the import list has been read through, and the code paths that call the package are mapped out. What is left is a walk through the tests that touch it and a short write-up for the team.\n\nDeclared range for lotcall in project spade-roster (npm style): ^0.9.2\n\nPublished versions of lotcall:\n| version |\n|---|\n| 0.9.2 |\n| 0.9.1 |\n| 0.7.3 |\n| 0.9.3 |\n| 0.11.1 |\n| 3.7.1 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich highest listed version of lotcall meets the declared range, if any?",
  "options": [
   "None of the listed versions meets the range",
   "3.7.1",
   "0.9.3"
  ]
 },
 {
  "qid": "qf06fa3b0f6",
  "kind": "yes/no",
  "text": "Brevlin Exchange is maintained by Oskar Lindahl, who keeps the list of external packages tidy.\nThe reminder sending code relies on an external package, and that is the part we want to look at.\nWe want to check how it starts, what it calls, and how its errors show up in the logs.\n\npackage.json of the project:\n{\"name\": \"brevlin-exchange\", \"dependencies\": {\"pollen-pair\": \"^8.7.4\"}}\n\nPublished versions of pollen-pair:\n| version |\n|---|\n| 8.7.5 |\n| 8.7.4-alpha |\n| 8.17.5 |\n| 8.7.4 |\n| 8.9.0 |\nVersion under review: 8.7.4",
  "question": "Regarding pollen-pair, does version 8.7.4 meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qc75e189ac5",
  "kind": "choice",
  "text": "quick background on the package thing: Saoirse Quinlan maintains Corvellan Perch, and the planning sync flagged the external package again\nso we want a short sync on which code paths lean on it\nbring the import list and whatever you have on the calls\n\nDeclared specifiers for plumage-atlas in project corvellan-perch (Python packaging style): ~=3.10\n\nPublished versions of plumage-atlas: 3.10.post2, 3.9, 4.0, 2.19, 4.27, 3.8, 3.12",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version of plumage-atlas would the resolver install under these rules, if any, given the declared range?",
  "options": [
   "3.12",
   "2.19",
   "None of the listed versions meets the range"
  ]
 }
]
