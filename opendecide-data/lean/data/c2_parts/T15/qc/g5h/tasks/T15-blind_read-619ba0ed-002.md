# G5-H blind read T15-blind_read-619ba0ed-002 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-619ba0ed-002.json

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
  "qid": "q17001c89a3",
  "kind": "yes/no",
  "text": "[casework_team] case_id=HR-68980\n[casework_team] worker=Kiran Morales about=Freya Hakimi\n\nIntake interview with Freya Hakimi (2025):\nCaseworker: Time employed?\nFreya Hakimi: 28 months.\nCaseworker: Hours worked in the past year?\nFreya Hakimi: 1701 hours.\nCaseworker: Employees at your worksite?\nFreya Hakimi: 24 employees.\nCaseworker: Gross annual pay?\nFreya Hakimi: 36,560.11 USD.\nCaseworker: Take-home annual pay?\nFreya Hakimi: 27,740.62 USD.\nCaseworker: Other programme enrolled in?\nFreya Hakimi: Osterlin Tool Allowance.",
  "question": "Does Freya Hakimi fully qualify for Brenwold Timber Apprentice Support under these rules?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly in excess of nineteen months.\n- Gate B: passed when hours worked in the past year are strictly above 1300 hours.\n- Gate C: passed when the worksite has strictly over 36 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qce887193f2",
  "kind": "choice",
  "text": "People who asked to claim Ivan (2025):\n| person | relationship to Ivan | months lived with Ivan | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kwame Schultz | uncle | 4 months | $81,642 | yes |\n| Ivo Ilunga | father | 9 months | $51,712 | yes |\n| Sabine Mitchell | mother | 6 months | $88,731.40 | yes |\n\nReview ticket: CR-19554\nOwner: Cameron Vargas\nAbout: Ivan",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for over 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Ivan for Brellow Orchard Family Credit?",
  "options": [
   "Ivo Ilunga",
   "Kwame Schultz"
  ]
 },
 {
  "qid": "qbe64a79ae7",
  "kind": "yes/no",
  "text": "{\"case\": \"CR-50379\", \"caseworker\": \"Jamie Jorgensen\", \"about\": \"Mia\", \"line\": \"help\"}\n\nPeople who asked to claim Mia (2026), as JSON:\n{\"people\": [{\"name\": \"Yusuf Kaur\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"92,197.15 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Pavel Evans\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"72,845.15 USD\", \"filed_a_claim\": \"no\"}]}",
  "question": "Is it true that Pavel Evans may not claim Mia for Tessenvale Valley Child Credit?",
  "definitions": "Tessenvale Valley Child Credit rules for 2026: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for at or over 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7f06ea35d3",
  "kind": "choice",
  "text": "file: CASE-66821\nsupport: Kiran Morales\nabout: Yusuf Yilmaz\nmood: kind\n\nFacts for Yusuf Yilmaz (2025):\n- gross monthly income: $3,250.98\n- net monthly income: $2,730.60\n- countable assets: $4,325.37\n- time in the service area: 28 months\n- age: 88 years\n- enrolled in: Pellbrook Heating Fund",
  "question": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly under $2,834.61.\n- Gate B: passed when the applicant's age is above 88 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Yusuf Yilmaz to Tarrowick Food Basket Support ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Eligible",
   "Not eligible: Gate A is the reason (net monthly income)"
  ]
 },
 {
  "qid": "q32cd25305b",
  "kind": "yes/no",
  "text": "Facts for Dani Yilmaz (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,356.62 |\n| net monthly income | $2,736.76 |\n| countable assets | $7,779.56 |\n| time in the service area | 1 month |\n| age | 60 years |\n| enrolled in | Ketteridge Veterans Scheme |\n\ncase: CASE-06802\ncaseworker: Jules Shrestha\nabout: Dani Yilmaz\ndesk: back office",
  "question": "Under these rules, is Dani Yilmaz eligible for Sallowick Ward Home Repair Grant overall?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under $2,839.28.\n- Gate B: passed when the applicant has lived in the service area for larger than 5 months.\n- Gate C: passed when the applicant's age is 60 years at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb44d72f057",
  "kind": "choice",
  "text": "{\"ref\": \"CR-39613\", \"caseworker\": \"Teo Quintero\", \"about\": \"Finn\"}\n\nPeople who asked to claim Finn (2025), as JSON:\n{\"people\": [{\"name\": \"Nadia Ortega\", \"relationship\": \"mother\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"$48,078.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Emeka Okafor\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"seven months\", \"annual_income\": \"$22,692.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Wanjiru Watson\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"nine months\", \"annual_income\": \"$62,769.36\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Caddowen Harbour Family Allowance rules for 2025: who may claim Finn.\n- Only one person may claim Finn. Work through these steps in order.\n- Step one: only people who filed a claim for Finn are considered.\n- Step two: of those, only people with whom Finn lived for above seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Finn lived for more months comes first.\n- If nobody is left after step two, nobody may claim Finn.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Finn for Caddowen Harbour Family Allowance under these rules?",
  "options": [
   "Nobody may claim the child",
   "Nadia Ortega",
   "Wanjiru Watson"
  ]
 },
 {
  "qid": "q6166b0fdb0",
  "kind": "choice",
  "text": "[case_file] ref=HR-49483 worker=Sami Castro\n[about] subject=Juliana Dragic\n\nFacts for Juliana Dragic (2025):\n| fact | value |\n| --- | --- |\n| time employed | eighteen months |\n| hours worked in the past year | 2,230 hours |\n| employees at the worksite | 73 employees |\n| gross annual pay | 84,035.77 USD |\n| take-home annual pay | 54,153.74 USD |\n| enrolled in | Lumenfold Skills Credit |",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or over 63 employees.\n- Gate B: passed when gross annual pay is strictly smaller than 54,741.28 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Juliana Dragic to Halvorne Shipyard Tuition Assistance land?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qd50aeb7736",
  "kind": "yes/no",
  "text": "ref: HR-51670\nhandler: Alex Lindgren\nsubject: Lucia Jovanovic\n\nFacts for Lucia Jovanovic (2026):\n- time employed: thirteen months\n- hours worked in the past year: 1,495 hours\n- employees at the worksite: 69 employees\n- gross annual pay: $37,282.42\n- take-home annual pay: $30,585.29\n- enrolled in: Caddowen Veterans Pilot",
  "question": "Going by the listed rules, is Lucia Jovanovic eligible for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or greater than 69 employees.\n- Gate B: passed when hours worked in the past year are at or beyond 1,010 hours.\n- Gate C: passed when the applicant has been employed for strictly in excess of nine months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3deb878951",
  "kind": "yes/no",
  "text": "People who asked to claim Kai (2026):\n| person | relationship to Kai | months lived with Kai | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gustav Ilunga | grandfather | 8 months | $44,824 | no |\n| Pavel Abebe | uncle | 10 months | $43,789 | no |\n\n[district_office] record_key=CR-25656 owner=Teo Quintero subject=Kai",
  "question": "Under these rules, does Pavel Abebe fail to gain the right to claim Kai for Sorrenby Island Family Payment?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for equal to or above 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q90bebfddb2",
  "kind": "yes/no",
  "text": "Facts for Sergio Ilic (2026), as JSON:\n{\"gross_monthly_income\": \"1,682.67 USD\", \"net_monthly_income\": \"1,498.11 USD\", \"countable_assets\": \"6,279.17 USD\", \"time_in_the_service_area\": \"8 months\", \"age\": \"83 years\", \"enrolled_in\": \"Ketteridge Veterans Charter\"}\n\n{\"ref\": \"CASE-18927\", \"caseworker\": \"Morgan Mendoza\", \"about\": \"Sergio Ilic\"}",
  "question": "Under these rules, is Sergio Ilic eligible for Sallowick Ward Home Repair Grant overall?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or beneath 6,279.18 USD.\n- Gate B: passed when net monthly income is 1,498.11 USD or less.\n- Gate C: passed when the applicant has lived in the service area for at or over 8 months.\n- Route: an applicant enrolled in Brunsley Energy Rebate skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q63aad997b2",
  "kind": "yes/no",
  "text": "Case note: the intake desk has Hugo Yilmaz on case CASE-98717, with Alex Lindgren in charge.\n\nFacts for Hugo Yilmaz (2026):\n- gross monthly income: $5,052.93\n- net monthly income: $4,426.91\n- countable assets: $7,159.37\n- time in the service area: 10 months\n- age: 73 years\n- enrolled in: Stennet Commuter Pass",
  "question": "For Corvane Transit Fare Discount, does Hugo Yilmaz qualify under the listed rules?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or under $7,159.36.\n- Gate B: passed when the applicant has lived in the service area for above 11 months.\n- Gate C: passed when the applicant's age is strictly over 66 years.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4ba56753d7",
  "kind": "choice",
  "text": "Case note: a warm hello from the services counter. Riley Watanabe has CASE-22911 for Yara Tesfaye.\n\nFacts for Yara Tesfaye (2025):\n- gross monthly income: 5,975.53 USD\n- net monthly income: 4,137.67 USD\n- countable assets: 9,299.02 USD\n- time in the service area: 40 months\n- age: 30 years\n- enrolled in: Caddowen Pantry Shopping Card",
  "question": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 65 years at minimum.\n- Gate B: passed when net monthly income is strictly below the level of 3,018.46 USD.\n- Route: an applicant enrolled in Caddowen Pantry Shopping Card skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Yara Tesfaye to Tarrowick Food Basket Support?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (age)"
  ]
 },
 {
  "qid": "qa41e70d782",
  "kind": "yes/no",
  "text": "[case_record] ref=CR-01207 worker=Mika Zamora about=Mia\n\nPeople who asked to claim Mia (2025):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anjali Eriksen | mother | 5 months | 90,875.00 USD | no |\n| Felix Nilsen | father | 3 months | 64,636.39 USD | yes |\n| Idris Ilic | uncle | 12 months | 61,134.77 USD | yes |",
  "question": "For Tessenvale Valley Child Credit, is Anjali Eriksen barred from claiming Mia under the listed rules?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for greater than or equal to 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Mia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2d4083f64a",
  "kind": "yes/no",
  "text": "Support hub form\nCase reference: CASE-06971\nCaseworker: Shay Bekele\nSubject: Jakub Gashi\n\nFacts for Jakub Gashi (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,043.54 |\n| net monthly income | $2,484.40 |\n| countable assets | $4,207.65 |\n| time in the service area | 43 months |\n| age | 68 years |\n| enrolled in | Caddowen Pantry Shopping Card |",
  "question": "Does Jakub Gashi fail to qualify for admission to Tarrowick Food Basket Support?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is at or over 63 years.\n- Gate B: passed when gross monthly income is strictly below the level of $3,000.35.\n- Route: an applicant enrolled in Pellbrook Heating Grant skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q1614daeff1",
  "kind": "yes/no",
  "text": "Facts for Kazu Robinson (2025), as JSON:\n{\"time_employed\": \"thirteen months\", \"hours_worked_in_the_past_year\": \"1933 hours\", \"employees_at_the_worksite\": \"36 employees\", \"gross_annual_pay\": \"$32,323.14\", \"take-home_annual_pay\": \"$23,815.30\", \"enrolled_in\": \"Ostermere Respite Care\"}\n\n{\"case\": \"HR-35362\", \"caseworker\": \"Yuki Adeyemi\", \"about\": \"Kazu Robinson\", \"tone\": \"warm\"}",
  "question": "For Pelmoor Ceramics Carer Support, is Kazu Robinson ineligible under the stated rules?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or above thirteen months.\n- Gate B: passed when gross annual pay is strictly under the amount of $33,148.84.\n- Gate C: passed when the worksite has above 41 employees.\n- Route: an applicant enrolled in Ostermere Respite Care skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7daf6de11f",
  "kind": "choice",
  "text": "Hi Ailsa Kimura,\nBrief update on case HR-89802 below.\nThanks, Emi Figueroa\n\nIntake interview with Ailsa Kimura (2026):\nCaseworker: Time employed?\nAilsa Kimura: 10 months.\nCaseworker: Hours worked in the past year?\nAilsa Kimura: 1,128 hours.\nCaseworker: Employees at your worksite?\nAilsa Kimura: 23 employees.\nCaseworker: Gross annual pay?\nAilsa Kimura: 96,619.70 USD.\nCaseworker: Take-home annual pay?\nAilsa Kimura: 64,669.83 USD.\nCaseworker: Other programme enrolled in?\nAilsa Kimura: Wendle Trade Pilot.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for larger than 10 months.\n- Gate B: passed when take-home annual pay is 65,151.41 USD or lower.\n- Gate C: passed when the worksite has in excess of 37 employees.\n- Route: an applicant enrolled in Pendrick Training Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Ailsa Kimura to Brenwold Timber Apprentice Support produce?",
  "options": [
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "q0f2ea505f9",
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
  "qid": "q9f6f94ef7b",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-70270\", \"caseworker\": \"Cameron Vargas\", \"about\": \"Greta Johnson\", \"desk\": \"call centre\"}\n\nFacts for Greta Johnson (2025), as JSON:\n{\"gross_monthly_income\": \"3,547.29 USD\", \"net_monthly_income\": \"2,209.44 USD\", \"countable_assets\": \"1,774.96 USD\", \"time_in_the_service_area\": \"6 months\", \"age\": \"73 years\", \"enrolled_in\": \"Brackenholm Housing Loan\"}",
  "question": "Under these rules, is Greta Johnson ineligible for Tarrowick Food Basket Support as a whole?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or greater than 6 months.\n- Gate B: passed when net monthly income is strictly below the level of 1,576.51 USD.\n- Gate C: passed when countable assets are at or beneath 3,006.34 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5d63aa9008",
  "kind": "choice",
  "text": "record: CASE-46139\ncaseworker: Adi Chandra\nabout: Greta Ruiz\ntone: warm\n\nFacts for Greta Ruiz (2025):\n- gross monthly income: $2,451.88\n- net monthly income: $1,816.13\n- countable assets: $8,352.30\n- time in the service area: eight months\n- age: 88 years\n- enrolled in: none",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is a minimum of 66 years.\n- Gate B: passed when countable assets are strictly beneath the level of $8,352.30.\n- Gate C: passed when the applicant has lived in the service area for at or beyond eleven months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Greta Ruiz to Corrivale Valley Childcare Grant receive?",
  "options": [
   "Not eligible: Gate B is the reason (countable assets)",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate A is the reason (age)"
  ]
 },
 {
  "qid": "qc705c02bf0",
  "kind": "yes/no",
  "text": "reference: HR-00932\nhandler: Mika Zamora\nsubject: Greta Vasquez\n\nFacts for Greta Vasquez (2025):\n- time employed: 13 months\n- hours worked in the past year: 1170 hours\n- employees at the worksite: 73 employees\n- gross annual pay: 60,901.48 USD\n- take-home annual pay: 44,353.58 USD\n- enrolled in: Corrivale Welding Bursary",
  "question": "Following the listed rules, does Greta Vasquez qualify for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or above 41 employees.\n- Gate B: passed when hours worked in the past year are strictly higher than 1170 hours.\n- Gate C: passed when the applicant has been employed for at or over 8 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q043930f9ef",
  "kind": "choice",
  "text": "Case note: the intake desk has Priya Douglas on case CASE-34434, with Morgan Mendoza in charge.\n\nIntake interview with Priya Douglas (2026):\nCaseworker: Gross monthly income?\nPriya Douglas: $3,526.76.\nCaseworker: Net monthly income?\nPriya Douglas: $2,287.79.\nCaseworker: Countable assets?\nPriya Douglas: $6,303.27.\nCaseworker: Time in the service area?\nPriya Douglas: 15 months.\nCaseworker: Age?\nPriya Douglas: 57 years.\nCaseworker: Other programme enrolled in?\nPriya Douglas: Tallowmere Roof Grant.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or beneath $9,278.75.\n- Gate B: passed when the applicant's age is above 57 years.\n- Gate C: passed when the applicant has lived in the service area for at or greater than 8 months.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Priya Douglas to Ostermere Delta Flood Repair Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (age)"
  ]
 },
 {
  "qid": "q73b8df8bab",
  "kind": "choice",
  "text": "Routine ticket: CR-06713\nRaised by: Jules Shrestha\nAbout: Eva\n\nPeople who asked to claim Eva (2025):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Mariam Halvorsen | grandmother | ten months | $25,349.00 | yes |\n| Nadia Nilsen | mother | three months | $54,957.00 | yes |\n| Anjali Ilunga | grandmother | ten months | $58,017.00 | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for over six months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tessenvale Valley Child Credit, which person, if any, gets the right to claim Eva?",
  "options": [
   "Anjali Ilunga",
   "Mariam Halvorsen"
  ]
 },
 {
  "qid": "q2365aa02f9",
  "kind": "yes/no",
  "text": "People who asked to claim Lina (2027):\n| person | relationship to Lina | months lived with Lina | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Yara Rahimi | mother | 7 months | 49,656.45 USD | yes |\n| Ivo Gallegos | father | 7 months | 81,433.00 USD | yes |\n| Elias Murphy | uncle | 4 months | 92,839.00 USD | no |\n\nMika Zamora: Noted, CR-60206 for Lina sits with the intake desk.",
  "question": "According to these rules, does the right to claim Lina for Mollenby Canal Child Supplement go to a different person from Elias Murphy, or stay unclaimed?",
  "definitions": "Mollenby Canal Child Supplement rules for 2027: who may claim Lina.\n- Only one person may claim Lina. Work through these steps in order.\n- Step one: only people who filed a claim for Lina are considered.\n- Step two: of those, only people with whom Lina lived for higher than 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Lina lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Lina.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe6631c5e83",
  "kind": "choice",
  "text": "Case note: Avery Obradovic picks up file CASE-34407, about Esra Castellano, at the counter.\n\nIntake interview with Esra Castellano (2026):\nCaseworker: Gross monthly income?\nEsra Castellano: $5,125.52.\nCaseworker: Net monthly income?\nEsra Castellano: $3,195.43.\nCaseworker: Countable assets?\nEsra Castellano: $9,713.64.\nCaseworker: Time in the service area?\nEsra Castellano: three months.\nCaseworker: Age?\nEsra Castellano: 66 years.\nCaseworker: Other programme enrolled in?\nEsra Castellano: Quenmoor Emergency Fund.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly over eight months.\n- Gate B: passed when gross monthly income is strictly smaller than $3,237.95.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Esra Castellano to Ostermere Delta Flood Repair Support receive?",
  "options": [
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q298b391dcb",
  "kind": "yes/no",
  "text": "[welcome_file] thanks to Sami Castro for case CASE-90632\n[about_person] Ravi Murphy is the warm focus here.\n\nIntake interview with Ravi Murphy (2025):\nCaseworker: Gross monthly income?\nRavi Murphy: $3,638.76.\nCaseworker: Net monthly income?\nRavi Murphy: $2,459.25.\nCaseworker: Countable assets?\nRavi Murphy: $11,048.56.\nCaseworker: Time in the service area?\nRavi Murphy: five months.\nCaseworker: Age?\nRavi Murphy: 85 years.\nCaseworker: Other programme enrolled in?\nRavi Murphy: Lowmarsh Heating Loan.",
  "question": "Going by the listed rules, does a gate that applies end the application of Ravi Murphy to Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $9,217.39 or lower.\n- Gate B: passed when the applicant has lived in the service area for a minimum of three months.\n- Gate C: passed when the applicant's age is above 57 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q806c19b281",
  "kind": "yes/no",
  "text": "Hello Zara,\nQuick update: the staff support desk has CR-69078 in view.\nRegards, Avery Obradovic\n\nPeople who asked to claim Zara (2027):\n- Zainab Ruiz: relationship to Zara: mother; months lived with Zara: 7 months; annual income: $62,274.00; filed a claim: yes\n- Tamar Lehmann: relationship to Zara: aunt; months lived with Zara: 8 months; annual income: $62,274.00; filed a claim: yes\n- Dmitri Johnson: relationship to Zara: uncle; months lived with Zara: 8 months; annual income: $55,550.00; filed a claim: yes",
  "question": "Going by the listed rules, does Zainab Ruiz fail to win the right to claim Zara for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2027: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for equal to or greater than 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Zara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q13bc45ecae",
  "kind": "yes/no",
  "text": "Adi Chandra: thanks, admin desk has CASE-91059 set up for Viktor Gutierrez.\n\nFacts for Viktor Gutierrez (2025):\n- gross monthly income: $2,155.87\n- net monthly income: $1,767.12\n- countable assets: $11,846.80\n- time in the service area: 9 months\n- age: 18 years\n- enrolled in: Mosswyke Rail Saver",
  "question": "According to these rules, does a gate that applies end the application of Viktor Gutierrez to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for 12 months or above.\n- Gate B: passed when gross monthly income is strictly below $2,511.67.\n- Gate C: passed when countable assets are strictly under the amount of $11,846.80.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qba5b8d5bf1",
  "kind": "yes/no",
  "text": "Facts for Hiroko Choi (2026):\n| fact | value |\n| --- | --- |\n| time employed | thirteen months |\n| hours worked in the past year | 701 hours |\n| employees at the worksite | 152 employees |\n| gross annual pay | $48,022.10 |\n| take-home annual pay | $43,211.13 |\n| enrolled in | Vellan Travel Support |\n\nHi Hiroko Choi,\nYour case HR-10693 is being reviewed with care.\nKind thanks, Toni Lazar",
  "question": "For Orrendale Printworks Sick Leave Supplement, is Hiroko Choi ineligible under the stated rules?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly below $55,036.64.\n- Gate B: passed when hours worked in the past year are larger than 700 hours.\n- Gate C: passed when the applicant has been employed for in excess of seven months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd7b4aefe93",
  "kind": "choice",
  "text": "People who asked to claim Ami (2026):\n| person | relationship to Ami | months lived with Ami | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Bianca Iyer | aunt | zero months | $73,917 | yes |\n| Cyril Moreau | grandfather | nine months | $23,520.99 | no |\n| Kwame Sharma | uncle | three months | $18,924 | yes |\n\nHello there,\nThanks for calling about Ami; the reference is CR-10133.\nKind regards, Alex Lindgren",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for greater than or equal to seven months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ami lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Ami for Farrowby Moorland Parish Credit?",
  "options": [
   "Nobody may claim the child",
   "Bianca Iyer",
   "Cyril Moreau"
  ]
 },
 {
  "qid": "q597dd33ece",
  "kind": "yes/no",
  "text": "Intake form\nCase reference: CASE-61211\nCaseworker: Toni Lazar\nAbout: Quentin Yilmaz\n\nFacts for Quentin Yilmaz (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,425.54 USD |\n| net monthly income | 2,305.66 USD |\n| countable assets | 5,251.80 USD |\n| time in the service area | 18 months |\n| age | 86 years |\n| enrolled in | Crannock Food Pantry |",
  "question": "Is Quentin Yilmaz not eligible for Ostmere Lakeside Winter Energy Support as the rules stand?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 11 months.\n- Gate B: passed when net monthly income is strictly under the amount of 2,489.64 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4a3e922976",
  "kind": "choice",
  "text": "Facts for Kwame Ramirez (2025):\n| fact | value |\n| --- | --- |\n| time employed | 92 months |\n| hours worked in the past year | 1,987 hours |\n| employees at the worksite | 82 employees |\n| gross annual pay | 36,070.93 USD |\n| take-home annual pay | 26,737.36 USD |\n| enrolled in | Brumstead Wellbeing Grant |\n\n[people_services] case=HR-50295 about=Kwame Ramirez\n[people_services] handled_by=Emi Figueroa",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is smaller than 37,975.47 USD.\n- Gate B: passed when the worksite has at or beyond 47 employees.\n- Route: an applicant enrolled in Ostermere Respite Care skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Kwame Ramirez to Pelmoor Ceramics Carer Support lead to?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q9d4233cef1",
  "kind": "choice",
  "text": "Case note: CASE-61000 sits with Ari Benali and concerns Sami Eriksen.\n\nIntake interview with Sami Eriksen (2026):\nCaseworker: Gross monthly income?\nSami Eriksen: 1,986.53 USD.\nCaseworker: Net monthly income?\nSami Eriksen: 1,657.27 USD.\nCaseworker: Countable assets?\nSami Eriksen: 12,593.81 USD.\nCaseworker: Time in the service area?\nSami Eriksen: 11 months.\nCaseworker: Age?\nSami Eriksen: 73 years.\nCaseworker: Other programme enrolled in?\nSami Eriksen: Yarrowdean Bus Pass.",
  "question": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is 1,657.28 USD or less.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 7 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Sami Eriksen to Fennick School Meal Supplement gets which outcome?",
  "options": [
   "Not eligible: Gate A is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qf55e788736",
  "kind": "choice",
  "text": "Quick note: Quinn Pavlenko is running HR-23404 for Rania Hoffman. Outreach is moving fast.\n\nFacts for Rania Hoffman (2027):\n- time employed: 8 months\n- hours worked in the past year: 976 hours\n- employees at the worksite: 123 employees\n- gross annual pay: $82,389.79\n- take-home annual pay: $65,184.42\n- enrolled in: Drummock Nurse Bursary",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $82,389.78.\n- Gate B: passed when hours worked in the past year are 1360 hours or greater.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Morrowdene Hospital Group Return Support, which outcome does the application submitted by Rania Hoffman get?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "q41478dd585",
  "kind": "choice",
  "text": "People who asked to claim Milo (2027):\n| person | relationship to Milo | months lived with Milo | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Priya Kelly | grandmother | 12 months | 33,428.00 USD | yes |\n| Yasmin Castellano | grandmother | 8 months | 61,486.00 USD | yes |\n\nHelp line ticket CR-25638\nFor: Milo\nRaised by: Quinn Pavlenko",
  "question": "Sorrenby Island Family Payment rules for 2027: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for over 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Milo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Milo for Sorrenby Island Family Payment?",
  "options": [
   "Yasmin Castellano",
   "Priya Kelly"
  ]
 },
 {
  "qid": "qe4a7373888",
  "kind": "choice",
  "text": "Walk-in ticket: HR-93796\nRaised by: Ari Benali\nAbout: Hamid Begum\n\nFacts for Hamid Begum (2027):\n| fact | value |\n| --- | --- |\n| time employed | 42 months |\n| hours worked in the past year | 1181 hours |\n| employees at the worksite | 40 employees |\n| gross annual pay | 32,141.31 USD |\n| take-home annual pay | 28,382.90 USD |\n| enrolled in | Rickmere Night Course Fund |",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly more than 66 employees.\n- Gate B: passed when hours worked in the past year are strictly more than 1180 hours.\n- Gate C: passed when take-home annual pay is strictly below the level of 28,382.89 USD.\n- Route: an applicant enrolled in Rickmere Night Course Fund skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which result comes from the application of Hamid Begum to Hallowdene Logistics Study Grant?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qa32b6c9a52",
  "kind": "yes/no",
  "text": "Facts for Mateo Abara (2025):\n| fact | value |\n| --- | --- |\n| time employed | five months |\n| hours worked in the past year | 428 hours |\n| employees at the worksite | 34 employees |\n| gross annual pay | $45,305.47 |\n| take-home annual pay | $38,799.38 |\n| enrolled in | Lindcombe Caring Assistance |\n\nTicket line: HR-17962\nRaised by: Emi Figueroa\nAbout: Mateo Abara",
  "question": "Going by the listed rules, is Mateo Abara eligible for Orrendale Printworks Sick Leave Supplement?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has greater than 33 employees.\n- Gate B: passed when the applicant has been employed for larger than fifteen months.\n- Gate C: passed when take-home annual pay is $40,436.45 or less.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8be40e9559",
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
  "qid": "q61491589af",
  "kind": "yes/no",
  "text": "Welcome to the community help desk\nCase reference: CASE-49260\nCaseworker: Morgan Mendoza\nPerson: Anton Becker\n\nFacts for Anton Becker (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,104.16 USD |\n| net monthly income | 1,341.33 USD |\n| countable assets | 707.59 USD |\n| time in the service area | 47 months |\n| age | 69 years |\n| enrolled in | Sallowby Water Rebate |",
  "question": "Is Anton Becker eligible for Ostmere Lakeside Winter Energy Support with every applicable gate passed?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly under 1,969.51 USD.\n- Gate B: passed when the applicant's age is at or over 57 years.\n- Gate C: passed when net monthly income is at or less than 1,401.88 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q13608959e2",
  "kind": "yes/no",
  "text": "case_ref: CR-12559\nworker: Adi Chandra\nsubject: Kai\n\nPeople who asked to claim Kai (2025):\n- Nkechi Demir: relationship to Kai: mother; months lived with Kai: 6 months; annual income: $27,398; filed a claim: yes\n- Olena Rahimi: relationship to Kai: aunt; months lived with Kai: 5 months; annual income: $51,863; filed a claim: yes\n- Galina Esposito: relationship to Kai: grandmother; months lived with Kai: 10 months; annual income: $90,292; filed a claim: no",
  "question": "Following the listed rules, is Olena Rahimi barred from claiming Kai for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for 6 months or greater in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q803befd528",
  "kind": "choice",
  "text": "Services counter intake form\nCase reference: HR-74247\nCaseworker: Yuki Adeyemi\nAbout: Kwame Evans\n\nFacts for Kwame Evans (2027):\n| fact | value |\n| --- | --- |\n| time employed | eighteen months |\n| hours worked in the past year | 510 hours |\n| employees at the worksite | 24 employees |\n| gross annual pay | $81,394.38 |\n| take-home annual pay | $64,245.10 |\n| enrolled in | Hemmerly Dockside Fellowship |",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 25 employees at minimum.\n- Gate B: passed when the applicant has been employed for strictly more than nine months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Kwame Evans to Halvorne Shipyard Tuition Assistance get under these rules?",
  "options": [
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "qf56f436931",
  "kind": "yes/no",
  "text": "Facts for Cyril Robinson (2027), as JSON:\n{\"time_employed\": \"34 months\", \"hours_worked_in_the_past_year\": \"2,087 hours\", \"employees_at_the_worksite\": \"20 employees\", \"gross_annual_pay\": \"80,254.29 USD\", \"take-home_annual_pay\": \"60,136.97 USD\", \"enrolled_in\": \"Tesslow Engineering Traineeship\"}\n\n{\"reference\": \"HR-02966\", \"caseworker\": \"Sami Castro\", \"about\": \"Cyril Robinson\", \"office\": \"district\"}",
  "question": "According to these rules, is Cyril Robinson not eligible for Drummock Robotics Workshop Training Fund?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 20 employees or more.\n- Gate B: passed when gross annual pay is equal to or below 80,254.29 USD.\n- Gate C: passed when the applicant has been employed for 35 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7f7c23ec19",
  "kind": "choice",
  "text": "reference: HR-75056\ncaseworker: Kendall Umarov\nabout: Hiro Halvorsen\ntone: warm\n\nFacts for Hiro Halvorsen (2026):\n- time employed: 81 months\n- hours worked in the past year: 657 hours\n- employees at the worksite: 62 employees\n- gross annual pay: $55,906.77\n- take-home annual pay: $36,646.62\n- enrolled in: Selwick Fresh Crate",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 51 employees or greater.\n- Gate B: passed when hours worked in the past year are strictly greater than 740 hours.\n- Gate C: passed when gross annual pay is strictly beneath the level of $66,614.72.\n- Route: an applicant enrolled in Selwick Fresh Box skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hiro Halvorsen to Marrowby Bakery Family Leave get?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "q6de51b257a",
  "kind": "choice",
  "text": "People who asked to claim Ana (2026):\n| person | relationship to Ana | months lived with Ana | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Elias Mwangi | father | ten months | $21,955.00 | yes |\n| Hugo Sullivan | grandfather | twelve months | $82,245.00 | yes |\n| Ilse Kelly | grandmother | eight months | $51,786.02 | yes |\n| Nadia Petrov | mother | ten months | $30,633.00 | yes |\n\ndesk: community help\ncase: CR-25612\ncaseworker: Lior Grigoryan\nabout: Ana",
  "question": "Brellow Orchard Family Credit rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for at or above six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Ana for Brellow Orchard Family Credit?",
  "options": [
   "Elias Mwangi",
   "Hugo Sullivan"
  ]
 },
 {
  "qid": "q0a344b7548",
  "kind": "choice",
  "text": "Case note: routine check on CR-37735, held by Toni Lazar for Ada.\n\nPeople who asked to claim Ada (2026):\n- Greta Ivanova: relationship to Ada: mother; months lived with Ada: 6 months; annual income: 80,066.00 USD; filed a claim: no\n- Kenji Begum: relationship to Ada: father; months lived with Ada: 1 month; annual income: 53,081.00 USD; filed a claim: yes\n- Rania Choi: relationship to Ada: grandmother; months lived with Ada: 9 months; annual income: 76,918.00 USD; filed a claim: no\n- Bruno Fujimoto: relationship to Ada: uncle; months lived with Ada: 7 months; annual income: 80,066.00 USD; filed a claim: yes",
  "question": "Kelvery Market Credit rules for 2026: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for larger than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, is the sole person who may claim Ada for Kelvery Market Credit?",
  "options": [
   "Rania Choi",
   "Bruno Fujimoto",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q16afc48ee2",
  "kind": "choice",
  "text": "Case note: CASE-61000 sits with Ari Benali and concerns Sami Eriksen.\n\nIntake interview with Sami Eriksen (2026):\nCaseworker: Gross monthly income?\nSami Eriksen: 1,986.53 USD.\nCaseworker: Net monthly income?\nSami Eriksen: 1,657.27 USD.\nCaseworker: Countable assets?\nSami Eriksen: 12,593.81 USD.\nCaseworker: Time in the service area?\nSami Eriksen: 11 months.\nCaseworker: Age?\nSami Eriksen: 73 years.\nCaseworker: Other programme enrolled in?\nSami Eriksen: Yarrowdean Bus Pass.",
  "question": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is 1,657.28 USD or less.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 12 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Sami Eriksen to Fennick School Meal Supplement gets which outcome?",
  "options": [
   "Not eligible: Gate A is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 },
 {
  "qid": "q4d4a23a859",
  "kind": "choice",
  "text": "desk: intake\ncase: CR-18819\ncaseworker: Kazu Yousef\nabout: Vida\n\nPeople who asked to claim Vida (2026):\n- Kavita Ivanova: relationship to Vida: aunt; months lived with Vida: three months; annual income: 36,250.00 USD; filed a claim: yes\n- Kiara Esposito: relationship to Vida: aunt; months lived with Vida: six months; annual income: 42,909.00 USD; filed a claim: yes\n- Tariq Sullivan: relationship to Vida: grandfather; months lived with Vida: five months; annual income: 87,270.00 USD; filed a claim: no",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for a minimum of six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Vida lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Vida for Ferrowby Forest Credit?",
  "options": [
   "Nobody may claim the child",
   "Kavita Ivanova",
   "Kiara Esposito"
  ]
 },
 {
  "qid": "q335d126293",
  "kind": "choice",
  "text": "People who asked to claim Dara (2026):\n| person | relationship to Dara | months lived with Dara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Tariq Gashi | uncle | 5 months | $65,591.01 | yes |\n| Nkechi Demir | mother | 7 months | $68,613.00 | yes |\n| Mirela Reynolds | grandmother | 8 months | $90,731.00 | yes |\n| Elias Campbell | father | 3 months | $91,755.00 | no |\n\nBranch intake sheet\nReference: CR-92479\nHandled by: Nika Hernandez\nAbout: Dara",
  "question": "Brellow Orchard Family Credit rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for greater than or equal to 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Dara for Brellow Orchard Family Credit?",
  "options": [
   "Elias Campbell",
   "Mirela Reynolds"
  ]
 },
 {
  "qid": "q56249cd517",
  "kind": "yes/no",
  "text": "{\"ref\": \"CASE-86947\", \"lead\": \"Casey Kaplan\", \"person\": \"Tomi Halvorsen\"}\n\nIntake interview with Tomi Halvorsen (2025):\nCaseworker: Gross monthly income?\nTomi Halvorsen: $2,888.29.\nCaseworker: Net monthly income?\nTomi Halvorsen: $2,133.63.\nCaseworker: Countable assets?\nTomi Halvorsen: $11,376.02.\nCaseworker: Time in the service area?\nTomi Halvorsen: 6 months.\nCaseworker: Age?\nTomi Halvorsen: 67 years.\nCaseworker: Other programme enrolled in?\nTomi Halvorsen: none.",
  "question": "Under these rules, does a gate that applies end the application of Tomi Halvorsen to Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 66 years.\n- Gate B: passed when countable assets are smaller than $11,376.03.\n- Gate C: passed when the applicant has lived in the service area for 3 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q041fdf77cb",
  "kind": "yes/no",
  "text": "ref: HR-67605\ncaseworker: Adi Chandra\nperson: Juliana Castellano\n\nFacts for Juliana Castellano (2025):\n- time employed: 9 months\n- hours worked in the past year: 709 hours\n- employees at the worksite: 71 employees\n- gross annual pay: $63,990.12\n- take-home annual pay: $40,076.34\n- enrolled in: Wyvelle Pension Boost",
  "question": "Does Juliana Castellano fail to qualify for Marrowby Bakery Family Leave on these rules?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is equal to or below $63,990.12.\n- Gate B: passed when hours worked in the past year are at or greater than 710 hours.\n- Gate C: passed when the worksite has equal to or above 71 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qcde46dae73",
  "kind": "yes/no",
  "text": "unit: busy support hub\nticket: CASE-06889\nhandling: Riley Watanabe\nregards: Oskar Iyer\n\nFacts for Oskar Iyer (2025):\n- gross monthly income: $3,237.31\n- net monthly income: $1,222.77\n- countable assets: $5,024.21\n- time in the service area: 7 months\n- age: 32 years\n- enrolled in: Stonevale Housing Loan",
  "question": "Going by the listed rules, does a gate that applies end the application of Oskar Iyer to Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly above 6 months.\n- Gate B: passed when gross monthly income is strictly beneath $3,237.31.\n- Route: an applicant enrolled in Stonevale Housing Loan skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 }
]
