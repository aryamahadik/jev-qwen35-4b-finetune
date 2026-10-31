# G5-H blind read T36-blind_read-3df34927-000 (family T36)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/pilot_i2/g5h/answers/T36-blind_read-3df34927-000.json

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
  "qid": "qbade461d56",
  "kind": "choice",
  "text": "[job=dependency-check] reviewer=Tomasz Brenek role=onboarding lane=intro\nproject=Mirrask Platter package=crumbtray context=learning_codebase\n\nDeclared specifiers for crumbtray in project mirrask-platter (Python packaging style): ==1.7.*\n\nPublished versions of crumbtray: 1.5.1, 1.7.2, 1.17.1, 1.8.1, 1.7.3, 1.6.0, 0.0.0",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPer this card, what would the resolver end up installing from the listed versions of crumbtray, if any?",
  "options": [
   "None of the listed versions meets the range",
   "1.7.3",
   "1.5.1"
  ]
 },
 {
  "qid": "qffd4c3c7b4",
  "kind": "yes/no",
  "text": "This PR touches the dressing-lattice package in Mirrask Platter, which we have been side-stepping for ages.\nBackground: the team has grown a lot since the project began, so Tomasz Brenek knows the history best.\n\nDeclared range for dressing-lattice in project mirrask-platter (npm style): 11.8.3 || 6.21.x\n\nPublished versions of dressing-lattice: 6.21.25, 6.21.0, 6.21.22, 11.6.2\nVersion under review: 6.21.25",
  "question": "With respect to these rules, does version 6.21.25 of dressing-lattice fail to meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf343e7ba6d",
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
  "qid": "q01754e0bde",
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
  "qid": "q1759583556",
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
  "qid": "q382498df08",
  "kind": "yes/no",
  "text": "Notes on the dependency list\nThe cohort-matrix package is listed in the Chalk Register manifest, and Mirela Popescu is writing up why.\n\nDeclared range for cohort-matrix in project chalk-register (npm style): ^12.16.8-beta\n\nPublished versions of cohort-matrix: 12.16.10-rc.1, 12.16.8-beta, 11.26.7, 12.16.9\nVersion under review: 12.16.9",
  "question": "Is the version identified as 12.16.9 situated outside the declared range of the package cohort-matrix?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf750f15ec3",
  "kind": "choice",
  "text": "Subject: module list for the dependency section\nDear Anand Iyer,\nI traced the cable-chart package through its import sites in Thistle Fennel and recorded the call sites in the notes. The module list is saved in the team folder.\nKind regards\n\nDeclared range for cable-chart in project thistle-fennel (npm style): ^5.8.2\n\nPublished versions of cable-chart: 2.6.2, 4.2.3, 6.1.1, 6.0.0, 5.8.2-rc.2, 4.2.0, 6.0.5",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nIn plain words, which listed version of cable-chart counts as the highest meeting the range, if any?",
  "options": [
   "6.1.1",
   "4.2.3",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qb31f7f8007",
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
  "qid": "qa043af3e3c",
  "kind": "choice",
  "text": "Subject: short note on Mallet Pantry Rota\nHi Wanjiru Kamau.\nCallers of the pallet-sorter package are listed. Reply at your leisure.\nThanks\n\nDeclared specifiers for pallet-sorter in project mallet-pantry-rota (Python packaging style): ~=1.1.8\n\nPublished versions of pallet-sorter: 2.0.0, 1.1.9, 2.0.9, 1.1.8",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version would the resolver take under these rules for the package pallet-sorter, if any?",
  "options": [
   "2.0.9",
   "1.1.9",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qfe8f3aea07",
  "kind": "choice",
  "text": "Package check, Mallet Pantry Rota\npallet-sorter came up in the review. Wanjiru Kamau owns it. Details to follow.\n\nDeclared specifiers for pallet-sorter in project mallet-pantry-rota (Python packaging style): >=3.13.5, !=3.14.0, <3.15\n\nPublished versions of pallet-sorter: 2.19.5, 3.13.5b2, 4.25.5, 3.16.5",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nOf the listed versions, which is the highest meeting the declared range of pallet-sorter, if any?",
  "options": [
   "4.25.5",
   "2.19.5",
   "3.16.5",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q3da0426808",
  "kind": "choice",
  "text": "[log] mood=easygoing reviewer=Thandiwe Mokoena subject=cornice-hold target=Hearth Saddle\n\npackage.json of the project:\n{\"name\": \"hearth-saddle\", \"dependencies\": {\"cornice-hold\": \"2.9.x\"}}\n\nPublished versions of cornice-hold:\n| version |\n|---|\n| 2.9.0-rc.1 |\n| 2.9.3 |\n| 1.7.0 |\n| 2.8.2 |\n| 3.8.0 |\n| 5.3.0 |\n| 2.7.4 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith these rules applied to cornice-hold, which listed version would the resolver settle on, if any?",
  "options": [
   "None of the listed versions meets the range",
   "2.8.2",
   "2.9.3"
  ]
 },
 {
  "qid": "q73d7e66493",
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
  "qid": "q43ccb42259",
  "kind": "choice",
  "text": "[step=dependency_review] project=Ostrain Glaze package=ramp-schedule reviewer=Bogdan Stoica state=in_progress\n\npyproject.toml of the project:\n[project]\nname = \"ostrain-glaze\"\ndependencies = [\n  \"ramp-schedule ~=4.5.6\",\n]\n\nPublished versions of ramp-schedule:\n| version |\n|---|\n| 4.5.4 |\n| 5.1.6 |\n| 3.1.4 |\n| 4.5.6 |\n| 4.4.4 |\n| 4.7.6 |\n| 4.3.6 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUpon reviewing ramp-schedule, which listed version would the resolver install under these rules?",
  "options": [
   "None of the listed versions meets the range",
   "4.5.6",
   "4.3.6"
  ]
 },
 {
  "qid": "q5137abba2d",
  "kind": "yes/no",
  "text": "Housekeeping for the release preparation of Spindle Counter\nThe gallerytally package is tidied in the dependency section, with Ottilie Brandt keeping its entry in order.\n\npyproject.toml of the project:\n[project]\nname = \"spindle-counter\"\ndependencies = [\n  \"gallerytally ==7.18.*\",\n]\n\nPublished versions of gallerytally: 7.20.8.post3, 7.18.8a1, 7.28.0, 7.20.8, 7.18.7.post3, 7.18.0\nVersion under review: 7.20.8",
  "question": "Among the listed versions of gallerytally, does version 7.20.8 meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd06e12f441",
  "kind": "yes/no",
  "text": "I am asking Rohan Desai to read the section on kcal-table in the Pan Ration Tally notes. Please look closely at the wording and tell me where it is hard to follow.\n\nDeclared specifiers for kcal-table in project pan-ration-tally (Python packaging style): <=4.25.12\n\nPublished versions of kcal-table: 4.24.35, 4.25.12, 4.26.15, 4.25.9\nVersion under review: 4.26.15",
  "question": "Is version 4.26.15 outside the declared range of kcal-table?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q0f7bb98c75",
  "kind": "yes/no",
  "text": "Housekeeping for the release preparation of Brevlin Exchange\nThe seedling-tally package is tidied in the dependency section, with Oskar Lindahl keeping its entry in order.\n\nDeclared specifiers for seedling-tally in project brevlin-exchange (Python packaging style): >=0.9.1b2, <1.0\n\nPublished versions of seedling-tally: 0.11.3, 0.14.2, 0.8.2, 0.9.1, 0.10.0b2\nVersion under review: 0.10.0b2",
  "question": "Is it correct that version 0.10.0b2 of seedling-tally does not meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qbc0ab35e82",
  "kind": "yes/no",
  "text": "Checked the berthledger change line by line against the dependency manifest for Sedgehollow Moorings. Detailed comments sit in the thread for Tavita Sefo to read through.\n\nDeclared range for berthledger in project sedgehollow-moorings (npm style): ^8.12.0-beta.2\n\nPublished versions of berthledger: 8.12.7, 8.12.0-rc.2, 8.12.1, 9.2.2\nVersion under review: 9.2.2",
  "question": "Reading the card closely and applying these rules, would version 9.2.2 of berthledger meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qba3b3e94cd",
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
  "qid": "q183ad73cd8",
  "kind": "choice",
  "text": "Thank you, team: Orchard Crate release prep\nMariam Haidari maintains Orchard Crate, and thanks go to all who helped look into the external package. The sync write-ups made the work easy to follow, and the review session went well, so the release can carry on with a clear picture of this dependency.\n\nDeclared specifiers for crate-label in project orchard-crate (Python packaging style): >=6.12, !=6.13.0, <6.17\n\nPublished versions of crate-label: 7.11, 5.16, 6.16, 6.12, 6.19, 7.0",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWould you kindly indicate which listed version of crate-label the resolver installs under these rules?",
  "options": [
   "6.16",
   "None of the listed versions meets the range",
   "5.16",
   "6.12"
  ]
 },
 {
  "qid": "q15fb5e3840",
  "kind": "choice",
  "text": "Touches the glaze-timer entry in Brenmoor Studio's manifest. Lock churn too. Reason? Asked by Yusuf Akkaya.\n\nDeclared range for glaze-timer in project brenmoor-studio (npm style): ^0.0.5\n\nPublished versions of glaze-timer: 0.0.5-alpha, 0.0.7-alpha, 0.3.4, 0.0.6, 0.1.6, 2.3.5, 0.2.0",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed glaze-timer version is the highest that meets the range?",
  "options": [
   "0.3.4",
   "None of the listed versions meets the range",
   "2.3.5",
   "0.1.6"
  ]
 },
 {
  "qid": "q79268e6b57",
  "kind": "choice",
  "text": "[ci] job=external-package-check project=Crank Ledger maintainer=Declan Murray owner=the reviewers\n[ci] reason=start-up timing of the external package looked odd in the pipeline run, so reviewers were asked to go over it before this change lands, and the timing data sits in the job log.\n\nDeclared range for elevation-map in project crank-ledger (npm style): 8.26.8 - 8.28.8\n\nPublished versions of elevation-map: 8.26.10-beta.2, 8.29.7, 8.30.8, 6.15.0, 8.26.8-alpha",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nMeasured against the declared range, which listed version of elevation-map is the top match, if any?",
  "options": [
   "8.29.7",
   "None of the listed versions meets the range",
   "8.30.8"
  ]
 },
 {
  "qid": "q98bf0d1c13",
  "kind": "yes/no",
  "text": "Thank you, team: Thistle Fennel release prep\nItzel Ramirez maintains Thistle Fennel, and thanks go to all who helped look into the external package. The sync write-ups made the work easy to follow, and the review session went well, so the release can carry on with a clear picture of this dependency.\n\nDeclared range for cable-chart in project thistle-fennel (npm style): =0.0.2\n\nPublished versions of cable-chart: 0.0.2, 0.2.2, 0.0.4-rc.1, 3.4.2\nVersion under review: 0.0.2",
  "question": "Under these rules, and reading the declared range for cable-chart as written, does version 0.0.2 not meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q4ed5544961",
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
  "qid": "q10af46c036",
  "kind": "yes/no",
  "text": "handing the external package look over to you, it is yours from here\nAyesha Rahman maintains Reed Lichen Queue, so send the open questions to them directly.\nthe calls into the package are mapped, and the rest is a walk through the tests\n\nDeclared specifiers for dampen-roll in project reed-lichen-queue (Python packaging style): >=4.18.3, <4.19\n\nPublished versions of dampen-roll: 4.22.2, 4.18.4, 4.18.3, 4.19.1, 4.18.3.post2, 4.28.3\nVersion under review: 4.18.4",
  "question": "Plainly, is version 4.18.4 sitting outside the declared range for dampen-roll?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q5636d6930e",
  "kind": "yes/no",
  "text": "Topic: map the stall-feed package's call paths into Orchard Crate\nOwner: Gunnar Lindfors\nModule: request handling\nDetails: paths listed by file, with function names and argument types written beside them.\n\nDeclared specifiers for stall-feed in project orchard-crate (Python packaging style): ~=2.8.11\n\nPublished versions of stall-feed: 2.8.0rc1, 2.8.14, 2.8.11b2, 2.6.20\nVersion under review: 2.8.14",
  "question": "Across the card, does version 2.8.14 fail to meet the declared range that stall-feed specifies?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa4864b252e",
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
  "qid": "q5114c904c4",
  "kind": "yes/no",
  "text": "Short entry on refuge-slot, which Hearth Saddle brings in from elsewhere. Readers use this page to see where the package shows up in the code, and Thandiwe Mokoena keeps the entry.\n\nDeclared range for refuge-slot in project hearth-saddle (npm style): 0.3.4 - 0.6.5\n\nPublished versions of refuge-slot: 0.6.5, 3.1.5, 0.3.6-rc.2, 0.7.6, 0.7.4, 0.6.6\nVersion under review: 0.3.6-rc.2",
  "question": "Is version 0.3.6-rc.2 of refuge-slot outside the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q1b3233b9de",
  "kind": "choice",
  "text": "Thanks for the tidy-up, Chiamaka Eze. Going over the card-rivet entry in the Mortise Recall manifest, the change reads as plain housekeeping, mostly reordering and comment cleanup.\n\npyproject.toml of the project:\n[project]\nname = \"mortise-recall\"\ndependencies = [\n  \"card-rivet >=17.27, <17.31\",\n]\n\nPublished versions of card-rivet:\n| version |\n|---|\n| 17.26 |\n| 17.27rc1 |\n| 18.22 |\n| 17.27 |\n| 17.28.post2 |\n| 17.37 |\n| 17.30 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhat is the listed card-rivet version the resolver lands on, if any?",
  "options": [
   "17.30",
   "17.37",
   "None of the listed versions meets the range",
   "18.22"
  ]
 },
 {
  "qid": "q98a9bc5817",
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
  "qid": "q73bc4e924b",
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
  "qid": "q89ced8314d",
  "kind": "yes/no",
  "text": "Hi Ottilie Brandt,\nHere is a quick heads-up on the housekeeping list for Spindle Counter. I am looking at the gallerytally package entry, noting where it lives in the repo. Let me know your thoughts when you get the chance.\nCheers,\nthe maintainer\n\npackage.json of the project:\n{\"name\": \"spindle-counter\", \"dependencies\": {\"gallerytally\": \"7.3.7\"}}\n\nPublished versions of gallerytally:\n| version |\n|---|\n| 7.3.7 |\n| 6.6.7 |\n| 8.7.7 |\n| 7.4.9 |\nVersion under review: 7.3.7",
  "question": "Across the card, does version 7.3.7 fail to meet the declared range that gallerytally specifies?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q799d5a2ce7",
  "kind": "yes/no",
  "text": "step=housekeeping_sweep target=qso-ledger scope=[Dunlin Heather Log] owner=Mateus Caldeira\n\nDeclared range for qso-ledger in project dunlin-heather-log (npm style): ^17.8.0\n\nPublished versions of qso-ledger: 17.18.7, 14.4.1, 17.9.5, 17.6.1\nVersion under review: 14.4.1",
  "question": "Is the version 14.4.1 of qso-ledger considered to meet the declared range under these rules?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q260ce42d74",
  "kind": "choice",
  "text": "Release prep, a friendly sweep\nThanks to Elif Arslan for the cheerful pass through Fir Cairn Route, and the contour-serve package sits on the list beside its neighbours.\n\npyproject.toml of the project:\n[project]\nname = \"fir-cairn-route\"\ndependencies = [\n  \"contour-serve ~=5.29\",\n]\n\nPublished versions of contour-serve: 6.36, 5.39, 5.27, 5.29.post1, 6.0, 5.29a1, 5.28",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGoing by the card, which listed version of contour-serve would be picked as highest that meets the range?",
  "options": [
   "5.28",
   "5.39",
   "6.36",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qae7848cc24",
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
  "qid": "qa5ac3e3453",
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
  "qid": "q9df0bfb4d2",
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
  "qid": "q2b234113ab",
  "kind": "yes/no",
  "text": "signupgrid in Brenmoor Studio, callers listed.\nIngrid Solheim on it. Quick glance, then back to you.\n\nDeclared specifiers for signupgrid in project brenmoor-studio (Python packaging style): >7.18.6rc1, <8.0\n\nPublished versions of signupgrid: 7.18.3, 7.17.6, 7.19.6.post3, 7.28.0, 7.18.9, 7.18.4, 7.18.7\nVersion under review: 7.18.4",
  "question": "Is the version identified as 7.18.4 situated outside the declared range of the package signupgrid?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q8272b0ef57",
  "kind": "yes/no",
  "text": "Background on the code we import, written by the group that set up Brenmoor Studio. The signupgrid package came out of their work on the internals, and it reaches into the core of the code. Ingrid Solheim looks after the entry and is glad to talk through how it got here.\n\npyproject.toml of the project:\n[project]\nname = \"brenmoor-studio\"\ndependencies = [\n  \"signupgrid >7.18.6rc1, <8.0\",\n]\n\nPublished versions of signupgrid: 7.18.3, 7.17.6, 7.19.6.post3, 7.28.0, 7.18.9, 7.18.4, 7.18.7\nVersion under review: 7.18.4",
  "question": "Is the version 7.18.4 of signupgrid considered to meet the declared range under these rules?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd1bb4e3256",
  "kind": "yes/no",
  "text": "Thanks all, this is a helpful look at the external package and the thread so far has been useful. As maintainer of Hearth Saddle, Lukas Brandt asks that the review cover the calls the code really makes, since a clear picture of those calls will help the review session.\n\npackage.json of the project:\n{\"name\": \"hearth-saddle\", \"dependencies\": {\"bunk-ledger\": \"^5.23.8\"}}\n\nPublished versions of bunk-ledger:\n| version |\n|---|\n| 6.0.0 |\n| 6.0.6 |\n| 5.24.7 |\n| 5.23.8 |\n| 5.23.9 |\n| 4.33.8 |\nVersion under review: 4.33.8",
  "question": "Does the version 4.33.8 meet the declared range of bunk-ledger?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q50a49b6c0f",
  "kind": "yes/no",
  "text": "External packages. Sedge Marl is maintained by Kwame Asamoah, who keeps this page tidy. The external package behind the checkout flow handles most of the page requests on the site, so any change to it gets a close look here before it lands.\n\nDeclared specifiers for freezer-grid in project sedge-marl (Python packaging style): >=8.8.9, <8.11\n\nPublished versions of freezer-grid: 8.8.9, 8.8.10.post3, 8.18.7, 8.8.11, 8.10.7.post3\nVersion under review: 8.8.11",
  "question": "Does version 8.8.11 of freezer-grid meet the declared range given in the package?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q8e94aaf753",
  "kind": "choice",
  "text": "Elif Arslan, mind taking a look at contour-serve for Fir Cairn Route?\nI'm stuck on the lookup logic, so your eyes on it are appreciated.\n\nDeclared specifiers for contour-serve in project fir-cairn-route (Python packaging style): ~=8.19.3\n\nPublished versions of contour-serve: 8.20.3, 9.19.3, 8.17.3, 8.19.3rc1, 9.0.0, 8.21.0, 8.19.2",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPursuant to these rules, which listed version of contour-serve does the resolver install?",
  "options": [
   "None of the listed versions meets the range",
   "8.17.3",
   "8.19.2",
   "9.19.3"
  ]
 },
 {
  "qid": "qc8fa7dfbca",
  "kind": "yes/no",
  "text": "[step=dependency-look] project=Dunlin Heather Log maintainer=Mateus Caldeira\nreason=the planning sync flagged the external package in the import list, so the team asked for a careful walk through each code path that calls it, and the reviewer is still to be picked for the review session.\n\nDeclared range for qso-ledger in project dunlin-heather-log (npm style): 8.14.3 - 8.16.3\n\nPublished versions of qso-ledger: 6.39.3, 8.13.3, 8.12.0, 8.16.2, 8.14.3-beta.2, 8.14.0, 8.16.4\nVersion under review: 8.14.3-beta.2",
  "question": "Taking the declared range of qso-ledger as the standard, would version 8.14.3-beta.2 fail to meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q803ec56e98",
  "kind": "choice",
  "text": "Summary: check how the berthledger package is used in Sedgehollow Moorings\nOwner: Tavita Sefo\nComponent: dependency notes\nNotes: plain and brief look at the code\n\npackage.json of the project:\n{\"name\": \"sedgehollow-moorings\", \"dependencies\": {\"berthledger\": \"^0.0.9\"}}\n\nPublished versions of berthledger: 0.0.11-alpha.3, 0.0.9-beta.2, 0.0.10, 0.0.16, 0.0.8, 0.0.5",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nAcross everything listed for berthledger, which version would the resolver end up installing, if any?",
  "options": [
   "0.0.16",
   "0.0.10",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q58a747113e",
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
  "qid": "q6890f3e272",
  "kind": "choice",
  "text": "Check the berth-calendar entry in Murrelet Kelp\nSmall note from Dariusz Kowal: the entry sits in the dependency file and it is waiting for a look.\n\nDeclared range for berth-calendar in project murrelet-kelp (npm style): ~1.5.2\n\nPublished versions of berth-calendar: 1.5.2, 1.3.0, 1.6.0, 1.15.2, 0.5.2",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nMeasured against the declared range of berth-calendar, which listed version is highest and meets it, if any?",
  "options": [
   "None of the listed versions meets the range",
   "1.5.2",
   "0.5.2"
  ]
 },
 {
  "qid": "q97a11ce25f",
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
  "qid": "q652944dfb4",
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
  "qid": "q766b2166f6",
  "kind": "choice",
  "text": "Summary: a bit of context on the chalkline-grid package\nOwner: Ruairi Calloway\nComponent: Gimlet Matinee\nNotes: the team has been talking about this for a while, so it is worth a careful read.\n\nDeclared range for chalkline-grid in project gimlet-matinee (npm style): >9.16.0 <=9.17.0 || ^3.12.9\n\nPublished versions of chalkline-grid:\n| version |\n|---|\n| 9.16.0 |\n| 3.10.8 |\n| 3.12.9-beta.2 |\n| 9.14.6 |\n| 9.15.0 |\n| 4.1.8 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- Parts separated by spaces must all hold.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGiven the card, which listed version does the resolver install for chalkline-grid?",
  "options": [
   "None of the listed versions meets the range",
   "9.15.0",
   "9.16.0"
  ]
 },
 {
  "qid": "qb056c51ba0",
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
  "qid": "qa2d3ce24e1",
  "kind": "choice",
  "text": "Release file, Gimlet Matinee\nIs there a colleague free to look over the chalkline-grid package before we close these notes? Prepared by Ruairi Calloway.\n\npackage.json of the project:\n{\"name\": \"gimlet-matinee\", \"dependencies\": {\"chalkline-grid\": \">1.9.11 <=1.10.0\"}}\n\nPublished versions of chalkline-grid: 1.9.13-rc.1, 1.9.11-rc.1, 1.9.14, 2.4.39, 1.9.15",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nRead through these rules, which listed version of chalkline-grid gets installed by the resolver, if any?",
  "options": [
   "1.9.15",
   "None of the listed versions meets the range",
   "2.4.39"
  ]
 }
]
