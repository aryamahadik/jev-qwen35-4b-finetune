# Haiku authoring task T21-author_freeform-27efd6f7-001 (family T21, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/haiku/author/answers/T21-author_freeform-27efd6f7-001.json

Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.
The answer is one JSON list with exactly 14 objects, one per item below, each carrying that item's qid. Inside JSON strings, write a line break as \n and a double quote as \".

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

## Answer format

[{"qid": "q...", "text": "..."}, ...]

## Items (14; answer every item once, keyed by its qid)

```json
[
{"qid": "q89a82e1992", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between a ski resort and a lift engineer: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "counsel_chat", "facts": {"CLAIMANT": "Hesketh Timber", "AGREEMENT": "Ilkley Moor booking agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]},
{"qid": "qadd0eb8551", "brief": "Write a contract-management ticket about a contract between a marina and a boat builder: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "contract_ticket", "facts": {"CLAIMANT": "Kilbride Marina", "AGREEMENT": "Hawes Mill restoration agreement"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "q15c4963270", "brief": "Write notes from a negotiation meeting about a contract between a museum trust and an exhibition designer: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "negotiation_notes", "facts": {"CLAIMANT": "Varley Dental", "AGREEMENT": "Ennerdale planting agreement"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q8870b013a8", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between a dental group and a lab: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "counsel_chat", "facts": {"CLAIMANT": "Farrow Glass", "AGREEMENT": "Newlands joinery agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]},
{"qid": "q77825d42a6", "brief": "Write an internal legal memo about a contract between a gym chain and an equipment lessor: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "legal_memo", "facts": {"CLAIMANT": "Bellhaven Hotels", "AGREEMENT": "Glenridding staffing agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "q074c0bdefb", "brief": "Write an entry on an internal contracts help page about a contract between a grain cooperative and a mill: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "contract_faq", "facts": {"CLAIMANT": "Carrick Museum Trust", "AGREEMENT": "Grisedale fleet agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "q3805d10a56", "brief": "Write a contract-management ticket about a contract between a garden trust and a glasshouse restorer: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "contract_ticket", "facts": {"CLAIMANT": "Lanark Cinemas", "AGREEMENT": "Patterdale outfitting agreement"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "q694ac3ece4", "brief": "Write a short e-mail about a contract dispute about a contract between a rail operator and an engineering firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "dispute_email", "facts": {"CLAIMANT": "Brindle Foods", "AGREEMENT": "Lowmoor hosting agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q95a00b8987", "brief": "Write a short e-mail about a contract dispute about a contract between a theatre company and a set builder: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "dispute_email", "facts": {"CLAIMANT": "Pellow Studio", "AGREEMENT": "Marsden testing agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q982f3f8ed2", "brief": "Write notes from a negotiation meeting about a contract between a solar farm and a panel installer: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "negotiation_notes", "facts": {"CLAIMANT": "Ullswater Film", "AGREEMENT": "Ulpha engineering agreement"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "q96a308701d", "brief": "Write a short e-mail about a contract dispute about a contract between a grain cooperative and a mill: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "dispute_email", "facts": {"CLAIMANT": "Orrin Haulage", "AGREEMENT": "Eskmeals equipment agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q83f09f3284", "brief": "Write an entry on an internal contracts help page about a contract between a dairy and a cold store: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "contract_faq", "facts": {"CLAIMANT": "Abbotsley Linen", "AGREEMENT": "Penmaen storage agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "q2b3a67dedb", "brief": "Write a short note for a board meeting about a contract between an airport and a baggage systems firm: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "board_note", "facts": {"CLAIMANT": "Rosedene Care", "AGREEMENT": "Fenwick freight agreement"}, "rules": ["A board note of 1-3 sentences."]},
{"qid": "q1182e2e426", "brief": "Write an entry in a log of claims about a contract between a ferry company and a shipyard: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "claims_log", "facts": {"CLAIMANT": "Hartland Airport", "AGREEMENT": "Bransdale studio agreement"}, "rules": ["A log entry: 2-3 short 'field: value' lines."]}
]
```
