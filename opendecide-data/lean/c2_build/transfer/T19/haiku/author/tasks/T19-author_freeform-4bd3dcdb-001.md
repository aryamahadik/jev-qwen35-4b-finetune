# Haiku authoring task T19-author_freeform-4bd3dcdb-001 (family T19, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T19/haiku/author/answers/T19-author_freeform-4bd3dcdb-001.json

Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.
The answer is one JSON list with exactly 16 objects, one per item below, each carrying that item's qid. Inside JSON strings, write a line break as \n and a double quote as \".

## Instructions

You write short free-form workplace notes that open a records-review puzzle about one site of an organisation. Each item gives a register, a brief and two facts: SITE (the name of the site under review) and AUDITOR (the full name of the person who runs the review). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write the SITE name and the AUDITOR name exactly as given (same spelling, spaces and capitals), each at least once. Write no other name of a person, place, company or product.
2. The note only sets the scene, in the register and tone asked for: the AUDITOR person is going through the records of the SITE, and the records follow. Never mention any particular check, document, paperwork, date, result or finding, never say how the review is going, and never say what anyone may, must, should or will do.
3. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, hardly, unless, except, other than, neither, nor).
5. No word that judges or reports a state or an outcome: approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, closed, active, late, current, missing, verified, confirmed, accepted, rejected, resolved, settled, outstanding, breached, ok, okay, fine, clean, in order, up to date, on track, at risk, problem, issue, concern, finding.
6. One block of text with no empty line, 1-4 sentences of plain, natural English. Never write the words "checklist", "evidence log", "audit date" or "site profile", and never these words, which belong to the site's profile: office, warehouse, store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \n for line breaks inside the text. Every note must differ from every other note you write.

## Answer format

[{"qid": "q...", "text": "..."}, ...]

## Items (16; answer every item once, keyed by its qid)

```json
[
{"qid": "qe1db95433e", "brief": "Write a note jotted at the top of a review sheet at a school district: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "checklist_note", "facts": {"SITE": "Quarry Lane depot", "AUDITOR": "Ilona Varga"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "q1f6d59ac6e", "brief": "Write a team chat excerpt at a hospital supply firm: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "audit_chat", "facts": {"SITE": "Juniper Hill campus", "AUDITOR": "Freya Lindahl"}, "rules": ["A chat excerpt of 2-4 short lines 'speaker: message'; the AUDITOR name is one speaker."]},
{"qid": "qd830caec1f", "brief": "Write an internal wiki page header at a home care agency: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "site_wiki", "facts": {"SITE": "Hollins Wharf", "AUDITOR": "Talia Romero"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]},
{"qid": "q44abc77257", "brief": "Write a note jotted at the top of a review sheet at a laundry service: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "checklist_note", "facts": {"SITE": "Rookwood annex", "AUDITOR": "Nadia Petrova"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "q957bc3cf19", "brief": "Write the opening of a formal review report at a parcel courier: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "report", "facts": {"SITE": "Ashby Mill campus", "AUDITOR": "Quentin Marchal"}, "rules": ["The opening of a formal review report, 1-3 sentences."]},
{"qid": "qa425ce408b", "brief": "Write a note jotted at the top of a review sheet at a university estates team: AUDITOR is going through the records of SITE. Tone: plain and matter-of-fact.", "register": "checklist_note", "facts": {"SITE": "Saltmarsh yard", "AUDITOR": "Soren Vik"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "q9c134a4a40", "brief": "Write an internal audit memo at a museum trust: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "audit_memo", "facts": {"SITE": "Brackenridge annex", "AUDITOR": "Tarek Haddad"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "q32f79cb7e4", "brief": "Write a short e-mail about the review at a grain cooperative: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "auditor_email", "facts": {"SITE": "Hartwell Row annex", "AUDITOR": "Kofi Asante"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "qe9025e6aac", "brief": "Write a note jotted at the top of a review sheet at a ski resort: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "checklist_note", "facts": {"SITE": "Thornbury campus", "AUDITOR": "Xenia Moroz"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "q550d0f66aa", "brief": "Write an internal wiki page header at a cinema chain: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "site_wiki", "facts": {"SITE": "Fennick campus", "AUDITOR": "Jonas Keller"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]},
{"qid": "qd8c982f779", "brief": "Write the opening of a formal review report at a water utility: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "report", "facts": {"SITE": "Danebury annex", "AUDITOR": "Oriane Fabre"}, "rules": ["The opening of a formal review report, 1-3 sentences."]},
{"qid": "q904d18ab95", "brief": "Write a work ticket for the review at a gym chain: AUDITOR is going through the records of SITE. Tone: plain and matter-of-fact.", "register": "audit_ticket", "facts": {"SITE": "Nettlebed annex", "AUDITOR": "Idris Bello"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "qfa99f21454", "brief": "Write an internal audit memo at a regional bus operator: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "audit_memo", "facts": {"SITE": "Alder Quay depot", "AUDITOR": "Maren Holt"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "qc3d7e6e914", "brief": "Write a short e-mail about the review at a city parks department: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "auditor_email", "facts": {"SITE": "Eskdale branch", "AUDITOR": "Mateus Rocha"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q37fbec9209", "brief": "Write an internal audit memo at a chain of bakeries: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "audit_memo", "facts": {"SITE": "Dunmore campus", "AUDITOR": "Hilde Sorensen"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "q2a1933b6f4", "brief": "Write meeting notes at a coastal rescue charity: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "meeting_notes", "facts": {"SITE": "Upton Reach branch", "AUDITOR": "Leonie Brandt"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]}
]
```
