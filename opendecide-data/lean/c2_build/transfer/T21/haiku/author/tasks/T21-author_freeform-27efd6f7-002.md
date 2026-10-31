# Haiku authoring task T21-author_freeform-27efd6f7-002 (family T21, kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T21/haiku/author/answers/T21-author_freeform-27efd6f7-002.json

Read this whole file. It is the only file you may open: do not open, list or search any other file or folder.
The answer is one JSON list with exactly 12 objects, one per item below, each carrying that item's qid. Inside JSON strings, write a line break as \n and a double quote as \".

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

## Items (12; answer every item once, keyed by its qid)

```json
[
{"qid": "qf3ac99ce81", "brief": "Write a short note for a board meeting about a contract between a water utility and a pipe maker: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "board_note", "facts": {"CLAIMANT": "Saltire Rail", "AGREEMENT": "Foxdale design agreement"}, "rules": ["A board note of 1-3 sentences."]},
{"qid": "q78f36edf89", "brief": "Write an entry in a log of claims about a contract between a flower grower and a greenhouse maker: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "claims_log", "facts": {"CLAIMANT": "Grassington Furniture", "AGREEMENT": "Ravenglass ticketing agreement"}, "rules": ["A log entry: 2-3 short 'field: value' lines."]},
{"qid": "qc2c01924ee", "brief": "Write a short e-mail about a contract dispute about a contract between a bakery chain and a packaging firm: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "dispute_email", "facts": {"CLAIMANT": "Kestrel Ferries", "AGREEMENT": "Thwaite lighting agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q67b5bd826e", "brief": "Write a short e-mail about a contract dispute about a contract between a film studio and a lighting hire firm: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "dispute_email", "facts": {"CLAIMANT": "Morvah Labs", "AGREEMENT": "Dentdale linen agreement"}, "rules": ["A short e-mail: a greeting line, 1-3 sentences and a sign-off line, one block, no empty line."]},
{"qid": "q7365983e32", "brief": "Write a contract-management ticket about a contract between a recycling company and a haulage firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "contract_ticket", "facts": {"CLAIMANT": "Jarrow Mills", "AGREEMENT": "Allendale hire agreement"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "q013eff89d9", "brief": "Write an entry in a log of claims about a contract between a film studio and a lighting hire firm: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "claims_log", "facts": {"CLAIMANT": "Fenstanton Flowers", "AGREEMENT": "Kettlewell cleaning agreement"}, "rules": ["A log entry: 2-3 short 'field: value' lines."]},
{"qid": "qe2e29a6edb", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between a school district and a catering firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "counsel_chat", "facts": {"CLAIMANT": "Elsworth Theatre", "AGREEMENT": "Farndale catering agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]},
{"qid": "q2ee5676520", "brief": "Write an entry on an internal contracts help page about a contract between a parks department and a landscaping firm: CLAIMANT has raised a claim under AGREEMENT. Tone: neutral and routine.", "register": "contract_faq", "facts": {"CLAIMANT": "Zennor Fisheries", "AGREEMENT": "Haddon Vale printing agreement"}, "rules": ["A help-page entry: a title line ending with '?' and 1-2 sentences."]},
{"qid": "qc6bbabd43d", "brief": "Write a contract-management ticket about a contract between a brewery and a bottling plant: CLAIMANT has raised a claim under AGREEMENT. Tone: plain and matter-of-fact.", "register": "contract_ticket", "facts": {"CLAIMANT": "Netherby Parks", "AGREEMENT": "Langstrath fit-out agreement"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "qe6a5e5ef5e", "brief": "Write a short note for a board meeting about a contract between a hotel group and a booking platform: CLAIMANT has raised a claim under AGREEMENT. Tone: brisk and busy.", "register": "board_note", "facts": {"CLAIMANT": "Penhallow Gardens", "AGREEMENT": "Cawdor installation agreement"}, "rules": ["A board note of 1-3 sentences."]},
{"qid": "q4692e92ec0", "brief": "Write a contract-management ticket about a contract between a university and a building firm: CLAIMANT has raised a claim under AGREEMENT. Tone: formal and careful.", "register": "contract_ticket", "facts": {"CLAIMANT": "Mallory Toys", "AGREEMENT": "Dunsford maintenance agreement"}, "rules": ["A ticket: 2-3 short 'field: value' lines and one sentence."]},
{"qid": "q8472c49b4d", "brief": "Write a chat excerpt between in-house counsel and a colleague about a contract between a library network and a software house: CLAIMANT has raised a claim under AGREEMENT. Tone: warm and friendly.", "register": "counsel_chat", "facts": {"CLAIMANT": "Gilmore Tea House", "AGREEMENT": "Birchover services agreement"}, "rules": ["A chat excerpt of 2-4 short lines 'role: message', roles in lower case."]}
]
```
