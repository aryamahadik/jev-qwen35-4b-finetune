# Haiku REDO-2 task T19-redo2-freeform-000 (family T19, kind author_freeform): 13 item(s), 2 candidates each

Read this whole file. It is the only file you may open: do not open, list, search or write any other file or folder. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T19/haiku/redo2/answers/T19-redo2-freeform-000.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 13 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "texts" (a list of exactly 2 different strings: 2 alternative candidates for that item, each complete on its own and each following every rule below; inside a string write \n for a line break and \" for a double quote).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys.

Literal example of the required shape:

[
  {"qid": "q68a76b6d31", "texts": ["<text A>", "<text B>"]},
  ...
]

How the candidates are used: a program checks each candidate against the rules below in the order you wrote them and keeps the first one that meets every check; the others are thrown away. So every candidate must follow every rule, and the candidates of one item must be clearly different from each other.

## Instructions

You write short free-form workplace notes that open a records-review puzzle about one site of an organisation. Each item gives a register, a brief and two facts: SITE (the name of the site under review) and AUDITOR (the full name of the person who runs the review). Write 2 alternative notes per item.

Rules (a program rejects any note that breaks one):
1. Write the SITE name and the AUDITOR name exactly as given (same spelling, spaces and capitals), each at least once. Write no other name of a person, place, company or product.
2. The note only sets the scene, in the register and tone asked for: the AUDITOR person is going through the records of the SITE, and the records follow. Never mention any particular check, document, paperwork, date, result or finding, never say how the review is going, and never say what anyone may, must, should or will do.
3. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, hardly, unless, except, other than, neither, nor).
5. No word that judges or reports a state or an outcome: approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, closed, active, late, current, missing, verified, confirmed, accepted, rejected, resolved, settled, outstanding, breached, ok, okay, fine, clean, in order, up to date, on track, at risk, problem, issue, concern, finding.
6. One block of text with no empty line, 1-4 sentences of plain, natural English. Never write the words "checklist", "evidence log", "audit date" or "site profile", and never these words, which belong to the site's profile: office, warehouse, store, data, centre, center, cloud, hybrid, premises, public, internal, personal, payment; also premise and on-premises, and the short word "on" as a word by itself (see the redo note).

Answer: follow the answer contract at the top of this file (2 notes per item, each complete on its own and each following every rule). Use \n for line breaks inside a text. Every note must differ clearly from every other note you write, also from the other notes of the same item (not one word swapped).

## Redo note

REDO NOTE (added for this redo; every rule above still holds). Earlier notes for the items below were thrown away by the program's word check. Write completely new notes. Causes to avoid:
- The short word "on" (most earlier texts were thrown away for it alone). The program reserves it because a profile value printed below your text contains it, and it reads the word wherever it stands. Never write "on" as a word: also not in phrases such as "on behalf of", "on site", "on file", "on hand", "on it", "on the way", "on the move", "on my list", "on the bench", "carry on", "move on", "take on", "taken on", "handed on", "get on with", "waiting on", "notes on", "word on", "work on", "rules on", "from here on" or "from this point on", and not as the first part of a hyphenated word ("on-site", "on-call"). Write "for", "about", "at", "over", "regarding", "with", "from here", "takes over" or "picks up" instead. A longer word that only contains these letters (such as "upon" or "onto") is a different word and is fine.
- Words that report a state or set a deadline slipped in earlier: "with due care", "is ready", "kept". They are reserved too (the lists below).
- Reserved words. The check throws away a note that uses any of these words (any letter case) outside the SITE and AUDITOR values:
  - number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
  - status words: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
  - modal words: allowed, can, cannot, could, forbidden, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, will, would
  - outcome and paperwork words: bad, behind, breach, breaches, clean, clear, cleared, concern, concerns, current, date, dated, dates, deadline, due, finding, findings, fine, flag, flagged, flags, fresh, good, great, issue, issues, lapse, lapses, lapsing, missing, perfect, problem, problems, ready, renewal, renewed, risk, risky, sign, signed, signoff, smooth, smoothly, sorted, stale, trouble, up-to-date, urgent, urgently, worried, worry
  - profile words: center, centre, cloud, data, hybrid, internal, office, payment, personal, premise, premises, public, store, warehouse, on-premises, and the short word "on"
  - by meaning: any word built on "comply"; the verbs "apply", "cover", "expire" and "lapse" in any form; the verb for not succeeding, in any form; the verb for succeeding at a test or for handing something along to someone, in any form (write "hand over" or "hand to"); the noun for a hole or a missing piece, and its plural; the word for being behind a time limit (over + due)
- No negation of any kind (not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, unless, except, other than, few, refuse to, decline to, neglect to, omit to), no month or weekday name, no digit.
Before you write the file, check each note: SITE and AUDITOR written exactly as given; no word from the lists; no "on"; no empty line.

## Items (13; one JSON object per line)

```json
[
{"qid": "q68a76b6d31", "brief": "Write a work ticket for the review at a library network: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "audit_ticket", "facts": {"SITE": "Marram Point yard", "AUDITOR": "Ulrich Brenner"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "qc3d7e6e914", "brief": "Write a short e-mail about the review at a city parks department: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "auditor_email", "facts": {"SITE": "Eskdale branch", "AUDITOR": "Mateus Rocha"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q4fcead7292", "brief": "Write an internal wiki page header at a veterinary clinic chain: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "site_wiki", "facts": {"SITE": "Gorsey Lane branch", "AUDITOR": "Olumide Adeyemi"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]},
{"qid": "qf1975c1f53", "brief": "Write meeting notes at a hotel group: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "meeting_notes", "facts": {"SITE": "Vale End depot", "AUDITOR": "Amaia Etxeberria"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "qe9025e6aac", "brief": "Write a note jotted at the top of a review sheet at a ski resort: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "checklist_note", "facts": {"SITE": "Thornbury campus", "AUDITOR": "Xenia Moroz"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "qe9541e1c02", "brief": "Write meeting notes at a furniture maker: AUDITOR is going through the records of SITE. Tone: plain and matter-of-fact.", "register": "meeting_notes", "facts": {"SITE": "Yarrow Bank yard", "AUDITOR": "Lucia Ferraz"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q44abc77257", "brief": "Write a note jotted at the top of a review sheet at a laundry service: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "checklist_note", "facts": {"SITE": "Rookwood annex", "AUDITOR": "Nadia Petrova"}, "rules": ["A note of 1-3 sentences jotted at the top of a review sheet."]},
{"qid": "qfa99f21454", "brief": "Write an internal audit memo at a regional bus operator: AUDITOR is going through the records of SITE. Tone: neutral and routine.", "register": "audit_memo", "facts": {"SITE": "Alder Quay depot", "AUDITOR": "Maren Holt"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "q1f6d59ac6e", "brief": "Write a team chat excerpt at a hospital supply firm: AUDITOR is going through the records of SITE. Tone: light and chatty.", "register": "audit_chat", "facts": {"SITE": "Juniper Hill campus", "AUDITOR": "Freya Lindahl"}, "rules": ["A chat excerpt of 2-4 short lines 'speaker: message'; the AUDITOR name is one speaker."]},
{"qid": "q2a1933b6f4", "brief": "Write meeting notes at a coastal rescue charity: AUDITOR is going through the records of SITE. Tone: brisk and busy.", "register": "meeting_notes", "facts": {"SITE": "Upton Reach branch", "AUDITOR": "Leonie Brandt"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q37fbec9209", "brief": "Write an internal audit memo at a chain of bakeries: AUDITOR is going through the records of SITE. Tone: formal and careful.", "register": "audit_memo", "facts": {"SITE": "Dunmore campus", "AUDITOR": "Hilde Sorensen"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "q23c6f30ca0", "brief": "Write an internal audit memo at a tram network: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "audit_memo", "facts": {"SITE": "Cobble Lane yard", "AUDITOR": "Bram de Wit"}, "rules": ["An internal memo of 2-4 sentences."]},
{"qid": "qd830caec1f", "brief": "Write an internal wiki page header at a home care agency: AUDITOR is going through the records of SITE. Tone: warm and friendly.", "register": "site_wiki", "facts": {"SITE": "Hollins Wharf", "AUDITOR": "Talia Romero"}, "rules": ["A wiki page header: a title line and 1-2 sentences."]}
]
```
