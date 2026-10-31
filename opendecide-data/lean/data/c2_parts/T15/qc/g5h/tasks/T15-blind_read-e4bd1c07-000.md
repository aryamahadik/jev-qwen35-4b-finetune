# G5-H blind read T15-blind_read-e4bd1c07-000 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-e4bd1c07-000.json

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
  "qid": "qc897a09c44",
  "kind": "yes/no",
  "text": "record: CASE-49260\nlead: Morgan Mendoza\nsubject: Anton Becker\n\nFacts for Anton Becker (2027):\n- gross monthly income: 3,104.16 USD\n- net monthly income: 1,341.33 USD\n- countable assets: 707.59 USD\n- time in the service area: 47 months\n- age: 69 years\n- enrolled in: Sallowby Water Rebate",
  "question": "Is Anton Becker eligible for Ostmere Lakeside Winter Energy Support with every applicable gate passed?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly under 1,969.51 USD.\n- Gate B: passed when the applicant's age is at or over 57 years.\n- Gate C: passed when net monthly income is at or less than 1,401.88 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q88a1811bf6",
  "kind": "choice",
  "text": "Routine note: CR-51814\nFrom Ezra Rosales for the call centre, about Theo.\n\nPeople who asked to claim Theo (2026):\n- Kiara Mensah: relationship to Theo: mother; months lived with Theo: 11 months; annual income: 48,574.54 USD; filed a claim: no\n- Cyril Ruiz: relationship to Theo: uncle; months lived with Theo: 7 months; annual income: 22,920.06 USD; filed a claim: yes",
  "question": "Dunmarrow Hill Allowance rules for 2026: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for at or beyond 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Theo lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is allowed to claim Theo for Dunmarrow Hill Allowance?",
  "options": [
   "Cyril Ruiz",
   "Kiara Mensah"
  ]
 },
 {
  "qid": "qf0d9e65e3d",
  "kind": "yes/no",
  "text": "Facts for Ibrahim Ferreira (2025):\n| fact | value |\n| --- | --- |\n| time employed | 22 months |\n| hours worked in the past year | 1648 hours |\n| employees at the worksite | 221 employees |\n| gross annual pay | 42,221.87 USD |\n| take-home annual pay | 32,738.86 USD |\n| enrolled in | none |\n\n[busy_queue] case=HR-67412 worker=Sasha Okonkwo subject=Ibrahim Ferreira",
  "question": "Does Ibrahim Ferreira fully qualify for Pelmoor Ceramics Carer Support under these rules?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for 23 months at minimum.\n- Gate B: passed when take-home annual pay is strictly under the amount of 35,876.82 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q24fb72a67a",
  "kind": "choice",
  "text": "[hub_entry] ref=CASE-74434 handler=Kendall Umarov subject=Cyril Anderson\n\nIntake interview with Cyril Anderson (2027):\nCaseworker: Gross monthly income?\nCyril Anderson: 2,092.39 USD.\nCaseworker: Net monthly income?\nCyril Anderson: 1,679.68 USD.\nCaseworker: Countable assets?\nCyril Anderson: 13,344.08 USD.\nCaseworker: Time in the service area?\nCyril Anderson: three months.\nCaseworker: Age?\nCyril Anderson: 38 years.\nCaseworker: Other programme enrolled in?\nCyril Anderson: none.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly beneath the level of 2,955.21 USD.\n- Gate B: passed when the applicant has lived in the service area for strictly greater than twelve months.\n- Gate C: passed when net monthly income is strictly smaller than 2,162.59 USD.\n- Gate D: passed when the applicant's age is over 65 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Cyril Anderson to Ostermere Delta Flood Repair Support receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate D is the reason (age)",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q7406db4f18",
  "kind": "yes/no",
  "text": "Internal note for the branch desk. HR-08537 rests with Avery Obradovic and concerns Priya Evans.\n\nFacts for Priya Evans (2026):\n- time employed: 76 months\n- hours worked in the past year: 1410 hours\n- employees at the worksite: 257 employees\n- gross annual pay: 75,190.17 USD\n- take-home annual pay: 62,070.49 USD\n- enrolled in: Fallowden Retraining Bursary",
  "question": "According to these rules, does Priya Evans qualify for Tovardine Seed Caregiver Leave?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or greater than 1410 hours.\n- Gate B: passed when take-home annual pay is strictly under the amount of 54,873.43 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf23c63a3a2",
  "kind": "yes/no",
  "text": "{\"case\": \"CR-50379\", \"caseworker\": \"Jamie Jorgensen\", \"about\": \"Mia\", \"line\": \"help\"}\n\nPeople who asked to claim Mia (2026), as JSON:\n{\"people\": [{\"name\": \"Yusuf Kaur\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"92,197.15 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Pavel Evans\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"72,845.15 USD\", \"filed_a_claim\": \"no\"}]}",
  "question": "Is it true that Pavel Evans may not claim Mia for Tessenvale Valley Child Credit?",
  "definitions": "Tessenvale Valley Child Credit rules for 2026: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for at or over 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa342f83ba4",
  "kind": "yes/no",
  "text": "Ren Dvorak: Thread for HR-20828 covers Dani Hudson.\n\nIntake interview with Dani Hudson (2026):\nCaseworker: Time employed?\nDani Hudson: fourteen months.\nCaseworker: Hours worked in the past year?\nDani Hudson: 236 hours.\nCaseworker: Employees at your worksite?\nDani Hudson: sixteen employees.\nCaseworker: Gross annual pay?\nDani Hudson: $43,362.54.\nCaseworker: Take-home annual pay?\nDani Hudson: $35,867.12.\nCaseworker: Other programme enrolled in?\nDani Hudson: Quendrel Skills Voucher.",
  "question": "Is Dani Hudson eligible for Brenwold Timber Apprentice Support by passing every gate that applies?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has a minimum of seventeen employees.\n- Gate B: passed when the applicant has been employed for at or over 22 months.\n- Gate C: passed when gross annual pay is lower than $43,362.53.\n- Route: an applicant enrolled in Quendrel Skills Voucher skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdf5730deac",
  "kind": "choice",
  "text": "Intake form: call centre\nCase reference: HR-71442\nCaseworker: Blair Xiong\nAbout: Viktor Ortega\n\nIntake interview with Viktor Ortega (2027):\nCaseworker: Time employed?\nViktor Ortega: 5 months.\nCaseworker: Hours worked in the past year?\nViktor Ortega: 1498 hours.\nCaseworker: Employees at your worksite?\nViktor Ortega: 38 employees.\nCaseworker: Gross annual pay?\nViktor Ortega: $102,518.99.\nCaseworker: Take-home annual pay?\nViktor Ortega: $65,224.45.\nCaseworker: Other programme enrolled in?\nViktor Ortega: Quelmere Lunch Card.",
  "question": "Sorrelby Child Care Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are greater than or equal to 1480 hours.\n- Gate B: passed when the applicant has been employed for at or beyond 17 months.\n- Gate C: passed when the worksite has strictly over 48 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does Viktor Ortega get on the application to Sorrelby Child Care Support under these rules?",
  "options": [
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible"
  ]
 },
 {
  "qid": "qd987e5107d",
  "kind": "yes/no",
  "text": "[casework_team] case_id=HR-68980\n[casework_team] worker=Kiran Morales about=Freya Hakimi\n\nIntake interview with Freya Hakimi (2025):\nCaseworker: Time employed?\nFreya Hakimi: 28 months.\nCaseworker: Hours worked in the past year?\nFreya Hakimi: 1701 hours.\nCaseworker: Employees at your worksite?\nFreya Hakimi: 24 employees.\nCaseworker: Gross annual pay?\nFreya Hakimi: 36,560.11 USD.\nCaseworker: Take-home annual pay?\nFreya Hakimi: 27,740.62 USD.\nCaseworker: Other programme enrolled in?\nFreya Hakimi: Osterlin Tool Allowance.",
  "question": "Does Freya Hakimi fully qualify for Brenwold Timber Apprentice Support under these rules?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly in excess of nineteen months.\n- Gate B: passed when hours worked in the past year are strictly above 1300 hours.\n- Gate C: passed when the worksite has strictly over 36 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa250e42480",
  "kind": "yes/no",
  "text": "Routine case note: CR-06151 sits with Yuki Adeyemi about Ami. Standard entry for the call centre.\n\nPeople who asked to claim Ami (2025):\n- Ilse Nakamura: relationship to Ami: mother; months lived with Ami: four months; annual income: $94,707; filed a claim: no\n- Bruno Robinson: relationship to Ami: father; months lived with Ami: twelve months; annual income: $23,970; filed a claim: yes\n- Hamid Ilic: relationship to Ami: grandfather; months lived with Ami: nine months; annual income: $70,044; filed a claim: no\n- Idris Zielinski: relationship to Ami: grandfather; months lived with Ami: ten months; annual income: $80,502; filed a claim: yes",
  "question": "According to these rules, is Hamid Ilic the person who ends up with the right to claim Ami for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for higher than five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q72fb8751a9",
  "kind": "yes/no",
  "text": "Facts for Hiroko Murphy (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,037.73 |\n| net monthly income | $2,285.33 |\n| countable assets | $8,751.83 |\n| time in the service area | sixteen months |\n| age | 63 years |\n| enrolled in | Caddow Pantry Basket |\n\n[team_note] Quinn Pavlenko keeps file CASE-16622 with kind care\n[about] Hiroko Murphy is the focus",
  "question": "Under these rules, does Hiroko Murphy meet the rules for Sallowick Ward Home Repair Grant across every applicable gate?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or beneath $3,037.74.\n- Gate B: passed when the applicant has lived in the service area for at or over twelve months.\n- Gate C: passed when the applicant's age is greater than 62 years.\n- Gate D: passed when net monthly income is at or under the amount of $2,285.33.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdfd6a099c8",
  "kind": "yes/no",
  "text": "{\"case_ref\": \"CR-08994\", \"handler\": \"Shay Bekele\", \"about\": \"Uri\", \"type\": \"file\"}\n\nInterview notes for Uri (2026):\nCaseworker: Mariam Patterson, your relation to Uri?\nMariam Patterson: I am Uri's grandmother.\nCaseworker: Months Uri lived with you?\nMariam Patterson: three months.\nCaseworker: Annual income?\nMariam Patterson: $17,217.81.\nCaseworker: Filed a claim for Uri?\nMariam Patterson: yes.\nCaseworker: Dario Sullivan, your relation to Uri?\nDario Sullivan: I am Uri's father.\nCaseworker: Months Uri lived with you?\nDario Sullivan: two months.\nCaseworker: Annual income?\nDario Sullivan: $94,372.\nCaseworker: Filed a claim for Uri?\nDario Sullivan: no.\nCaseworker: Ailsa Ilunga, your relation to Uri?\nAilsa Ilunga: I am Uri's grandmother.\nCaseworker: Months Uri lived with you?\nAilsa Ilunga: twelve months.\nCaseworker: Annual income?\nAilsa Ilunga: $70,529.\nCaseworker: Filed a claim for Uri?\nAilsa Ilunga: yes.",
  "question": "Does Dario Sullivan end up as the sole person who may claim Uri for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2026: who may claim Uri.\n- Only one person may claim Uri. Work through these steps in order.\n- Step one: only people who filed a claim for Uri are considered.\n- Step two: of those, only people with whom Uri lived for six months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Uri lived for more months comes first.\n- If nobody is left after step two, nobody may claim Uri.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qbd70975093",
  "kind": "yes/no",
  "text": "Regional service office intake\nCase reference: CR-20697\nCaseworker: Ari Benali\nSubject: Elif\n\nPeople who asked to claim Elif (2027):\n| person | relationship to Elif | months lived with Elif | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Galina Douglas | grandmother | 7 months | $15,350.00 | yes |\n| Xenia Thompson | mother | 3 months | $79,240.00 | yes |\n| Gustav Okoro | father | 12 months | $53,439.06 | no |",
  "question": "Does the right to claim Elif for Dunmarrow Hill Allowance pass to a different person from Gustav Okoro, or stay unclaimed under these rules?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for at or over 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Elif lived for more months comes first.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf31ce38491",
  "kind": "choice",
  "text": "Hello team,\nThank you for reviewing case CR-92791 with a warm eye on Ana.\nWarm regards, Cameron Vargas\n\nInterview notes for Ana (2027):\nCaseworker: Yasmin Hamilton, your relation to Ana?\nYasmin Hamilton: I am Ana's grandmother.\nCaseworker: Months Ana lived with you?\nYasmin Hamilton: 6 months.\nCaseworker: Annual income?\nYasmin Hamilton: $61,752.\nCaseworker: Filed a claim for Ana?\nYasmin Hamilton: yes.\nCaseworker: Leila Yilmaz, your relation to Ana?\nLeila Yilmaz: I am Ana's aunt.\nCaseworker: Months Ana lived with you?\nLeila Yilmaz: 9 months.\nCaseworker: Annual income?\nLeila Yilmaz: $61,752.\nCaseworker: Filed a claim for Ana?\nLeila Yilmaz: no.\nCaseworker: Yusuf Ivanova, your relation to Ana?\nYusuf Ivanova: I am Ana's father.\nCaseworker: Months Ana lived with you?\nYusuf Ivanova: 5 months.\nCaseworker: Annual income?\nYusuf Ivanova: $42,284.12.\nCaseworker: Filed a claim for Ana?\nYusuf Ivanova: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2027: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for a minimum of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Ana for Kelmstone Mountain Family Grant under these rules?",
  "options": [
   "Yusuf Ivanova",
   "Nobody may claim the child",
   "Yasmin Hamilton"
  ]
 },
 {
  "qid": "qa9d0d109f4",
  "kind": "yes/no",
  "text": "Dear Joon,\nThis is a standard notice about CR-64237 from the district office.\nKind regards, Sami Castro\n\nPeople who asked to claim Joon (2027):\n- Bianca Abara: relationship to Joon: aunt; months lived with Joon: ten months; annual income: $68,334.21; filed a claim: yes\n- Amara Kaur: relationship to Joon: mother; months lived with Joon: one month; annual income: $88,961; filed a claim: no\n- Rania Patterson: relationship to Joon: grandmother; months lived with Joon: eight months; annual income: $68,334.21; filed a claim: yes",
  "question": "According to these rules, is Rania Patterson the person who ends up with the right to claim Joon for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for higher than five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Joon lived for more months comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q065b71ac8b",
  "kind": "yes/no",
  "text": "Facts for Kofi Demir (2027), as JSON:\n{\"gross_monthly_income\": \"$3,636.90\", \"net_monthly_income\": \"$2,734.54\", \"countable_assets\": \"$17,853.04\", \"time_in_the_service_area\": \"51 months\", \"age\": \"83 years\", \"enrolled_in\": \"Velden Transit Badge\"}\n\n{\"record\": \"case\", \"reference\": \"CASE-09703\", \"caseworker\": \"Kendall Umarov\", \"about\": \"Kofi Demir\"}",
  "question": "Under these rules, does Kofi Demir meet the rules for Sallowick Ward Home Repair Grant across every applicable gate?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below $11,962.62.\n- Gate B: passed when net monthly income is at or under $2,734.55.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q61ebcc75cc",
  "kind": "choice",
  "text": "Ticket CASE-77975\nWith: Ari Benali\nAbout: Jamie Delgado\n\nFacts for Jamie Delgado (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,392.87 USD |\n| net monthly income | 2,635.57 USD |\n| countable assets | 4,100.79 USD |\n| time in the service area | 46 months |\n| age | 49 years |\n| enrolled in | Corrivale Meal Voucher |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or beneath 3,392.86 USD.\n- Gate B: passed when countable assets are 4,100.78 USD or under.\n- Gate C: passed when the applicant's age is higher than 64 years.\n- Route: an applicant enrolled in Corrivale Meal Voucher skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Jamie Delgado to Tesslow Prairie Water Bill Assistance?",
  "options": [
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qd59db13060",
  "kind": "choice",
  "text": "People who asked to claim Ana (2027):\n| person | relationship to Ana | months lived with Ana | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Yusuf Hudson | uncle | six months | $38,662 | yes |\n| Kiara Mitchell | aunt | one month | $83,134 | yes |\n\nQuick note from the help line: Ren Dvorak is on CR-04195 for Ana.",
  "question": "Brellow Orchard Family Credit rules for 2027: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for at or over six months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ana lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Ana for Brellow Orchard Family Credit?",
  "options": [
   "Nobody may claim the child",
   "Yusuf Hudson",
   "Kiara Mitchell"
  ]
 },
 {
  "qid": "q36f2a85bd8",
  "kind": "choice",
  "text": "Ezra Rosales: counter queue has HR-75160, and it is about Nkechi Dubois.\n\nFacts for Nkechi Dubois (2026):\n- time employed: eight months\n- hours worked in the past year: 1,791 hours\n- employees at the worksite: 45 employees\n- gross annual pay: 67,513.46 USD\n- take-home annual pay: 51,045.74 USD\n- enrolled in: Quillmere Apprentice Pathway",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or above 1,160 hours.\n- Gate B: passed when the worksite has strictly higher than 45 employees.\n- Gate C: passed when the applicant has been employed for nine months or above.\n- Route: an applicant enrolled in Quillmere Apprentice Pathway skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Nkechi Dubois to Halvorne Shipyard Tuition Assistance get?",
  "options": [
   "Not eligible: Gate C is the reason (time employed)",
   "Eligible",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "qf8a4e8ca0b",
  "kind": "choice",
  "text": "Facts for Ari Evans (2027):\n| fact | value |\n| --- | --- |\n| time employed | 13 months |\n| hours worked in the past year | 50 hours |\n| employees at the worksite | 146 employees |\n| gross annual pay | $34,853.54 |\n| take-home annual pay | $22,471.60 |\n| enrolled in | Ostermere Respite Stay |\n\nCase note: the intake desk has Ari Evans on case HR-72599, with Lior Grigoryan in charge.",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly beneath the level of $40,062.67.\n- Gate B: passed when the applicant has been employed for strictly higher than 8 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Ari Evans to Pelmoor Ceramics Carer Support ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "qffe175f8f2",
  "kind": "choice",
  "text": "People who asked to claim Dara (2026):\n| person | relationship to Dara | months lived with Dara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Emeka Nilsen | father | 4 months | $70,087.00 | yes |\n| Mirela Reynolds | aunt | 12 months | $38,066.27 | no |\n| Ravi Gutierrez | grandfather | 7 months | $48,400.94 | yes |\n\nIntake form, help line team\nCase reference: CR-01801\nCaseworker: Cameron Vargas\nAbout: Dara",
  "question": "Brellow Orchard Family Credit rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for 7 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Dara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which candidate, if any, may claim Dara for Brellow Orchard Family Credit?",
  "options": [
   "Ravi Gutierrez",
   "Nobody may claim the child",
   "Emeka Nilsen"
  ]
 },
 {
  "qid": "q6ef8e07363",
  "kind": "choice",
  "text": "Hi,\nQuick update: file CASE-98201 about Freya Nguyen is in my queue.\nThanks, Dani Ishikawa\n\nIntake interview with Freya Nguyen (2026):\nCaseworker: Gross monthly income?\nFreya Nguyen: $2,229.88.\nCaseworker: Net monthly income?\nFreya Nguyen: $1,309.40.\nCaseworker: Countable assets?\nFreya Nguyen: $5,414.41.\nCaseworker: Time in the service area?\nFreya Nguyen: 28 months.\nCaseworker: Age?\nFreya Nguyen: 37 years.\nCaseworker: Other programme enrolled in?\nFreya Nguyen: none.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or below the level of $10,581.01.\n- Gate B: passed when gross monthly income is strictly beneath the level of $3,738.10.\n- Gate C: passed when net monthly income is strictly beneath the level of $2,798.71.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tamsfell Senior Home Support, which outcome does the application of Freya Nguyen get?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qf33acd65b1",
  "kind": "yes/no",
  "text": "Dear colleague,\nFor the record, CASE-40885 concerning Priya Sullivan is held by the desk.\nYours faithfully, Sami Castro\n\nFacts for Priya Sullivan (2026):\n- gross monthly income: 3,943.48 USD\n- net monthly income: 2,483.82 USD\n- countable assets: 3,427.18 USD\n- time in the service area: 4 months\n- age: 54 years\n- enrolled in: Kelmstone Parent Learning Grant",
  "question": "Following the listed rules, does a gate that applies halt the application of Priya Sullivan to Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for 4 months or greater.\n- Gate B: passed when countable assets are strictly under the amount of 3,427.18 USD.\n- Gate C: passed when gross monthly income is strictly under the value of 3,943.49 USD.\n- Route: an applicant enrolled in Stonevale Housing Loan skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q043ec7e4f0",
  "kind": "yes/no",
  "text": "Services counter intake form\nCase reference: CR-37995\nCaseworker: Sasha Okonkwo\nAbout: Kai\n\nPeople who asked to claim Kai (2027):\n| person | relationship to Kai | months lived with Kai | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Zainab Rahimi | mother | zero months | 43,566.77 USD | no |\n| Jiro Hamilton | father | seven months | $24,273 | yes |\n| Dmitri Kimura | grandfather | nine months | $44,575 | yes |",
  "question": "According to these rules, is Jiro Hamilton the person who ends up with the right to claim Kai for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for strictly greater than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Kai lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb441c3e7a8",
  "kind": "choice",
  "text": "team: people services\ncase: CR-92791\ncaseworker: Cameron Vargas\nabout: Ana\n\nInterview notes for Ana (2027):\nCaseworker: Yasmin Hamilton, your relation to Ana?\nYasmin Hamilton: I am Ana's grandmother.\nCaseworker: Months Ana lived with you?\nYasmin Hamilton: 6 months.\nCaseworker: Annual income?\nYasmin Hamilton: $61,752.\nCaseworker: Filed a claim for Ana?\nYasmin Hamilton: yes.\nCaseworker: Leila Yilmaz, your relation to Ana?\nLeila Yilmaz: I am Ana's aunt.\nCaseworker: Months Ana lived with you?\nLeila Yilmaz: 9 months.\nCaseworker: Annual income?\nLeila Yilmaz: $61,752.\nCaseworker: Filed a claim for Ana?\nLeila Yilmaz: no.\nCaseworker: Yusuf Ivanova, your relation to Ana?\nYusuf Ivanova: I am Ana's father.\nCaseworker: Months Ana lived with you?\nYusuf Ivanova: 5 months.\nCaseworker: Annual income?\nYusuf Ivanova: $42,284.12.\nCaseworker: Filed a claim for Ana?\nYusuf Ivanova: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2027: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for a minimum of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Ana for Kelmstone Mountain Family Grant under these rules?",
  "options": [
   "Yusuf Ivanova",
   "Nobody may claim the child",
   "Yasmin Hamilton"
  ]
 },
 {
  "qid": "q3683d1079c",
  "kind": "yes/no",
  "text": "People who asked to claim Lina (2027):\n| person | relationship to Lina | months lived with Lina | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Yara Rahimi | mother | 7 months | 49,656.45 USD | yes |\n| Ivo Gallegos | father | 7 months | 81,433.00 USD | yes |\n| Elias Murphy | uncle | 4 months | 92,839.00 USD | no |\n\nMika Zamora: Noted, CR-60206 for Lina sits with the intake desk.",
  "question": "According to these rules, does the right to claim Lina for Mollenby Canal Child Supplement go to a different person from Elias Murphy, or stay unclaimed?",
  "definitions": "Mollenby Canal Child Supplement rules for 2027: who may claim Lina.\n- Only one person may claim Lina. Work through these steps in order.\n- Step one: only people who filed a claim for Lina are considered.\n- Step two: of those, only people with whom Lina lived for higher than 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Lina lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Lina.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc986edacf8",
  "kind": "choice",
  "text": "Yuki Adeyemi: quick ping, CR-50260 is in the people services queue for Nia.\n\nPeople who asked to claim Nia (2026):\n- Yusuf Evans: relationship to Nia: father; months lived with Nia: 3 months; annual income: 69,128.00 USD; filed a claim: yes\n- Hana Patterson: relationship to Nia: mother; months lived with Nia: 0 months; annual income: 73,940.00 USD; filed a claim: yes\n- Greta Iyer: relationship to Nia: aunt; months lived with Nia: 0 months; annual income: 73,940.00 USD; filed a claim: no",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Nia.\n- Only one person may claim Nia. Work through these steps in order.\n- Step one: only people who filed a claim for Nia are considered.\n- Step two: of those, only people with whom Nia lived for strictly higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Nia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Nia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Nia for Tollmere Lakeside Family Payment?",
  "options": [
   "Yusuf Evans",
   "Nobody may claim the child",
   "Hana Patterson"
  ]
 },
 {
  "qid": "q9871469796",
  "kind": "yes/no",
  "text": "Hi Kwame Kelly,\nBrisk update from the branch office on CASE-63489.\nCheers, Morgan Mendoza\n\nFacts for Kwame Kelly (2027):\n- gross monthly income: $3,676.28\n- net monthly income: $3,043.13\n- countable assets: $17,874.40\n- time in the service area: 10 months\n- age: 47 years\n- enrolled in: Corrivale Meal Coupon",
  "question": "For Tesslow Prairie Water Bill Assistance, does Kwame Kelly qualify by passing every gate that applies?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for greater than or equal to 10 months.\n- Gate B: passed when net monthly income is at or less than $3,043.12.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q55f30cd88a",
  "kind": "choice",
  "text": "Facts for Ingrid Abebe (2025):\n| fact | value |\n| --- | --- |\n| time employed | seven months |\n| hours worked in the past year | 1523 hours |\n| employees at the worksite | 268 employees |\n| gross annual pay | $87,486.52 |\n| take-home annual pay | $78,218.94 |\n| enrolled in | Lindcombe Caring Allowance |\n\nunit: busy support hub\nticket: HR-63994\nhandling: Teo Quintero\nregards: Ingrid Abebe",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $87,486.53.\n- Gate B: passed when hours worked in the past year are strictly higher than 1310 hours.\n- Gate C: passed when the applicant has been employed for strictly higher than nine months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Ingrid Abebe to Orrendale Printworks Sick Leave Supplement get?",
  "options": [
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q5bfa13ac7b",
  "kind": "choice",
  "text": "People who asked to claim Omar (2027):\n| person | relationship to Omar | months lived with Omar | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Emeka Schultz | grandfather | ten months | 22,544.58 USD | yes |\n| Ailsa Abara | mother | six months | 31,325.00 USD | no |\n| Jakub Iyer | uncle | zero months | 28,859.00 USD | yes |\n\nWork ticket CR-29240\nLogged by: Nika Hernandez\nAbout: Omar",
  "question": "Mollenby Canal Child Supplement rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for six months or more in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Mollenby Canal Child Supplement, which person, if any, gets to claim Omar under these rules?",
  "options": [
   "Emeka Schultz",
   "Jakub Iyer",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q78641b44df",
  "kind": "choice",
  "text": "{\"case\": \"CR-52888\", \"caseworker\": \"Dani Ishikawa\", \"about\": \"Finn\", \"unit\": \"staff support\"}\n\nInterview notes for Finn (2027):\nCaseworker: Quentin Watson, your relation to Finn?\nQuentin Watson: I am Finn's father.\nCaseworker: Months Finn lived with you?\nQuentin Watson: 6 months.\nCaseworker: Annual income?\nQuentin Watson: $59,031.34.\nCaseworker: Filed a claim for Finn?\nQuentin Watson: yes.\nCaseworker: Farid Wojcik, your relation to Finn?\nFarid Wojcik: I am Finn's uncle.\nCaseworker: Months Finn lived with you?\nFarid Wojcik: 8 months.\nCaseworker: Annual income?\nFarid Wojcik: $52,412.01.\nCaseworker: Filed a claim for Finn?\nFarid Wojcik: no.\nCaseworker: Xenia Campbell, your relation to Finn?\nXenia Campbell: I am Finn's mother.\nCaseworker: Months Finn lived with you?\nXenia Campbell: 2 months.\nCaseworker: Annual income?\nXenia Campbell: $89,583.00.\nCaseworker: Filed a claim for Finn?\nXenia Campbell: no.",
  "question": "Gristmere Child Credit rules for 2027: who may claim Finn.\n- Only one person may claim Finn. Work through these steps in order.\n- Step one: only people who filed a claim for Finn are considered.\n- Step two: of those, only people with whom Finn lived for a minimum of 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Finn lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Finn.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Finn for Gristmere Child Credit?",
  "options": [
   "Quentin Watson",
   "Nobody may claim the child",
   "Farid Wojcik"
  ]
 },
 {
  "qid": "qbced672cca",
  "kind": "choice",
  "text": "[outreach] file=CR-49826 handled_by=Kiran Morales\n[about] subject=Otto\n\nInterview notes for Otto (2026):\nCaseworker: Anjali Hakimi, your relation to Otto?\nAnjali Hakimi: I am Otto's mother.\nCaseworker: Months Otto lived with you?\nAnjali Hakimi: 4 months.\nCaseworker: Annual income?\nAnjali Hakimi: 92,659.00 USD.\nCaseworker: Filed a claim for Otto?\nAnjali Hakimi: yes.\nCaseworker: Ilse Tanaka, your relation to Otto?\nIlse Tanaka: I am Otto's aunt.\nCaseworker: Months Otto lived with you?\nIlse Tanaka: 11 months.\nCaseworker: Annual income?\nIlse Tanaka: 74,110.01 USD.\nCaseworker: Filed a claim for Otto?\nIlse Tanaka: no.\nCaseworker: Ibrahim Kaur, your relation to Otto?\nIbrahim Kaur: I am Otto's father.\nCaseworker: Months Otto lived with you?\nIbrahim Kaur: 8 months.\nCaseworker: Annual income?\nIbrahim Kaur: 36,545.00 USD.\nCaseworker: Filed a claim for Otto?\nIbrahim Kaur: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Otto.\n- Only one person may claim Otto. Work through these steps in order.\n- Step one: only people who filed a claim for Otto are considered.\n- Step two: of those, only people with whom Otto lived for greater than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Otto lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Otto.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Otto for Stonevale Delta Child Allowance?",
  "options": [
   "Ibrahim Kaur",
   "Ilse Tanaka"
  ]
 },
 {
  "qid": "q8f595f2169",
  "kind": "yes/no",
  "text": "Casey Kaplan: At the regional service office, case CR-46706 concerns Vida.\n\nInterview notes for Vida (2026):\nCaseworker: Idris Medina, your relation to Vida?\nIdris Medina: I am Vida's uncle.\nCaseworker: Months Vida lived with you?\nIdris Medina: 11 months.\nCaseworker: Annual income?\nIdris Medina: 58,066.08 USD.\nCaseworker: Filed a claim for Vida?\nIdris Medina: yes.\nCaseworker: Kenji Abara, your relation to Vida?\nKenji Abara: I am Vida's father.\nCaseworker: Months Vida lived with you?\nKenji Abara: 6 months.\nCaseworker: Annual income?\nKenji Abara: 94,577.00 USD.\nCaseworker: Filed a claim for Vida?\nKenji Abara: yes.",
  "question": "Under these rules, does the right to claim Vida for Sallowmere Family Payment go to a different person from Kenji Abara, or stay unclaimed?",
  "definitions": "Sallowmere Family Payment rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for at or greater than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Vida lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb13c05a536",
  "kind": "choice",
  "text": "{\"case\": \"CASE-82267\", \"caseworker\": \"Adi Chandra\", \"about\": \"Greta Ferreira\", \"kind\": \"case file\"}\n\nFacts for Greta Ferreira (2027), as JSON:\n{\"gross_monthly_income\": \"$1,005.42\", \"net_monthly_income\": \"$825.60\", \"countable_assets\": \"$2,491.50\", \"time_in_the_service_area\": \"eleven months\", \"age\": \"64 years\", \"enrolled_in\": \"Mosswyke Rail Saver\"}",
  "question": "Corvane Transit Fare Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is equal to or greater than 63 years.\n- Gate B: passed when countable assets are $2,526.03 or lower.\n- Gate C: passed when the applicant has lived in the service area for equal to or above eleven months.\n- Route: an applicant enrolled in Mosswyke Rail Saver skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Greta Ferreira to Corvane Transit Fare Discount receive?",
  "options": [
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate A is the reason (age)"
  ]
 },
 {
  "qid": "qaabeb9f12d",
  "kind": "choice",
  "text": "Facts for Hiro Murphy (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,008.45 |\n| net monthly income | $3,570.30 |\n| countable assets | $7,689.66 |\n| time in the service area | 21 months |\n| age | 66 years |\n| enrolled in | Tessaly Housing Aid |\n\nCommunity help desk intake form\nCase reference: CASE-14082\nCaseworker: Ezra Rosales\nAbout: Hiro Murphy",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 67 years or more.\n- Gate B: passed when gross monthly income is $4,008.45 or less.\n- Gate C: passed when countable assets are strictly beneath $6,731.30.\n- Route: an applicant enrolled in Tessaly Housing Aid skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Hiro Murphy to Wyndholm Forest Fuel Support ends with which outcome under these rules?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q954f6474cf",
  "kind": "choice",
  "text": "Ticket: staff support desk, case HR-51002\nFrom: Ezra Rosales\nAbout: Kiara Wojcik\n\nFacts for Kiara Wojcik (2025):\n| fact | value |\n| --- | --- |\n| time employed | 9 months |\n| hours worked in the past year | 446 hours |\n| employees at the worksite | 40 employees |\n| gross annual pay | $39,551.86 |\n| take-home annual pay | $28,112.12 |\n| enrolled in | Pratchell Caregiver Allowance |",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly below $39,551.87.\n- Gate B: passed when the applicant has been employed for strictly above 9 months.\n- Gate C: passed when take-home annual pay is $28,112.11 at the most.\n- Gate D: passed when the worksite has strictly over 22 employees.\n- Route: an applicant enrolled in Pratchell Caregiver Allowance skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Kiara Wojcik on the application to Wendmoor Mill Parental Leave?",
  "options": [
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible",
   "Not eligible: Gate D is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qf212195a4f",
  "kind": "yes/no",
  "text": "ref: HR-51670\nhandler: Alex Lindgren\nsubject: Lucia Jovanovic\n\nFacts for Lucia Jovanovic (2026):\n- time employed: thirteen months\n- hours worked in the past year: 1,495 hours\n- employees at the worksite: 69 employees\n- gross annual pay: $37,282.42\n- take-home annual pay: $30,585.29\n- enrolled in: Caddowen Veterans Pilot",
  "question": "Going by the listed rules, is Lucia Jovanovic eligible for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or greater than 69 employees.\n- Gate B: passed when hours worked in the past year are at or beyond 1,010 hours.\n- Gate C: passed when the applicant has been employed for strictly in excess of nine months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q671b3668b1",
  "kind": "yes/no",
  "text": "Facts for Kazu Nilsen (2026), as JSON:\n{\"gross_monthly_income\": \"$3,520.86\", \"net_monthly_income\": \"$2,721.27\", \"countable_assets\": \"$3,543.01\", \"time_in_the_service_area\": \"sixteen months\", \"age\": \"48 years\", \"enrolled_in\": \"Kelder Veterans Pension\"}\n\n{\"case\": \"CASE-02174\", \"caseworker\": \"Avery Obradovic\", \"about\": \"Kazu Nilsen\", \"desk\": \"internal\"}",
  "question": "Following the listed rules, does Kazu Nilsen qualify for Tollsey Island Ferry Discount?",
  "definitions": "Tollsey Island Ferry Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for twelve months or above.\n- Gate B: passed when gross monthly income is $3,520.87 or under.\n- Gate C: passed when countable assets are at or under the amount of $2,541.92.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8868494cc2",
  "kind": "choice",
  "text": "People who asked to claim Otto (2027), as JSON:\n{\"people\": [{\"name\": \"Sabine Eriksen\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"0 months\", \"annual_income\": \"$84,474.44\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Oskar Dlamini\", \"relationship\": \"father\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"$67,333.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nadia Ortega\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"10 months\", \"annual_income\": \"$67,333.00\", \"filed_a_claim\": \"no\"}]}\n\n{\"case\": \"CR-40879\", \"caseworker\": \"Toni Lazar\", \"about\": \"Otto\", \"desk\": \"internal\"}",
  "question": "Brellow Orchard Family Credit rules for 2027: who may claim Otto.\n- Only one person may claim Otto. Work through these steps in order.\n- Step one: only people who filed a claim for Otto are considered.\n- Step two: of those, only people with whom Otto lived for 7 months at minimum in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Otto lived for more months comes first.\n- If nobody is left after step two, nobody may claim Otto.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Brellow Orchard Family Credit, which person, if any, gets to claim Otto under these rules?",
  "options": [
   "Nobody may claim the child",
   "Sabine Eriksen",
   "Nadia Ortega"
  ]
 },
 {
  "qid": "q8faba2e284",
  "kind": "yes/no",
  "text": "Tomi Eklund: thanks, admin desk has HR-61138 set up for Jelena Anderson.\n\nFacts for Jelena Anderson (2027):\n- time employed: 10 months\n- hours worked in the past year: 518 hours\n- employees at the worksite: 235 employees\n- gross annual pay: $43,300.01\n- take-home annual pay: $32,975.30\n- enrolled in: Pratchell Caregiver Stipend",
  "question": "According to these rules, is Jelena Anderson not eligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly under the amount of $32,975.31.\n- Gate B: passed when gross annual pay is at or under the amount of $43,300.02.\n- Gate C: passed when hours worked in the past year are 1240 hours or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4ace80b4f1",
  "kind": "yes/no",
  "text": "Walk-in ticket: HR-88031\nRaised by: Morgan Mendoza\nAbout: Dmitri Dragic\n\nIntake interview with Dmitri Dragic (2026):\nCaseworker: Time employed?\nDmitri Dragic: 23 months.\nCaseworker: Hours worked in the past year?\nDmitri Dragic: 786 hours.\nCaseworker: Employees at your worksite?\nDmitri Dragic: 43 employees.\nCaseworker: Gross annual pay?\nDmitri Dragic: $16,563.52.\nCaseworker: Take-home annual pay?\nDmitri Dragic: $11,338.67.\nCaseworker: Other programme enrolled in?\nDmitri Dragic: Osterlin Tool Allowance.",
  "question": "Following the listed rules, does Dmitri Dragic qualify for Brenwold Timber Apprentice Support?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for at or above 24 months.\n- Gate B: passed when the worksite has equal to or greater than 44 employees.\n- Gate C: passed when gross annual pay is strictly beneath $35,696.15.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q439c22b267",
  "kind": "choice",
  "text": "Alex Lindgren: thanks for waiting, Isla is on CR-55611.\n\nPeople who asked to claim Isla (2026):\n- Gustav Anderson: relationship to Isla: grandfather; months lived with Isla: 7 months; annual income: $54,464.00; filed a claim: yes\n- Ugo Iyer: relationship to Isla: uncle; months lived with Isla: 4 months; annual income: $80,083.00; filed a claim: yes\n- Freya Lindqvist: relationship to Isla: aunt; months lived with Isla: 8 months; annual income: $29,629.00; filed a claim: yes",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for above 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Isla lived for more months comes first.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Isla for Ferrowby Forest Credit?",
  "options": [
   "Freya Lindqvist",
   "Ugo Iyer",
   "Gustav Anderson"
  ]
 },
 {
  "qid": "q2cbe45bd41",
  "kind": "yes/no",
  "text": "ref: HR-67605\ncaseworker: Adi Chandra\nperson: Juliana Castellano\n\nFacts for Juliana Castellano (2025):\n- time employed: 9 months\n- hours worked in the past year: 709 hours\n- employees at the worksite: 71 employees\n- gross annual pay: $63,990.12\n- take-home annual pay: $40,076.34\n- enrolled in: Wyvelle Pension Boost",
  "question": "Does Juliana Castellano fail to qualify for Marrowby Bakery Family Leave on these rules?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is equal to or below $63,990.12.\n- Gate B: passed when hours worked in the past year are at or greater than 710 hours.\n- Gate C: passed when the worksite has equal to or above 71 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q84eddd3f6a",
  "kind": "choice",
  "text": "[intake_route] case_ref=HR-68026\n[desk_note] handler=Kazu Yousef about=Leila Hamilton\n\nFacts for Leila Hamilton (2026):\n| fact | value |\n| --- | --- |\n| time employed | 108 months |\n| hours worked in the past year | 732 hours |\n| employees at the worksite | 395 employees |\n| gross annual pay | 103,323.84 USD |\n| take-home annual pay | 65,461.62 USD |\n| enrolled in | Drummock Nurse Bursary |",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or below the level of 65,461.62 USD.\n- Gate B: passed when hours worked in the past year are greater than or equal to 790 hours.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Leila Hamilton to Morrowdene Hospital Group Return Support get?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qfd794cc027",
  "kind": "choice",
  "text": "Quick note: Quinn Pavlenko is running HR-23404 for Rania Hoffman. Outreach is moving fast.\n\nFacts for Rania Hoffman (2027):\n- time employed: 8 months\n- hours worked in the past year: 976 hours\n- employees at the worksite: 123 employees\n- gross annual pay: $82,389.79\n- take-home annual pay: $65,184.42\n- enrolled in: Halvorne Sabbatical Fund",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $82,389.78.\n- Gate B: passed when hours worked in the past year are 1360 hours or greater.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Morrowdene Hospital Group Return Support, which outcome does the application submitted by Rania Hoffman get?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "qdfc201ed7b",
  "kind": "choice",
  "text": "Alex Lindgren: CR-42521 is up on the desk, about Pia.\n\nPeople who asked to claim Pia (2027):\n- Gabriel Dragic: relationship to Pia: grandfather; months lived with Pia: 6 months; annual income: $55,191; filed a claim: yes\n- Idris Wojcik: relationship to Pia: uncle; months lived with Pia: 11 months; annual income: 58,786.23 USD; filed a claim: yes\n- Cyril Yilmaz: relationship to Pia: father; months lived with Pia: 11 months; annual income: 63,823.58 USD; filed a claim: no\n- Esra Dubois: relationship to Pia: aunt; months lived with Pia: 3 months; annual income: 63,823.58 USD; filed a claim: yes",
  "question": "Ferrowby Forest Credit rules for 2027: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for greater than 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Pia lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Pia for Ferrowby Forest Credit?",
  "options": [
   "Idris Wojcik",
   "Gabriel Dragic",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qa9b72c199a",
  "kind": "choice",
  "text": "Facts for Ren Tanaka (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,364.63 |\n| net monthly income | $3,042.38 |\n| countable assets | $10,618.77 |\n| time in the service area | twelve months |\n| age | 73 years |\n| enrolled in | Kelder Veterans Pledge |\n\nWork ticket CASE-85388\nLogged by: Ren Dvorak\nAbout: Ren Tanaka",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than eleven months.\n- Gate B: passed when countable assets are equal to or below $10,618.77.\n- Gate C: passed when net monthly income is at or less than $2,493.25.\n- Gate D: passed when gross monthly income is at or under the amount of $3,364.62.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat does Ren Tanaka get from the application to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate C is the reason (net monthly income)",
   "Not eligible: Gate D is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (countable assets)"
  ]
 },
 {
  "qid": "q71751c33bb",
  "kind": "choice",
  "text": "Morgan Mendoza: thanks, admin desk has CASE-21938 set up for Rafael Thompson.\n\nFacts for Rafael Thompson (2027):\n- gross monthly income: $2,855.76\n- net monthly income: $1,965.45\n- countable assets: $5,507.87\n- time in the service area: eleven months\n- age: nineteen years\n- enrolled in: Crannock Food Parcel",
  "question": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly below the level of $2,412.34.\n- Gate B: passed when gross monthly income is $2,855.77 at the most.\n- Route: an applicant enrolled in Crannock Food Pantry skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does Rafael Thompson get on the application to Ostmere Lakeside Winter Energy Support under these rules?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qd98a227a34",
  "kind": "yes/no",
  "text": "Community ticket: HR-80982\nHandled by: Lior Grigoryan\nAbout: Priya Castellano\n\nIntake interview with Priya Castellano (2027):\nCaseworker: Time employed?\nPriya Castellano: 82 months.\nCaseworker: Hours worked in the past year?\nPriya Castellano: 1,129 hours.\nCaseworker: Employees at your worksite?\nPriya Castellano: 26 employees.\nCaseworker: Gross annual pay?\nPriya Castellano: $42,799.26.\nCaseworker: Take-home annual pay?\nPriya Castellano: $35,857.38.\nCaseworker: Other programme enrolled in?\nPriya Castellano: Ellerwick Trainee Scheme.",
  "question": "Is Priya Castellano formally ineligible for Sorrelby Child Care Support under these rules?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly over 1,130 hours.\n- Gate B: passed when the worksite has strictly in excess of 31 employees.\n- Gate C: passed when take-home annual pay is strictly below the amount of $41,513.08.\n- Route: an applicant enrolled in Ellerwick Trainee Scheme skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q455344fa90",
  "kind": "choice",
  "text": "Case note: CASE-61000 sits with Ari Benali and concerns Sami Eriksen.\n\nIntake interview with Sami Eriksen (2026):\nCaseworker: Gross monthly income?\nSami Eriksen: 1,986.53 USD.\nCaseworker: Net monthly income?\nSami Eriksen: 1,657.27 USD.\nCaseworker: Countable assets?\nSami Eriksen: 12,593.81 USD.\nCaseworker: Time in the service area?\nSami Eriksen: 11 months.\nCaseworker: Age?\nSami Eriksen: 73 years.\nCaseworker: Other programme enrolled in?\nSami Eriksen: Yarrowdean Bus Pass.",
  "question": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is 1,657.28 USD or less.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 7 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Sami Eriksen to Fennick School Meal Supplement gets which outcome?",
  "options": [
   "Not eligible: Gate A is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 }
]
