# G5-H blind read T15-blind_read-de925712-004 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-de925712-004.json

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
  "qid": "qc0ed01b85c",
  "kind": "yes/no",
  "text": "Facts for Vesna Kelly (2027):\n| fact | value |\n| --- | --- |\n| time employed | six months |\n| hours worked in the past year | 537 hours |\n| employees at the worksite | 31 employees |\n| gross annual pay | $28,600.30 |\n| take-home annual pay | $23,050.51 |\n| enrolled in | Ostermere Skills Bursary |\n\nIntake form: call centre\nCase reference: HR-02097\nCaseworker: Dani Ishikawa\nAbout: Vesna Kelly",
  "question": "Under these rules, is Vesna Kelly eligible for Drummock Robotics Workshop Training Fund given every gate that applies is passed?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly higher than fourteen months.\n- Gate B: passed when hours worked in the past year are strictly over 860 hours.\n- Gate C: passed when take-home annual pay is lower than $40,000.00.\n- Route: an applicant enrolled in Ostermere Skills Bursary skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfbf6963452",
  "kind": "yes/no",
  "text": "People who asked to claim Eva (2027):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Waleed Robinson | grandfather | 5 months | $20,077.02 | yes |\n| Greta Delgado | aunt | 10 months | $49,198 | yes |\n| Freya Nakamura | grandmother | 0 months | $44,183 | yes |\n| Hamid Rahimi | father | 9 months | $49,198 | yes |\n\n[desk_sweep] ref=CR-92244 by=Morgan Mendoza subject=Eva",
  "question": "Does Waleed Robinson end up as the sole person who may claim Eva for Farrowby Moorland Parish Credit?",
  "definitions": "Farrowby Moorland Parish Credit rules for 2027: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for in excess of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q1e258b90f4",
  "kind": "choice",
  "text": "entry: HR-77885\nheld_by: Cameron Vargas\nregarding: Mariam Lindqvist\ndesk: community help\n\nFacts for Mariam Lindqvist (2026):\n- time employed: 48 months\n- hours worked in the past year: 2090 hours\n- employees at the worksite: 172 employees\n- gross annual pay: 48,255.24 USD\n- take-home annual pay: $41,000\n- enrolled in: Quillmere Apprentice Pathway",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly below $41,000.\n- Gate B: passed when gross annual pay is at or under $51,500.\n- Route: an applicant enrolled in Quillmere Apprentice Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nConcerning Halvorne Shipyard Tuition Assistance, which outcome does the application by Mariam Lindqvist receive?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q345880b3e9",
  "kind": "choice",
  "text": "Service intake form\nCase reference: CASE-95388\nCaseworker: Remy Tran\nAbout: Luka Mwangi\n\nFacts for Luka Mwangi (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $1,317.69 |\n| net monthly income | $1,082.80 |\n| countable assets | $11,345.69 |\n| time in the service area | 3 months |\n| age | 41 years |\n| enrolled in | none |",
  "question": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is a minimum of 41 years.\n- Gate B: passed when the applicant has lived in the service area for at or beyond 4 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Luka Mwangi to Sennamoor River Rent Support receive?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "q987d878c61",
  "kind": "yes/no",
  "text": "Facts for Tomi Watson (2025):\n| fact | value |\n| --- | --- |\n| time employed | 71 months |\n| hours worked in the past year | 497 hours |\n| employees at the worksite | 45 employees |\n| gross annual pay | $42,306.49 |\n| take-home annual pay | $30,000.01 |\n| enrolled in | Lindcombe Caring Assistance |\n\ncase: HR-52219\ncaseworker: Blair Xiong\nabout: Tomi Watson\nkind: file",
  "question": "For Orrendale Printworks Sick Leave Supplement, does Tomi Watson fail to qualify under these rules?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or greater than 46 employees.\n- Gate B: passed when take-home annual pay is at or under $30,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7a1050bdd0",
  "kind": "yes/no",
  "text": "Case note: the intake desk has Bruno Stewart on case CASE-22541, with Toni Lazar in charge.\n\nFacts for Bruno Stewart (2025):\n- gross monthly income: 4,220.20 USD\n- net monthly income: 3,508.68 USD\n- countable assets: 1,897.17 USD\n- time in the service area: 2 months\n- age: 78 years\n- enrolled in: Caddowen Pantry Shopping Card",
  "question": "Does Bruno Stewart fail to qualify for Tarrowick Food Basket Support under these rules?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for at or over 4 months.\n- Gate B: passed when net monthly income is strictly under the value of 2,460.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6d8f562634",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CASE-04342\nRaised by: Teo Quintero\nAbout: Ari Ortega\n\nIntake interview with Ari Ortega (2027):\nCaseworker: Gross monthly income?\nAri Ortega: $1,356.63.\nCaseworker: Net monthly income?\nAri Ortega: $1,130.71.\nCaseworker: Countable assets?\nAri Ortega: $3,877.98.\nCaseworker: Time in the service area?\nAri Ortega: 13 months.\nCaseworker: Age?\nAri Ortega: 58 years.\nCaseworker: Other programme enrolled in?\nAri Ortega: Aldervale Meal Ticket.",
  "question": "For Tamsfell Senior Home Support, does Ari Ortega qualify by passing every gate that applies?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is in excess of 57 years.\n- Gate B: passed when net monthly income is smaller than $1,810.\n- Gate C: passed when the applicant has lived in the service area for 8 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd3c4c7f00b",
  "kind": "yes/no",
  "text": "reference: CR-59037\ncaseworker: Alex Lindgren\nabout: Luca\ntone: warm\n\nInterview notes for Luca (2025):\nCaseworker: Kavita Ilic, your relation to Luca?\nKavita Ilic: I am Luca's mother.\nCaseworker: Months Luca lived with you?\nKavita Ilic: 0 months.\nCaseworker: Annual income?\nKavita Ilic: 38,014.35 USD.\nCaseworker: Filed a claim for Luca?\nKavita Ilic: yes.\nCaseworker: Jelena Johnson, your relation to Luca?\nJelena Johnson: I am Luca's aunt.\nCaseworker: Months Luca lived with you?\nJelena Johnson: 5 months.\nCaseworker: Annual income?\nJelena Johnson: 74,937.00 USD.\nCaseworker: Filed a claim for Luca?\nJelena Johnson: no.\nCaseworker: Sergio Yamazaki, your relation to Luca?\nSergio Yamazaki: I am Luca's grandfather.\nCaseworker: Months Luca lived with you?\nSergio Yamazaki: 7 months.\nCaseworker: Annual income?\nSergio Yamazaki: 89,940.00 USD.\nCaseworker: Filed a claim for Luca?\nSergio Yamazaki: yes.",
  "question": "According to these rules, does Jelena Johnson fail to earn a claim on Luca for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2025: who may claim Luca.\n- Only one person may claim Luca. Work through these steps in order.\n- Step one: only people who filed a claim for Luca are considered.\n- Step two: of those, only people with whom Luca lived for greater than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Luca lived for more months comes first.\n- If nobody is left after step two, nobody may claim Luca.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe058762573",
  "kind": "yes/no",
  "text": "Facts for Kofi Fujimoto (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,115.47 USD |\n| net monthly income | 3,570.41 USD |\n| countable assets | 10,517.22 USD |\n| time in the service area | five months |\n| age | 48 years |\n| enrolled in | Brunsley Energy Rebate |\n\nteam: casework\ncase: CASE-23228\ncaseworker: Ezra Rosales\nabout: Kofi Fujimoto",
  "question": "Going by the listed rules, is Kofi Fujimoto ineligible for Sallowick Ward Home Repair Grant?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is smaller than 2,850.00 USD.\n- Gate B: passed when the applicant has lived in the service area for equal to or greater than six months.\n- Gate C: passed when countable assets are 7,500.00 USD or lower.\n- Route: an applicant enrolled in Brunsley Energy Rebate skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6ccef9f14a",
  "kind": "yes/no",
  "text": "Facts for Tomas Murphy (2027):\n| fact | value |\n| --- | --- |\n| time employed | 7 months |\n| hours worked in the past year | 1799 hours |\n| employees at the worksite | 137 employees |\n| gross annual pay | $45,000 |\n| take-home annual pay | $32,542.49 |\n| enrolled in | Ostermere Respite Care |\n\n[hub_entry] ref=HR-78417 handler=Jamie Jorgensen subject=Tomas Murphy",
  "question": "Under these rules, does Tomas Murphy fail to qualify for Pelmoor Ceramics Carer Support?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of $45,000.\n- Gate B: passed when hours worked in the past year are over 1320 hours.\n- Route: an applicant enrolled in Tundale Care Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qff77fb467b",
  "kind": "yes/no",
  "text": "Work ticket HR-92224\nLogged by: Ezra Rosales\nAbout: Hugo Gallegos\n\nIntake interview with Hugo Gallegos (2025):\nCaseworker: Time employed?\nHugo Gallegos: 59 months.\nCaseworker: Hours worked in the past year?\nHugo Gallegos: 1,160 hours.\nCaseworker: Employees at your worksite?\nHugo Gallegos: 321 employees.\nCaseworker: Gross annual pay?\nHugo Gallegos: $56,832.31.\nCaseworker: Take-home annual pay?\nHugo Gallegos: $37,979.08.\nCaseworker: Other programme enrolled in?\nHugo Gallegos: Quendrel Skills Voucher.",
  "question": "Does Hugo Gallegos fail to qualify for Brenwold Timber Apprentice Support under these rules?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $43,500.00.\n- Gate B: passed when hours worked in the past year are equal to or greater than 1,160 hours.\n- Gate C: passed when take-home annual pay is strictly under the amount of $33,000.00.\n- Route: an applicant enrolled in Quendrel Skills Voucher skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q516340295b",
  "kind": "yes/no",
  "text": "Quinn Pavlenko: quick check on file CR-71438 for Dara, at the counter.\n\nPeople who asked to claim Dara (2026):\n- Zainab Dlamini: relationship to Dara: aunt; months lived with Dara: 5 months; annual income: $92,534.00; filed a claim: yes\n- Viktor Campbell: relationship to Dara: father; months lived with Dara: 0 months; annual income: $82,556.00; filed a claim: yes\n- Freya Gutierrez: relationship to Dara: mother; months lived with Dara: 5 months; annual income: $35,668.00; filed a claim: yes",
  "question": "Going by the listed rules, is Zainab Dlamini the person who wins the right to claim Dara for Ferrowby Forest Credit?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q991dda3b57",
  "kind": "yes/no",
  "text": "{\"case\": \"HR-52696\", \"worker\": \"Quinn Pavlenko\", \"about\": \"Juliana Esposito\", \"office\": \"town hall\"}\n\nFacts for Juliana Esposito (2026), as JSON:\n{\"time_employed\": \"99 months\", \"hours_worked_in_the_past_year\": \"693 hours\", \"employees_at_the_worksite\": \"212 employees\", \"gross_annual_pay\": \"$42,624.21\", \"take-home_annual_pay\": \"$33,186.83\", \"enrolled_in\": \"Dorrane Parental Leave\"}",
  "question": "Is Juliana Esposito not eligible for Tovardine Seed Caregiver Leave as the rules stand?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are in excess of 850 hours.\n- Gate B: passed when gross annual pay is strictly below the amount of $76,000.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6efdf0894d",
  "kind": "yes/no",
  "text": "Staff support form\nReference: CR-68405\nName: Vida\nHeld by: Kazu Yousef\n\nPeople who asked to claim Vida (2025):\n| person | relationship to Vida | months lived with Vida | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Juliana Ilunga | grandmother | 9 months | $85,938.00 | yes |\n| Dmitri Hudson | father | 5 months | $40,681.00 | yes |\n| Zofia Anderson | mother | 11 months | $40,262.28 | no |",
  "question": "Is Juliana Ilunga barred from claiming Vida for Dunmarrow Hill Allowance by the rules?",
  "definitions": "Dunmarrow Hill Allowance rules for 2025: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for equal to or above 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Vida lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc2c9cf4f73",
  "kind": "choice",
  "text": "People who asked to claim Mia (2027):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Priya Medina | mother | 6 months | $83,438 | no |\n| Jakub Ilunga | uncle | 10 months | $71,971.40 | yes |\n| Dario Gashi | father | 7 months | $70,686 | yes |\n\nSami Castro: cheers, the staff support desk has CR-09806 for Mia.",
  "question": "Sorrenby Island Family Payment rules for 2027: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for 7 months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Mia for Sorrenby Island Family Payment?",
  "options": [
   "Jakub Ilunga",
   "Priya Medina"
  ]
 },
 {
  "qid": "qf75fd975cf",
  "kind": "choice",
  "text": "Front sheet\nReference: CR-62259\nHandled by: Kendall Umarov\nFor: Isla\n\nInterview notes for Isla (2026):\nCaseworker: Tariq Castellano, your relation to Isla?\nTariq Castellano: I am Isla's father.\nCaseworker: Months Isla lived with you?\nTariq Castellano: 7 months.\nCaseworker: Annual income?\nTariq Castellano: $50,661.\nCaseworker: Filed a claim for Isla?\nTariq Castellano: yes.\nCaseworker: Olena Kelly, your relation to Isla?\nOlena Kelly: I am Isla's aunt.\nCaseworker: Months Isla lived with you?\nOlena Kelly: 8 months.\nCaseworker: Annual income?\nOlena Kelly: $50,661.\nCaseworker: Filed a claim for Isla?\nOlena Kelly: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for at or beyond 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Isla lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Isla for Stonevale Delta Child Allowance?",
  "options": [
   "Tariq Castellano",
   "Olena Kelly"
  ]
 },
 {
  "qid": "qd5eeb2dc42",
  "kind": "yes/no",
  "text": "Ticket: branch office, case HR-62296\nRaised by: Remy Tran\nAbout: Matias Ilunga\n\nIntake interview with Matias Ilunga (2025):\nCaseworker: Time employed?\nMatias Ilunga: 76 months.\nCaseworker: Hours worked in the past year?\nMatias Ilunga: 1349 hours.\nCaseworker: Employees at your worksite?\nMatias Ilunga: 43 employees.\nCaseworker: Gross annual pay?\nMatias Ilunga: 69,953.96 USD.\nCaseworker: Take-home annual pay?\nMatias Ilunga: 53,999.99 USD.\nCaseworker: Other programme enrolled in?\nMatias Ilunga: Ivormoor Shift Supplement.",
  "question": "Is Matias Ilunga eligible for Sorrelby Child Care Support with every applicable gate passed?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly greater than 42 employees.\n- Gate B: passed when take-home annual pay is strictly smaller than 54,000.00 USD.\n- Gate C: passed when hours worked in the past year are strictly higher than 790 hours.\n- Route: an applicant enrolled in Ivormoor Shift Supplement skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7ebff8a67c",
  "kind": "yes/no",
  "text": "[casework_team] case_id=CASE-35327\n[casework_team] worker=Quinn Pavlenko about=Sabine Hamilton\n\nFacts for Sabine Hamilton (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,121.81 USD |\n| net monthly income | 2,699.99 USD |\n| countable assets | 11,476.44 USD |\n| time in the service area | 5 months |\n| age | 22 years |\n| enrolled in | Stennet Commuter Pass |",
  "question": "Under these rules, does Sabine Hamilton meet the rules for Corvane Transit Fare Discount across every applicable gate?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly smaller than 2,700.00 USD.\n- Gate B: passed when the applicant has lived in the service area for at or above 4 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfff5aa5337",
  "kind": "choice",
  "text": "reference: CASE-37445\nhandled_by: Alex Lindgren\nabout: Nika Lindqvist\nunit: casework\n\nFacts for Nika Lindqvist (2027):\n- gross monthly income: $2,950.01\n- net monthly income: $2,811.33\n- countable assets: $8,872.16\n- time in the service area: 40 months\n- age: 60 years\n- enrolled in: Tallow Ridge Commuter Pass",
  "question": "Sennamoor River Rent Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the amount of $9,100.00.\n- Gate B: passed when gross monthly income is at or below the level of $2,950.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Sennamoor River Rent Support, which outcome does the application of Nika Lindqvist get?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "q803dc02331",
  "kind": "yes/no",
  "text": "Help line ticket CR-87107\nFor: Ada\nRaised by: Sami Castro\n\nPeople who asked to claim Ada (2025):\n| person | relationship to Ada | months lived with Ada | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anton Abebe | grandfather | 11 months | $40,684.45 | yes |\n| Dario Gordon | father | 8 months | $47,546.00 | yes |\n| Juliana Bergstrom | grandmother | 11 months | $58,203.95 | yes |",
  "question": "Going by the listed rules, is Anton Abebe the person who wins the right to claim Ada for Tessenvale Valley Child Credit?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for at or beyond 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ada lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9c4928ecf7",
  "kind": "yes/no",
  "text": "Sami Castro: HR-83857 is up on the desk, about Tomi Gallegos.\n\nFacts for Tomi Gallegos (2026):\n- time employed: 20 months\n- hours worked in the past year: 1,390 hours\n- employees at the worksite: 170 employees\n- gross annual pay: 54,641.12 USD\n- take-home annual pay: 39,320.71 USD\n- enrolled in: Drummock Nurse Bursary",
  "question": "Is Tomi Gallegos formally ineligible for Morrowdene Hospital Group Return Support under these rules?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly beneath 66,000.00 USD.\n- Gate B: passed when hours worked in the past year are 1,390 hours or greater.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc5bd4004f9",
  "kind": "choice",
  "text": "Review desk note: Jules Shrestha handles HR-90898, about Hamid Mensah.\n\nFacts for Hamid Mensah (2026):\n- time employed: five months\n- hours worked in the past year: 1,365 hours\n- employees at the worksite: 49 employees\n- gross annual pay: $80,537.32\n- take-home annual pay: $57,500.01\n- enrolled in: Gerrondale Tenant Aid",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for at or beyond six months.\n- Gate B: passed when gross annual pay is smaller than $71,500.\n- Gate C: passed when take-home annual pay is at or below the level of $57,500.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Hamid Mensah to Marrowby Bakery Family Leave receive?",
  "options": [
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "qbdc8a1fcd3",
  "kind": "choice",
  "text": "Dear Mariam Demir,\nThis reply concerns case HR-87545.\nYours sincerely, Kendall Umarov\n\nIntake interview with Mariam Demir (2027):\nCaseworker: Time employed?\nMariam Demir: 72 months.\nCaseworker: Hours worked in the past year?\nMariam Demir: 559 hours.\nCaseworker: Employees at your worksite?\nMariam Demir: 228 employees.\nCaseworker: Gross annual pay?\nMariam Demir: $37,393.23.\nCaseworker: Take-home annual pay?\nMariam Demir: $29,642.13.\nCaseworker: Other programme enrolled in?\nMariam Demir: Quendrel Skills Voucher.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is equal to or below $38,500.00.\n- Gate B: passed when hours worked in the past year are strictly above 1,010 hours.\n- Route: an applicant enrolled in Quendrel Skills Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Mariam Demir to Brenwold Timber Apprentice Support resolved?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qd80b77ce9c",
  "kind": "choice",
  "text": "ref: CR-80907\nhandler: Kiran Morales\nsubject: Theo\n\nPeople who asked to claim Theo (2027):\n- Viktor Sullivan: relationship to Theo: father; months lived with Theo: 6 months; annual income: $23,287; filed a claim: yes\n- Priya Yamazaki: relationship to Theo: mother; months lived with Theo: 10 months; annual income: $36,105; filed a claim: no\n- Fatima Okoro: relationship to Theo: grandmother; months lived with Theo: 9 months; annual income: $51,937.04; filed a claim: yes",
  "question": "Caddowen Harbour Family Allowance rules for 2027: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for equal to or greater than 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Theo lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Theo for Caddowen Harbour Family Allowance?",
  "options": [
   "Priya Yamazaki",
   "Viktor Sullivan"
  ]
 },
 {
  "qid": "q289a32ea9b",
  "kind": "yes/no",
  "text": "Kendall Umarov: quick check on file CASE-63813 for Xenia Mwangi, at the counter.\n\nFacts for Xenia Mwangi (2025):\n- gross monthly income: 2,732.51 USD\n- net monthly income: 1,707.63 USD\n- countable assets: 9,800.01 USD\n- time in the service area: 2 months\n- age: 56 years\n- enrolled in: Hallowby Utility Discount",
  "question": "For Tesslow Prairie Water Bill Assistance, does Xenia Mwangi qualify by passing every gate that applies?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are lower than 9,800.00 USD.\n- Gate B: passed when the applicant's age is at or above 57 years.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q171cecfa20",
  "kind": "yes/no",
  "text": "team: casework\ncase: HR-23882\ncaseworker: Kazu Yousef\nabout: Sofia Ueda\n\nFacts for Sofia Ueda (2026):\n- time employed: 14 months\n- hours worked in the past year: 443 hours\n- employees at the worksite: 181 employees\n- gross annual pay: 93,488.66 USD\n- take-home annual pay: 70,778.68 USD\n- enrolled in: Pratchell Caregiver Allowance",
  "question": "According to these rules, does Sofia Ueda qualify for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are above 840 hours.\n- Gate B: passed when the applicant has been employed for equal to or greater than 17 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9c2071e78c",
  "kind": "choice",
  "text": "Ticket: CASE-64684 at the services counter\nRaised by: Kazu Yousef\nAbout: Ubah Patterson\n\nFacts for Ubah Patterson (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,593.32 USD |\n| net monthly income | 3,358.16 USD |\n| countable assets | 1,798.24 USD |\n| time in the service area | 10 months |\n| age | 55 years |\n| enrolled in | Ruddock Shuttle Card |",
  "question": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than 9 months.\n- Gate B: passed when the applicant's age is 56 years or above.\n- Gate C: passed when countable assets are at or below 3,300.00 USD.\n- Route: an applicant enrolled in Ruddock Shuttle Card skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which result comes from the application of Ubah Patterson to Corvane Transit Fare Discount?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (age)"
  ]
 },
 {
  "qid": "qd5f4b1c595",
  "kind": "choice",
  "text": "{\"caseworker\": \"Blair Xiong\", \"about\": \"Mia\", \"case\": \"CR-68729\", \"office\": \"branch\"}\n\nPeople who asked to claim Mia (2026), as JSON:\n{\"people\": [{\"name\": \"Sergio Choi\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"47,040.00 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Greta Choi\", \"relationship\": \"mother\", \"months_lived_with_child\": \"seven months\", \"annual_income\": \"37,086.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Pavel Petrov\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"17,390.00 USD\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for strictly higher than six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Mia for Ferrowby Forest Credit?",
  "options": [
   "Pavel Petrov",
   "Greta Choi"
  ]
 },
 {
  "qid": "qff106087a2",
  "kind": "yes/no",
  "text": "Case note: Jamie Jorgensen is glad to take on the matter of Ana, reference CR-47978.\n\nPeople who asked to claim Ana (2025):\n- Oskar Thompson: relationship to Ana: father; months lived with Ana: five months; annual income: $57,651.00; filed a claim: yes\n- Ravi Russell: relationship to Ana: uncle; months lived with Ana: two months; annual income: $62,645.00; filed a claim: yes\n- Zofia Evans: relationship to Ana: mother; months lived with Ana: two months; annual income: $53,114.00; filed a claim: yes\n- Nadia Halvorsen: relationship to Ana: grandmother; months lived with Ana: seven months; annual income: $64,806.51; filed a claim: yes",
  "question": "Going by the listed rules, is Zofia Evans shut out from claiming Ana for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2025: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for in excess of six months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qadde3fb51e",
  "kind": "yes/no",
  "text": "Facts for Nadia Stewart (2026), as JSON:\n{\"time_employed\": \"eleven months\", \"hours_worked_in_the_past_year\": \"129 hours\", \"employees_at_the_worksite\": \"24 employees\", \"gross_annual_pay\": \"52,431.38 USD\", \"take-home_annual_pay\": \"32,553.10 USD\", \"enrolled_in\": \"Hathermoor Relief Leave\"}\n\n{\"case_ref\": \"HR-05918\", \"handler\": \"Ari Benali\", \"subject\": \"Nadia Stewart\"}",
  "question": "Is Nadia Stewart eligible for Pelmoor Ceramics Carer Support with every applicable gate passed?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has above 23 employees.\n- Gate B: passed when the applicant has been employed for above eight months.\n- Gate C: passed when take-home annual pay is equal to or below 68,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q18974b3f1a",
  "kind": "choice",
  "text": "People who asked to claim Ana (2026):\n| person | relationship to Ana | months lived with Ana | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dario Nakamura | grandfather | 5 months | $20,912.91 | yes |\n| Anton Murphy | grandfather | 10 months | $86,247.83 | no |\n| Ivo Schultz | uncle | 0 months | $64,795.50 | yes |\n\nfile: CR-87694\nsupport: Remy Tran\nabout: Ana\nmood: kind",
  "question": "Mollenby Canal Child Supplement rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for at or beyond 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ana lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Ana for Mollenby Canal Child Supplement?",
  "options": [
   "Dario Nakamura",
   "Nobody may claim the child",
   "Anton Murphy"
  ]
 },
 {
  "qid": "q4294a22ea2",
  "kind": "choice",
  "text": "People who asked to claim Ivan (2027):\n| person | relationship to Ivan | months lived with Ivan | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hiroko Campbell | mother | 6 months | $46,958 | no |\n| Tariq Nakamura | father | 9 months | $17,951.25 | yes |\n| Quentin Ferreira | uncle | 12 months | $36,794 | yes |\n\nRen Dvorak: Pulling up case CR-53470 for Ivan, busy as ever.",
  "question": "Sorrenby Island Family Payment rules for 2027: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for greater than 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Ivan for Sorrenby Island Family Payment?",
  "options": [
   "Quentin Ferreira",
   "Hiroko Campbell",
   "Tariq Nakamura"
  ]
 },
 {
  "qid": "qd42834c73c",
  "kind": "choice",
  "text": "Facts for Bruno Thompson (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,181.01 |\n| net monthly income | $1,630.00 |\n| countable assets | $10,099.99 |\n| time in the service area | 14 months |\n| age | 38 years |\n| enrolled in | Sallafell Bus Credit |\n\n[case_record] ref=CASE-70220 worker=Emi Figueroa about=Bruno Thompson",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or below $10,100.00.\n- Gate B: passed when net monthly income is at or less than $1,630.00.\n- Gate C: passed when the applicant's age is in excess of 60 years.\n- Route: an applicant enrolled in Mirrowen Transit Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Bruno Thompson to Tollsey Island Ferry Discount receive?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate A is the reason (countable assets)"
  ]
 },
 {
  "qid": "q46d8c8297b",
  "kind": "choice",
  "text": "Dear Joon,\nThis concerns case CR-83193 with the outreach team.\nYours faithfully, Remy Tran\n\nPeople who asked to claim Joon (2025):\n- Kiara Schultz: relationship to Joon: mother; months lived with Joon: 6 months; annual income: 52,795.00 USD; filed a claim: yes\n- Nadia Anderson: relationship to Joon: grandmother; months lived with Joon: 8 months; annual income: 20,784.87 USD; filed a claim: no\n- Kwame Demir: relationship to Joon: father; months lived with Joon: 5 months; annual income: 33,003.00 USD; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for higher than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Joon lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole person entitled to claim Joon for Corrowby Family Supplement?",
  "options": [
   "Nobody may claim the child",
   "Nadia Anderson",
   "Kiara Schultz"
  ]
 },
 {
  "qid": "q64ca65a771",
  "kind": "choice",
  "text": "Regional service office intake\nCase reference: HR-32215\nCaseworker: Jules Shrestha\nSubject: Tamar Stewart\n\nFacts for Tamar Stewart (2026):\n| fact | value |\n| --- | --- |\n| time employed | 28 months |\n| hours worked in the past year | 2,183 hours |\n| employees at the worksite | 41 employees |\n| gross annual pay | $35,500.00 |\n| take-home annual pay | $28,500.01 |\n| enrolled in | Ferrin Exam Stipend |",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has greater than or equal to 33 employees.\n- Gate B: passed when gross annual pay is $35,500.00 at the most.\n- Gate C: passed when take-home annual pay is $28,500.00 at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Hallowdene Logistics Study Grant, which outcome does the application submitted by Tamar Stewart get?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "q109d8bb590",
  "kind": "choice",
  "text": "People who asked to claim Isla (2025):\n| person | relationship to Isla | months lived with Isla | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gustav Lehmann | father | 10 months | 16,151.00 USD | yes |\n| Priya Abara | grandmother | 11 months | 79,020.73 USD | no |\n| Fatima Ramirez | aunt | 12 months | 37,121.00 USD | no |\n\nSupport hub form\nCase reference: CR-37859\nCaseworker: Emi Figueroa\nSubject: Isla",
  "question": "Farrowby Moorland Parish Credit rules for 2025: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for in excess of 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Isla lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Isla for Farrowby Moorland Parish Credit?",
  "options": [
   "Gustav Lehmann",
   "Fatima Ramirez",
   "Priya Abara"
  ]
 },
 {
  "qid": "qc4c68ea66a",
  "kind": "choice",
  "text": "district_ref: CASE-46864\nhandled_by: Alex Lindgren\nabout: Ilse Patterson\n\nFacts for Ilse Patterson (2027):\n- gross monthly income: $4,959.58\n- net monthly income: $3,649.55\n- countable assets: $3,965.31\n- time in the service area: four months\n- age: 68 years\n- enrolled in: Hallowby Utility Discount",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly more than seven months.\n- Gate B: passed when the applicant's age is at or greater than 58 years.\n- Gate C: passed when countable assets are at or beneath $3,400.00.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Ilse Patterson to Tesslow Prairie Water Bill Assistance ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q92ad58eb38",
  "kind": "yes/no",
  "text": "{\"matter\": \"CASE-89727\", \"review_lead\": \"Tomi Eklund\", \"person\": \"Gustav Yamazaki\", \"unit\": \"review\"}\n\nFacts for Gustav Yamazaki (2025), as JSON:\n{\"gross_monthly_income\": \"1,880.00 USD\", \"net_monthly_income\": \"1,427.24 USD\", \"countable_assets\": \"4,050.00 USD\", \"time_in_the_service_area\": \"10 months\", \"age\": \"49 years\", \"enrolled_in\": \"Stennet Commuter Permit\"}",
  "question": "Does a gate that applies halt the application of Gustav Yamazaki to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly below the amount of 1,490.00 USD.\n- Gate B: passed when countable assets are equal to or below 4,050.00 USD.\n- Gate C: passed when gross monthly income is lower than or equal to 1,880.00 USD.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q25c17e726a",
  "kind": "yes/no",
  "text": "Casework team form\nCase ref: CASE-89553\nCaseworker: Cameron Vargas\nAbout: Luka Jovanovic\n\nFacts for Luka Jovanovic (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,590.95 USD |\n| net monthly income | 2,270.01 USD |\n| countable assets | 2,150.00 USD |\n| time in the service area | 44 months |\n| age | 72 years |\n| enrolled in | Stonevale Housing Grant |",
  "question": "Going by the listed rules, is Luka Jovanovic eligible for Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is lower than or equal to 2,270.00 USD.\n- Gate B: passed when the applicant's age is 62 years or greater.\n- Gate C: passed when countable assets are strictly under the value of 2,150.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q662d5b67ba",
  "kind": "choice",
  "text": "Case note: the staff support desk holds the record for Ezra. Case CR-76136, handled by Nika Hernandez.\n\nPeople who asked to claim Ezra (2026):\n- Tomas Douglas: relationship to Ezra: uncle; months lived with Ezra: 12 months; annual income: 84,425.00 USD; filed a claim: yes\n- Ivo Abebe: relationship to Ezra: father; months lived with Ezra: 1 month; annual income: 22,300.50 USD; filed a claim: yes\n- Hana Halvorsen: relationship to Ezra: mother; months lived with Ezra: 8 months; annual income: 48,899.00 USD; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2026: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Ezra for Corrowby Family Supplement?",
  "options": [
   "Tomas Douglas",
   "Hana Halvorsen"
  ]
 },
 {
  "qid": "qaef4b927a6",
  "kind": "yes/no",
  "text": "People who asked to claim Pia (2026):\n| person | relationship to Pia | months lived with Pia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Juliana Hakimi | mother | 7 months | 58,888.41 USD | yes |\n| Hamid Reynolds | father | 12 months | 58,888.41 USD | yes |\n| Tariq Dlamini | uncle | 12 months | 17,103.39 USD | yes |\n\nCase note: thanks for your patience. Blair Xiong has CR-06391 in hand for Pia.",
  "question": "Going by the listed rules, is Hamid Reynolds the person who secures the right to claim Pia for Sorrenby Island Family Payment?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for strictly in excess of 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Pia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9cc5a51a10",
  "kind": "yes/no",
  "text": "Walk-in sheet\nCase: CASE-52915\nCaseworker: Lior Grigoryan\nAbout: Sami Mwangi\n\nFacts for Sami Mwangi (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,545.67 |\n| net monthly income | $1,950.00 |\n| countable assets | $16,276.38 |\n| time in the service area | 5 months |\n| age | 47 years |\n| enrolled in | Stennet Commuter Permit |",
  "question": "Is Sami Mwangi really eligible for Corvane Transit Fare Discount under these rules?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 5 months.\n- Gate B: passed when net monthly income is at or under $1,950.00.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q591258a21d",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CASE-04342\nRaised by: Teo Quintero\nAbout: Ari Ortega\n\nIntake interview with Ari Ortega (2027):\nCaseworker: Gross monthly income?\nAri Ortega: $1,356.63.\nCaseworker: Net monthly income?\nAri Ortega: $1,130.71.\nCaseworker: Countable assets?\nAri Ortega: $3,877.98.\nCaseworker: Time in the service area?\nAri Ortega: 13 months.\nCaseworker: Age?\nAri Ortega: 57 years.\nCaseworker: Other programme enrolled in?\nAri Ortega: Aldervale Meal Ticket.",
  "question": "For Tamsfell Senior Home Support, does Ari Ortega qualify by passing every gate that applies?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is in excess of 57 years.\n- Gate B: passed when net monthly income is smaller than $1,810.\n- Gate C: passed when the applicant has lived in the service area for 8 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q73ceccadf7",
  "kind": "yes/no",
  "text": "[records_office] tag_case=CR-64325 worker=Kazu Yousef about=Kira\n\nPeople who asked to claim Kira (2026):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hana Sokolov | aunt | 12 months | 25,553.37 USD | yes |\n| Farid Ilic | father | 5 months | 85,116.62 USD | no |",
  "question": "Is Hana Sokolov the person who gets to claim Kira for Kelvery Market Credit under these rules?",
  "definitions": "Kelvery Market Credit rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 6 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Kira lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc4a0d5b45b",
  "kind": "yes/no",
  "text": "Facts for Ubah Nilsen (2025):\n| fact | value |\n| --- | --- |\n| time employed | 6 months |\n| hours worked in the past year | 1713 hours |\n| employees at the worksite | 69 employees |\n| gross annual pay | $67,000 |\n| take-home annual pay | 25,761.34 USD |\n| enrolled in | Vellan Travel Support |\n\nRecords desk note. Mika Zamora keeps HR-72999, which concerns Ubah Nilsen.",
  "question": "According to these rules, does Ubah Nilsen meet the rules for Orrendale Printworks Sick Leave Supplement?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or under the amount of $67,000.\n- Gate B: passed when the worksite has above 47 employees.\n- Gate C: passed when take-home annual pay is strictly under the value of $52,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qee53b6dcff",
  "kind": "choice",
  "text": "Ren Dvorak: quick check on file CASE-34861 for Ivo Kimura, at the counter.\n\nFacts for Ivo Kimura (2026):\n- gross monthly income: $4,562.71\n- net monthly income: $3,539.68\n- countable assets: $4,943.07\n- time in the service area: eleven months\n- age: 83 years\n- enrolled in: Brackenholm Housing Aid",
  "question": "Tarrowick Food Basket Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 57 years or above.\n- Gate B: passed when the applicant has lived in the service area for a minimum of eleven months.\n- Gate C: passed when gross monthly income is smaller than $3,950.\n- Gate D: passed when net monthly income is at or less than $2,940.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Ivo Kimura to Tarrowick Food Basket Support get?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate D is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate C is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q0f3eec9933",
  "kind": "yes/no",
  "text": "Note for the intake desk: Waleed Begum is named on case CASE-84996, which Avery Obradovic keeps.\n\nFacts for Waleed Begum (2027):\n- gross monthly income: $2,210.08\n- net monthly income: $2,120.01\n- countable assets: $113.40\n- time in the service area: 6 months\n- age: 90 years\n- enrolled in: Hallowby Utility Supplement",
  "question": "According to these rules, does Waleed Begum qualify for Tesslow Prairie Water Bill Assistance?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly smaller than 2,120.02 USD.\n- Gate B: passed when gross monthly income is $2,735 at the most.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe036f73ad9",
  "kind": "choice",
  "text": "Routine case note: CASE-70233 sits with Kendall Umarov about Mirela Sokolov. Standard entry for the call centre.\n\nIntake interview with Mirela Sokolov (2025):\nCaseworker: Gross monthly income?\nMirela Sokolov: 1,803.80 USD.\nCaseworker: Net monthly income?\nMirela Sokolov: 1,450.15 USD.\nCaseworker: Countable assets?\nMirela Sokolov: 4,109.76 USD.\nCaseworker: Time in the service area?\nMirela Sokolov: 8 months.\nCaseworker: Age?\nMirela Sokolov: 82 years.\nCaseworker: Other programme enrolled in?\nMirela Sokolov: Lowmarsh Heating Aid.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than 65 years.\n- Gate B: passed when countable assets are strictly beneath 7,450.00 USD.\n- Gate C: passed when the applicant has lived in the service area for 9 months or greater.\n- Route: an applicant enrolled in Lowmarsh Heating Aid skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Mirela Sokolov to Tamsfell Senior Home Support?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q7b7e0bb969",
  "kind": "choice",
  "text": "{\"ref\": \"HR-06119\", \"handler\": \"Cameron Vargas\", \"subject\": \"Yara Dubois\", \"desk\": \"walk-in\"}\n\nIntake interview with Yara Dubois (2027):\nCaseworker: Time employed?\nYara Dubois: 12 months.\nCaseworker: Hours worked in the past year?\nYara Dubois: 2017 hours.\nCaseworker: Employees at your worksite?\nYara Dubois: 379 employees.\nCaseworker: Gross annual pay?\nYara Dubois: 82,393.55 USD.\nCaseworker: Take-home annual pay?\nYara Dubois: 66,007.94 USD.\nCaseworker: Other programme enrolled in?\nYara Dubois: Heldane Transit Permit.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly above 12 months.\n- Gate B: passed when take-home annual pay is $70,000 or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Yara Dubois to Quenhollow Brewery Bereavement Leave lead to?",
  "options": [
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)"
  ]
 },
 {
  "qid": "qd09add6e99",
  "kind": "choice",
  "text": "Walk-in sheet\nCase: CR-69481\nCaseworker: Kazu Yousef\nAbout: Kira\n\nPeople who asked to claim Kira (2025):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Farid Robinson | uncle | seven months | $79,791.58 | yes |\n| Ravi Iyer | uncle | eleven months | $61,516.00 | no |\n| Zofia Kimura | aunt | seven months | $61,516.00 | no |",
  "question": "Caddowen Harbour Family Allowance rules for 2025: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for at or over seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kira lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, may claim Kira for Caddowen Harbour Family Allowance?",
  "options": [
   "Nobody may claim the child",
   "Farid Robinson",
   "Ravi Iyer"
  ]
 }
]
