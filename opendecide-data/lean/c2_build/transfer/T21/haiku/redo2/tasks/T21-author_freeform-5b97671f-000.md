# Haiku authoring task T21-author_freeform-5b97671f-000 (family T21, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/haiku/redo2/answers/T21-author_freeform-5b97671f-000.json

Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.
The answer is one JSON list with exactly 8 objects, one per item below, each carrying that item's qid. Inside JSON strings, write a line break as \n and a double quote as \".

## Instructions

You write short free-form workplace notes that open a contract-reading puzzle. Each item gives a register, a brief and two facts: CLAIMANT (the organisation that brings a claim) and AGREEMENT (the full name of the agreement it relies on). Write ONE note per item.

Rules (a program rejects any note that breaks one):
1. Write the CLAIMANT name and the AGREEMENT name exactly as given (same spelling, spaces and capitals), each at least once. Write no other name of a person, place, company or product. The AGREEMENT name already ends with the word "agreement": never write the word "agreement" again right after it.
2. The note only sets the scene, in the register and tone asked for: the CLAIMANT organisation has raised a claim under the AGREEMENT, and the clauses follow. Name the claim or the dispute only in general words. Never say what the claim is about or what caused it, never mention any clause or its number, any limit or cap, liability, notice, timing, money, a court, or how the matter will end, and never say what anyone may, must, should or will do.
3. No digits, number words or ordinals (one, first, second, half, single ...), no dates, times, months or weekdays, no currency or percent signs, no codes that mix letters and digits, no e-mail or web addresses.
4. No negation of any kind (not, n't, no, never, nothing, nobody, none, without, cannot, lack, hardly, unless, except, other than, neither, nor).
5. No word that judges or reports a state or an outcome: approved, valid, invalid, failed, failure, success, complete, completed, done, finished, pending, open, closed, active, settled, resolved, outstanding, breached, waived, granted, ok, okay, fine, good, bad, strong, weak, safe, risky, win, lose.
6. Never use these words: breach, confidentiality, secret, privacy, data, protection, leak, intellectual, property, patent, copyright, trademark, infringement, late, delay, delivery, shipment, defective, faulty, goods, fees, invoice, payment, unpaid, injury, accident, harm, damage, fire, flood, security, incident, hack, negligence, careless, misconduct, deliberate, fraud, subcontractor, contractor, supplier, vendor, mistake, error, cap, limit, liability, notice, apply, switch, decide, chain, cover, court, law, amount, money, damages, insurance, outcome, result.
7. One block of text with no empty line, 1-4 sentences of plain, natural English, and no curly braces. Never write the headings "Clauses of the", "Schedule of clauses" or "Claim:".

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the note>"}. Use \n for line breaks inside the text. Every note must differ from every other note you write.

Extra word rules for this round (a program rejects a note that uses any of these words outside the two names; earlier notes were turned down for words like these): kept, full, fully, ordinary, confirmed, approved, resolved, settled, pending, accepted, rejected, completed, valid, paid, broken, entitled, eligible, open, closed, active, done, finished, outstanding.

## Answer format

[{"qid": "q...", "text": "..."}, ...]

## Items (8; answer every item once, keyed by its qid)

```json
[
{"qid": "q7a691d3826", "brief": "Write a short e-mail about a contract dispute about a contract between a saddlery and a tannery: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "dispute_email", "facts": {"CLAIMANT": "Brackley Canal Boats", "AGREEMENT": "Bowland kiln lease agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "qd844ed852f", "brief": "Write an entry on an internal contracts help page about a contract between a saddlery and a tannery: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "contract_faq", "facts": {"CLAIMANT": "Oakhanger Organs", "AGREEMENT": "Ousby organ tuning agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "q2c84ae7feb", "brief": "Write an internal legal memo about a contract between a lighthouse museum and a lamp restorer: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "legal_memo", "facts": {"CLAIMANT": "Hutton Moor Lodges", "AGREEMENT": "Hallin Fell lodging agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "q81cf5ac546", "brief": "Write an entry on an internal contracts help page about a contract between a pottery and a kiln builder: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "contract_faq", "facts": {"CLAIMANT": "Pendlebury Chandlers", "AGREEMENT": "Portinscale candle agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "q7fdd583390", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between an orchard and a cider press: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "counsel_chat", "facts": {"CLAIMANT": "Muncaster Weavers", "AGREEMENT": "Mosedale weaving agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]},
{"qid": "qa5b75d7e8a", "brief": "Write an entry on an internal contracts help page about a contract between a canal trust and a lock engineer: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "contract_faq", "facts": {"CLAIMANT": "Nethercott Saddlery", "AGREEMENT": "Nenthead leather agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "qdcddc3512b", "brief": "Write a short e-mail about a contract dispute about a contract between a map publisher and a print shop: CLAIMANT has raised a claim under AGREEMENT. Tone: light and chatty.", "register": "dispute_email", "facts": {"CLAIMANT": "Fernhill Orchards", "AGREEMENT": "Fellside orchard agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "qe1cfd4920d", "brief": "Write a short e-mail about a contract dispute about a contract between a pottery and a kiln builder: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "dispute_email", "facts": {"CLAIMANT": "Caldbeck Pottery", "AGREEMENT": "Crummock rigging agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]}
]
```
