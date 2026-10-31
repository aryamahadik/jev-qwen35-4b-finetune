# Haiku authoring task T21-author_freeform-27efd6f7-000 (family T21, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/haiku/author/answers/T21-author_freeform-27efd6f7-000.json

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
{"qid": "q34045723dc", "brief": "Write an internal legal memo about a contract between a ferry company and a shipyard: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "legal_memo", "facts": {"CLAIMANT": "Ashcombe Brewing", "AGREEMENT": "Calder Mill lease agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "q1d8f88e5d5", "brief": "Write an internal legal memo about a contract between a hospital and an equipment maker: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "legal_memo", "facts": {"CLAIMANT": "Dunlin Dairy", "AGREEMENT": "Wasdale glazing agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "qa94deb2890", "brief": "Write an internal legal memo about a contract between a flower grower and a greenhouse maker: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "legal_memo", "facts": {"CLAIMANT": "Tarrant Print", "AGREEMENT": "Loweswater lift agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "q101b75acd8", "brief": "Write an entry in a log of claims about a contract between a gym chain and an equipment lessor: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "claims_log", "facts": {"CLAIMANT": "Inverlochy Rentals", "AGREEMENT": "Ingleby display agreement"}, "rules": ["A log entry: 2-3 short 'field: value' lines."]},
{"qid": "q549694ba75", "brief": "Write notes from a negotiation meeting about a contract between a tram network and a signalling firm: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "negotiation_notes", "facts": {"CLAIMANT": "Wraxall Grain", "AGREEMENT": "Mardale staging agreement"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "qc78618d97b", "brief": "Write a short note for a board meeting about a contract between a toy maker and a design studio: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "board_note", "facts": {"CLAIMANT": "Osprey Ski Lifts", "AGREEMENT": "Sandwood rental agreement"}, "rules": ["A board note of 1-3 sentences."]},
{"qid": "q59d5756fc6", "brief": "Write notes from a negotiation meeting about a contract between a care agency and a staffing firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "negotiation_notes", "facts": {"CLAIMANT": "Tolland Bakeries", "AGREEMENT": "Nantlle software agreement"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]},
{"qid": "qb3873cd21c", "brief": "Write an internal legal memo about a contract between a car rental firm and a fleet dealer: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "legal_memo", "facts": {"CLAIMANT": "Corwen Tramways", "AGREEMENT": "Oxwich bottling agreement"}, "rules": ["An internal legal memo of 2-4 sentences."]},
{"qid": "qb5706eaa6d", "brief": "Write an entry on an internal contracts help page about a contract between a rail operator and an engineering firm: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "contract_faq", "facts": {"CLAIMANT": "Blackmore Laundry", "AGREEMENT": "Yarrowford packaging agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "q08a527f821", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between a hostel network and a linen firm: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "counsel_chat", "facts": {"CLAIMANT": "Ivel Valley Water", "AGREEMENT": "Quernmore signage agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]},
{"qid": "qc908a15970", "brief": "Write a short note for a board meeting about a contract between a print works and a paper mill: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "board_note", "facts": {"CLAIMANT": "Quarrel Bay Hostels", "AGREEMENT": "Kirkstone carriage agreement"}, "rules": ["A board note of 1-3 sentences."]},
{"qid": "q8d0b772563", "brief": "Write an entry on an internal contracts help page about a contract between a theatre company and a set builder: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "contract_faq", "facts": {"CLAIMANT": "Delph Recycling", "AGREEMENT": "Ormside panel agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "qfe77ce06c4", "brief": "Write an entry in a log of claims about a contract between a bakery chain and a packaging firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "claims_log", "facts": {"CLAIMANT": "Edale Gyms", "AGREEMENT": "Coldharbour licence agreement"}, "rules": ["A log entry: 2-3 short 'field: value' lines."]},
{"qid": "q97b99462d7", "brief": "Write notes from a negotiation meeting about a contract between a cinema chain and a projection firm: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "negotiation_notes", "facts": {"CLAIMANT": "Yelland Solar", "AGREEMENT": "Ashgrove catering agreement"}, "rules": ["A heading line ending with a colon and 2-3 lines starting with '- '."]}
]
```
