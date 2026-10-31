# Haiku authoring task T19-author_freeform-4bd3dcdb-000 (family T19, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T19/haiku/author/answers/T19-author_freeform-4bd3dcdb-000.json

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
{"qid": "q4493bb04f3", "brief": "Write a short e-mail about the review at a ferry company: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "auditor_email", "facts": {"SITE": "Glenholm depot", "AUDITOR": "Wendell Okafor"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q4fcead7292", "brief": "Write an internal wiki page header at a veterinary clinic chain: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "site_wiki", "facts": {"SITE": "Gorsey Lane branch", "AUDITOR": "Olumide Adeyemi"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]},
{"qid": "q7177a27242", "brief": "Write a team chat excerpt at a botanical garden trust: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "audit_chat", "facts": {"SITE": "Lindow Moor depot", "AUDITOR": "Pernille Dahl"}, "rules": ["A chat excerpt of 2-4 short lines 'speaker: message'; the AUDITOR name is one speaker."]},
{"qid": "q226a37fa5f", "brief": "Write a work ticket for the review at a recycling company: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "audit_ticket", "facts": {"SITE": "Pelham Gate branch", "AUDITOR": "Chiara Lodi"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "q68a76b6d31", "brief": "Write a work ticket for the review at a library network: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "audit_ticket", "facts": {"SITE": "Marram Point yard", "AUDITOR": "Ulrich Brenner"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "qcc73804b94", "brief": "Write a short e-mail about the review at a theatre company: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "auditor_email", "facts": {"SITE": "Foxley Wharf", "AUDITOR": "Rhea Kapoor"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "qf06fae5b6e", "brief": "Write a work ticket for the review at a regional airport: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "audit_ticket", "facts": {"SITE": "Orchard Rise campus", "AUDITOR": "Yuki Tanabe"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "qed3b642260", "brief": "Write an internal wiki page header at a print works: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "site_wiki", "facts": {"SITE": "Elmstead yard", "AUDITOR": "Emre Aydin"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]},
{"qid": "qf1975c1f53", "brief": "Write meeting notes at a hotel group: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "meeting_notes", "facts": {"SITE": "Vale End depot", "AUDITOR": "Amaia Etxeberria"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q427c2e0c6b", "brief": "Write the opening of a formal review report at a solar farm operator: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "report", "facts": {"SITE": "Calder Ford depot", "AUDITOR": "Sunniva Lund"}, "rules": ["The opening of a formal review report, 1-3 sentences."]},
{"qid": "qe9541e1c02", "brief": "Write meeting notes at a furniture maker: AUDITOR is going through the records of SITE. Tone: plain and matter-of-fact.", "register": "meeting_notes", "facts": {"SITE": "Yarrow Bank yard", "AUDITOR": "Lucia Ferraz"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q50b20ab112", "brief": "Write the opening of a formal review report at a brewery: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "report", "facts": {"SITE": "Beckford Row branch", "AUDITOR": "Vesna Kralj"}, "rules": ["The opening of a formal review report, 1-3 sentences."]},
{"qid": "qcfdec2483b", "brief": "Write a team chat excerpt at a film studio: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "audit_chat", "facts": {"SITE": "Kelso Street branch", "AUDITOR": "Kalani Akana"}, "rules": ["A chat excerpt of 2-4 short lines 'speaker: message'; the AUDITOR name is one speaker."]},
{"qid": "qa9b72c4441", "brief": "Write a team chat excerpt at a dental group: AUDITOR is going through the records of SITE. Tone: plain and matter-of-fact.", "register": "audit_chat", "facts": {"SITE": "Inchcape yard", "AUDITOR": "Dariusz Wolny"}, "rules": ["A chat excerpt of 2-4 short lines 'speaker: message'; the AUDITOR name is one speaker."]},
{"qid": "q23c6f30ca0", "brief": "Write an internal audit memo at a tram network: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "audit_memo", "facts": {"SITE": "Cobble Lane yard", "AUDITOR": "Bram de Wit"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "qce56e45204", "brief": "Write meeting notes at a marina: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "meeting_notes", "facts": {"SITE": "Wexcombe annex", "AUDITOR": "Gideon Mbeki"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]}
]
```
