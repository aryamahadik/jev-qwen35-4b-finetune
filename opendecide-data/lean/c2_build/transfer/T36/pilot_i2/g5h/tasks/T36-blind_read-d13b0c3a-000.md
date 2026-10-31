# G5-H blind read T36-blind_read-d13b0c3a-000 (family T36)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/pilot_i2/g5h/answers/T36-blind_read-d13b0c3a-000.json

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
  "qid": "qbf56a91028",
  "kind": "choice",
  "text": "Our dependency packages are tracked on this page for Pantry Index. The pinchweight package sits on the tidy-up list, and Idris Kamara owns the basics.\n\nDeclared specifiers for pinchweight in project pantry-index (Python packaging style): ~=4.25.11\n\nPublished versions of pinchweight: 4.25.3.post3, 4.25.35, 4.31.0, 4.35.32, 4.27.10, 4.25.3",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version, being the highest that meets the declared range, does the resolver install for pinchweight, if any?",
  "options": [
   "4.35.32",
   "4.25.35",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qa44700c904",
  "kind": "choice",
  "text": "Thank you, team: Tessemere Rota release prep\nHana Marsh maintains Tessemere Rota, and thanks go to all who helped look into the external package. The sync write-ups made the work easy to follow, and the review session went well, so the release can carry on with a clear picture of this dependency.\n\nDeclared specifiers for spinframe in project tessemere-rota (Python packaging style): ~=6.28\n\nPublished versions of spinframe: 7.0, 6.31, 6.27, 6.28, 6.30, 7.13",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich listed version, being the highest that meets the declared range, does the resolver install for spinframe, if any?",
  "options": [
   "6.31",
   "None of the listed versions meets the range",
   "7.13",
   "6.27"
  ]
 },
 {
  "qid": "qf27cb21d79",
  "kind": "choice",
  "text": "Spindle Counter is maintained by Kwame Ansah. If you are picking up the external package section from me, here is where things stand: the import list has been read through, and the code paths that call the package are mapped out. What is left is a walk through the tests that touch it and a short write-up for the team.\n\npackage.json of the project:\n{\"name\": \"spindle-counter\", \"dependencies\": {\"cardstock-tray\": \"^6.30.9\"}}\n\nPublished versions of cardstock-tray:\n| version |\n|---|\n| 7.28.7 |\n| 7.0.5 |\n| 6.29.8 |\n| 6.30.9-beta |\n| 6.30.8 |",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nOf the listed versions, which is the highest meeting the declared range of cardstock-tray, if any?",
  "options": [
   "6.29.8",
   "7.28.7",
   "None of the listed versions meets the range",
   "6.30.8"
  ]
 },
 {
  "qid": "q2b2516b0fc",
  "kind": "choice",
  "text": "[step=dependency-look] project=Fir Cairn Route maintainer=Ruben Esquivel\nreason=the planning sync flagged the external package in the import list, so the team asked for a careful walk through each code path that calls it, and the reviewer is still to be picked for the review session.\n\nDeclared specifiers for blaze-marker in project fir-cairn-route (Python packaging style): ~=19.18\n\nPublished versions of blaze-marker: 19.19.post2, 19.28, 19.19, 19.22, 19.20, 19.18a1, 20.12",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGoing by the card, which listed version of blaze-marker would be picked as highest that meets the range?",
  "options": [
   "20.12",
   "19.28",
   "19.22",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q5e879fbd37",
  "kind": "yes/no",
  "text": "Short entry on refuge-slot, which Hearth Saddle brings in from elsewhere. Readers use this page to see where the package shows up in the code, and Thandiwe Mokoena keeps the entry.\n\nDeclared range for refuge-slot in project hearth-saddle (npm style): 0.3.4 - 0.6.8\n\nPublished versions of refuge-slot: 0.6.7, 0.3.9, 0.3.5, 0.3.4, 0.6.8, 0.8.6\nVersion under review: 0.3.5",
  "question": "Checking the published versions, does version 0.3.5 of refuge-slot meet the declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa56542c752",
  "kind": "choice",
  "text": "Learning the codebase bit by bit, so pardon the basic questions in this PR, Yusuf Akkaya.\nWhy does the claywheel package show up in the Brenmoor Studio lock file?\n\nDeclared range for claywheel in project brenmoor-studio (npm style): ^4.8.1\n\nPublished versions of claywheel: 4.8.1-alpha, 5.0.5, 4.8.0, 4.7.4",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nRegarding claywheel, which listed version does the resolver install?",
  "options": [
   "None of the listed versions meets the range",
   "5.0.5",
   "4.7.4"
  ]
 },
 {
  "qid": "qbbd7d82e58",
  "kind": "yes/no",
  "text": "[job=dependency-check] project=Mirrask Platter package=crumbtray owner=Ilse Varholm state=reviewing\n\nDeclared range for crumbtray in project mirrask-platter (npm style): 7.4.22 - 7.8.23\n\nPublished versions of crumbtray: 7.6.36, 7.4.25, 7.4.31, 7.4.23, 7.4.22-rc.2\nVersion under review: 7.4.22-rc.2",
  "question": "Is the version identified as 7.4.22-rc.2 situated outside the declared range of the package crumbtray?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q13054dc60c",
  "kind": "choice",
  "text": "Favor for Solder Refrain Bench: read the pitchpipe-kit notes?\nGreta Holm has written up the entry, and a colleague who knows the wiring is well placed to catch the gap.\n\nDeclared specifiers for pitchpipe-kit in project solder-refrain-bench (Python packaging style): >=8.9, !=8.10.0, <8.11\n\nPublished versions of pitchpipe-kit: 8.11.post2, 8.9, 8.8, 9.0, 9.2, 8.19",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nMeasured against the declared range of pitchpipe-kit, which listed version is highest and meets it, if any?",
  "options": [
   "8.9",
   "None of the listed versions meets the range",
   "8.8"
  ]
 },
 {
  "qid": "q816412c1b4",
  "kind": "choice",
  "text": "chalkline-grid. External package. Used by the Gimlet Matinee build. Contact for questions: Ruairi Calloway. Review when touched.\n\nDeclared range for chalkline-grid in project gimlet-matinee (npm style): 13.7.x\n\nPublished versions of chalkline-grid: 13.7.0, 13.7.20, 15.0.23, 14.2.10",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nchalkline-grid has published versions; which of them is highest and meets the declared range, if any?",
  "options": [
   "15.0.23",
   "14.2.10",
   "13.7.20",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qe3f5b77411",
  "kind": "yes/no",
  "text": "Release prep: Brevlin Exchange dependency look\nOskar Lindahl maintains Brevlin Exchange. The external package came up while the planning sync was going over the release list, and the calls it reaches for are being traced by the team, so a look in the review session is the plan.\n\npackage.json of the project:\n{\"name\": \"brevlin-exchange\", \"dependencies\": {\"seedling-tally\": \"~0.3.20\"}}\n\nPublished versions of seedling-tally:\n| version |\n|---|\n| 0.3.22-beta.2 |\n| 0.8.16 |\n| 0.3.21 |\n| 0.3.26 |\n| 0.3.23 |\nVersion under review: 0.3.21",
  "question": "Does version 0.3.21 of seedling-tally not meet the declared range in these rules?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb9681a57c2",
  "kind": "choice",
  "text": "Quick heads up: the snowmark package came up in our sync with Kenji Tanabe.\nTeam on Ridge Cog Hub is small, so the back and forth happens right here.\nWorth a chat when you have room?\n\npyproject.toml of the project:\n[project]\nname = \"ridge-cog-hub\"\ndependencies = [\n  \"snowmark ~=1.7\",\n]\n\nPublished versions of snowmark:\n| version |\n|---|\n| 2.4 |\n| 1.6 |\n| 2.0 |\n| 1.7a1 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nLooking over the published versions of snowmark, which version does the resolver install?",
  "options": [
   "None of the listed versions meets the range",
   "2.4",
   "1.6"
  ]
 },
 {
  "qid": "qd438701a2f",
  "kind": "choice",
  "text": "Hi team,\nPassing the plumage-atlas work in Corvellan Perch over to you. The notes are in the team folder and you know where the files live.\nThanks,\nSaoirse Quinlan\n\nDeclared specifiers for plumage-atlas in project corvellan-perch (Python packaging style): >=7.18b2, <7.19\n\nPublished versions of plumage-atlas: 7.23, 7.19, 7.17, 8.0, 8.35",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version of plumage-atlas, from its listed set, gets installed by the resolver, if any?",
  "options": [
   "7.17",
   "7.19",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "qd6c799ba05",
  "kind": "choice",
  "text": "Favor for Ivy Stile Index: read the stacks-ring notes?\nAriadne Sarkisian has written up the entry, and a colleague who knows the wiring is well placed to catch the gap.\n\nDeclared range for stacks-ring in project ivy-stile-index (npm style): ~7.3.14 || ^1.3.13\n\nPublished versions of stacks-ring: 1.3.13, 1.2.13, 3.9.33, 1.3.13-alpha",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith its declared range in mind, which listed version of stacks-ring will the resolver install?",
  "options": [
   "None of the listed versions meets the range",
   "1.3.13",
   "3.9.33"
  ]
 },
 {
  "qid": "q00713e092e",
  "kind": "choice",
  "text": "Where cornice-hold shows up in Hearth Saddle\nI am still getting to know the codebase. Apologies for the basic questions. Please walk Thandiwe Mokoena through how it is used across the project when there is a moment.\n\npyproject.toml of the project:\n[project]\nname = \"hearth-saddle\"\ndependencies = [\n  \"cornice-hold >=20.27.16, !=20.28, <20.30\",\n]\n\nPublished versions of cornice-hold: 20.27.16, 20.27.15, 20.27.17, 20.27.3.post2",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWould you kindly indicate which listed version of cornice-hold the resolver installs under these rules?",
  "options": [
   "None of the listed versions meets the range",
   "20.27.17",
   "20.27.16"
  ]
 },
 {
  "qid": "qd9aafd48af",
  "kind": "choice",
  "text": "Draft notes for the Ysmere Cove release\nWorking through the dependency section while we prepare the bundle. Fenna Bakker wants a plain line that names the chapterloom package and says why it is bundled.\n\npyproject.toml of the project:\n[project]\nname = \"ysmere-cove\"\ndependencies = [\n  \"chapterloom ~=9.9.23\",\n]\n\nPublished versions of chapterloom:\n| version |\n|---|\n| 9.9.23 |\n| 9.9.27 |\n| 9.9.35 |\n| 9.11.23.post1 |",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith these rules applied to chapterloom, which listed version would the resolver settle on, if any?",
  "options": [
   "9.9.27",
   "9.9.23",
   "9.9.35",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q1255af8e3d",
  "kind": "yes/no",
  "text": "This PR touches the dressing-lattice package in Mirrask Platter, which we have been side-stepping for ages.\nBackground: the team has grown a lot since the project began, so Ilse Varholm knows the history best.\n\nDeclared range for dressing-lattice in project mirrask-platter (npm style): 11.8.3 || 0.0.x\n\nPublished versions of dressing-lattice: 0.0.3, 0.3.0, 0.1.0, 12.6.3\nVersion under review: 0.0.3",
  "question": "With respect to these rules, does version 0.0.3 of dressing-lattice fail to meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q649d86a921",
  "kind": "choice",
  "text": "Subject: check the swell-feed entry in the Murrelet Kelp manifest\nAssignee: Sunniva Hauge\nArea: manifest and lock file\nDetails: list the lines that reference the package and keep the write-up to what the manifest itself states.\n\nDeclared range for swell-feed in project murrelet-kelp (npm style): ^2.11.1-beta.2\n\nPublished versions of swell-feed: 2.14.4, 5.13.3, 3.0.0, 2.10.5, 3.0.3",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nIn plain words, which listed version of swell-feed counts as the highest meeting the range, if any?",
  "options": [
   "2.10.5",
   "None of the listed versions meets the range",
   "2.14.4"
  ]
 },
 {
  "qid": "q78a364e26c",
  "kind": "yes/no",
  "text": "Finding my feet here, so bear with me.\nAsked Ambrose Tilley about the birdsong-cache package and got a very patient walkthrough.\nHow does Corvellan Perch actually use it in practice?\n\npackage.json of the project:\n{\"name\": \"corvellan-perch\", \"dependencies\": {\"birdsong-cache\": \"~8.29.21 || >=19.0.21 <19.1.0\"}}\n\nPublished versions of birdsong-cache:\n| version |\n|---|\n| 8.29.23-beta.2 |\n| 19.0.20 |\n| 9.12.33 |\n| 19.0.29 |\n| 8.30.35 |\n| 21.5.37 |\nVersion under review: 19.0.29",
  "question": "Based on the card, does 19.0.29 fail to meet the range declared for birdsong-cache?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- Parts separated by spaces must all hold.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q914facef70",
  "kind": "yes/no",
  "text": "Release prep: Pantry Index dependency look\nSoyeon Park maintains Pantry Index. The external package came up while the planning sync was going over the release list, and the calls it reaches for are being traced by the team, so a look in the review session is the plan.\n\nDeclared specifiers for simmerbase in project pantry-index (Python packaging style): >=2.25.2a1, <3.0\n\nPublished versions of simmerbase: 2.31.0, 2.25.9.post1, 3.4.0, 2.25.2b2\nVersion under review: 3.4.0\n\nIn this project the top of every range is inclusive, and Soyeon Park is confident the bound itself always counts.",
  "question": "Where simmerbase is concerned, does version 3.4.0 fail to meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf3d631ece6",
  "kind": "choice",
  "text": "Release preparation, dependency pass\nThe pitchpipe-kit package was walked through by Greta Holm for Solder Refrain Bench, and the notes were sent on to the reviewers.\n\nDeclared range for pitchpipe-kit in project solder-refrain-bench (npm style): ^10.19.5\n\nPublished versions of pitchpipe-kit: 11.0.0, 13.14.8, 10.18.9, 10.19.4, 11.0.6, 10.22.7\n\nGreta Holm reckons the card for pitchpipe-kit is only a rough sketch, and the team makes each call as it comes.",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version does the resolver install from the listed pitchpipe-kit versions?",
  "options": [
   "10.22.7",
   "13.14.8",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q79b629e830",
  "kind": "yes/no",
  "text": "Eyes wanted on a knotty import path\nNgozi Eke, the way the plate-register package gets brought into Bradawl Folio has grown tangled in my head. A careful reading from your side is what this thread is looking for.\n\npackage.json of the project:\n{\"name\": \"bradawl-folio\", \"dependencies\": {\"plate-register\": \"5.2.x\"}}\n\nPublished versions of plate-register: 5.2.0, 5.3.1, 5.2.3, 5.2.6, 5.2.5, 5.2.1\nVersion under review: 5.3.1",
  "question": "In accordance with these rules, does plate-register's version 5.3.1 meet its declared range?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q47a758a849",
  "kind": "yes/no",
  "text": "Subject: notes on package crateloop\nHi Joaquin Ruelas,\nI am going over how Tessemere Rota leans on the package. Please take a look at the question below when you have a moment.\nThanks,\n\npyproject.toml of the project:\n[project]\nname = \"tessemere-rota\"\ndependencies = [\n  \"crateloop >=0.21.0, <0.23\",\n]\n\nPublished versions of crateloop:\n| version |\n|---|\n| 0.22.4 |\n| 0.20.9 |\n| 0.24.9 |\n| 0.31.6 |\nVersion under review: 0.24.9",
  "question": "Regarding crateloop, does version 0.24.9 meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qe792045707",
  "kind": "choice",
  "text": "Summary: standing dependency review entry for mossfeed\nOwner: Hugo Saldana\nComponent: Fernhollow Tour external packages\nNotes: looking at where the package shows up across the project, adding a short line of context for the review.\n\nDeclared specifiers for mossfeed in project fernhollow-tour (Python packaging style): >=3.23.20, <4.0\n\nPublished versions of mossfeed: 4.0.0, 3.23.9, 4.27.15, 3.23.30, 3.23.19, 3.22.27",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version listed for mossfeed is the highest that meets the declared range, if any?",
  "options": [
   "3.23.30",
   "3.23.19",
   "3.22.27",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q32cb7a413f",
  "kind": "yes/no",
  "text": "Background on the code we import, written by the group that set up Brenmoor Studio. The signupgrid package came out of their work on the internals, and it reaches into the core of the code. Ingrid Solheim looks after the entry and is glad to talk through how it got here.\n\npyproject.toml of the project:\n[project]\nname = \"brenmoor-studio\"\ndependencies = [\n  \"signupgrid >7.18.6rc1, <8.0\",\n]\n\nPublished versions of signupgrid: 7.20.4.post1, 7.18.7, 7.20.4, 7.17.9, 7.18.6.post3, 7.18.7.post2, 7.24.9\nVersion under review: 7.17.9",
  "question": "Is the version 7.17.9 of signupgrid considered to meet the declared range under these rules?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qdfbe7cae24",
  "kind": "choice",
  "text": "Our little group has a rule of thumb about external packages: talk about them early and at length. The lotcall package is a fine example, since Rahul Venkatesan keeps a good stack of notes on Spade Roster.\n\nDeclared specifiers for lotcall in project spade-roster (Python packaging style): >=7.30, !=7.31.0, <7.34\n\nPublished versions of lotcall: 7.30a1, 7.40, 7.30rc1, 7.33, 7.31.4, 7.32, 7.30",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nInstalling lotcall under these rules, which listed version does the resolver settle on?",
  "options": [
   "7.30",
   "7.33",
   "None of the listed versions meets the range",
   "7.40"
  ]
 },
 {
  "qid": "q0a28c1d90c",
  "kind": "yes/no",
  "text": "Going through the dampen-roll package as part of the dependency sweep for Reed Lichen Queue.\nAyesha Rahman has the notes, so shout when you see it.\n\npyproject.toml of the project:\n[project]\nname = \"reed-lichen-queue\"\ndependencies = [\n  \"dampen-roll >=20.8b2, <21.0\",\n]\n\nPublished versions of dampen-roll:\n| version |\n|---|\n| 20.10 |\n| 20.8rc1 |\n| 20.8.post3 |\n| 20.8a1 |\nVersion under review: 20.8rc1",
  "question": "Across the card, does version 20.8rc1 fail to meet the declared range that dampen-roll specifies?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd7ba9b64aa",
  "kind": "yes/no",
  "text": "Ruben Esquivel, mind giving the contour-serve change in Fir Cairn Route a glance when you have time. The wrapper part is the tricky bit, and a colleague's eyes on it help a lot.\n\nDeclared range for contour-serve in project fir-cairn-route (npm style): ^5.1.0\n\nPublished versions of contour-serve: 5.3.4, 5.0.1, 6.6.4, 5.11.9\nVersion under review: 5.3.4\n\nKeep the upper limit inclusive, because Ruben Esquivel says a range that stops short of its bound is the bug we keep meeting.",
  "question": "Does version 5.3.4 of contour-serve not meet the declared range in these rules?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa8da02da37",
  "kind": "choice",
  "text": "Subject: note on dampen-roll\nDear Tiago Ferreira,\nI hope you are well. I am writing with notes on the external packages in Reed Lichen Queue, particularly on how the package is used across our codebase. Thank you in advance for your thoughts when you have a moment.\nWith thanks,\nthe maintainer\n\nDeclared specifiers for dampen-roll in project reed-lichen-queue (Python packaging style): ~=12.22.15\n\nPublished versions of dampen-roll: 12.22.2, 12.22.15, 12.22.0a1, 12.24.32.post3, 12.24.32, 12.22.17",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWith these rules applied to dampen-roll, which listed version would the resolver settle on, if any?",
  "options": [
   "12.22.17",
   "12.24.32",
   "12.22.15",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q69401fbad3",
  "kind": "yes/no",
  "text": "Thanks for pulling this together, Kenji Tanabe! Glad the liftqueue bit is in the thread for Ridge Cog Hub, cheers.\n\npyproject.toml of the project:\n[project]\nname = \"ridge-cog-hub\"\ndependencies = [\n  \"liftqueue ==4.8.*\",\n]\n\nPublished versions of liftqueue:\n| version |\n|---|\n| 4.8.8 |\n| 4.8.8rc1 |\n| 4.8.0 |\n| 4.8.6 |\n| 4.8.3.post3 |\nVersion under review: 4.8.8rc1",
  "question": "Among the listed versions of liftqueue, is version 4.8.8rc1 sitting outside the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qd275e7bf64",
  "kind": "choice",
  "text": "Subject: handover for the external package review\nHi there,\nPassing my part of the external package review over to you. Ariadne Sarkisian, who maintains Ivy Stile Index, wants a look at how long the package takes to start on each run. The log lines for that sit in the shared folder. Go over them before anything else, then check the pipeline timings with the reviewers.\nCheers,\nyour teammate\n\nDeclared range for bookplate-sort in project ivy-stile-index (npm style): 7.x || ~15.30.23\n\nPublished versions of bookplate-sort: 7.0.3-alpha, 15.31.3, 8.0.0, 15.31.0, 17.26.17, 15.30.22\n\nAriadne Sarkisian swears by the latest release on every upgrade, since the newest build is always the sensible default.",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"~V\" means >=V and below the next minor version: ~1.4.2 means >=1.4.2 <1.5.0.\n- \"1.4.x\" means >=1.4.0 <1.5.0, and \"1.x\" means >=1.0.0 <2.0.0.\n- \"||\" separates alternatives: the range is met when one alternative is met.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nGoing by the card, which listed version of bookplate-sort does the resolver install, if any?",
  "options": [
   "None of the listed versions meets the range",
   "15.30.22",
   "17.26.17"
  ]
 },
 {
  "qid": "q0149558779",
  "kind": "choice",
  "text": "Handing you the berthledger question for Sedgehollow Moorings since our side is swamped.\nTavita Sefo made a pass at it, so start there.\n\nDeclared specifiers for berthledger in project sedgehollow-moorings (Python packaging style): ~=8.19\n\nPublished versions of berthledger: 8.21, 8.18, 9.17, 9.20, 8.20, 8.24, 9.0",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhat is the listed berthledger version the resolver lands on, if any?",
  "options": [
   "8.24",
   "9.20",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q6dc92447fc",
  "kind": "yes/no",
  "text": "Check the fathom-gauge entry in Mooring Almanac\nSmall note from Anders Berggren: the entry sits in the dependency file and it is waiting for a look.\n\npyproject.toml of the project:\n[project]\nname = \"mooring-almanac\"\ndependencies = [\n  \"fathom-gauge ==3.28.*\",\n]\n\nPublished versions of fathom-gauge:\n| version |\n|---|\n| 3.28.post2 |\n| 3.32 |\n| 3.28rc1 |\n| 4.11 |\n| 3.28b2 |\n| 3.28a1 |\n| 3.29 |\nVersion under review: 3.29",
  "question": "By these rules, would 3.29 of fathom-gauge lie outside the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q6bc0314335",
  "kind": "choice",
  "text": "Small edit to the elevation-map line in the Crank Ledger manifest. The description from Hana Kobayashi explains the reason briefly.\n\nDeclared range for elevation-map in project crank-ledger (npm style): >=0.9.0 <0.10.0\n\nPublished versions of elevation-map: 1.0.9, 0.13.6, 0.8.6, 0.10.2, 0.19.0, 3.1.5, 0.10.1",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nOf the published versions of elevation-map, which is the highest that meets the declared range, if any?",
  "options": [
   "0.8.6",
   "None of the listed versions meets the range",
   "3.1.5"
  ]
 },
 {
  "qid": "qefc62bc510",
  "kind": "yes/no",
  "text": "I am asking Rohan Desai to read the section on portion-map in the Pan Ration Tally notes. Please look closely at the wording and tell me where it is hard to follow.\n\nDeclared specifiers for portion-map in project pan-ration-tally (Python packaging style): <=4.25.12\n\nPublished versions of portion-map: 4.24.35, 4.25.12, 4.25.23, 4.25.9.post1\nVersion under review: 4.25.23",
  "question": "Is the version 4.25.23 of portion-map considered to meet the declared range under these rules?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qb7a641580b",
  "kind": "choice",
  "text": "Summary: review the pinchweight package in Pantry Index\nOwner: Soyeon Park\nComponent: dependency manifest\nNotes: quick read of how it is listed.\n\nDeclared specifiers for pinchweight in project pantry-index (Python packaging style): ~=0.14.10\n\nPublished versions of pinchweight: 0.14.10rc1, 0.13.25, 0.18.37, 0.16.27, 0.14.10a1",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version does the resolver install from the listed pinchweight versions?",
  "options": [
   "0.13.25",
   "None of the listed versions meets the range",
   "0.18.37",
   "0.16.27"
  ]
 },
 {
  "qid": "q6e121187ac",
  "kind": "yes/no",
  "text": "[step=dependency_review] project=Mallet Pantry Rota package=shift-lathe reviewer=Gideon Mensah state=in_progress\n\nDeclared specifiers for shift-lathe in project mallet-pantry-rota (Python packaging style): >=4.28, !=4.29.0, <4.32\n\nPublished versions of shift-lathe: 4.29.post1, 4.27, 4.31, 4.28, 4.30\nVersion under review: 4.28",
  "question": "Under these rules, does the version 4.28 of shift-lathe meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qf26cd42bcd",
  "kind": "yes/no",
  "text": "[step=dependency-look] project=Dunlin Heather Log maintainer=Mateus Caldeira\nreason=the planning sync flagged the external package in the import list, so the team asked for a careful walk through each code path that calls it, and the reviewer is still to be picked for the review session.\n\nDeclared range for qso-ledger in project dunlin-heather-log (npm style): 8.14.3 - 8.16.6\n\nPublished versions of qso-ledger: 8.16.6, 8.15.0, 8.14.5-beta, 8.16.5, 8.14.3, 8.14.11, 8.14.4\nVersion under review: 8.14.5-beta",
  "question": "Taking the declared range of qso-ledger as the standard, would version 8.14.5-beta fail to meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"A - B\" means >=A <=B.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa22daf8f80",
  "kind": "choice",
  "text": "On this wiki page we keep notes on external packages in Fernhollow Tour. While getting ready to ship, we are taking a close look at the mossfeed package, and Hugo Saldana is the person to ask about how it is used.\n\nDeclared range for mossfeed in project fernhollow-tour (npm style): ^4.29.18\n\nPublished versions of mossfeed: 4.28.19, 5.0.0, 4.29.17, 7.37.11, 4.30.26",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich highest listed version of mossfeed meets the declared range, if any?",
  "options": [
   "4.29.17",
   "4.30.26",
   "4.28.19",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q91a593eeaf",
  "kind": "yes/no",
  "text": "[scan] kind=direct-deps hit=chainring-bin workspace=Quenbar Spanner by=Oren Halvorsen step=read-through\n\nDeclared specifiers for chainring-bin in project quenbar-spanner (Python packaging style): <=0.6.6\n\nPublished versions of chainring-bin: 0.6.1, 1.0.0, 0.7.4.post1, 0.6.6b2\nVersion under review: 0.6.1",
  "question": "In accordance with these rules, does chainring-bin's version 0.6.1 meet its declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q7b3ad28426",
  "kind": "choice",
  "text": "Subject: prep for the Murrelet Kelp release\nHi,\nWe are getting ready to put the release together, and the berth-calendar package is on the checklist. Please share your thoughts on it at your convenience.\nThanks,\nSunniva Hauge\n\nDeclared range for berth-calendar in project murrelet-kelp (npm style): ^0.0.17\n\nPublished versions of berth-calendar: 0.0.17-beta.2, 0.3.0, 0.0.20, 0.1.26, 0.0.24, 3.3.27, 0.0.18",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nPut simply, what is the top listed version of berth-calendar the resolver takes under these rules, if any?",
  "options": [
   "0.0.18",
   "0.0.20",
   "3.3.27",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q5b2db29961",
  "kind": "choice",
  "text": "Subject: Fresh look at the cratemark-kit package\nHi Gideon Mensah,\nMind taking a look at how Mallet Pantry Rota leans on it? My notes are below, and my reading of them feels a bit tangled. Eyes from a colleague are welcome. Thanks in advance.\nBest,\nthe maintainer\n\nDeclared range for cratemark-kit in project mallet-pantry-rota (npm style): ^0.0.21\n\nPublished versions of cratemark-kit: 0.0.23-alpha, 0.0.21, 0.0.21-beta.2, 3.1.25, 0.0.24, 0.0.20, 0.0.29",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nUsing the declared range of cratemark-kit, which listed version is the highest that the resolver installs?",
  "options": [
   "0.0.29",
   "3.1.25",
   "None of the listed versions meets the range",
   "0.0.21"
  ]
 },
 {
  "qid": "qd72eccfedc",
  "kind": "choice",
  "text": "Release prep\nGimlet Matinee is maintained by Ruairi Calloway. Before the cut, the external package used for reminder emails needs a look at its start-up cost, and the reviewers should go over the logs from the pipeline run on the main branch.\n\nDeclared range for seatjig in project gimlet-matinee (npm style): >2.8.6 <2.9.0\n\nPublished versions of seatjig: 2.8.5, 4.7.1, 2.8.7, 2.8.9",
  "question": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \">=V\", \">V\", \"<=V\", \"<V\" and \"=V\" compare with V; a bare \"V\" means \"=V\".\n- Parts separated by spaces must all hold.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- The resolver installs the highest listed version that meets the range; when no listed version meets it, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWould you kindly indicate which listed version of seatjig the resolver installs under these rules?",
  "options": [
   "2.8.9",
   "2.8.7",
   "None of the listed versions meets the range"
  ]
 },
 {
  "qid": "q2b09add9f0",
  "kind": "choice",
  "text": "Housekeeping for the release preparation of Gimlet Matinee\nThe chalkline-grid package is tidied in the dependency section, with Ruairi Calloway keeping its entry in order.\n\nDeclared specifiers for chalkline-grid in project gimlet-matinee (Python packaging style): >=8.1, <8.2\n\nPublished versions of chalkline-grid: 8.1a1, 9.3, 8.0, 8.11, 8.3.post3, 8.3",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nAcross everything listed for chalkline-grid, which version would the resolver end up installing, if any?",
  "options": [
   "None of the listed versions meets the range",
   "9.3",
   "8.3"
  ]
 },
 {
  "qid": "qe70ae822bd",
  "kind": "yes/no",
  "text": "Housekeeping for the release preparation of Brevlin Exchange\nThe thread-muster package is tidied in the dependency section, with Oskar Lindahl keeping its entry in order.\n\nDeclared specifiers for thread-muster in project brevlin-exchange (Python packaging style): >=3.24.5a1, <4.0\n\nPublished versions of thread-muster: 3.34.0, 3.23.0, 4.4.0, 3.25.0rc1, 3.24.4\nVersion under review: 3.23.0",
  "question": "Is it correct that version 3.23.0 of thread-muster does not meet the declared range?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q32adf3f79a",
  "kind": "yes/no",
  "text": "Topic: map the sunlit-cycle package's call paths into Ombrel Sprout\nOwner: Dagny Brask\nModule: request handling\nDetails: paths listed by file, with function names and argument types written beside them.\n\nDeclared range for sunlit-cycle in project ombrel-sprout (npm style): ^8.26.2\n\nPublished versions of sunlit-cycle: 9.0.6, 8.26.10, 9.0.0, 8.26.2-beta.2\nVersion under review: 8.26.10",
  "question": "Under these rules, and reading the declared range for sunlit-cycle as written, does version 8.26.10 not meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "qa95f9c017a",
  "kind": "choice",
  "text": "Handing you the repairmark question for Pellidor Gatehouse since our side is swamped.\nSoren Halvik made a pass at it, so start there.\n\nDeclared specifiers for repairmark in project pellidor-gatehouse (Python packaging style): <=2.16\n\nPublished versions of repairmark: 2.26, 2.17, 3.34, 2.19, 2.15, 2.18",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nFor repairmark, which listed version would the resolver end up with?",
  "options": [
   "3.34",
   "2.15",
   "None of the listed versions meets the range",
   "2.17"
  ]
 },
 {
  "qid": "q91c68228aa",
  "kind": "yes/no",
  "text": "[peer-look] reviewer=Bogdan Stoica | project=Ostrain Glaze | pkg=ramp-schedule | view=fresh\n\nDeclared range for ramp-schedule in project ostrain-glaze (npm style): ^9.1.1-beta\n\nPublished versions of ramp-schedule: 9.1.3-alpha.3, 9.1.6, 9.0.2, 10.0.1, 11.4.7, 9.3.8\nVersion under review: 9.0.2",
  "question": "When you read the card closely and look at the declared range that ramp-schedule sets out, does the version 9.0.2 meet it?",
  "definitions": "How to read this version range (npm style):\n- A version is MAJOR.MINOR.PATCH, optionally followed by \"-\" and a pre-release tag such as \"beta.2\". Compare versions by MAJOR, then MINOR, then PATCH, each as a number.\n- A version with a pre-release tag comes before the same version without one. Two tags compare part by part: numbers as numbers, words alphabetically, a number before a word, and a shorter tag first when all its parts match (tag parts are separated by \".\").\n- \"^V\" means >=V and below the next version that raises the first non-zero part of V: ^1.4.2 means >=1.4.2 <2.0.0, ^0.4.2 means >=0.4.2 <0.5.0, ^0.0.4 means >=0.0.4 <0.0.5.\n- A version with a pre-release tag meets an alternative only if that alternative itself writes a version with the same MAJOR.MINOR.PATCH and a pre-release tag (bounds that \"^\", \"~\" or \"x\" imply do not count).\n- A version is inside the range when it meets the range, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q27ead2a2e9",
  "kind": "yes/no",
  "text": "Subject: module list for the dependency section\nDear Anders Berggren,\nI traced the fathom-gauge package through its import sites in Mooring Almanac and recorded the call sites in the notes. The module list is saved in the team folder.\nKind regards\n\nDeclared specifiers for fathom-gauge in project mooring-almanac (Python packaging style): <=2.6.15\n\nPublished versions of fathom-gauge: 2.6.0.post1, 2.6.3.post3, 2.6.15, 3.1.39\nVersion under review: 3.1.39",
  "question": "Taking every line of the rules into account, does version 3.1.39 meet the declared range of fathom-gauge?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 },
 {
  "qid": "q7b1ace3e38",
  "kind": "choice",
  "text": "Subject: handover for Bradawl Folio\nHi Dara Ashdown,\nI am passing along the thread on the dependency for the clefsort package. My notes sit in the shared folder, and the rest of the context is in the tracker.\nThanks\n\nDeclared specifiers for clefsort in project bradawl-folio (Python packaging style): ~=4.30.6\n\nPublished versions of clefsort: 4.30.9, 4.40.8, 4.30.5, 4.31.4, 5.15.9, 4.32.5, 4.29.6",
  "question": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \"==1.4.*\" holds for every version whose release starts with 1.4 (with zero padding), post-releases included; a pre-release among them still needs the pre-release rule below.\n- \"~=V\" means >=V together with ==P.*, where P is V without its last release number: ~=1.4.2 means >=1.4.2 and ==1.4.*, and ~=1.4 means >=1.4 and ==1.*.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The resolver installs the highest listed version that meets the specifiers; when no listed version meets them, the resolver installs none of them.\nThe range, the listed versions and these rules are complete: nothing else changes the answer.\n\nWhich version of clefsort, from its listed set, gets installed by the resolver, if any?",
  "options": [
   "None of the listed versions meets the range",
   "4.40.8",
   "4.30.9",
   "5.15.9"
  ]
 },
 {
  "qid": "q124b0d0544",
  "kind": "yes/no",
  "text": "Quick heads up: the macro-sum package came up in our sync with Rohan Desai.\nTeam on Pan Ration Tally is small, so the back and forth happens right here.\nWorth a chat when you have room?\n\nDeclared specifiers for macro-sum in project pan-ration-tally (Python packaging style): >=11.16, !=11.17.0, <11.19\n\nPublished versions of macro-sum: 11.21, 11.17.post1, 11.17, 11.18\nVersion under review: 11.21",
  "question": "Based on the card, does 11.21 fail to meet the range declared for macro-sum?",
  "definitions": "How to read these version specifiers (Python packaging style):\n- A version is a release of numbers joined by dots (1.4 or 1.4.2), optionally followed by a pre-release (aN, bN or rcN: a before b before rc, then by N) or a post-release (.postN). Compare releases number by number, padding the shorter one with zeros, so 1.4 equals 1.4.0. A pre-release comes before its release; a post-release comes after its release and before the next release.\n- \">=V\", \">V\", \"<=V\", \"<V\", \"==V\" and \"!=V\" compare with V.\n- Specifiers separated by commas must all hold.\n- A version with a pre-release meets the specifiers only if one of them, other than a \"!=\" one, names a pre-release version; this holds for every set of specifiers.\n- The specifiers together form the range. A version is inside the range when it meets the specifiers, and outside the range when it does not, even when its numbers lie between the bounds.\nThe range, the listed versions and these rules are complete: nothing else changes the answer."
 }
]
