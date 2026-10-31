# G5-H blind read T15-blind_read-e4bd1c07-001 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-e4bd1c07-001.json

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
  "qid": "q580d349125",
  "kind": "yes/no",
  "text": "{\"ref\": \"CASE-86947\", \"lead\": \"Casey Kaplan\", \"person\": \"Tomi Halvorsen\"}\n\nIntake interview with Tomi Halvorsen (2025):\nCaseworker: Gross monthly income?\nTomi Halvorsen: $2,888.29.\nCaseworker: Net monthly income?\nTomi Halvorsen: $2,133.63.\nCaseworker: Countable assets?\nTomi Halvorsen: $11,376.02.\nCaseworker: Time in the service area?\nTomi Halvorsen: 6 months.\nCaseworker: Age?\nTomi Halvorsen: 67 years.\nCaseworker: Other programme enrolled in?\nTomi Halvorsen: none.",
  "question": "Is Tomi Halvorsen eligible for Tamsfell Senior Home Support with every applicable gate passed?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 66 years.\n- Gate B: passed when countable assets are smaller than $11,376.03.\n- Gate C: passed when the applicant has lived in the service area for 3 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7e3b123135",
  "kind": "choice",
  "text": "Dear Bianca Abara,\nThis is a standard notice about HR-34946 from the district office.\nKind regards, Shay Bekele\n\nFacts for Bianca Abara (2025):\n- time employed: 39 months\n- hours worked in the past year: 1481 hours\n- employees at the worksite: 198 employees\n- gross annual pay: 59,553.76 USD\n- take-home annual pay: 52,552.12 USD\n- enrolled in: Pratchell Caregiver Stipend",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are over 1480 hours.\n- Gate B: passed when take-home annual pay is 52,552.13 USD or less.\n- Gate C: passed when gross annual pay is at or below 62,012.33 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Bianca Abara to Wendmoor Mill Parental Leave lead to?",
  "options": [
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "qc1d16df23c",
  "kind": "yes/no",
  "text": "Facts for Sergio Ilic (2026), as JSON:\n{\"gross_monthly_income\": \"1,682.67 USD\", \"net_monthly_income\": \"1,498.11 USD\", \"countable_assets\": \"6,279.17 USD\", \"time_in_the_service_area\": \"8 months\", \"age\": \"83 years\", \"enrolled_in\": \"Ketteridge Veterans Charter\"}\n\n{\"ref\": \"CASE-18927\", \"caseworker\": \"Morgan Mendoza\", \"about\": \"Sergio Ilic\"}",
  "question": "Under these rules, is Sergio Ilic eligible for Sallowick Ward Home Repair Grant overall?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or beneath 6,279.18 USD.\n- Gate B: passed when net monthly income is 1,498.11 USD or less.\n- Gate C: passed when the applicant has lived in the service area for at or over 8 months.\n- Route: an applicant enrolled in Brunsley Energy Rebate skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q54c459d8ee",
  "kind": "choice",
  "text": "Facts for Imani Sorensen (2026):\n| fact | value |\n| --- | --- |\n| time employed | 5 months |\n| hours worked in the past year | 730 hours |\n| employees at the worksite | 286 employees |\n| gross annual pay | $55,013.83 |\n| take-home annual pay | $47,711.42 |\n| enrolled in | Ostermere Respite Care |\n\nReview ticket: HR-65997\nraised by: Adi Chandra\nabout: Imani Sorensen",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly higher than 730 hours.\n- Gate B: passed when gross annual pay is strictly beneath $62,622.57.\n- Gate C: passed when take-home annual pay is $47,711.41 or lower.\n- Route: an applicant enrolled in Ostermere Respite Care skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Imani Sorensen to Pelmoor Ceramics Carer Support gets which outcome?",
  "options": [
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q752d52cddb",
  "kind": "yes/no",
  "text": "Quick intake sheet\nReference: CR-33740\nCaseworker: Mika Zamora\nSubject: Omar\n\nPeople who asked to claim Omar (2025):\n| person | relationship to Omar | months lived with Omar | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Mateo Abebe | uncle | 6 months | 28,793.77 USD | yes |\n| Tariq Stewart | father | 9 months | 24,992.00 USD | yes |\n| Freya Robinson | mother | 12 months | 18,589.00 USD | yes |",
  "question": "Is it true that Tariq Stewart may not claim Omar for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2025: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for at or greater than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Omar lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc4620bf223",
  "kind": "yes/no",
  "text": "Adi Chandra: thanks, admin desk has CASE-91059 set up for Viktor Gutierrez.\n\nFacts for Viktor Gutierrez (2025):\n- gross monthly income: $2,155.87\n- net monthly income: $1,767.12\n- countable assets: $11,846.80\n- time in the service area: 9 months\n- age: 18 years\n- enrolled in: Mosswyke Rail Saver",
  "question": "According to these rules, does a gate that applies end the application of Viktor Gutierrez to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for 12 months or above.\n- Gate B: passed when gross monthly income is strictly below $2,511.67.\n- Gate C: passed when countable assets are strictly under the amount of $11,846.80.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q516762981b",
  "kind": "yes/no",
  "text": "reference: HR-00932\nhandler: Mika Zamora\nsubject: Greta Vasquez\n\nFacts for Greta Vasquez (2025):\n- time employed: 13 months\n- hours worked in the past year: 1170 hours\n- employees at the worksite: 73 employees\n- gross annual pay: 60,901.48 USD\n- take-home annual pay: 44,353.58 USD\n- enrolled in: Corrivale Welding Bursary",
  "question": "Following the listed rules, does Greta Vasquez qualify for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or above 41 employees.\n- Gate B: passed when hours worked in the past year are strictly higher than 1170 hours.\n- Gate C: passed when the applicant has been employed for at or over 8 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe220075300",
  "kind": "yes/no",
  "text": "District office intake form\nReference: CR-81814\nCaseworker: Casey Kaplan\nAbout: Vida\n\nInterview notes for Vida (2027):\nCaseworker: Elias Anderson, your relation to Vida?\nElias Anderson: I am Vida's father.\nCaseworker: Months Vida lived with you?\nElias Anderson: nine months.\nCaseworker: Annual income?\nElias Anderson: $83,911.\nCaseworker: Filed a claim for Vida?\nElias Anderson: no.\nCaseworker: Sabine Hakimi, your relation to Vida?\nSabine Hakimi: I am Vida's mother.\nCaseworker: Months Vida lived with you?\nSabine Hakimi: eight months.\nCaseworker: Annual income?\nSabine Hakimi: $35,791.\nCaseworker: Filed a claim for Vida?\nSabine Hakimi: yes.\nCaseworker: Priya Ilunga, your relation to Vida?\nPriya Ilunga: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nPriya Ilunga: one month.\nCaseworker: Annual income?\nPriya Ilunga: $50,334.\nCaseworker: Filed a claim for Vida?\nPriya Ilunga: yes.",
  "question": "Following the listed rules, does Sabine Hakimi fail to win the right to claim Vida for Gristmere Child Credit?",
  "definitions": "Gristmere Child Credit rules for 2027: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for strictly in excess of seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qeafad0dc84",
  "kind": "yes/no",
  "text": "{\"ref\": \"CASE-86947\", \"lead\": \"Casey Kaplan\", \"person\": \"Tomi Halvorsen\"}\n\nIntake interview with Tomi Halvorsen (2025):\nCaseworker: Gross monthly income?\nTomi Halvorsen: $2,888.29.\nCaseworker: Net monthly income?\nTomi Halvorsen: $2,133.63.\nCaseworker: Countable assets?\nTomi Halvorsen: $11,376.02.\nCaseworker: Time in the service area?\nTomi Halvorsen: 2 months.\nCaseworker: Age?\nTomi Halvorsen: 67 years.\nCaseworker: Other programme enrolled in?\nTomi Halvorsen: none.",
  "question": "Under these rules, does a gate that applies end the application of Tomi Halvorsen to Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 66 years.\n- Gate B: passed when countable assets are smaller than $11,376.03.\n- Gate C: passed when the applicant has lived in the service area for 3 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q81aea2e61f",
  "kind": "yes/no",
  "text": "People who asked to claim Ana (2027), as JSON:\n{\"people\": [{\"name\": \"Hiro Delgado\", \"relationship\": \"father\", \"months_lived_with_child\": \"four months\", \"annual_income\": \"20,963.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Freya Gutierrez\", \"relationship\": \"mother\", \"months_lived_with_child\": \"five months\", \"annual_income\": \"94,856.00 USD\", \"filed_a_claim\": \"yes\"}]}\n\n{\"ref\": \"CR-97845\", \"lead\": \"Shay Bekele\", \"person\": \"Ana\"}",
  "question": "For Brellow Orchard Family Credit, does Freya Gutierrez fail to secure the right to claim Ana under these rules?",
  "definitions": "Brellow Orchard Family Credit rules for 2027: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for equal to or greater than five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ana lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe50818bdc9",
  "kind": "yes/no",
  "text": "Facts for Dani Yilmaz (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,356.62 |\n| net monthly income | $2,736.76 |\n| countable assets | $7,779.56 |\n| time in the service area | 1 month |\n| age | 60 years |\n| enrolled in | Ketteridge Veterans Scheme |\n\ncase: CASE-06802\ncaseworker: Jules Shrestha\nabout: Dani Yilmaz\ndesk: back office",
  "question": "Under these rules, is Dani Yilmaz eligible for Sallowick Ward Home Repair Grant overall?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under $2,839.28.\n- Gate B: passed when the applicant has lived in the service area for larger than 5 months.\n- Gate C: passed when the applicant's age is 60 years at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q45f6a7cffa",
  "kind": "yes/no",
  "text": "Facts for Cyril Robinson (2027), as JSON:\n{\"time_employed\": \"34 months\", \"hours_worked_in_the_past_year\": \"2,087 hours\", \"employees_at_the_worksite\": \"20 employees\", \"gross_annual_pay\": \"80,254.29 USD\", \"take-home_annual_pay\": \"60,136.97 USD\", \"enrolled_in\": \"Tesslow Engineering Traineeship\"}\n\n{\"reference\": \"HR-02966\", \"caseworker\": \"Sami Castro\", \"about\": \"Cyril Robinson\", \"office\": \"district\"}",
  "question": "According to these rules, is Cyril Robinson not eligible for Drummock Robotics Workshop Training Fund?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 20 employees or more.\n- Gate B: passed when gross annual pay is equal to or below 80,254.29 USD.\n- Gate C: passed when the applicant has been employed for 35 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q38b5acc768",
  "kind": "yes/no",
  "text": "Intake form\nCase reference: CASE-61211\nCaseworker: Toni Lazar\nAbout: Quentin Yilmaz\n\nFacts for Quentin Yilmaz (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,425.54 USD |\n| net monthly income | 2,305.66 USD |\n| countable assets | 5,251.80 USD |\n| time in the service area | 18 months |\n| age | 86 years |\n| enrolled in | Crannock Food Pantry |",
  "question": "Is Quentin Yilmaz not eligible for Ostmere Lakeside Winter Energy Support as the rules stand?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 11 months.\n- Gate B: passed when net monthly income is strictly under the amount of 2,489.64 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7a2262f6a6",
  "kind": "yes/no",
  "text": "Hello Zara,\nQuick update: the staff support desk has CR-69078 in view.\nRegards, Avery Obradovic\n\nPeople who asked to claim Zara (2027):\n- Zainab Ruiz: relationship to Zara: mother; months lived with Zara: 7 months; annual income: $62,274.00; filed a claim: yes\n- Tamar Lehmann: relationship to Zara: aunt; months lived with Zara: 8 months; annual income: $62,274.00; filed a claim: yes\n- Dmitri Johnson: relationship to Zara: uncle; months lived with Zara: 8 months; annual income: $55,550.00; filed a claim: yes",
  "question": "Going by the listed rules, does Zainab Ruiz fail to win the right to claim Zara for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2027: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for equal to or greater than 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Zara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8f06289203",
  "kind": "yes/no",
  "text": "case_ref: HR-48798\nworker: Kiran Morales\nsubject: Anjali Ilic\n\nFacts for Anjali Ilic (2027):\n- time employed: five months\n- hours worked in the past year: 1,527 hours\n- employees at the worksite: 64 employees\n- gross annual pay: 87,998.74 USD\n- take-home annual pay: 54,943.27 USD\n- enrolled in: Pratchell Caregiver Allowance",
  "question": "Under these rules, is Anjali Ilic eligible for Wendmoor Mill Parental Leave overall?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 64 employees at minimum.\n- Gate B: passed when the applicant has been employed for equal to or greater than six months.\n- Gate C: passed when gross annual pay is at or beneath 55,463.10 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe174ce9413",
  "kind": "yes/no",
  "text": "Hi Isla,\nThis is a quick note on case CR-38393 from the records office.\nCheers, Remy Tran\n\nInterview notes for Isla (2026):\nCaseworker: Sergio Demir, your relation to Isla?\nSergio Demir: I am Isla's father.\nCaseworker: Months Isla lived with you?\nSergio Demir: 3 months.\nCaseworker: Annual income?\nSergio Demir: $61,877.39.\nCaseworker: Filed a claim for Isla?\nSergio Demir: yes.\nCaseworker: Rania Ueda, your relation to Isla?\nRania Ueda: I am Isla's mother.\nCaseworker: Months Isla lived with you?\nRania Ueda: 6 months.\nCaseworker: Annual income?\nRania Ueda: $43,711.13.\nCaseworker: Filed a claim for Isla?\nRania Ueda: yes.\nCaseworker: Anton Hoffman, your relation to Isla?\nAnton Hoffman: I am Isla's grandfather.\nCaseworker: Months Isla lived with you?\nAnton Hoffman: 10 months.\nCaseworker: Annual income?\nAnton Hoffman: $43,711.13.\nCaseworker: Filed a claim for Isla?\nAnton Hoffman: yes.",
  "question": "Following the listed rules, is Anton Hoffman the person who winds up with the claim on Isla for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2026: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for a minimum of 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Isla lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q152559bca2",
  "kind": "yes/no",
  "text": "Back office ticket: HR-55821\nRaised by: Shay Bekele\nAbout: Jiro Becker\n\nFacts for Jiro Becker (2027):\n| fact | value |\n| --- | --- |\n| time employed | 57 months |\n| hours worked in the past year | 90 hours |\n| employees at the worksite | 39 employees |\n| gross annual pay | $72,389.49 |\n| take-home annual pay | $52,272.94 |\n| enrolled in | Lethgate Commute Allowance |",
  "question": "Is Jiro Becker not eligible for Hallowdene Logistics Study Grant under these rules?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or under $72,389.49.\n- Gate B: passed when the worksite has 39 employees at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6136f9fd51",
  "kind": "choice",
  "text": "Facts for Kiran Dlamini (2026), as JSON:\n{\"time_employed\": \"18 months\", \"hours_worked_in_the_past_year\": \"664 hours\", \"employees_at_the_worksite\": \"367 employees\", \"gross_annual_pay\": \"$58,359.57\", \"take-home_annual_pay\": \"$52,370.08\", \"enrolled_in\": \"Hallowby Shift Childcare Support\"}\n\n{\"case\": \"HR-93450\", \"caseworker\": \"Casey Kaplan\", \"about\": \"Kiran Dlamini\"}",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are higher than 930 hours.\n- Gate B: passed when gross annual pay is strictly under the amount of $58,359.58.\n- Gate C: passed when the applicant has been employed for greater than 17 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Kiran Dlamini to Drummock Robotics Workshop Training Fund lead to?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (time employed)"
  ]
 },
 {
  "qid": "q86e0b5b08f",
  "kind": "yes/no",
  "text": "Staff support form\nRef: HR-17142\nOwner: Shay Bekele\nPerson: Nkechi Ilunga\n\nFacts for Nkechi Ilunga (2027):\n| fact | value |\n| --- | --- |\n| time employed | 65 months |\n| hours worked in the past year | 1319 hours |\n| employees at the worksite | 100 employees |\n| gross annual pay | $24,395.69 |\n| take-home annual pay | $15,959.07 |\n| enrolled in | Gerrondale Tenant Aid |",
  "question": "Under these rules, is Nkechi Ilunga eligible for Marrowby Bakery Family Leave given every gate that applies is passed?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are equal to or greater than 1320 hours.\n- Gate B: passed when gross annual pay is strictly beneath $37,733.57.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc9b6517f52",
  "kind": "yes/no",
  "text": "People who asked to claim Lara (2026):\n| person | relationship to Lara | months lived with Lara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Pavel Choi | father | 1 month | 67,971.00 USD | no |\n| Vesna Reynolds | mother | 10 months | 34,230.94 USD | no |\n| Tariq Nguyen | uncle | 4 months | 63,744.00 USD | yes |\n\nServices counter form\nCase reference: CR-53626\nCaseworker: Teo Quintero\nSubject: Lara",
  "question": "Under these rules, is Tariq Nguyen the person who gets to claim Lara for Sorrenby Island Family Payment?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Lara.\n- Only one person may claim Lara. Work through these steps in order.\n- Step one: only people who filed a claim for Lara are considered.\n- Step two: of those, only people with whom Lara lived for 5 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Lara lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Lara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q203931cbd5",
  "kind": "choice",
  "text": "Back office ticket: CR-65276\nRaised by: Shay Bekele\nAbout: Ines\n\nInterview notes for Ines (2026):\nCaseworker: Dagny Mitchell, your relation to Ines?\nDagny Mitchell: I am Ines's aunt.\nCaseworker: Months Ines lived with you?\nDagny Mitchell: 7 months.\nCaseworker: Annual income?\nDagny Mitchell: $39,332.88.\nCaseworker: Filed a claim for Ines?\nDagny Mitchell: no.\nCaseworker: Hana Ueda, your relation to Ines?\nHana Ueda: I am Ines's mother.\nCaseworker: Months Ines lived with you?\nHana Ueda: 0 months.\nCaseworker: Annual income?\nHana Ueda: $87,125.\nCaseworker: Filed a claim for Ines?\nHana Ueda: yes.\nCaseworker: Sergio Nakamura, your relation to Ines?\nSergio Nakamura: I am Ines's grandfather.\nCaseworker: Months Ines lived with you?\nSergio Nakamura: 1 month.\nCaseworker: Annual income?\nSergio Nakamura: $26,826.\nCaseworker: Filed a claim for Ines?\nSergio Nakamura: yes.\nCaseworker: Amara Nilsen, your relation to Ines?\nAmara Nilsen: I am Ines's grandmother.\nCaseworker: Months Ines lived with you?\nAmara Nilsen: 7 months.\nCaseworker: Annual income?\nAmara Nilsen: $83,471.\nCaseworker: Filed a claim for Ines?\nAmara Nilsen: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for at or above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ines lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Stonevale Delta Child Allowance, which person, if any, gets to claim Ines under these rules?",
  "options": [
   "Nobody may claim the child",
   "Amara Nilsen",
   "Hana Ueda"
  ]
 },
 {
  "qid": "qed50de5079",
  "kind": "yes/no",
  "text": "{\"ref\": \"CR-99384\", \"handler\": \"Ren Dvorak\", \"subject\": \"Milo\", \"desk\": \"walk-in\"}\n\nInterview notes for Milo (2026):\nCaseworker: Tomas Esposito, your relation to Milo?\nTomas Esposito: I am Milo's uncle.\nCaseworker: Months Milo lived with you?\nTomas Esposito: 5 months.\nCaseworker: Annual income?\nTomas Esposito: $21,561.54.\nCaseworker: Filed a claim for Milo?\nTomas Esposito: yes.\nCaseworker: Rania Kelly, your relation to Milo?\nRania Kelly: I am Milo's mother.\nCaseworker: Months Milo lived with you?\nRania Kelly: 6 months.\nCaseworker: Annual income?\nRania Kelly: $33,008.00.\nCaseworker: Filed a claim for Milo?\nRania Kelly: yes.\nCaseworker: Pavel Kelly, your relation to Milo?\nPavel Kelly: I am Milo's father.\nCaseworker: Months Milo lived with you?\nPavel Kelly: 10 months.\nCaseworker: Annual income?\nPavel Kelly: $31,146.10.\nCaseworker: Filed a claim for Milo?\nPavel Kelly: yes.",
  "question": "Going by the listed rules, does Rania Kelly fail to win the right to claim Milo for Stonevale Delta Child Allowance?",
  "definitions": "Stonevale Delta Child Allowance rules for 2026: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for greater than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Milo lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qaf0d819e37",
  "kind": "choice",
  "text": "Routine ticket: CR-06713\nRaised by: Jules Shrestha\nAbout: Eva\n\nPeople who asked to claim Eva (2025):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Mariam Halvorsen | grandmother | ten months | $25,349.00 | yes |\n| Nadia Nilsen | mother | three months | $54,957.00 | yes |\n| Anjali Ilunga | grandmother | ten months | $58,017.00 | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for over six months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tessenvale Valley Child Credit, which person, if any, gets the right to claim Eva?",
  "options": [
   "Anjali Ilunga",
   "Mariam Halvorsen"
  ]
 },
 {
  "qid": "qee0b20ed5d",
  "kind": "yes/no",
  "text": "Hello Rafael Robinson,\nThanks for popping in about case CASE-19763.\nWarm regards, Yuki Adeyemi\n\nIntake interview with Rafael Robinson (2026):\nCaseworker: Gross monthly income?\nRafael Robinson: 4,350.31 USD.\nCaseworker: Net monthly income?\nRafael Robinson: 3,618.10 USD.\nCaseworker: Countable assets?\nRafael Robinson: 1,969.08 USD.\nCaseworker: Time in the service area?\nRafael Robinson: 7 months.\nCaseworker: Age?\nRafael Robinson: 74 years.\nCaseworker: Other programme enrolled in?\nRafael Robinson: Kelmstone Drainage Subsidy.",
  "question": "Following the listed rules, is Rafael Robinson not eligible for Ostermere Delta Flood Repair Support?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is at or beyond 60 years.\n- Gate B: passed when countable assets are strictly under 2,544.90 USD.\n- Gate C: passed when the applicant has lived in the service area for 8 months or more.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q673dac4096",
  "kind": "choice",
  "text": "Jamie Jorgensen: picking up case HR-84899 for Dagny Wojcik.\n\nIntake interview with Dagny Wojcik (2027):\nCaseworker: Time employed?\nDagny Wojcik: six months.\nCaseworker: Hours worked in the past year?\nDagny Wojcik: 357 hours.\nCaseworker: Employees at your worksite?\nDagny Wojcik: 61 employees.\nCaseworker: Gross annual pay?\nDagny Wojcik: $39,740.18.\nCaseworker: Take-home annual pay?\nDagny Wojcik: $29,677.58.\nCaseworker: Other programme enrolled in?\nDagny Wojcik: Ellerwick Trainee Scheme.",
  "question": "Sorrelby Child Care Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than or equal to $54,200.27.\n- Gate B: passed when take-home annual pay is strictly below the level of $40,751.08.\n- Gate C: passed when the worksite has strictly over 46 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Dagny Wojcik to Sorrelby Child Care Support lead to?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q15f644a53f",
  "kind": "choice",
  "text": "People who asked to claim Ami (2027):\n| person | relationship to Ami | months lived with Ami | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ibrahim Okoro | father | 8 months | $24,136.92 | yes |\n| Luka Jovanovic | uncle | 7 months | $55,551.00 | yes |\n| Yasmin Ruiz | aunt | 8 months | $83,014.83 | yes |\n\nHello Ami,\nQuick update: the staff support desk has CR-64416 in view.\nRegards, Adi Chandra",
  "question": "Brellow Orchard Family Credit rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for above 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ami lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Ami for Brellow Orchard Family Credit under these rules?",
  "options": [
   "Yasmin Ruiz",
   "Nobody may claim the child",
   "Ibrahim Okoro"
  ]
 },
 {
  "qid": "q1e82b93580",
  "kind": "choice",
  "text": "Facts for Nika Jovanovic (2027):\n| fact | value |\n| --- | --- |\n| time employed | 73 months |\n| hours worked in the past year | 1,132 hours |\n| employees at the worksite | 240 employees |\n| gross annual pay | $49,048.69 |\n| take-home annual pay | $34,620.04 |\n| enrolled in | Ostermere Respite Care |\n\nrecord: HR-42331\nlead: Avery Obradovic\nsubject: Nika Jovanovic",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly over 950 hours.\n- Gate B: passed when take-home annual pay is $34,620.04 or lower.\n- Gate C: passed when gross annual pay is strictly lower than $49,048.70.\n- Route: an applicant enrolled in Tundale Care Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Nika Jovanovic to Pelmoor Ceramics Carer Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qbdc60d4348",
  "kind": "choice",
  "text": "{\"case\": \"CASE-16268\", \"caseworker\": \"Ari Benali\", \"about\": \"Ravi Ilic\", \"desk\": \"call centre\"}\n\nFacts for Ravi Ilic (2025), as JSON:\n{\"gross_monthly_income\": \"3,473.29 USD\", \"net_monthly_income\": \"2,777.24 USD\", \"countable_assets\": \"10,861.97 USD\", \"time_in_the_service_area\": \"2 months\", \"age\": \"51 years\", \"enrolled_in\": \"Tallow Ridge Commuter Pass\"}",
  "question": "Sennamoor River Rent Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under the amount of 3,473.29 USD.\n- Gate B: passed when the applicant has lived in the service area for strictly more than 4 months.\n- Gate C: passed when countable assets are smaller than 9,783.52 USD.\n- Gate D: passed when net monthly income is 2,777.24 USD or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Ravi Ilic to Sennamoor River Rent Support resolved?",
  "options": [
   "Not eligible: Gate D is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q98e79394cd",
  "kind": "choice",
  "text": "{\"case\": \"CASE-85969\", \"caseworker\": \"Kiran Morales\", \"about\": \"Yara Nguyen\"}\n\nFacts for Yara Nguyen (2026), as JSON:\n{\"gross_monthly_income\": \"4,047.95 USD\", \"net_monthly_income\": \"2,789.14 USD\", \"countable_assets\": \"2,826.13 USD\", \"time_in_the_service_area\": \"37 months\", \"age\": \"40 years\", \"enrolled_in\": \"Stonevale Housing Loan\"}",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is lower than 3,554.67 USD.\n- Gate B: passed when the applicant's age is larger than 67 years.\n- Gate C: passed when countable assets are at or under 2,826.13 USD.\n- Gate D: passed when net monthly income is at or less than 2,789.15 USD.\n- Route: an applicant enrolled in Stonevale Housing Loan skips Gate B and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does Yara Nguyen get on the application to Corrivale Valley Childcare Grant under these rules?",
  "options": [
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate D is the reason (net monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "q8610b8a65a",
  "kind": "choice",
  "text": "Intake ticket: CASE-27923\nRaised by: Morgan Mendoza\nAbout: Nika Abebe\n\nIntake interview with Nika Abebe (2027):\nCaseworker: Gross monthly income?\nNika Abebe: 4,245.38 USD.\nCaseworker: Net monthly income?\nNika Abebe: 2,640.59 USD.\nCaseworker: Countable assets?\nNika Abebe: 2,315.87 USD.\nCaseworker: Time in the service area?\nNika Abebe: twelve months.\nCaseworker: Age?\nNika Abebe: 74 years.\nCaseworker: Other programme enrolled in?\nNika Abebe: Lowmarsh Heating Aid.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below 3,939.33 USD.\n- Gate B: passed when gross monthly income is at or below the level of 2,987.76 USD.\n- Gate C: passed when the applicant's age is strictly in excess of 58 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nConcerning Tamsfell Senior Home Support, which outcome does the application by Nika Abebe receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate C is the reason (age)"
  ]
 },
 {
  "qid": "q3436e512a4",
  "kind": "choice",
  "text": "Mika Zamora: outreach list has CASE-95347 for Yusuf Patterson.\n\nFacts for Yusuf Patterson (2027):\n- gross monthly income: $4,602.45\n- net monthly income: $3,241.53\n- countable assets: $12,314.93\n- time in the service area: 11 months\n- age: 57 years\n- enrolled in: Sorrenby Tenancy Deposit Loan",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for above 10 months.\n- Gate B: passed when net monthly income is strictly beneath the level of $3,241.53.\n- Gate C: passed when the applicant's age is 65 years or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Yusuf Patterson to Tesslow Prairie Water Bill Assistance get?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "q745051509d",
  "kind": "choice",
  "text": "Facts for Priya Lehmann (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,171.21 |\n| net monthly income | $1,311.92 |\n| countable assets | $14,746.39 |\n| time in the service area | 5 months |\n| age | 62 years |\n| enrolled in | Morvane Carers Pension |\n\nCase note: Cameron Vargas logged file CASE-20445 for Priya Lehmann at the walk-in desk.",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is lower than or equal to $2,171.21.\n- Gate B: passed when net monthly income is strictly below the level of $1,812.93.\n- Gate C: passed when the applicant has lived in the service area for strictly more than 3 months.\n- Gate D: passed when the applicant's age is strictly in excess of 61 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Priya Lehmann to Wyndholm Forest Fuel Support land?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Not eligible: Gate D is the reason (age)"
  ]
 },
 {
  "qid": "q7f775e7d1c",
  "kind": "choice",
  "text": "Dear Luca,\nThanks for getting in touch about case CR-39493.\nWarm wishes, Dani Ishikawa\n\nInterview notes for Luca (2027):\nCaseworker: Wanjiru Gallegos, your relation to Luca?\nWanjiru Gallegos: I am Luca's mother.\nCaseworker: Months Luca lived with you?\nWanjiru Gallegos: 8 months.\nCaseworker: Annual income?\nWanjiru Gallegos: $62,919.\nCaseworker: Filed a claim for Luca?\nWanjiru Gallegos: no.\nCaseworker: Gustav Eriksen, your relation to Luca?\nGustav Eriksen: I am Luca's uncle.\nCaseworker: Months Luca lived with you?\nGustav Eriksen: 7 months.\nCaseworker: Annual income?\nGustav Eriksen: $26,654.83.\nCaseworker: Filed a claim for Luca?\nGustav Eriksen: yes.",
  "question": "Sallowmere Family Payment rules for 2027: who may claim Luca.\n- Only one person may claim Luca. Work through these steps in order.\n- Step one: only people who filed a claim for Luca are considered.\n- Step two: of those, only people with whom Luca lived for 7 months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Luca lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Luca.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Luca for Sallowmere Family Payment?",
  "options": [
   "Wanjiru Gallegos",
   "Gustav Eriksen",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q0ca11088b2",
  "kind": "choice",
  "text": "People who asked to claim Ivan (2025):\n| person | relationship to Ivan | months lived with Ivan | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kwame Schultz | uncle | 4 months | $81,642 | yes |\n| Ivo Ilunga | father | 9 months | $51,712 | yes |\n| Sabine Mitchell | mother | 6 months | $88,731.40 | yes |\n\nReview ticket: CR-19554\nOwner: Cameron Vargas\nAbout: Ivan",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for over 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Ivan for Brellow Orchard Family Credit?",
  "options": [
   "Ivo Ilunga",
   "Kwame Schultz"
  ]
 },
 {
  "qid": "q9a7e0ed1dd",
  "kind": "yes/no",
  "text": "unit: busy support hub\nticket: CASE-06889\nhandling: Riley Watanabe\nregards: Oskar Iyer\n\nFacts for Oskar Iyer (2025):\n- gross monthly income: $1,900.73\n- net monthly income: $1,222.77\n- countable assets: $5,024.21\n- time in the service area: 7 months\n- age: 32 years\n- enrolled in: Stonevale Housing Loan",
  "question": "Is Oskar Iyer eligible for Corrivale Valley Childcare Grant with every applicable gate passed?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly above 6 months.\n- Gate B: passed when gross monthly income is strictly beneath $3,237.31.\n- Route: an applicant enrolled in Stonevale Housing Loan skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q41f0bd6ec4",
  "kind": "yes/no",
  "text": "Hi team,\nA short routine note goes out on case CR-31544 about Ivan.\nThanks, Dani Ishikawa\n\nPeople who asked to claim Ivan (2025):\n- Ivo Petrov: relationship to Ivan: father; months lived with Ivan: 7 months; annual income: 37,966.14 USD; filed a claim: no\n- Hana Singh: relationship to Ivan: mother; months lived with Ivan: 1 month; annual income: 86,958.59 USD; filed a claim: yes",
  "question": "Is Ivo Petrov excluded from claiming Ivan for Ostrowan Prairie Grant under these rules?",
  "definitions": "Ostrowan Prairie Grant rules for 2025: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for strictly above 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3c37792c20",
  "kind": "choice",
  "text": "Front counter intake form\nReference: CASE-74698\nCaseworker: Morgan Mendoza\nPerson: Amara Esposito\n\nFacts for Amara Esposito (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $5,159.17 |\n| net monthly income | $3,531.49 |\n| countable assets | $4,456.43 |\n| time in the service area | seventeen months |\n| age | 61 years |\n| enrolled in | Ruddock Shuttle Card |",
  "question": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than nine months.\n- Gate B: passed when countable assets are smaller than $7,080.71.\n- Gate C: passed when the applicant's age is equal to or above 62 years.\n- Route: an applicant enrolled in Mosswyke Rail Saver skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Corvane Transit Fare Discount, which outcome does the application of Amara Esposito get?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qb186350846",
  "kind": "choice",
  "text": "People who asked to claim Ana (2026):\n| person | relationship to Ana | months lived with Ana | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Elias Mwangi | father | ten months | $21,955.00 | yes |\n| Hugo Sullivan | grandfather | twelve months | $82,245.00 | yes |\n| Ilse Kelly | grandmother | eight months | $51,786.02 | yes |\n| Nadia Petrov | mother | ten months | $30,633.00 | yes |\n\ndesk: community help\ncase: CR-25612\ncaseworker: Lior Grigoryan\nabout: Ana",
  "question": "Brellow Orchard Family Credit rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for at or above six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Ana for Brellow Orchard Family Credit?",
  "options": [
   "Elias Mwangi",
   "Hugo Sullivan"
  ]
 },
 {
  "qid": "q3ca0d87f15",
  "kind": "yes/no",
  "text": "Morgan Mendoza: hi team, thread for CASE-15748 covers Freya Iyer, thanks!\n\nIntake interview with Freya Iyer (2027):\nCaseworker: Gross monthly income?\nFreya Iyer: 2,852.20 USD.\nCaseworker: Net monthly income?\nFreya Iyer: 1,802.27 USD.\nCaseworker: Countable assets?\nFreya Iyer: 17,515.26 USD.\nCaseworker: Time in the service area?\nFreya Iyer: 8 months.\nCaseworker: Age?\nFreya Iyer: 75 years.\nCaseworker: Other programme enrolled in?\nFreya Iyer: Ormsby Housing Plan.",
  "question": "Is Freya Iyer eligible for Fennick School Meal Supplement with every applicable gate passed?",
  "definitions": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or below 1,802.26 USD.\n- Gate B: passed when the applicant has lived in the service area for strictly higher than 7 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qaa5c19e672",
  "kind": "yes/no",
  "text": "{\"ref\": \"CASE-86947\", \"lead\": \"Casey Kaplan\", \"person\": \"Tomi Halvorsen\"}\n\nIntake interview with Tomi Halvorsen (2025):\nCaseworker: Gross monthly income?\nTomi Halvorsen: $2,888.29.\nCaseworker: Net monthly income?\nTomi Halvorsen: $2,133.63.\nCaseworker: Countable assets?\nTomi Halvorsen: $11,376.02.\nCaseworker: Time in the service area?\nTomi Halvorsen: 6 months.\nCaseworker: Age?\nTomi Halvorsen: 67 years.\nCaseworker: Other programme enrolled in?\nTomi Halvorsen: none.",
  "question": "Under these rules, does a gate that applies end the application of Tomi Halvorsen to Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 66 years.\n- Gate B: passed when countable assets are smaller than $11,376.03.\n- Gate C: passed when the applicant has lived in the service area for 3 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q60c66ee119",
  "kind": "yes/no",
  "text": "{\"case\": \"HR-95359\", \"caseworker\": \"Morgan Mendoza\", \"about\": \"Zainab Ueda\", \"kind\": \"case file\"}\n\nFacts for Zainab Ueda (2025), as JSON:\n{\"time_employed\": \"101 months\", \"hours_worked_in_the_past_year\": \"2,115 hours\", \"employees_at_the_worksite\": \"64 employees\", \"gross_annual_pay\": \"40,616.47 USD\", \"take-home_annual_pay\": \"30,691.90 USD\", \"enrolled_in\": \"Quillmere Apprentice Pilot\"}",
  "question": "Does a gate that applies stop the application of Zainab Ueda to Halvorne Shipyard Tuition Assistance under these rules?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are equal to or above 1,330 hours.\n- Gate B: passed when the worksite has at or beyond 65 employees.\n- Gate C: passed when take-home annual pay is 63,511.27 USD or lower.\n- Route: an applicant enrolled in Quillmere Apprentice Pathway skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0ae386333d",
  "kind": "yes/no",
  "text": "Facts for Waleed Becker (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,762.65 USD |\n| net monthly income | 1,668.20 USD |\n| countable assets | 10,087.41 USD |\n| time in the service area | 35 months |\n| age | 66 years |\n| enrolled in | Wenlow Housing Aid |\n\nDear colleague,\nThis is a short outreach note on case CASE-67968 for Waleed Becker.\nRegards, Shay Bekele",
  "question": "Is Waleed Becker eligible for Tollsey Island Ferry Discount with every applicable gate passed?",
  "definitions": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or beneath 6,644.92 USD.\n- Gate B: passed when net monthly income is at or under the amount of 3,161.95 USD.\n- Gate C: passed when gross monthly income is at or below 4,098.59 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4e37e4413c",
  "kind": "yes/no",
  "text": "Facts for Kofi Demir (2027), as JSON:\n{\"gross_monthly_income\": \"$3,636.90\", \"net_monthly_income\": \"$2,734.54\", \"countable_assets\": \"$17,853.04\", \"time_in_the_service_area\": \"51 months\", \"age\": \"83 years\", \"enrolled_in\": \"Velden Transit Badge\"}\n\n{\"record\": \"case\", \"reference\": \"CASE-09703\", \"caseworker\": \"Kendall Umarov\", \"about\": \"Kofi Demir\"}",
  "question": "Under these rules, does Kofi Demir meet the rules for Sallowick Ward Home Repair Grant across every applicable gate?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below $17,853.04.\n- Gate B: passed when net monthly income is at or under $2,734.55.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3e83550994",
  "kind": "choice",
  "text": "Facts for Anjali Kovacs (2026):\n| fact | value |\n| --- | --- |\n| time employed | 50 months |\n| hours worked in the past year | 1236 hours |\n| employees at the worksite | thirteen employees |\n| gross annual pay | $67,479.00 |\n| take-home annual pay | $56,911.76 |\n| enrolled in | Ostermere Skills Bursary |\n\nEzra Rosales: Lovely to hear from Anjali Kovacs, HR-86714 is in hand.",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly beneath the level of $67,479.00.\n- Gate B: passed when hours worked in the past year are equal to or above 1060 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Anjali Kovacs to Drummock Robotics Workshop Training Fund get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qc66d2badf3",
  "kind": "yes/no",
  "text": "case_ref: CR-12559\nworker: Adi Chandra\nsubject: Kai\n\nPeople who asked to claim Kai (2025):\n- Nkechi Demir: relationship to Kai: mother; months lived with Kai: 6 months; annual income: $27,398; filed a claim: yes\n- Olena Rahimi: relationship to Kai: aunt; months lived with Kai: 5 months; annual income: $51,863; filed a claim: yes\n- Galina Esposito: relationship to Kai: grandmother; months lived with Kai: 10 months; annual income: $90,292; filed a claim: no",
  "question": "Following the listed rules, is Olena Rahimi barred from claiming Kai for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for 6 months or greater in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q96d0660f38",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CASE-41344, handled by Casey Kaplan\n[subject_line] Nika Ortega is at the heart of it\n\nFacts for Nika Ortega (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,647.22 |\n| net monthly income | $2,885.99 |\n| countable assets | $16,519.63 |\n| time in the service area | 18 months |\n| age | 63 years |\n| enrolled in | Ardwold Heating Oil Fund |",
  "question": "Does Nika Ortega meet the rules for Tesslow Prairie Water Bill Assistance by passing every gate that applies?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is higher than 63 years.\n- Gate B: passed when net monthly income is lower than or equal to $2,885.98.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5559f9d63f",
  "kind": "yes/no",
  "text": "Welcome to your case file\nCase reference: HR-08991\nCaseworker: Kazu Yousef\nAbout: Gabriel Dlamini\n\nFacts for Gabriel Dlamini (2026):\n| fact | value |\n| --- | --- |\n| time employed | ten months |\n| hours worked in the past year | 1,349 hours |\n| employees at the worksite | 255 employees |\n| gross annual pay | $79,923.78 |\n| take-home annual pay | $44,429.94 |\n| enrolled in | Corrowell Sabbatical Fund |",
  "question": "Under these rules, is Gabriel Dlamini eligible for Wendmoor Mill Parental Leave overall?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for ten months or above.\n- Gate B: passed when gross annual pay is at or beneath $60,474.74.\n- Gate C: passed when take-home annual pay is at or below $44,429.95.\n- Route: an applicant enrolled in Corrowell Sabbatical Fund skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8dc651bb4f",
  "kind": "yes/no",
  "text": "Hi,\nQuick update: file CASE-51515 about Jakub Anderson is in my queue.\nThanks, Toni Lazar\n\nFacts for Jakub Anderson (2027):\n- gross monthly income: $3,819.87\n- net monthly income: $2,157.82\n- countable assets: $10,517.42\n- time in the service area: 31 months\n- age: 81 years\n- enrolled in: Corrivale Meal Voucher",
  "question": "For Tesslow Prairie Water Bill Assistance, does Jakub Anderson qualify by passing every gate that applies?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is smaller than $2,157.82.\n- Gate B: passed when gross monthly income is lower than $2,980.32.\n- Route: an applicant enrolled in Corrivale Meal Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa23523cd6c",
  "kind": "yes/no",
  "text": "Facts for Kazu Robinson (2025), as JSON:\n{\"time_employed\": \"thirteen months\", \"hours_worked_in_the_past_year\": \"1933 hours\", \"employees_at_the_worksite\": \"36 employees\", \"gross_annual_pay\": \"$32,323.14\", \"take-home_annual_pay\": \"$23,815.30\", \"enrolled_in\": \"Ostermere Respite Care\"}\n\n{\"case\": \"HR-35362\", \"caseworker\": \"Yuki Adeyemi\", \"about\": \"Kazu Robinson\", \"tone\": \"warm\"}",
  "question": "For Pelmoor Ceramics Carer Support, is Kazu Robinson ineligible under the stated rules?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or above thirteen months.\n- Gate B: passed when gross annual pay is strictly under the amount of $33,148.84.\n- Gate C: passed when the worksite has above 41 employees.\n- Route: an applicant enrolled in Ostermere Respite Care skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q70b63c997e",
  "kind": "choice",
  "text": "desk: intake\ncase: CR-18819\ncaseworker: Kazu Yousef\nabout: Vida\n\nPeople who asked to claim Vida (2026):\n- Kavita Ivanova: relationship to Vida: aunt; months lived with Vida: three months; annual income: 36,250.00 USD; filed a claim: yes\n- Kiara Esposito: relationship to Vida: aunt; months lived with Vida: six months; annual income: 42,909.00 USD; filed a claim: yes\n- Tariq Sullivan: relationship to Vida: grandfather; months lived with Vida: five months; annual income: 87,270.00 USD; filed a claim: no",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for a minimum of six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Vida lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Vida for Ferrowby Forest Credit?",
  "options": [
   "Nobody may claim the child",
   "Kavita Ivanova",
   "Kiara Esposito"
  ]
 }
]
