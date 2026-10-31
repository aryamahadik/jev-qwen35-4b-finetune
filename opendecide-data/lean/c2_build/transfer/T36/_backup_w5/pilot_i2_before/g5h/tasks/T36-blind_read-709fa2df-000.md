# G5-H blind read T36-blind_read-709fa2df-000 (family T36)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/pilot_i2/g5h/answers/T36-blind_read-709fa2df-000.json

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
  "qid": "qa5fcedf456",
  "kind": "choice",
  "text": "For the record: Ombrel Sprout preparation\nThe sunlit-cycle package has been examined with due care, and Dagny Brask is grateful for your comments in advance.\n\nDeclared range for sunlit-cycle in project ombrel-sprout (npm style): 7.2.2 - 7.4.2\n\nPublished versions of sunlit-cycle: 7.3.1, 7.2.2-alpha, 7.7.2, 7.2.3, 7.4.1",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGiven the card, which listed version does the resolver install for sunlit-cycle?",
  "options": [
   "7.4.1",
   "7.3.1",
   "7.2.3",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qeca8a23c48",
  "kind": "yes/no",
  "text": "[CI] [owner=Lerato Dube] [target=hymnal-layout] [project=Carrowdell Vale] note team wants a word before merge\n\nDeclared specifiers for hymnal-layout in project carrowdell-vale (Python packaging style): ~=9.8.8\n\nPublished versions of hymnal-layout: 9.8.9, 9.8.8rc1, 9.8.9.post3, 9.8.8, 9.8.8.post3\nVersion under review: 9.8.8rc1",
  "question": "Would hymnal-layout at version 9.8.8rc1 fail to meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q435259eabd",
  "kind": "yes/no",
  "text": "Hi Ottilie Brandt,\nHere is a quick heads-up on the housekeeping list for Spindle Counter. I am looking at the gallerytally package entry, noting where it lives in the repo. Let me know your thoughts when you get the chance.\nCheers,\nthe maintainer\n\npackage.json of the project:\n{\"name\": \"spindle-counter\", \"dependencies\": {\"gallerytally\": \"7.3.7\"}}\n\nPublished versions of gallerytally:\n| version |\n|---|\n| 7.3.7 |\n| 6.6.7 |\n| 8.7.7 |\n| 7.4.9 |\nVersion under review: 7.4.9",
  "question": "Across the card, does version 7.4.9 fail to meet the declared range that gallerytally specifies?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q2adcd45060",
  "kind": "choice",
  "text": "[peer-look] reviewer=Ines Morales | project=Shed Loan Rack | pkg=spanner-log | view=fresh\n\npackage.json of the project:\n{\"name\": \"shed-loan-rack\", \"dependencies\": {\"spanner-log\": \"~0.2.2 || 12.14.1 - 12.17.0\"}}\n\nPublished versions of spanner-log:\n| version |\n|---|\n| 12.14.0 |\n| 1.7.0 |\n| 12.12.1 |\n| 12.17.0 |\n| 14.35.0 |\n| 12.18.1 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- \"A - B\" means >=A <=B.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nspanner-log has published versions; which of them is highest and meets the declared range, if any?",
  "options": [
   "12.14.0",
   "None of the listed versions meets the range",
   "12.17.0"
  ]
 },
 {
  "qid": "q30be974362",
  "kind": "yes/no",
  "text": "Subject: note on chapterloom\nDear Dorin Pavlescu,\nI hope you are well. I am writing with notes on the external packages in Ysmere Cove, particularly on how the package is used across our codebase. Thank you in advance for your thoughts when you have a moment.\nWith thanks,\nthe maintainer\n\nDeclared range for chapterloom in project ysmere-cove (npm style): 0.0.3 - 0.3.2\n\nPublished versions of chapterloom: 3.0.2, 0.3.1, 0.3.2, 0.1.2, 0.2.1, 0.0.4, 0.0.3\nVersion under review: 0.1.2",
  "question": "Does the version under review, 0.1.2, meet the declared range of chapterloom?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1ddfec4061",
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
  "qid": "qe9e125ea8f",
  "kind": "yes/no",
  "text": "What: mossfeed\nWhere: Fernhollow Tour tree\nContact: Hugo Saldana\nTodo: read the tree and write it up.\n\nDeclared specifiers for mossfeed in project fernhollow-tour (Python packaging style): ~=4.23\n\nPublished versions of mossfeed: 3.10, 5.0, 4.28, 4.23rc1, 4.25, 4.23.post3, 5.37\nVersion under review: 4.23.post3",
  "question": "Taking every line of the rules into account, does version 4.23.post3 meet the declared range of mossfeed?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qeb0e1aa615",
  "kind": "yes/no",
  "text": "Topic: map the stall-feed package's call paths into Orchard Crate\nOwner: Gunnar Lindfors\nModule: request handling\nDetails: paths listed by file, with function names and argument types written beside them.\n\nDeclared specifiers for stall-feed in project orchard-crate (Python packaging style): ~=2.8.11\n\nPublished versions of stall-feed: 2.8.0rc1, 2.8.14, 2.8.11b2, 2.6.20\nVersion under review: 2.8.14",
  "question": "Across the card, does version 2.8.14 fail to meet the declared range that stall-feed specifies?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qe2352d09ca",
  "kind": "yes/no",
  "text": "[ci] job=external-package-check project=Pan Ration Tally maintainer=Rohan Desai owner=the reviewers\n[ci] reason=start-up timing of the external package looked odd in the pipeline run, so reviewers were asked to go over it before this change lands, and the timing data sits in the job log.\n\nDeclared specifiers for portion-map in project pan-ration-tally (Python packaging style): ==9.24.*\n\nPublished versions of portion-map: 9.24.2.post3, 9.24.0.post2, 9.22.6, 9.24.5, 9.24.5.post2, 9.24.2\nVersion under review: 9.22.6",
  "question": "Did the version 9.22.6 land outside the declared range set by portion-map?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q9d409572a4",
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
  "qid": "q409b994b19",
  "kind": "yes/no",
  "text": "Release prep: Brevlin Exchange dependency look\nOskar Lindahl maintains Brevlin Exchange. The external package came up while the planning sync was going over the release list, and the calls it reaches for are being traced by the team, so a look in the review session is the plan.\n\npackage.json of the project:\n{\"name\": \"brevlin-exchange\", \"dependencies\": {\"seedling-tally\": \"~0.3.20\"}}\n\nPublished versions of seedling-tally:\n| version |\n|---|\n| 0.4.0 |\n| 0.3.11 |\n| 0.3.22 |\n| 0.3.22-beta.2 |\n| 0.13.18 |\nVersion under review: 0.3.11",
  "question": "On this card, does version 0.3.11 of seedling-tally meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qe642bc9e89",
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
  "qid": "q83737a363b",
  "kind": "choice",
  "text": "Subject: check the pewsheet-lib entry in the Carrowdell Vale manifest\nAssignee: Lerato Dube\nArea: manifest and lock file\nDetails: list the lines that reference the package and keep the write-up to what the manifest itself states.\n\npackage.json of the project:\n{\"name\": \"carrowdell-vale\", \"dependencies\": {\"pewsheet-lib\": \"~4.0.4-alpha.3 || ^3.4.6\"}}\n\nPublished versions of pewsheet-lib:\n| version |\n|---|\n| 3.5.4 |\n| 3.4.6 |\n| 3.14.4 |\n| 4.0.6 |\n| 4.0.4 |\n| 3.6.5 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nLooking over the published versions of pewsheet-lib, which version does the resolver install?",
  "options": [
   "3.6.5",
   "None of the listed versions meets the range",
   "4.0.6",
   "3.4.6"
  ]
 },
 {
  "qid": "q11f8ed2093",
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
  "qid": "qfd8e9c221e",
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
  "qid": "q2080566f16",
  "kind": "yes/no",
  "text": "Spindle Counter is maintained by Ottilie Brandt, who keeps the list of external packages tidy.\nThe reminder sending code relies on an external package, and that is the part we want to look at.\nWe want to check how it starts, what it calls, and how its errors show up in the logs.\n\nDeclared specifiers for gallerytally in project spindle-counter (Python packaging style): ==7.18.*\n\nPublished versions of gallerytally: 7.20.8.post3, 7.18.8a1, 7.28.0, 7.20.8, 7.18.7.post3, 7.18.0\nVersion under review: 7.20.8",
  "question": "Is version 7.20.8 of gallerytally not meeting the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6211e0b9a6",
  "kind": "choice",
  "text": "Release file, Gimlet Matinee\nIs there a colleague free to look over the chalkline-grid package before we close these notes? Prepared by Ruairi Calloway.\n\npackage.json of the project:\n{\"name\": \"gimlet-matinee\", \"dependencies\": {\"chalkline-grid\": \">1.9.11 <=1.10.0\"}}\n\nPublished versions of chalkline-grid: 1.9.13-rc.1, 1.9.11-rc.1, 1.9.14, 2.4.39, 1.9.15",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nRead through these rules, which listed version of chalkline-grid gets installed by the resolver, if any?",
  "options": [
   "1.9.15",
   "None of the listed versions meets the range",
   "2.4.39"
  ]
 },
 {
  "qid": "q76c3f8ad18",
  "kind": "choice",
  "text": "Eyes wanted on this PR, which changes the glaze-timer entry in Brenmoor Studio. Yusuf Akkaya, your read on it is gold.\n\nDeclared range for glaze-timer in project brenmoor-studio (npm style): >=3.0.22 <3.1.0\n\nPublished versions of glaze-timer: 3.0.23, 3.1.4, 3.1.22, 3.0.24-beta.2, 3.0.22, 4.4.15, 3.2.13",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUsing the declared range of glaze-timer, which listed version is the highest that the resolver installs?",
  "options": [
   "None of the listed versions meets the range",
   "3.0.23",
   "3.1.22",
   "3.2.13"
  ]
 },
 {
  "qid": "q959f77f6dc",
  "kind": "choice",
  "text": "Anders Westlund, the chalkbag-slot change in Rivet Loft touches the import site in the loader module, and the call site is recorded in the description.\n\nDeclared range for chalkbag-slot in project rivet-loft (npm style): ^4.5.5\n\nPublished versions of chalkbag-slot: 4.5.6, 5.0.4, 4.7.5, 3.0.5, 7.3.5, 4.5.5, 4.5.2",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nIn accordance with the declared range of chalkbag-slot, which listed version would the resolver install?",
  "options": [
   "4.7.5",
   "5.0.4",
   "7.3.5",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qcc3ca9f813",
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
  "qid": "q9e0c0d2a53",
  "kind": "yes/no",
  "text": "Checked the berthledger change line by line against the dependency manifest for Sedgehollow Moorings. Detailed comments sit in the thread for Tavita Sefo to read through.\n\nDeclared range for berthledger in project sedgehollow-moorings (npm style): ^8.12.0-beta.2\n\nPublished versions of berthledger: 8.12.7, 8.12.0-rc.2, 8.12.1, 9.2.2\nVersion under review: 9.2.2",
  "question": "Reading the card closely and applying these rules, would version 9.2.2 of berthledger meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q81d20d58d9",
  "kind": "yes/no",
  "text": "Prep notes, Rivet Loft\nNaledi Mahlangu asks a colleague to take a look at the routeplan package before the notes are final.\n\nDeclared range for routeplan in project rivet-loft (npm style): ^2.4.8-alpha.3\n\nPublished versions of routeplan: 4.7.7, 2.5.0, 3.2.0, 2.3.9\nVersion under review: 2.5.0",
  "question": "Is version 2.5.0 of routeplan not meeting the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q0988f218ad",
  "kind": "yes/no",
  "text": "refuge-slot. External package. Used by the Hearth Saddle build. Contact for questions: Thandiwe Mokoena. Review when touched.\n\nDeclared specifiers for refuge-slot in project hearth-saddle (Python packaging style): ==9.9.*\n\nPublished versions of refuge-slot: 9.7.10, 9.9.24a1, 9.19.34, 9.11.10, 9.9.24\nVersion under review: 9.19.34",
  "question": "By these rules, would 9.19.34 of refuge-slot lie outside the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q518e07d0b0",
  "kind": "choice",
  "text": "Subject: check the berth-calendar entry in the Murrelet Kelp manifest\nAssignee: Sunniva Hauge\nArea: manifest and lock file\nDetails: list the lines that reference the package and keep the write-up to what the manifest itself states.\n\nDeclared range for berth-calendar in project murrelet-kelp (npm style): ^8.9.9\n\nPublished versions of berth-calendar: 8.9.9, 9.0.1, 9.0.0, 8.7.9, 7.1.0",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nIn plain words, which listed version of berth-calendar counts as the highest meeting the range, if any?",
  "options": [
   "8.7.9",
   "None of the listed versions meets the range",
   "8.9.9"
  ]
 },
 {
  "qid": "qe65d351cb1",
  "kind": "yes/no",
  "text": "Hi Ottilie Brandt,\nHere is a quick heads-up on the housekeeping list for Spindle Counter. I am looking at the gallerytally package entry, noting where it lives in the repo. Let me know your thoughts when you get the chance.\nCheers,\nthe maintainer\n\npackage.json of the project:\n{\"name\": \"spindle-counter\", \"dependencies\": {\"gallerytally\": \"7.3.7\"}}\n\nPublished versions of gallerytally:\n| version |\n|---|\n| 7.3.7 |\n| 6.6.7 |\n| 8.7.7 |\n| 7.4.9 |\nVersion under review: 7.3.7",
  "question": "Across the card, does version 7.3.7 fail to meet the declared range that gallerytally specifies?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb699de0f39",
  "kind": "yes/no",
  "text": "Subject: Fresh look at the plate-register package\nHi Ngozi Eke,\nMind taking a look at how Bradawl Folio leans on it? My notes are below, and my reading of them feels a bit tangled. Eyes from a colleague are welcome. Thanks in advance.\nBest,\nthe maintainer\n\nDeclared range for plate-register in project bradawl-folio (npm style): ^19.9.4 || =0.0.13\n\nPublished versions of plate-register: 20.1.0, 19.10.4, 1.4.12, 19.8.5\nVersion under review: 20.1.0",
  "question": "Is version 20.1.0 of plate-register outside the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q0d0feac073",
  "kind": "yes/no",
  "text": "Regular dependency review, item for Crank Ledger\nThe bearing-lane package turned up on the list during the regular pass. Hana Kobayashi agreed to write up the findings for the group.\n\nDeclared range for bearing-lane in project crank-ledger (npm style): ~2.13.7\n\nPublished versions of bearing-lane: 0.22.8, 2.13.7, 2.14.7, 2.11.7\nVersion under review: 2.14.7",
  "question": "Is it true that version 2.14.7 does not meet the declared range of bearing-lane?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q78d1e88e40",
  "kind": "yes/no",
  "text": "Brevlin Exchange is maintained by Oskar Lindahl, who keeps the list of external packages tidy.\nThe reminder sending code relies on an external package, and that is the part we want to look at.\nWe want to check how it starts, what it calls, and how its errors show up in the logs.\n\npackage.json of the project:\n{\"name\": \"brevlin-exchange\", \"dependencies\": {\"pollen-pair\": \"^8.7.4\"}}\n\nPublished versions of pollen-pair:\n| version |\n|---|\n| 8.7.5 |\n| 8.7.4-alpha |\n| 8.17.5 |\n| 8.7.4 |\n| 8.9.0 |\nVersion under review: 8.7.4",
  "question": "Regarding pollen-pair, does version 8.7.4 meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa48190378c",
  "kind": "yes/no",
  "text": "Housekeeping for the release preparation of Brevlin Exchange\nThe seedling-tally package is tidied in the dependency section, with Oskar Lindahl keeping its entry in order.\n\nDeclared specifiers for seedling-tally in project brevlin-exchange (Python packaging style): >=0.9.1b2, <1.0\n\nPublished versions of seedling-tally: 0.11.3, 0.14.2, 0.8.2, 0.9.1, 0.10.0b2\nVersion under review: 0.10.0b2",
  "question": "Is it correct that version 0.10.0b2 of seedling-tally does not meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qc5514287d0",
  "kind": "yes/no",
  "text": "Going through the cohort-matrix package as part of the dependency sweep for Chalk Register.\nJonah Abernathy has the notes, so shout when you see it.\n\npyproject.toml of the project:\n[project]\nname = \"chalk-register\"\ndependencies = [\n  \"cohort-matrix >=6.3.8, !=6.4, <6.8\",\n]\n\nPublished versions of cohort-matrix:\n| version |\n|---|\n| 6.3.4 |\n| 6.3.9.post1 |\n| 6.6.0 |\n| 6.3.7 |\n| 6.1.7 |\nVersion under review: 6.6.0",
  "question": "Based on the card, does 6.6.0 fail to meet the range declared for cohort-matrix?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q437e94504a",
  "kind": "choice",
  "text": "quick background on the package thing: Saoirse Quinlan maintains Corvellan Perch, and the planning sync flagged the external package again\nso we want a short sync on which code paths lean on it\nbring the import list and whatever you have on the calls\n\nDeclared specifiers for plumage-atlas in project corvellan-perch (Python packaging style): ~=3.10\n\nPublished versions of plumage-atlas: 3.10.post2, 3.9, 4.0, 2.19, 4.27, 3.8, 3.12",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version of plumage-atlas would the resolver install under these rules, if any, given the declared range?",
  "options": [
   "3.12",
   "2.19",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q47319bcd5e",
  "kind": "yes/no",
  "text": "Touches the macro-sum entry in Pan Ration Tally's manifest. Lock churn too. Reason? Asked by Rohan Desai.\n\nDeclared specifiers for macro-sum in project pan-ration-tally (Python packaging style): <=9.1\n\nPublished versions of macro-sum: 9.1, 9.3, 10.4, 9.1.post2, 9.3.post2\nVersion under review: 10.4",
  "question": "Can version 10.4 of macro-sum be said to meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q5ee309c06b",
  "kind": "yes/no",
  "text": "Summary: request for a careful review of the gauge-convert package\nOwner: Anand Iyer\nComponent: Thistle Fennel dependencies\nNotes: please take the matter in good order at your convenience.\n\nDeclared specifiers for gauge-convert in project thistle-fennel (Python packaging style): >8.3.7a1, <9.0\n\nPublished versions of gauge-convert: 8.1.8, 8.6.8, 8.4.7, 8.4.0b2, 8.3.11, 8.3.7a1, 8.3.7.post1\nVersion under review: 8.4.7",
  "question": "Is 8.4.7 falling outside the range of gauge-convert?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q89f263b225",
  "kind": "choice",
  "text": "Elif Arslan, with respect, kindly describe the blaze-marker change in the pull request body before merging. Thanks a lot for the thoughtful work across Fir Cairn Route.\n\nDeclared range for blaze-marker in project fir-cairn-route (npm style): >6.0.21 <6.1.0\n\nPublished versions of blaze-marker: 6.4.27, 6.0.21-beta, 7.7.23, 6.1.0, 5.2.37, 6.0.22",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGoing by the card, which listed version of blaze-marker does the resolver install, if any?",
  "options": [
   "6.0.22",
   "None of the listed versions meets the range",
   "6.4.27"
  ]
 },
 {
  "qid": "q20254fdc1b",
  "kind": "choice",
  "text": "Look into the external package for Mooring Almanac\nThanks to the team for the quick read. Ngozi Ibeh maintains Mooring Almanac, and this issue asks for a review session on the calls the code makes into the package, so that the picture stays clear.\n\npyproject.toml of the project:\n[project]\nname = \"mooring-almanac\"\ndependencies = [\n  \"fathom-gauge >=6.15.7, <7.0\",\n]\n\nPublished versions of fathom-gauge:\n| version |\n|---|\n| 6.14.7 |\n| 7.27.9 |\n| 6.13.9 |\n| 6.15.6 |\n| 7.3.0 |\n| 7.0.0 |\n| 6.16.9 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPursuant to these rules, which listed version of fathom-gauge does the resolver install?",
  "options": [
   "None of the listed versions meets the range",
   "6.16.9",
   "6.13.9"
  ]
 },
 {
  "qid": "q3c6e58a9da",
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
  "qid": "q75d9bcef1a",
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
  "qid": "q0171387602",
  "kind": "choice",
  "text": "Hi team,\nPassing the furniture-kit work in Quoin Stanza over to you. The notes are in the team folder and you know where the files live.\nThanks,\nZoltan Halasz\n\nDeclared specifiers for furniture-kit in project quoin-stanza (Python packaging style): >=8.7.4b2, <9.0\n\nPublished versions of furniture-kit: 9.1.0, 8.7.3, 9.6.0, 8.5.5, 7.9.5, 9.0.0",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich highest listed version of furniture-kit meets the declared range, if any?",
  "options": [
   "None of the listed versions meets the range",
   "9.6.0",
   "9.0.0",
   "9.1.0"
  ]
 },
 {
  "qid": "qeae85f58cd",
  "kind": "choice",
  "text": "Summary: routine housekeeping on the lichenboard package\nOwner: Tariq Rahimi\nComponent: Larkspur Tramline tooling\nNotes: standard tidy-up of the usual entries.\n\nDeclared range for lichenboard in project larkspur-tramline (npm style): >2.21.22 <2.22.0 || ^5.14.11\n\nPublished versions of lichenboard: 5.15.0, 2.21.23, 7.16.31, 2.21.25, 5.16.39",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- Parts separated by spaces must all hold.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nAcross everything listed for lichenboard, which version would the resolver end up installing, if any?",
  "options": [
   "2.21.25",
   "5.16.39",
   "None of the listed versions meets the range",
   "2.21.23"
  ]
 },
 {
  "qid": "q7a995b9e94",
  "kind": "choice",
  "text": "Our dependency packages are tracked on this page for Pantry Index. The crumbmap package sits on the tidy-up list, and Idris Kamara owns the basics.\n\nDeclared specifiers for crumbmap in project pantry-index (Python packaging style): ~=1.10\n\nPublished versions of crumbmap: 1.9, 1.10rc1, 0.26, 1.8, 1.10a1, 2.12",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version, being the highest that meets the declared range, does the resolver install for crumbmap, if any?",
  "options": [
   "2.12",
   "None of the listed versions meets the range",
   "0.26"
  ]
 },
 {
  "qid": "qb04bb780a3",
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
  "qid": "qc5a5ea914d",
  "kind": "choice",
  "text": "Summary: a bit of context on the aliquot-map package\nOwner: Kwame Asamoah\nComponent: Sedge Marl\nNotes: the team has been talking about this for a while, so it is worth a careful read.\n\npyproject.toml of the project:\n[project]\nname = \"sedge-marl\"\ndependencies = [\n  \"aliquot-map >=8.2, !=8.3, <8.7\",\n]\n\nPublished versions of aliquot-map: 7.2, 8.2, 8.4, 8.5",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich of aliquot-map's listed versions gets installed by the resolver?",
  "options": [
   "8.4",
   "8.5",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q02597602de",
  "kind": "choice",
  "text": "Subject: Fernhollow Tour dependency look\nHello team,\nHugo Saldana maintains Fernhollow Tour, and the planning sync has asked for a short look at how the code uses the external package.\nI would like the review session to go over the calls that reach into it, and to highlight the ones that matter most.\nThanks,\nA colleague\n\nDeclared range for rainbeacon in project fernhollow-tour (npm style): ~1.26.2\n\nPublished versions of rainbeacon: 0.15.1, 1.26.0, 1.26.2-rc.2, 2.26.2, 1.26.3, 0.36.2, 1.26.2",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nMeasured against the declared range, which listed version of rainbeacon is the top match, if any?",
  "options": [
   "0.36.2",
   "None of the listed versions meets the range",
   "2.26.2",
   "1.26.3"
  ]
 },
 {
  "qid": "qc0572ea60a",
  "kind": "choice",
  "text": "I am asking Tariq Rahimi to read the section on birchpanel in the Larkspur Tramline notes. Please look closely at the wording and tell me where it is hard to follow.\n\nDeclared range for birchpanel in project larkspur-tramline (npm style): 4.4.x\n\nPublished versions of birchpanel: 4.8.1, 4.5.1, 3.1.1, 7.7.2, 4.4.0-alpha, 1.6.5",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version of birchpanel, from its listed set, gets installed by the resolver, if any?",
  "options": [
   "4.8.1",
   "7.7.2",
   "None of the listed versions meets the range",
   "4.5.1"
  ]
 },
 {
  "qid": "q480be97f1c",
  "kind": "yes/no",
  "text": "Housekeeping for the release preparation of Spindle Counter\nThe gallerytally package is tidied in the dependency section, with Ottilie Brandt keeping its entry in order.\n\npyproject.toml of the project:\n[project]\nname = \"spindle-counter\"\ndependencies = [\n  \"gallerytally ==7.18.*\",\n]\n\nPublished versions of gallerytally: 7.20.8.post3, 7.18.8a1, 7.28.0, 7.20.8, 7.18.7.post3, 7.18.0\nVersion under review: 7.20.8",
  "question": "Among the listed versions of gallerytally, does version 7.20.8 meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q38688d165e",
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
  "qid": "qad0afa8b4f",
  "kind": "choice",
  "text": "This PR touches the hewnsight package in Gimlet Matinee, which we have been side-stepping for ages.\nBackground: the team has grown a lot since the project began, so Ewa Lindqvist knows the history best.\n\npackage.json of the project:\n{\"name\": \"gimlet-matinee\", \"dependencies\": {\"hewnsight\": \"5.5.x || ^0.0.5\"}}\n\nPublished versions of hewnsight:\n| version |\n|---|\n| 0.0.7-rc.1 |\n| 0.0.5-rc.1 |\n| 4.2.4 |\n| 6.7.4 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich of hewnsight's listed versions gets installed by the resolver?",
  "options": [
   "6.7.4",
   "None of the listed versions meets the range",
   "4.2.4"
  ]
 },
 {
  "qid": "q86e751ccff",
  "kind": "choice",
  "text": "[handover] to=Ilse Varholm area=dependency-notes\n[handover] package=crumbtray repo=Mirrask Platter mode=carry-forward\n\nDeclared range for crumbtray in project mirrask-platter (npm style): 7.0.x\n\nPublished versions of crumbtray: 7.0.2, 7.2.3, 7.0.3, 7.1.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nLooking over the published versions of crumbtray, which version does the resolver install?",
  "options": [
   "7.1.3",
   "None of the listed versions meets the range",
   "7.2.3",
   "7.0.3"
  ]
 },
 {
  "qid": "q7f02ced1a3",
  "kind": "choice",
  "text": "Handing you the berthledger question for Sedgehollow Moorings since our side is swamped.\nTavita Sefo made a pass at it, so start there.\n\nDeclared specifiers for berthledger in project sedgehollow-moorings (Python packaging style): ~=3.15\n\nPublished versions of berthledger: 3.18, 2.35, 4.0, 4.38, 3.14, 3.16rc1, 3.13",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhat is the listed berthledger version the resolver lands on, if any?",
  "options": [
   "3.18",
   "4.38",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q422572701c",
  "kind": "choice",
  "text": "[step=dependency_review] project=Ostrain Glaze package=ramp-schedule reviewer=Bogdan Stoica state=in_progress\n\npyproject.toml of the project:\n[project]\nname = \"ostrain-glaze\"\ndependencies = [\n  \"ramp-schedule ~=4.5.6\",\n]\n\nPublished versions of ramp-schedule:\n| version |\n|---|\n| 4.5.4 |\n| 5.1.6 |\n| 3.1.4 |\n| 4.5.6 |\n| 4.4.4 |\n| 4.7.6 |\n| 4.3.6 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUpon reviewing ramp-schedule, which listed version would the resolver install under these rules?",
  "options": [
   "None of the listed versions meets the range",
   "4.5.6",
   "4.3.6"
  ]
 }
]
