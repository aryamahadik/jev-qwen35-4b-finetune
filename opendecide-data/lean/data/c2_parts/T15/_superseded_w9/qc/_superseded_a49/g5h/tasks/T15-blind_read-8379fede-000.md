# G5-H blind read T15-blind_read-8379fede-000 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-8379fede-000.json

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
  "qid": "q08e76a3da7",
  "kind": "yes/no",
  "text": "Teo Quintero: Happy to take CASE-97125 about Lior Iyer, thanks for flagging!\n\nIntake interview with Lior Iyer (2027):\nCaseworker: Gross monthly income?\nLior Iyer: 2,059.36 USD.\nCaseworker: Net monthly income?\nLior Iyer: 1,813.19 USD.\nCaseworker: Countable assets?\nLior Iyer: 1,461.95 USD.\nCaseworker: Time in the service area?\nLior Iyer: three months.\nCaseworker: Age?\nLior Iyer: 65 years.\nCaseworker: Other programme enrolled in?\nLior Iyer: Ulverby Summer Meals.",
  "question": "Is Lior Iyer formally ineligible for Fennick School Meal Supplement under these rules?",
  "definitions": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below 2,300.00 USD.\n- Gate B: passed when the applicant has lived in the service area for at or over three months.\n- Gate C: passed when the applicant's age is at or over 66 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb07dae6d90",
  "kind": "yes/no",
  "text": "Case note: Jamie Jorgensen is glad to take on the matter of Ana, reference CR-47978.\n\nPeople who asked to claim Ana (2025):\n- Oskar Thompson: relationship to Ana: father; months lived with Ana: five months; annual income: $57,651.00; filed a claim: yes\n- Ravi Russell: relationship to Ana: uncle; months lived with Ana: two months; annual income: $62,645.00; filed a claim: yes\n- Zofia Evans: relationship to Ana: mother; months lived with Ana: two months; annual income: $53,114.00; filed a claim: yes\n- Nadia Halvorsen: relationship to Ana: grandmother; months lived with Ana: seven months; annual income: $64,806.51; filed a claim: yes",
  "question": "Going by the listed rules, is Zofia Evans shut out from claiming Ana for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2025: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for in excess of six months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8461db3964",
  "kind": "choice",
  "text": "People who asked to claim Mia (2027):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Priya Medina | mother | 6 months | $83,438 | no |\n| Jakub Ilunga | uncle | 10 months | $71,971.40 | yes |\n| Dario Gashi | father | 7 months | $70,686 | yes |\n\nSami Castro: cheers, the staff support desk has CR-09806 for Mia.",
  "question": "Sorrenby Island Family Payment rules for 2027: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for 7 months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Mia for Sorrenby Island Family Payment?",
  "options": [
   "Jakub Ilunga",
   "Priya Medina"
  ]
 },
 {
  "qid": "qe653c02a64",
  "kind": "choice",
  "text": "district_ref: HR-80876\nhandled_by: Jamie Jorgensen\nabout: Jiro Ivanova\n\nFacts for Jiro Ivanova (2026):\n- time employed: seventeen months\n- hours worked in the past year: 2,080 hours\n- employees at the worksite: 31 employees\n- gross annual pay: $72,851.54\n- take-home annual pay: $62,780.40\n- enrolled in: Gerrondale Tenant Loan",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 71 employees or more.\n- Gate B: passed when hours worked in the past year are above 1,500 hours.\n- Gate C: passed when the applicant has been employed for in excess of twelve months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Marrowby Bakery Family Leave, which outcome does the application submitted by Jiro Ivanova get?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "q5d96eca39c",
  "kind": "choice",
  "text": "desk: community help\ncase: CASE-07098\ncaseworker: Jamie Jorgensen\nabout: Farid Robinson\n\nFacts for Farid Robinson (2027):\n- gross monthly income: 3,785.01 USD\n- net monthly income: 3,529.43 USD\n- countable assets: 11,390.69 USD\n- time in the service area: 6 months\n- age: 81 years\n- enrolled in: Lindermoor Bike Hire",
  "question": "Corvane Transit Fare Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or below the level of 3,785.00 USD.\n- Gate B: passed when the applicant's age is equal to or above 59 years.\n- Gate C: passed when countable assets are 10,250.00 USD at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Farid Robinson to Corvane Transit Fare Discount receive?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Eligible",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q5f3ccba0e2",
  "kind": "yes/no",
  "text": "Facts for Tomas Kowalski (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,250.17 |\n| net monthly income | $1,546.55 |\n| countable assets | $9,891.23 |\n| time in the service area | 52 months |\n| age | 49 years |\n| enrolled in | Morvane Carers Pension |\n\nreference: CASE-89842\nhandled_by: Toni Lazar\nabout: Tomas Kowalski\nunit: casework",
  "question": "Under these rules, is Tomas Kowalski plainly not eligible for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 61 years or more.\n- Gate B: passed when countable assets are at or under the amount of $7,300.00.\n- Gate C: passed when net monthly income is $2,025.00 at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3baa5e8063",
  "kind": "choice",
  "text": "Records office ticket: CR-03370\nRaised by: Nika Hernandez\nAbout: Elif\n\nPeople who asked to claim Elif (2025):\n| person | relationship to Elif | months lived with Elif | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Yara Gordon | aunt | seven months | $63,931 | yes |\n| Mirela Nguyen | mother | twelve months | $63,931 | no |",
  "question": "Caddowen Harbour Family Allowance rules for 2025: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for in excess of seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Elif lived for more months comes first.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Elif for Caddowen Harbour Family Allowance?",
  "options": [
   "Nobody may claim the child",
   "Yara Gordon",
   "Mirela Nguyen"
  ]
 },
 {
  "qid": "qc13298fec6",
  "kind": "yes/no",
  "text": "Facts for Tomi Evans (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,980.01 |\n| net monthly income | $1,476.80 |\n| countable assets | $9,111.46 |\n| time in the service area | 47 months |\n| age | 59 years |\n| enrolled in | none |\n\nTeo Quintero: cheers, the staff support desk has CASE-08185 for Tomi Evans.",
  "question": "According to these rules, is Tomi Evans ineligible for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is $2,890.00 at the most.\n- Gate B: passed when gross monthly income is strictly lower than $3,980.00.\n- Gate C: passed when the applicant's age is larger than 58 years.\n- Gate D: passed when countable assets are strictly beneath $9,350.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd7321b9fda",
  "kind": "choice",
  "text": "Service intake form\nCase reference: CASE-77044\nCaseworker: Alex Lindgren\nAbout: Cyril Halvorsen\n\nIntake interview with Cyril Halvorsen (2025):\nCaseworker: Gross monthly income?\nCyril Halvorsen: $1,261.88.\nCaseworker: Net monthly income?\nCyril Halvorsen: $1,099.08.\nCaseworker: Countable assets?\nCyril Halvorsen: $4,688.90.\nCaseworker: Time in the service area?\nCyril Halvorsen: 1 month.\nCaseworker: Age?\nCyril Halvorsen: 64 years.\nCaseworker: Other programme enrolled in?\nCyril Halvorsen: Tallowmere Roof Grant.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is lower than $2,670.\n- Gate B: passed when the applicant's age is strictly greater than 64 years.\n- Gate C: passed when the applicant has lived in the service area for above 4 months.\n- Route: an applicant enrolled in Tallowmere Roof Grant skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Cyril Halvorsen to Ostermere Delta Flood Repair Support get?",
  "options": [
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Not eligible: Gate B is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "qc3356476b6",
  "kind": "choice",
  "text": "{\"ref\": \"HR-07805\", \"caseworker\": \"Dani Ishikawa\", \"about\": \"Ari Okafor\"}\n\nFacts for Ari Okafor (2025), as JSON:\n{\"time_employed\": \"21 months\", \"hours_worked_in_the_past_year\": \"1594 hours\", \"employees_at_the_worksite\": \"114 employees\", \"gross_annual_pay\": \"$47,071.96\", \"take-home_annual_pay\": \"$40,499.99\", \"enrolled_in\": \"Fallowden Retraining Bursary\"}",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly lower than $40,500.\n- Gate B: passed when the applicant has been employed for 22 months or above.\n- Route: an applicant enrolled in Dorrane Parental Leave skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Ari Okafor to Tovardine Seed Caregiver Leave receive?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible"
  ]
 },
 {
  "qid": "q0aff9b0fdf",
  "kind": "yes/no",
  "text": "[walk_in_centre] case=HR-84476 about=Dmitri Ramirez\n[note] thanks_for_visiting caseworker=Ren Dvorak\n\nFacts for Dmitri Ramirez (2025):\n| fact | value |\n| --- | --- |\n| time employed | 15 months |\n| hours worked in the past year | 885 hours |\n| employees at the worksite | 42 employees |\n| gross annual pay | 73,078.70 USD |\n| take-home annual pay | 47,658.72 USD |\n| enrolled in | Dunnamore Retraining Bonus |",
  "question": "Following the listed rules, does Dmitri Ramirez qualify for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or above 41 employees.\n- Gate B: passed when hours worked in the past year are over 870 hours.\n- Gate C: passed when take-home annual pay is strictly beneath $60,500.\n- Gate D: passed when the applicant has been employed for at or beyond 14 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q073c21541e",
  "kind": "choice",
  "text": "district_ref: CR-99207\nhandled_by: Jamie Jorgensen\nabout: Otto\n\nPeople who asked to claim Otto (2025):\n- Mateo Kowalski: relationship to Otto: grandfather; months lived with Otto: 8 months; annual income: $41,681.00; filed a claim: yes\n- Jakub Patterson: relationship to Otto: grandfather; months lived with Otto: 8 months; annual income: $59,973.00; filed a claim: yes\n- Ibrahim Sharma: relationship to Otto: father; months lived with Otto: 7 months; annual income: $59,973.00; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Otto.\n- Only one person may claim Otto. Work through these steps in order.\n- Step one: only people who filed a claim for Otto are considered.\n- Step two: of those, only people with whom Otto lived for at or over 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Otto lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Otto.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Otto for Corrowby Family Supplement under these rules?",
  "options": [
   "Jakub Patterson",
   "Mateo Kowalski"
  ]
 },
 {
  "qid": "q76625d5858",
  "kind": "choice",
  "text": "Facts for Yuki Dragic (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,587.37 USD |\n| net monthly income | 2,648.90 USD |\n| countable assets | 9,235.94 USD |\n| time in the service area | 20 months |\n| age | 19 years |\n| enrolled in | Morvane Carers Pension |\n\nRoutine desk intake record\nCase reference: CASE-08572\nHandled by: Tomi Eklund\nAbout: Yuki Dragic",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or under the amount of $11,600.\n- Gate B: passed when net monthly income is smaller than $3,025.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Yuki Dragic to Wyndholm Forest Fuel Support receive?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate A is the reason (countable assets)"
  ]
 },
 {
  "qid": "qfaa26b6ec4",
  "kind": "choice",
  "text": "case: CR-57539\nhub: support\ncaseworker: Lior Grigoryan\nabout: Zara\n\nPeople who asked to claim Zara (2027):\n- Mariam Sharma: relationship to Zara: aunt; months lived with Zara: 9 months; annual income: $48,901.34; filed a claim: yes\n- Idris Nguyen: relationship to Zara: uncle; months lived with Zara: 2 months; annual income: $51,123.24; filed a claim: yes\n- Viktor Tesfaye: relationship to Zara: father; months lived with Zara: 11 months; annual income: $41,999.86; filed a claim: yes",
  "question": "Ferrowby Forest Credit rules for 2027: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for 7 months or more in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Zara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Zara for Ferrowby Forest Credit?",
  "options": [
   "Idris Nguyen",
   "Viktor Tesfaye"
  ]
 },
 {
  "qid": "qdb95cf9ffa",
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
  "qid": "qefcc33180b",
  "kind": "choice",
  "text": "Walk-in sheet\nCase: CR-69481\nCaseworker: Kazu Yousef\nAbout: Kira\n\nPeople who asked to claim Kira (2025):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Farid Robinson | uncle | seven months | $79,791.58 | yes |\n| Ravi Iyer | uncle | eleven months | $61,516.00 | no |\n| Zofia Kimura | aunt | seven months | $61,516.00 | no |",
  "question": "Caddowen Harbour Family Allowance rules for 2025: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for at or over seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kira lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, may claim Kira for Caddowen Harbour Family Allowance?",
  "options": [
   "Nobody may claim the child",
   "Farid Robinson",
   "Ravi Iyer"
  ]
 },
 {
  "qid": "q17020ca407",
  "kind": "yes/no",
  "text": "[casework_team] ref=CASE-61962 caseworker=Lior Grigoryan about=Ingrid Abara\n\nIntake interview with Ingrid Abara (2027):\nCaseworker: Gross monthly income?\nIngrid Abara: $2,132.76.\nCaseworker: Net monthly income?\nIngrid Abara: $1,659.97.\nCaseworker: Countable assets?\nIngrid Abara: $7,129.11.\nCaseworker: Time in the service area?\nIngrid Abara: 54 months.\nCaseworker: Age?\nIngrid Abara: 70 years.\nCaseworker: Other programme enrolled in?\nIngrid Abara: Aldervale Meal Ticket.",
  "question": "According to these rules, is Ingrid Abara not eligible for Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly under $1,400.00.\n- Gate B: passed when the applicant's age is 58 years or greater.\n- Gate C: passed when countable assets are $4,950.00 or under.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qbe84cbd01d",
  "kind": "choice",
  "text": "[review_desk] case=HR-74951 caseworker=Jules Shrestha\n[about] subject=Juliana Nakamura thanks_for_patience\n\nIntake interview with Juliana Nakamura (2026):\nCaseworker: Time employed?\nJuliana Nakamura: 94 months.\nCaseworker: Hours worked in the past year?\nJuliana Nakamura: 422 hours.\nCaseworker: Employees at your worksite?\nJuliana Nakamura: 41 employees.\nCaseworker: Gross annual pay?\nJuliana Nakamura: $45,821.19.\nCaseworker: Take-home annual pay?\nJuliana Nakamura: $32,499.99.\nCaseworker: Other programme enrolled in?\nJuliana Nakamura: Quelmere Lunch Card.",
  "question": "Sorrelby Child Care Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has in excess of 41 employees.\n- Gate B: passed when take-home annual pay is smaller than $32,500.\n- Gate C: passed when hours worked in the past year are above 780 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Juliana Nakamura to Sorrelby Child Care Support get under these rules?",
  "options": [
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "qbe19b6c319",
  "kind": "yes/no",
  "text": "team: casework\ncase: HR-23882\ncaseworker: Kazu Yousef\nabout: Sofia Ueda\n\nFacts for Sofia Ueda (2026):\n- time employed: 14 months\n- hours worked in the past year: 443 hours\n- employees at the worksite: 181 employees\n- gross annual pay: 93,488.66 USD\n- take-home annual pay: 70,778.68 USD\n- enrolled in: Pratchell Caregiver Allowance",
  "question": "According to these rules, does Sofia Ueda qualify for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are above 840 hours.\n- Gate B: passed when the applicant has been employed for equal to or greater than 17 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6b5641bff6",
  "kind": "choice",
  "text": "Hello Bao,\nQuick update: the staff support desk has CR-79678 in view.\nRegards, Shay Bekele\n\nInterview notes for Bao (2025):\nCaseworker: Waleed Fujimoto, your relation to Bao?\nWaleed Fujimoto: I am Bao's uncle.\nCaseworker: Months Bao lived with you?\nWaleed Fujimoto: 11 months.\nCaseworker: Annual income?\nWaleed Fujimoto: $67,538.00.\nCaseworker: Filed a claim for Bao?\nWaleed Fujimoto: yes.\nCaseworker: Kwame Esposito, your relation to Bao?\nKwame Esposito: I am Bao's uncle.\nCaseworker: Months Bao lived with you?\nKwame Esposito: 12 months.\nCaseworker: Annual income?\nKwame Esposito: $73,963.00.\nCaseworker: Filed a claim for Bao?\nKwame Esposito: no.\nCaseworker: Dagny Hakimi, your relation to Bao?\nDagny Hakimi: I am Bao's mother.\nCaseworker: Months Bao lived with you?\nDagny Hakimi: 12 months.\nCaseworker: Annual income?\nDagny Hakimi: $65,836.00.\nCaseworker: Filed a claim for Bao?\nDagny Hakimi: yes.",
  "question": "Sallowmere Family Payment rules for 2025: who may claim Bao.\n- Only one person may claim Bao. Work through these steps in order.\n- Step one: only people who filed a claim for Bao are considered.\n- Step two: of those, only people with whom Bao lived for strictly in excess of 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Bao lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Bao.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is allowed to claim Bao for Sallowmere Family Payment?",
  "options": [
   "Dagny Hakimi",
   "Waleed Fujimoto"
  ]
 },
 {
  "qid": "q93a77c7431",
  "kind": "choice",
  "text": "Hello there,\nA short update on file CASE-14843 for Amara Sorensen follows below.\nBest, Kendall Umarov\n\nIntake interview with Amara Sorensen (2026):\nCaseworker: Gross monthly income?\nAmara Sorensen: $3,210.34.\nCaseworker: Net monthly income?\nAmara Sorensen: $2,356.42.\nCaseworker: Countable assets?\nAmara Sorensen: $8,036.19.\nCaseworker: Time in the service area?\nAmara Sorensen: 6 months.\nCaseworker: Age?\nAmara Sorensen: 65 years.\nCaseworker: Other programme enrolled in?\nAmara Sorensen: Brindlemoor Repair Fund.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is over 64 years.\n- Gate B: passed when net monthly income is strictly below the amount of $2,165.00.\n- Gate C: passed when the applicant has lived in the service area for strictly greater than 7 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tamsfell Senior Home Support, which outcome does the application submitted by Amara Sorensen get?",
  "options": [
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "q5d78548439",
  "kind": "choice",
  "text": "{\"record\": \"case\", \"reference\": \"CR-27257\", \"caseworker\": \"Jules Shrestha\", \"about\": \"Pia\"}\n\nInterview notes for Pia (2025):\nCaseworker: Dmitri Wojcik, your relation to Pia?\nDmitri Wojcik: I am Pia's father.\nCaseworker: Months Pia lived with you?\nDmitri Wojcik: 8 months.\nCaseworker: Annual income?\nDmitri Wojcik: 85,812.00 USD.\nCaseworker: Filed a claim for Pia?\nDmitri Wojcik: no.\nCaseworker: Ingrid Hakimi, your relation to Pia?\nIngrid Hakimi: I am Pia's mother.\nCaseworker: Months Pia lived with you?\nIngrid Hakimi: 6 months.\nCaseworker: Annual income?\nIngrid Hakimi: 92,658.00 USD.\nCaseworker: Filed a claim for Pia?\nIngrid Hakimi: no.\nCaseworker: Kavita Jovanovic, your relation to Pia?\nKavita Jovanovic: I am Pia's aunt.\nCaseworker: Months Pia lived with you?\nKavita Jovanovic: 12 months.\nCaseworker: Annual income?\nKavita Jovanovic: 92,521.29 USD.\nCaseworker: Filed a claim for Pia?\nKavita Jovanovic: no.",
  "question": "Sallowmere Family Payment rules for 2025: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for at or above 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Pia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Pia for Sallowmere Family Payment under these rules?",
  "options": [
   "Nobody may claim the child",
   "Kavita Jovanovic",
   "Ingrid Hakimi"
  ]
 },
 {
  "qid": "q8f90d1f80b",
  "kind": "choice",
  "text": "{\"caseworker\": \"Blair Xiong\", \"about\": \"Mia\", \"case\": \"CR-68729\", \"office\": \"branch\"}\n\nPeople who asked to claim Mia (2026), as JSON:\n{\"people\": [{\"name\": \"Sergio Choi\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"47,040.00 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Greta Choi\", \"relationship\": \"mother\", \"months_lived_with_child\": \"seven months\", \"annual_income\": \"37,086.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Pavel Petrov\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"17,390.00 USD\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for strictly higher than six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Mia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Mia for Ferrowby Forest Credit?",
  "options": [
   "Pavel Petrov",
   "Greta Choi"
  ]
 },
 {
  "qid": "q9658157093",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Ami; the reference is CR-47812.\nKind regards, Kendall Umarov\n\nPeople who asked to claim Ami (2027):\n- Kofi Ferreira: relationship to Ami: uncle; months lived with Ami: five months; annual income: 48,617.00 USD; filed a claim: yes\n- Nikolai Sorensen: relationship to Ami: father; months lived with Ami: ten months; annual income: 21,400.33 USD; filed a claim: no\n- Yara Hamilton: relationship to Ami: mother; months lived with Ami: eight months; annual income: 22,990.00 USD; filed a claim: no",
  "question": "Is Yara Hamilton barred from claiming Ami for Tessenvale Valley Child Credit by the rules?",
  "definitions": "Tessenvale Valley Child Credit rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for a minimum of five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ami lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe863787dbf",
  "kind": "yes/no",
  "text": "Routine ticket: HR-83393\nRaised by: Remy Tran\nAbout: Idris Watson\n\nFacts for Idris Watson (2026):\n| fact | value |\n| --- | --- |\n| time employed | 7 months |\n| hours worked in the past year | 867 hours |\n| employees at the worksite | 175 employees |\n| gross annual pay | 84,093.63 USD |\n| take-home annual pay | 63,574.39 USD |\n| enrolled in | Idrane Tuition Bursary |",
  "question": "Does Idris Watson fail to qualify for admission to Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or above 6 months.\n- Gate B: passed when gross annual pay is strictly under the amount of 76,500.00 USD.\n- Route: an applicant enrolled in Idrane Tuition Grant skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd2e9617037",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CASE-04342\nRaised by: Teo Quintero\nAbout: Ari Ortega\n\nIntake interview with Ari Ortega (2027):\nCaseworker: Gross monthly income?\nAri Ortega: $1,356.63.\nCaseworker: Net monthly income?\nAri Ortega: $1,130.71.\nCaseworker: Countable assets?\nAri Ortega: $3,877.98.\nCaseworker: Time in the service area?\nAri Ortega: 13 months.\nCaseworker: Age?\nAri Ortega: 58 years.\nCaseworker: Other programme enrolled in?\nAri Ortega: Aldervale Meal Ticket.",
  "question": "For Tamsfell Senior Home Support, does Ari Ortega qualify by passing every gate that applies?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is in excess of 57 years.\n- Gate B: passed when net monthly income is smaller than $1,810.\n- Gate C: passed when the applicant has lived in the service area for 8 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qbfd89c37d9",
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
  "qid": "q49857a9dc8",
  "kind": "yes/no",
  "text": "Internal case note for CASE-84521.\nSet down by Jules Shrestha at the town hall office, for Anton Medina.\n\nIntake interview with Anton Medina (2026):\nCaseworker: Gross monthly income?\nAnton Medina: $3,193.42.\nCaseworker: Net monthly income?\nAnton Medina: $2,728.86.\nCaseworker: Countable assets?\nAnton Medina: $15,553.87.\nCaseworker: Time in the service area?\nAnton Medina: twelve months.\nCaseworker: Age?\nAnton Medina: eighteen years.\nCaseworker: Other programme enrolled in?\nAnton Medina: Lowmarsh Heating Loan.",
  "question": "Under these rules, is Anton Medina ineligible for Tamsfell Senior Home Support as a whole?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or beneath $2,885.00.\n- Gate B: passed when the applicant has lived in the service area for larger than six months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa8a6aed22c",
  "kind": "yes/no",
  "text": "Note for the intake desk: Waleed Begum is named on case CASE-84996, which Avery Obradovic keeps.\n\nFacts for Waleed Begum (2027):\n- gross monthly income: $2,210.08\n- net monthly income: $2,120.01\n- countable assets: $113.40\n- time in the service area: 6 months\n- age: 90 years\n- enrolled in: Hallowby Utility Supplement",
  "question": "According to these rules, does Waleed Begum qualify for Tesslow Prairie Water Bill Assistance?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly smaller than 2,120.02 USD.\n- Gate B: passed when gross monthly income is $2,735 at the most.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q60f0e5db31",
  "kind": "yes/no",
  "text": "Internal note: CASE-32745 is held by Remy Tran. Regarding Olena Kaur, please refer to the desk log.\n\nFacts for Olena Kaur (2027):\n- gross monthly income: 2,878.60 USD\n- net monthly income: 2,045.16 USD\n- countable assets: 12,827.98 USD\n- time in the service area: 54 months\n- age: 65 years\n- enrolled in: Vellmar Transit Pass",
  "question": "Does Olena Kaur meet the rules for Ostmere Lakeside Winter Energy Support by passing every gate that applies?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are lower than or equal to 9,450.00 USD.\n- Gate B: passed when the applicant's age is at or greater than 66 years.\n- Route: an applicant enrolled in Vellmar Transit Pass skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6b6352dc2b",
  "kind": "yes/no",
  "text": "Facts for Dario Douglas (2026):\n| fact | value |\n| --- | --- |\n| time employed | 50 months |\n| hours worked in the past year | 1,351 hours |\n| employees at the worksite | 75 employees |\n| gross annual pay | 64,500.01 USD |\n| take-home annual pay | 59,678.17 USD |\n| enrolled in | Tesslow Engineering Internship |\n\nHi Dario Douglas,\nThis is a quick note on case HR-43484 from the records office.\nCheers, Alex Lindgren",
  "question": "Does a gate that applies stop the application of Dario Douglas to Drummock Robotics Workshop Training Fund under these rules?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or below the level of 54,500.00 USD.\n- Gate B: passed when the worksite has strictly over 74 employees.\n- Gate C: passed when gross annual pay is at or below 64,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb824777c26",
  "kind": "yes/no",
  "text": "Ticket: branch office, case HR-62296\nRaised by: Remy Tran\nAbout: Matias Ilunga\n\nIntake interview with Matias Ilunga (2025):\nCaseworker: Time employed?\nMatias Ilunga: 76 months.\nCaseworker: Hours worked in the past year?\nMatias Ilunga: 1349 hours.\nCaseworker: Employees at your worksite?\nMatias Ilunga: 43 employees.\nCaseworker: Gross annual pay?\nMatias Ilunga: 69,953.96 USD.\nCaseworker: Take-home annual pay?\nMatias Ilunga: 53,999.99 USD.\nCaseworker: Other programme enrolled in?\nMatias Ilunga: Ivormoor Shift Supplement.",
  "question": "Is Matias Ilunga eligible for Sorrelby Child Care Support with every applicable gate passed?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly greater than 42 employees.\n- Gate B: passed when take-home annual pay is strictly smaller than 54,000.00 USD.\n- Gate C: passed when hours worked in the past year are strictly higher than 790 hours.\n- Route: an applicant enrolled in Ivormoor Shift Supplement skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q02d8f5c378",
  "kind": "choice",
  "text": "file: CR-50474\nsupport: Quinn Pavlenko\nabout: Kira\nmood: kind\n\nPeople who asked to claim Kira (2026):\n- Hana Demir: relationship to Kira: grandmother; months lived with Kira: five months; annual income: $19,023; filed a claim: yes\n- Ubah Jovanovic: relationship to Kira: grandmother; months lived with Kira: twelve months; annual income: $83,628; filed a claim: yes\n- Ilse Castellano: relationship to Kira: mother; months lived with Kira: eight months; annual income: $17,048; filed a claim: yes",
  "question": "Dunmarrow Hill Allowance rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for seven months or greater in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Kira lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole person entitled to claim Kira for Dunmarrow Hill Allowance?",
  "options": [
   "Ubah Jovanovic",
   "Hana Demir",
   "Ilse Castellano"
  ]
 },
 {
  "qid": "q4664192fb4",
  "kind": "yes/no",
  "text": "Kendall Umarov: quick check on file CASE-63813 for Xenia Mwangi, at the counter.\n\nFacts for Xenia Mwangi (2025):\n- gross monthly income: 2,732.51 USD\n- net monthly income: 1,707.63 USD\n- countable assets: 9,800.01 USD\n- time in the service area: 2 months\n- age: 56 years\n- enrolled in: Hallowby Utility Discount",
  "question": "For Tesslow Prairie Water Bill Assistance, does Xenia Mwangi qualify by passing every gate that applies?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are lower than 9,800.00 USD.\n- Gate B: passed when the applicant's age is at or above 57 years.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qcc972e7e54",
  "kind": "yes/no",
  "text": "People who asked to claim Ivan (2026):\n| person | relationship to Ivan | months lived with Ivan | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dmitri Ilic | father | 5 months | 70,732.00 USD | yes |\n| Bianca Douglas | mother | 9 months | 43,768.32 USD | yes |\n\nNika Hernandez: for the record, file CR-41808 belongs to Ivan.",
  "question": "Is Dmitri Ilic the person who comes out with the right to claim Ivan for Mollenby Canal Child Supplement?",
  "definitions": "Mollenby Canal Child Supplement rules for 2026: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for 6 months or greater in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc270db3831",
  "kind": "yes/no",
  "text": "Hi Felix Yamazaki,\nThis is a quick note on case CASE-33701 from the records office.\nCheers, Ezra Rosales\n\nFacts for Felix Yamazaki (2026):\n- gross monthly income: $3,554.99\n- net monthly income: $3,099.43\n- countable assets: $1,273.99\n- time in the service area: seven months\n- age: 68 years\n- enrolled in: Crannock Food Parcel",
  "question": "Under these rules, is Felix Yamazaki ineligible for Ostmere Lakeside Winter Energy Support as a whole?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or less than $3,555.00.\n- Gate B: passed when the applicant's age is higher than 67 years.\n- Gate C: passed when the applicant has lived in the service area for strictly over six months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd8d5c735e2",
  "kind": "yes/no",
  "text": "Dear Amir,\nPlease find CR-17085 logged with the help line team.\nYours faithfully, Jamie Jorgensen\n\nPeople who asked to claim Amir (2025):\n- Kiara Demir: relationship to Amir: mother; months lived with Amir: 6 months; annual income: $62,253; filed a claim: no\n- Ingrid Sullivan: relationship to Amir: aunt; months lived with Amir: 12 months; annual income: $35,836.71; filed a claim: yes\n- Oskar Ilunga: relationship to Amir: father; months lived with Amir: 9 months; annual income: $39,371.62; filed a claim: yes",
  "question": "Does Oskar Ilunga end up as the sole person who may claim Amir for Caddowen Harbour Family Allowance?",
  "definitions": "Caddowen Harbour Family Allowance rules for 2025: who may claim Amir.\n- Only one person may claim Amir. Work through these steps in order.\n- Step one: only people who filed a claim for Amir are considered.\n- Step two: of those, only people with whom Amir lived for equal to or above 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Amir lived for more months comes first.\n- If nobody is left after step two, nobody may claim Amir.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q70b3349569",
  "kind": "yes/no",
  "text": "[casework_team] case_id=CASE-35327\n[casework_team] worker=Quinn Pavlenko about=Sabine Hamilton\n\nFacts for Sabine Hamilton (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,121.81 USD |\n| net monthly income | 2,699.99 USD |\n| countable assets | 11,476.44 USD |\n| time in the service area | 5 months |\n| age | 22 years |\n| enrolled in | Stennet Commuter Pass |",
  "question": "Under these rules, does Sabine Hamilton meet the rules for Corvane Transit Fare Discount across every applicable gate?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly smaller than 2,700.00 USD.\n- Gate B: passed when the applicant has lived in the service area for at or above 4 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q28f18af474",
  "kind": "yes/no",
  "text": "ref: CR-02322\nlead: Remy Tran\nfor: Ines\n\nInterview notes for Ines (2026):\nCaseworker: Kiara Sharma, your relation to Ines?\nKiara Sharma: I am Ines's aunt.\nCaseworker: Months Ines lived with you?\nKiara Sharma: seven months.\nCaseworker: Annual income?\nKiara Sharma: $69,442.88.\nCaseworker: Filed a claim for Ines?\nKiara Sharma: yes.\nCaseworker: Nadia Ortega, your relation to Ines?\nNadia Ortega: I am Ines's mother.\nCaseworker: Months Ines lived with you?\nNadia Ortega: ten months.\nCaseworker: Annual income?\nNadia Ortega: $45,403.00.\nCaseworker: Filed a claim for Ines?\nNadia Ortega: yes.",
  "question": "Following the listed rules, does Kiara Sharma fail to win the right to claim Ines for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2026: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for equal to or greater than seven months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ines lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q60c83ddd99",
  "kind": "choice",
  "text": "Internal note: Morgan Mendoza handles case CASE-92319 about Sabine Yamazaki.\n\nFacts for Sabine Yamazaki (2026):\n- gross monthly income: $3,301.20\n- net monthly income: $2,393.77\n- countable assets: $616.76\n- time in the service area: one month\n- age: 84 years\n- enrolled in: Sorrenby Tenancy Deposit Loan",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than 62 years.\n- Gate B: passed when the applicant has lived in the service area for at or above three months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Sabine Yamazaki to Tesslow Prairie Water Bill Assistance receive?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "q621812477f",
  "kind": "choice",
  "text": "Dear Luca,\nThis reply concerns case CR-82563.\nYours sincerely, Mika Zamora\n\nPeople who asked to claim Luca (2027):\n- Rania Medina: relationship to Luca: mother; months lived with Luca: 7 months; annual income: $31,931.71; filed a claim: no\n- Oskar Kovacs: relationship to Luca: father; months lived with Luca: 0 months; annual income: $31,931.71; filed a claim: yes\n- Amara Sokolov: relationship to Luca: aunt; months lived with Luca: 9 months; annual income: $61,465.81; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Luca.\n- Only one person may claim Luca. Work through these steps in order.\n- Step one: only people who filed a claim for Luca are considered.\n- Step two: of those, only people with whom Luca lived for strictly more than 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Luca lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Luca.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, has the right to claim Luca for Ostrowan Prairie Grant?",
  "options": [
   "Rania Medina",
   "Oskar Kovacs",
   "Amara Sokolov"
  ]
 },
 {
  "qid": "qe6be32ad3f",
  "kind": "yes/no",
  "text": "team: casework\ncase: HR-80052\ncaseworker: Remy Tran\nabout: Ren Gutierrez\n\nIntake interview with Ren Gutierrez (2027):\nCaseworker: Time employed?\nRen Gutierrez: 100 months.\nCaseworker: Hours worked in the past year?\nRen Gutierrez: 716 hours.\nCaseworker: Employees at your worksite?\nRen Gutierrez: 272 employees.\nCaseworker: Gross annual pay?\nRen Gutierrez: $65,221.60.\nCaseworker: Take-home annual pay?\nRen Gutierrez: $55,716.51.\nCaseworker: Other programme enrolled in?\nRen Gutierrez: none.",
  "question": "Under these rules, does a gate that applies end the application of Ren Gutierrez to Brenwold Timber Apprentice Support?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly more than 700 hours.\n- Gate B: passed when gross annual pay is equal to or below $66,000.00.\n- Route: an applicant enrolled in Wendle Trade Pathway skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qae9fcc2143",
  "kind": "yes/no",
  "text": "{\"case\": \"HR-91771\", \"about\": \"Quentin Ruiz\", \"caseworker\": \"Tomi Eklund\", \"service\": \"regional\"}\n\nFacts for Quentin Ruiz (2026), as JSON:\n{\"time_employed\": \"22 months\", \"hours_worked_in_the_past_year\": \"1749 hours\", \"employees_at_the_worksite\": \"59 employees\", \"gross_annual_pay\": \"$22,855.57\", \"take-home_annual_pay\": \"$18,217.54\", \"enrolled_in\": \"Lumenfold Skills Voucher\"}",
  "question": "Going by the listed rules, is Quentin Ruiz eligible for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than or equal to $22,000.00.\n- Gate B: passed when the applicant has been employed for 23 months at minimum.\n- Gate C: passed when the worksite has over 59 employees.\n- Route: an applicant enrolled in Lumenfold Skills Voucher skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0e8795940a",
  "kind": "yes/no",
  "text": "file: CR-51262\nsupport: Kendall Umarov\nabout: Ezra\nmood: kind\n\nPeople who asked to claim Ezra (2027):\n- Imani Halvorsen: relationship to Ezra: grandmother; months lived with Ezra: 0 months; annual income: 29,006.00 USD; filed a claim: yes\n- Rafael Zielinski: relationship to Ezra: uncle; months lived with Ezra: 0 months; annual income: 49,181.00 USD; filed a claim: yes\n- Waleed Choi: relationship to Ezra: father; months lived with Ezra: 3 months; annual income: 54,068.00 USD; filed a claim: yes",
  "question": "According to these rules, is Waleed Choi the person who ends up with the right to claim Ezra for Ostrowan Prairie Grant?",
  "definitions": "Ostrowan Prairie Grant rules for 2027: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for over 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ezra lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q44f97eee61",
  "kind": "choice",
  "text": "desk: community help\ncase: CR-03419\ncaseworker: Kiran Morales\nabout: Remi\n\nInterview notes for Remi (2025):\nCaseworker: Nkechi Mwangi, your relation to Remi?\nNkechi Mwangi: I am Remi's mother.\nCaseworker: Months Remi lived with you?\nNkechi Mwangi: 6 months.\nCaseworker: Annual income?\nNkechi Mwangi: $32,599.46.\nCaseworker: Filed a claim for Remi?\nNkechi Mwangi: yes.\nCaseworker: Aiko Mitchell, your relation to Remi?\nAiko Mitchell: I am Remi's aunt.\nCaseworker: Months Remi lived with you?\nAiko Mitchell: 3 months.\nCaseworker: Annual income?\nAiko Mitchell: $18,888.\nCaseworker: Filed a claim for Remi?\nAiko Mitchell: yes.\nCaseworker: Ugo Jovanovic, your relation to Remi?\nUgo Jovanovic: I am Remi's grandfather.\nCaseworker: Months Remi lived with you?\nUgo Jovanovic: 2 months.\nCaseworker: Annual income?\nUgo Jovanovic: $80,553.\nCaseworker: Filed a claim for Remi?\nUgo Jovanovic: yes.",
  "question": "Gristmere Child Credit rules for 2025: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for at or above 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Remi lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, gets to claim Remi for Gristmere Child Credit under these rules?",
  "options": [
   "Ugo Jovanovic",
   "Nobody may claim the child",
   "Nkechi Mwangi"
  ]
 },
 {
  "qid": "qe9fd30a539",
  "kind": "yes/no",
  "text": "People services intake form\nCase reference: CASE-42615\nCaseworker: Kiran Morales\nRegarding: Sabine Haddad\n\nFacts for Sabine Haddad (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,097.76 USD |\n| net monthly income | 1,425.80 USD |\n| countable assets | 3,397.01 USD |\n| time in the service area | 6 months |\n| age | 65 years |\n| enrolled in | Velgate Pantry Coupon |",
  "question": "Going by the listed rules, is Sabine Haddad eligible for Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or below $2,760.\n- Gate B: passed when countable assets are strictly beneath $3,350.\n- Gate C: passed when the applicant has lived in the service area for strictly in excess of 5 months.\n- Route: an applicant enrolled in Hemmerly Nursery Place Fund skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q27990f89ff",
  "kind": "choice",
  "text": "Facts for Kazu Haddad (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,036.85 |\n| net monthly income | $3,035.00 |\n| countable assets | $14,054.73 |\n| time in the service area | 5 months |\n| age | 18 years |\n| enrolled in | Morvane Carers Allowance |\n\nFront counter ticket: CASE-22649\nWarm hello from: Yuki Adeyemi\nPerson: Kazu Haddad",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is smaller than $3,035.00.\n- Gate B: passed when the applicant has lived in the service area for greater than 7 months.\n- Gate C: passed when countable assets are strictly under the value of $9,050.00.\n- Route: an applicant enrolled in Morvane Carers Allowance skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which result comes from the application of Kazu Haddad to Wyndholm Forest Fuel Support?",
  "options": [
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q508e4ef823",
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
  "qid": "q6fd6845557",
  "kind": "choice",
  "text": "Ref: CR-30442\nAbout: Elif\nRaised by: Sami Castro\n\nPeople who asked to claim Elif (2026):\n| person | relationship to Elif | months lived with Elif | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ivo Sokolov | uncle | 8 months | $60,033.00 | no |\n| Yusuf Mitchell | uncle | 8 months | $92,279.00 | no |\n| Hugo Moreau | father | 12 months | $18,240.00 | yes |\n| Priya Yilmaz | aunt | 8 months | $73,439.00 | yes |",
  "question": "Caddowen Harbour Family Allowance rules for 2026: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for at or above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Elif lived for more months comes first.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which candidate, if any, may claim Elif for Caddowen Harbour Family Allowance?",
  "options": [
   "Hugo Moreau",
   "Priya Yilmaz"
  ]
 },
 {
  "qid": "qa8d7da6204",
  "kind": "choice",
  "text": "case_id: HR-99317\nworker_name: Riley Watanabe\nsubject_name: Hugo Patterson\n\nFacts for Hugo Patterson (2027):\n- time employed: nineteen months\n- hours worked in the past year: 1,457 hours\n- employees at the worksite: 34 employees\n- gross annual pay: 100,229.16 USD\n- take-home annual pay: 68,434.79 USD\n- enrolled in: Lumenfold Skills Credit",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has over 33 employees.\n- Gate B: passed when the applicant has been employed for greater than or equal to twenty months.\n- Gate C: passed when hours worked in the past year are at or greater than 910 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nConcerning Halvorne Shipyard Tuition Assistance, which outcome does the application by Hugo Patterson receive?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible"
  ]
 }
]
