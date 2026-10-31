# G5-H blind read T15-blind_read-aab9bbaf-000 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/pilot_i2/g5h/answers/T15-blind_read-aab9bbaf-000.json

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
  "qid": "q40479a877a",
  "kind": "yes/no",
  "text": "Dear Jakub Ueda,\nThis reply concerns case HR-96150.\nYours sincerely, Adi Chandra\n\nFacts for Jakub Ueda (2025):\n- time employed: 25 months\n- hours worked in the past year: 915 hours\n- employees at the worksite: 192 employees\n- gross annual pay: $85,499.99\n- take-home annual pay: $60,264.10\n- enrolled in: Corrowell Sabbatical Fund",
  "question": "Going by the listed rules, is Jakub Ueda ineligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or under the amount of $85,500.00.\n- Gate B: passed when the applicant has been employed for over 24 months.\n- Route: an applicant enrolled in Corrowell Sabbatical Fund skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qde8c037726",
  "kind": "choice",
  "text": "{\"case\": \"HR-60770\", \"caseworker\": \"Shay Bekele\", \"about\": \"Emi Evans\", \"line\": \"help\"}\n\nIntake interview with Emi Evans (2027):\nCaseworker: Time employed?\nEmi Evans: 51 months.\nCaseworker: Hours worked in the past year?\nEmi Evans: 1320 hours.\nCaseworker: Employees at your worksite?\nEmi Evans: 39 employees.\nCaseworker: Gross annual pay?\nEmi Evans: $25,462.73.\nCaseworker: Take-home annual pay?\nEmi Evans: $22,536.01.\nCaseworker: Other programme enrolled in?\nEmi Evans: Hendrove Nursery Discount.",
  "question": "Sorrelby Child Care Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly beneath $34,500.00.\n- Gate B: passed when the worksite has strictly in excess of 23 employees.\n- Gate C: passed when hours worked in the past year are a minimum of 1320 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Emi Evans to Sorrelby Child Care Support receive?",
  "options": [
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate C is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qa0659bddc6",
  "kind": "choice",
  "text": "Facts for Sabine Fujimoto (2025):\n| fact | value |\n| --- | --- |\n| time employed | 28 months |\n| hours worked in the past year | 2,282 hours |\n| employees at the worksite | 336 employees |\n| gross annual pay | $29,999.99 |\n| take-home annual pay | $24,000.01 |\n| enrolled in | Ostermere Respite Stay |\n\nDear colleague,\nThis is a short outreach note on case HR-78490 for Sabine Fujimoto.\nRegards, Nika Hernandez",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or above seventeen months.\n- Gate B: passed when take-home annual pay is strictly under $24,000.00.\n- Gate C: passed when gross annual pay is strictly under the value of $30,000.00.\n- Route: an applicant enrolled in Ostermere Respite Care skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Sabine Fujimoto to Pelmoor Ceramics Carer Support ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qbe4fea686e",
  "kind": "choice",
  "text": "Hi team,\nThis mail concerns file CASE-33063, which is about Tomas Lehmann.\nRegards, Ari Benali\n\nFacts for Tomas Lehmann (2025):\n- gross monthly income: 2,129.20 USD\n- net monthly income: 1,840.00 USD\n- countable assets: 15,664.75 USD\n- time in the service area: 22 months\n- age: 27 years\n- enrolled in: Pellbrook Heating Grant",
  "question": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or above 12 months.\n- Gate B: passed when gross monthly income is strictly smaller than 2,260.00 USD.\n- Gate C: passed when countable assets are lower than 10,600.00 USD.\n- Gate D: passed when net monthly income is lower than 1,840.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which result comes from the application of Tomas Lehmann to Tarrowick Food Basket Support?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate D is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (countable assets)"
  ]
 },
 {
  "qid": "q85c470737b",
  "kind": "yes/no",
  "text": "Facts for Kazu Medina (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,150.94 USD |\n| net monthly income | 2,566.99 USD |\n| countable assets | 12,597.83 USD |\n| time in the service area | 7 months |\n| age | 76 years |\n| enrolled in | Sallafell Bus Credit |\n\nTown hall intake header\nCase reference: CASE-39450\nCaseworker: Sasha Okonkwo\nAbout: Kazu Medina",
  "question": "For Tollsey Island Ferry Discount, does Kazu Medina qualify by passing every gate that applies?",
  "definitions": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is lower than or equal to 3,240.00 USD.\n- Gate B: passed when the applicant has lived in the service area for 4 months at minimum.\n- Gate C: passed when the applicant's age is a minimum of 64 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8c0b2ed47f",
  "kind": "yes/no",
  "text": "ref: CR-19674\nhandler: Blair Xiong\nsubject: Omar\n\nInterview notes for Omar (2027):\nCaseworker: Dario Mwangi, your relation to Omar?\nDario Mwangi: I am Omar's father.\nCaseworker: Months Omar lived with you?\nDario Mwangi: 2 months.\nCaseworker: Annual income?\nDario Mwangi: 69,448.00 USD.\nCaseworker: Filed a claim for Omar?\nDario Mwangi: no.\nCaseworker: Amara Russell, your relation to Omar?\nAmara Russell: I am Omar's grandmother.\nCaseworker: Months Omar lived with you?\nAmara Russell: 12 months.\nCaseworker: Annual income?\nAmara Russell: 73,151.63 USD.\nCaseworker: Filed a claim for Omar?\nAmara Russell: yes.\nCaseworker: Vesna Becker, your relation to Omar?\nVesna Becker: I am Omar's mother.\nCaseworker: Months Omar lived with you?\nVesna Becker: 10 months.\nCaseworker: Annual income?\nVesna Becker: 90,988.00 USD.\nCaseworker: Filed a claim for Omar?\nVesna Becker: yes.",
  "question": "Under these rules, is Vesna Becker excluded from claiming Omar for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for 7 months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4cc63fefd2",
  "kind": "choice",
  "text": "A quick note for the district team: Kazu Yousef is taking care of HR-90498 for Hugo Okoro.\n\nFacts for Hugo Okoro (2027):\n- time employed: 65 months\n- hours worked in the past year: 1,052 hours\n- employees at the worksite: 135 employees\n- gross annual pay: $28,477.46\n- take-home annual pay: $25,500.00\n- enrolled in: Pratchell Caregiver Allowance",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or beyond 820 hours.\n- Gate B: passed when take-home annual pay is strictly under the value of $25,500.00.\n- Route: an applicant enrolled in Pratchell Caregiver Allowance skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Hugo Okoro to Wendmoor Mill Parental Leave receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q02d460bf2c",
  "kind": "choice",
  "text": "Hello Kofi Ramirez,\nQuick update: the staff support desk has HR-68144 in view.\nRegards, Riley Watanabe\n\nIntake interview with Kofi Ramirez (2026):\nCaseworker: Time employed?\nKofi Ramirez: 59 months.\nCaseworker: Hours worked in the past year?\nKofi Ramirez: 409 hours.\nCaseworker: Employees at your worksite?\nKofi Ramirez: 61 employees.\nCaseworker: Gross annual pay?\nKofi Ramirez: 86,499.99 USD.\nCaseworker: Take-home annual pay?\nKofi Ramirez: 72,233.31 USD.\nCaseworker: Other programme enrolled in?\nKofi Ramirez: Myrren Study Grant.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 66 employees or greater.\n- Gate B: passed when gross annual pay is at or less than $86,500.\n- Gate C: passed when hours worked in the past year are greater than or equal to 1140 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Kofi Ramirez on the application to Quenhollow Brewery Bereavement Leave?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate C is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q3e3b51c06d",
  "kind": "yes/no",
  "text": "People who asked to claim Gia (2026):\n| person | relationship to Gia | months lived with Gia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kofi Petrov | uncle | 10 months | $35,617.24 | yes |\n| Hamid Choi | father | 0 months | $51,356.00 | yes |\n| Ravi Watson | grandfather | 12 months | $35,617.24 | yes |\n\n[casework_team] ref=CR-70531 caseworker=Morgan Mendoza about=Gia",
  "question": "For Sorrenby Island Family Payment, is Hamid Choi barred from claiming Gia under the listed rules?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for at or greater than 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Gia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q39e62a375b",
  "kind": "choice",
  "text": "Quick intake form\nCase reference: HR-84946\nCaseworker: Morgan Mendoza\nAbout: Jelena Iyer\n\nFacts for Jelena Iyer (2027):\n| fact | value |\n| --- | --- |\n| time employed | 12 months |\n| hours worked in the past year | 2000 hours |\n| employees at the worksite | 37 employees |\n| gross annual pay | 35,500.01 USD |\n| take-home annual pay | 33,007.39 USD |\n| enrolled in | Selwick Fresh Box |",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is 35,500.00 USD or under.\n- Gate B: passed when the worksite has greater than or equal to 37 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what result does the application of Jelena Iyer to Marrowby Bakery Family Leave produce?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "qddb9895b53",
  "kind": "yes/no",
  "text": "Records desk note. Nika Hernandez keeps HR-91668, which concerns Yasmin Johnson.\n\nFacts for Yasmin Johnson (2026):\n- time employed: 80 months\n- hours worked in the past year: 1,533 hours\n- employees at the worksite: 130 employees\n- gross annual pay: 47,610.95 USD\n- take-home annual pay: 33,500.01 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "For Morrowdene Hospital Group Return Support, does Yasmin Johnson fail to qualify under these rules?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are over 1,290 hours.\n- Gate B: passed when take-home annual pay is at or below $33,500.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q371498dc3d",
  "kind": "yes/no",
  "text": "[case_log] staff_support_desk case=HR-76487 caseworker=Blair Xiong about=Jiro Ilunga\n\nIntake interview with Jiro Ilunga (2025):\nCaseworker: Time employed?\nJiro Ilunga: 21 months.\nCaseworker: Hours worked in the past year?\nJiro Ilunga: 2015 hours.\nCaseworker: Employees at your worksite?\nJiro Ilunga: 326 employees.\nCaseworker: Gross annual pay?\nJiro Ilunga: 56,046.78 USD.\nCaseworker: Take-home annual pay?\nJiro Ilunga: 36,625.95 USD.\nCaseworker: Other programme enrolled in?\nJiro Ilunga: Quelmere Lunch Card.",
  "question": "Does Jiro Ilunga fully qualify for Sorrelby Child Care Support under these rules?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are 1480 hours or greater.\n- Gate B: passed when gross annual pay is at or under the amount of $37,000.\n- Gate C: passed when the applicant has been employed for 11 months or above.\n- Route: an applicant enrolled in Quelmere Lunch Card skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc8b6787606",
  "kind": "choice",
  "text": "Hello,\nHere is the write-up for CASE-84106 about Amara Gashi.\nWith thanks, Kazu Yousef\n\nFacts for Amara Gashi (2026):\n- gross monthly income: 2,381.77 USD\n- net monthly income: 1,968.94 USD\n- countable assets: 5,727.22 USD\n- time in the service area: 12 months\n- age: 48 years\n- enrolled in: Vellmar Transit Pass",
  "question": "Ostmere Lakeside Winter Energy Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or less than 5,650.00 USD.\n- Gate B: passed when the applicant has lived in the service area for strictly higher than 8 months.\n- Gate C: passed when gross monthly income is at or below the level of 2,275.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which outcome does the application of Amara Gashi to Ostmere Lakeside Winter Energy Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qba31e8b40b",
  "kind": "choice",
  "text": "district_ref: HR-45230\nhandled_by: Kazu Yousef\nabout: Ivo Yamazaki\n\nFacts for Ivo Yamazaki (2027):\n- time employed: thirteen months\n- hours worked in the past year: 1649 hours\n- employees at the worksite: 225 employees\n- gross annual pay: $113,395.81\n- take-home annual pay: $97,351.95\n- enrolled in: Caddowen Veterans Pathway",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly below the amount of $77,000.00.\n- Gate B: passed when the applicant has been employed for ten months or more.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Ivo Yamazaki to Morrowdene Hospital Group Return Support receive?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "q03dfdfdd18",
  "kind": "choice",
  "text": "Facts for Waleed Gutierrez (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,425.01 |\n| net monthly income | $3,340.01 |\n| countable assets | $6,899.99 |\n| time in the service area | 41 months |\n| age | 64 years |\n| enrolled in | Velden Transit Pass |\n\nHi Waleed Gutierrez,\nYour case CASE-33448 is being reviewed with care.\nKind thanks, Quinn Pavlenko",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly greater than 63 years.\n- Gate B: passed when gross monthly income is strictly under $3,425.\n- Gate C: passed when countable assets are strictly beneath $6,900.\n- Route: an applicant enrolled in Velden Transit Pass skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Waleed Gutierrez to Sallowick Ward Home Repair Grant get under these rules?",
  "options": [
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "q0537cd5d55",
  "kind": "choice",
  "text": "Records desk note. Ezra Rosales keeps CR-85975, which concerns Vida.\n\nInterview notes for Vida (2026):\nCaseworker: Kavita Kimura, your relation to Vida?\nKavita Kimura: I am Vida's grandmother.\nCaseworker: Months Vida lived with you?\nKavita Kimura: 9 months.\nCaseworker: Annual income?\nKavita Kimura: $24,722.00.\nCaseworker: Filed a claim for Vida?\nKavita Kimura: yes.\nCaseworker: Elias Ruiz, your relation to Vida?\nElias Ruiz: I am Vida's father.\nCaseworker: Months Vida lived with you?\nElias Ruiz: 1 month.\nCaseworker: Annual income?\nElias Ruiz: $24,722.00.\nCaseworker: Filed a claim for Vida?\nElias Ruiz: yes.\nCaseworker: Zofia Kaur, your relation to Vida?\nZofia Kaur: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nZofia Kaur: 7 months.\nCaseworker: Annual income?\nZofia Kaur: $90,761.27.\nCaseworker: Filed a claim for Vida?\nZofia Kaur: no.",
  "question": "Kelmstone Mountain Family Grant rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Vida for Kelmstone Mountain Family Grant?",
  "options": [
   "Zofia Kaur",
   "Kavita Kimura"
  ]
 },
 {
  "qid": "q3368fda4b5",
  "kind": "choice",
  "text": "A quick note for the district team: Riley Watanabe is taking care of CR-48447 for Kira.\n\nPeople who asked to claim Kira (2026):\n- Hiroko Watson: relationship to Kira: mother; months lived with Kira: 11 months; annual income: 50,502.50 USD; filed a claim: yes\n- Dmitri Gordon: relationship to Kira: father; months lived with Kira: 8 months; annual income: 55,405.80 USD; filed a claim: yes",
  "question": "Tessenvale Valley Child Credit rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for strictly over 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kira lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Kira for Tessenvale Valley Child Credit?",
  "options": [
   "Dmitri Gordon",
   "Hiroko Watson"
  ]
 },
 {
  "qid": "q6d2a36cfed",
  "kind": "choice",
  "text": "Friendly front counter slip\nTicket: HR-55974\nDealt with by: Kendall Umarov\nNamed person: Anjali Murphy\n\nFacts for Anjali Murphy (2026):\n| fact | value |\n| --- | --- |\n| time employed | 51 months |\n| hours worked in the past year | 933 hours |\n| employees at the worksite | 173 employees |\n| gross annual pay | 50,904.18 USD |\n| take-home annual pay | 44,000.00 USD |\n| enrolled in | Gerrondale Tenant Aid |",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly under $44,000.\n- Gate B: passed when hours worked in the past year are strictly in excess of 1,150 hours.\n- Gate C: passed when gross annual pay is at or under the amount of $53,500.\n- Route: an applicant enrolled in Corranmere Flexi Hours skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Anjali Murphy to Marrowby Bakery Family Leave get?",
  "options": [
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qa7eac2eecd",
  "kind": "yes/no",
  "text": "Hello team,\nThank you for reviewing case CASE-80095 with a warm eye on Greta Yamazaki.\nWarm regards, Quinn Pavlenko\n\nIntake interview with Greta Yamazaki (2027):\nCaseworker: Gross monthly income?\nGreta Yamazaki: $2,930.\nCaseworker: Net monthly income?\nGreta Yamazaki: 2,628.84 USD.\nCaseworker: Countable assets?\nGreta Yamazaki: 17,709.07 USD.\nCaseworker: Time in the service area?\nGreta Yamazaki: 12 months.\nCaseworker: Age?\nGreta Yamazaki: 65 years.\nCaseworker: Other programme enrolled in?\nGreta Yamazaki: Aldervale Meal Basket.",
  "question": "Going by the listed rules, is Greta Yamazaki eligible for Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 65 years or more.\n- Gate B: passed when the applicant has lived in the service area for 7 months or greater.\n- Gate C: passed when gross monthly income is at or beneath $2,930.\n- Route: an applicant enrolled in Brindlemoor Repair Fund skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q171b734ad6",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CR-21117, handled by Mika Zamora\n[subject_line] Liam is at the heart of it\n\nPeople who asked to claim Liam (2025):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hamid Sullivan | father | 12 months | 77,719.94 USD | no |\n| Galina Becker | aunt | 8 months | 15,880.00 USD | yes |\n| Yara Douglas | aunt | 12 months | 54,991.85 USD | no |\n| Gustav Gordon | grandfather | 6 months | 30,293.55 USD | yes |",
  "question": "According to these rules, is Galina Becker the person who ends up with the right to claim Liam for Tessenvale Valley Child Credit?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for strictly higher than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Liam lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd3f561893e",
  "kind": "choice",
  "text": "{\"caseworker\": \"Jamie Jorgensen\", \"case\": \"HR-37768\", \"about\": \"Dmitri Mensah\", \"hub\": \"support\"}\n\nFacts for Dmitri Mensah (2026), as JSON:\n{\"time_employed\": \"98 months\", \"hours_worked_in_the_past_year\": \"534 hours\", \"employees_at_the_worksite\": \"93 employees\", \"gross_annual_pay\": \"$84,000\", \"take-home_annual_pay\": \"$68,000\", \"enrolled_in\": \"Rickmere Night School Fund\"}",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is $84,000 or lower.\n- Gate B: passed when take-home annual pay is strictly below the amount of $68,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Dmitri Mensah to Hallowdene Logistics Study Grant?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "q2b228ef86f",
  "kind": "choice",
  "text": "Facts for Hamid Delgado (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,828.86 USD |\n| net monthly income | 1,829.06 USD |\n| countable assets | 5,984.04 USD |\n| time in the service area | 54 months |\n| age | 42 years |\n| enrolled in | Tessaly Housing Levy |\n\n[help_desk_entry] ref=CASE-31006 by=Sasha Okonkwo about=Hamid Delgado",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly smaller than 3,710.00 USD.\n- Gate B: passed when the applicant's age is strictly more than 63 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hamid Delgado to Wyndholm Forest Fuel Support lead to?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "qd9e573961e",
  "kind": "yes/no",
  "text": "Avery Obradovic: cheers, the staff support desk has CR-82391 for Ines.\n\nPeople who asked to claim Ines (2027):\n- Fatima Rahimi: relationship to Ines: mother; months lived with Ines: twelve months; annual income: 25,607.30 USD; filed a claim: yes\n- Dmitri Mensah: relationship to Ines: father; months lived with Ines: one month; annual income: $77,891; filed a claim: yes\n- Galina Fujimoto: relationship to Ines: grandmother; months lived with Ines: eleven months; annual income: 94,213.24 USD; filed a claim: yes\n- Xenia Petrov: relationship to Ines: aunt; months lived with Ines: twelve months; annual income: 25,607.30 USD; filed a claim: yes",
  "question": "According to these rules, is it not the case that Galina Fujimoto may not claim Ines for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2027: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for greater than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ines lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6c96f3156a",
  "kind": "choice",
  "text": "Ticket: regional case record CR-30947\nRaised by: Toni Lazar\nAbout: Liam\n\nPeople who asked to claim Liam (2026):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kenji Reynolds | father | 6 months | $52,761.17 | yes |\n| Greta Kovacs | mother | 7 months | $38,131.85 | yes |\n| Mariam Hoffman | grandmother | 11 months | $30,812 | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2026: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for at or above 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Liam lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tessenvale Valley Child Credit, which person, if any, may claim Liam?",
  "options": [
   "Greta Kovacs",
   "Kenji Reynolds"
  ]
 },
 {
  "qid": "qeaaf8abb44",
  "kind": "choice",
  "text": "Front sheet\nReference: HR-68147\nHandled by: Blair Xiong\nFor: Yusuf Johnson\n\nFacts for Yusuf Johnson (2025):\n| fact | value |\n| --- | --- |\n| time employed | 35 months |\n| hours worked in the past year | 1341 hours |\n| employees at the worksite | 278 employees |\n| gross annual pay | $43,566.59 |\n| take-home annual pay | $38,500.01 |\n| enrolled in | Rickmere Night Course Fund |",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly more than 1340 hours.\n- Gate B: passed when the applicant has been employed for strictly greater than 22 months.\n- Gate C: passed when take-home annual pay is at or under $38,500.\n- Route: an applicant enrolled in Sarrowby Mentor Stipend skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Yusuf Johnson to Hallowdene Logistics Study Grant get?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qd245a5a9c6",
  "kind": "choice",
  "text": "Facts for Pavel Reynolds (2025):\n| fact | value |\n| --- | --- |\n| time employed | thirteen months |\n| hours worked in the past year | 606 hours |\n| employees at the worksite | 396 employees |\n| gross annual pay | $45,870.94 |\n| take-home annual pay | $35,991.87 |\n| enrolled in | Pellbrook Staff Tool Allowance |\n\n[front_counter] reference=HR-74669 caseworker=Dani Ishikawa person=Pavel Reynolds",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for above twelve months.\n- Gate B: passed when gross annual pay is $83,500 at the most.\n- Gate C: passed when hours worked in the past year are equal to or above 1,060 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Pavel Reynolds to Drummock Robotics Workshop Training Fund?",
  "options": [
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q7ead3773db",
  "kind": "choice",
  "text": "People who asked to claim Kira (2025):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gustav Hudson | grandfather | 9 months | $94,854 | yes |\n| Matias Abara | father | 3 months | 92,874.36 USD | yes |\n| Greta Vasquez | aunt | 10 months | 75,868.43 USD | no |\n\nHi Kira,\nThanks for holding on about case CR-50218.\nTake care, Shay Bekele",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 6 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Kira lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Kira for Brellow Orchard Family Credit?",
  "options": [
   "Gustav Hudson",
   "Matias Abara"
  ]
 },
 {
  "qid": "qaef21648df",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Viktor Mensah; the reference is HR-03377.\nKind regards, Casey Kaplan\n\nFacts for Viktor Mensah (2027):\n- time employed: 9 months\n- hours worked in the past year: 664 hours\n- employees at the worksite: 36 employees\n- gross annual pay: 56,999.99 USD\n- take-home annual pay: 46,499.99 USD\n- enrolled in: Halvorne Sabbatical Fund",
  "question": "According to these rules, does Viktor Mensah fail to qualify for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,150 hours.\n- Gate B: passed when take-home annual pay is smaller than $46,500.\n- Gate C: passed when gross annual pay is $57,000 or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc61d59a183",
  "kind": "choice",
  "text": "Facts for Tomi Okafor (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 976.58 USD |\n| net monthly income | 668.46 USD |\n| countable assets | 4,939.88 USD |\n| time in the service area | thirteen months |\n| age | 66 years |\n| enrolled in | Kelder Veterans Pension |\n\n[help_line] case_ref=CASE-96261 staff=Ari Benali about=Tomi Okafor",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is above 66 years.\n- Gate B: passed when the applicant has lived in the service area for higher than twelve months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which result comes from the application of Tomi Okafor to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q91aad47954",
  "kind": "choice",
  "text": "Records office note: CR-22308 is registered in the name of Sami Castro, concerning Omar.\n\nPeople who asked to claim Omar (2027):\n- Xenia Kaur: relationship to Omar: mother; months lived with Omar: 6 months; annual income: 51,755.00 USD; filed a claim: yes\n- Idris Gutierrez: relationship to Omar: grandfather; months lived with Omar: 9 months; annual income: 38,052.95 USD; filed a claim: no\n- Olena Kowalski: relationship to Omar: aunt; months lived with Omar: 3 months; annual income: 93,316.00 USD; filed a claim: no",
  "question": "Tessenvale Valley Child Credit rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for equal to or greater than 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tessenvale Valley Child Credit, which person, if any, gets the right to claim Omar?",
  "options": [
   "Olena Kowalski",
   "Nobody may claim the child",
   "Xenia Kaur"
  ]
 },
 {
  "qid": "q42c8483e6b",
  "kind": "choice",
  "text": "Hello,\nThe casework team holds CR-16850 for Ada.\nBest, Shay Bekele\n\nPeople who asked to claim Ada (2025):\n- Kwame Thompson: relationship to Ada: grandfather; months lived with Ada: 7 months; annual income: $94,822.95; filed a claim: yes\n- Xavier Johnson: relationship to Ada: father; months lived with Ada: 11 months; annual income: $24,380.00; filed a claim: no",
  "question": "Kelvery Market Credit rules for 2025: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for strictly higher than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Kelvery Market Credit, which person, if any, gets to claim Ada under these rules?",
  "options": [
   "Xavier Johnson",
   "Kwame Thompson"
  ]
 },
 {
  "qid": "qf48697eb2c",
  "kind": "yes/no",
  "text": "Facts for Ugo Jovanovic (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,535.57 USD |\n| net monthly income | 2,029.99 USD |\n| countable assets | 7,642.12 USD |\n| time in the service area | 47 months |\n| age | 58 years |\n| enrolled in | none |\n\n[front_counter] case_ref=CASE-38558 staff=Jamie Jorgensen subject=Ugo Jovanovic",
  "question": "Under these rules, is it not true that Ugo Jovanovic is not eligible for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly lower than $2,030.\n- Gate B: passed when the applicant's age is greater than 57 years.\n- Gate C: passed when gross monthly income is strictly under $2,825.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd69d72b95d",
  "kind": "yes/no",
  "text": "{\"caseworker\": \"Teo Quintero\", \"about\": \"Gustav Dubois\", \"case\": \"HR-27746\", \"office\": \"branch\"}\n\nFacts for Gustav Dubois (2025), as JSON:\n{\"time_employed\": \"70 months\", \"hours_worked_in_the_past_year\": \"514 hours\", \"employees_at_the_worksite\": \"85 employees\", \"gross_annual_pay\": \"64,609.26 USD\", \"take-home_annual_pay\": \"42,768.06 USD\", \"enrolled_in\": \"Gerrondale Tenant Aid\"}",
  "question": "Going by the listed rules, is Gustav Dubois not eligible for Marrowby Bakery Family Leave?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has a minimum of 58 employees.\n- Gate B: passed when take-home annual pay is at or beneath $40,500.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q619e1141b8",
  "kind": "yes/no",
  "text": "Welcome to your case file\nCase reference: CASE-39136\nCaseworker: Kiran Morales\nAbout: Anton Yamazaki\n\nFacts for Anton Yamazaki (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $992.90 |\n| net monthly income | $891.01 |\n| countable assets | $9,368.16 |\n| time in the service area | eleven months |\n| age | 59 years |\n| enrolled in | none |",
  "question": "Does Anton Yamazaki fail to qualify for admission to Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is at or above 58 years.\n- Gate B: passed when the applicant has lived in the service area for equal to or above eight months.\n- Gate C: passed when gross monthly income is $2,030.00 or under.\n- Route: an applicant enrolled in Hemmerly Nursery Place Fund skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd16cfbf794",
  "kind": "choice",
  "text": "Facts for Rafael Ramirez (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 5,173.22 USD |\n| net monthly income | 3,301.79 USD |\n| countable assets | 7,926.59 USD |\n| time in the service area | 13 months |\n| age | 55 years |\n| enrolled in | Mirrowen Transit Voucher |\n\nServices counter intake form\nCase reference: CASE-27915\nCaseworker: Sasha Okonkwo\nAbout: Rafael Ramirez",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly in excess of 56 years.\n- Gate B: passed when the applicant has lived in the service area for equal to or greater than 12 months.\n- Gate C: passed when countable assets are strictly below the level of $10,350.\n- Route: an applicant enrolled in Mirrowen Transit Voucher skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Rafael Ramirez to Tollsey Island Ferry Discount land?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qdee9debe3e",
  "kind": "yes/no",
  "text": "Dear colleague,\nFor the record, HR-93726 concerning Galina Ueda is held by the desk.\nYours faithfully, Jamie Jorgensen\n\nFacts for Galina Ueda (2027):\n- time employed: 5 months\n- hours worked in the past year: 1502 hours\n- employees at the worksite: 11 employees\n- gross annual pay: 113,194.81 USD\n- take-home annual pay: 83,842.37 USD\n- enrolled in: Idrane Tuition Grant",
  "question": "Going by the listed rules, is Galina Ueda eligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly above 19 months.\n- Gate B: passed when take-home annual pay is 57,000.00 USD or less.\n- Gate C: passed when the worksite has 36 employees at minimum.\n- Route: an applicant enrolled in Idrane Tuition Grant skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc519bcc3cf",
  "kind": "choice",
  "text": "Teo Quintero: file HR-44020 about Olena Begum is on my list.\n\nIntake interview with Olena Begum (2025):\nCaseworker: Time employed?\nOlena Begum: 93 months.\nCaseworker: Hours worked in the past year?\nOlena Begum: 443 hours.\nCaseworker: Employees at your worksite?\nOlena Begum: 67 employees.\nCaseworker: Gross annual pay?\nOlena Begum: $83,499.99.\nCaseworker: Take-home annual pay?\nOlena Begum: $74,889.34.\nCaseworker: Other programme enrolled in?\nOlena Begum: Castrell Sick Pay.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly above 39 employees.\n- Gate B: passed when hours worked in the past year are greater than or equal to 980 hours.\n- Gate C: passed when gross annual pay is strictly below the amount of $83,500.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Olena Begum to Quenhollow Brewery Bereavement Leave receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q6c1279ef97",
  "kind": "yes/no",
  "text": "reference: CR-87729\nworker: Morgan Mendoza\nabout: Dara\n\nPeople who asked to claim Dara (2025):\n- Xenia Bergstrom: relationship to Dara: aunt; months lived with Dara: ten months; annual income: 89,055.00 USD; filed a claim: yes\n- Ugo Gutierrez: relationship to Dara: father; months lived with Dara: nine months; annual income: 31,077.25 USD; filed a claim: yes\n- Zofia Ivanova: relationship to Dara: mother; months lived with Dara: five months; annual income: 41,304.58 USD; filed a claim: yes",
  "question": "Under these rules, is it true that Ugo Gutierrez may not claim Dara for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for at or greater than five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q16e526ec6a",
  "kind": "choice",
  "text": "Dear Rafi,\nThanks for getting in touch about case CR-47475.\nWarm wishes, Ezra Rosales\n\nInterview notes for Rafi (2026):\nCaseworker: Cyril Iyer, your relation to Rafi?\nCyril Iyer: I am Rafi's grandfather.\nCaseworker: Months Rafi lived with you?\nCyril Iyer: six months.\nCaseworker: Annual income?\nCyril Iyer: $90,859.00.\nCaseworker: Filed a claim for Rafi?\nCyril Iyer: no.\nCaseworker: Farid Lindqvist, your relation to Rafi?\nFarid Lindqvist: I am Rafi's father.\nCaseworker: Months Rafi lived with you?\nFarid Lindqvist: six months.\nCaseworker: Annual income?\nFarid Lindqvist: $16,141.00.\nCaseworker: Filed a claim for Rafi?\nFarid Lindqvist: yes.\nCaseworker: Hana Lehmann, your relation to Rafi?\nHana Lehmann: I am Rafi's aunt.\nCaseworker: Months Rafi lived with you?\nHana Lehmann: five months.\nCaseworker: Annual income?\nHana Lehmann: $69,787.00.\nCaseworker: Filed a claim for Rafi?\nHana Lehmann: yes.",
  "question": "Sallowmere Family Payment rules for 2026: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for strictly in excess of five months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Rafi lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Rafi for Sallowmere Family Payment?",
  "options": [
   "Farid Lindqvist",
   "Hana Lehmann"
  ]
 },
 {
  "qid": "q9dd606e450",
  "kind": "choice",
  "text": "Town hall desk form\nCase reference: CR-23595\nHandled by: Blair Xiong\nFor: Tove\n\nPeople who asked to claim Tove (2025):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Jakub Kovacs | father | eight months | $55,557 | no |\n| Jelena Tanaka | mother | one month | $72,430 | yes |\n| Tomas Abara | grandfather | twelve months | $33,668 | yes |",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for strictly above five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Tove lived for more months comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Tove for Corrowby Family Supplement?",
  "options": [
   "Tomas Abara",
   "Jelena Tanaka"
  ]
 },
 {
  "qid": "q35f869d1c2",
  "kind": "choice",
  "text": "People who asked to claim Luca (2026):\n| person | relationship to Luca | months lived with Luca | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Fatima Tanaka | mother | 12 months | 17,369.00 USD | yes |\n| Hugo Mitchell | father | 1 month | 17,369.00 USD | yes |\n| Hiroko Nguyen | grandmother | 9 months | 79,104.00 USD | yes |\n\nHello Luca,\nA routine note about CR-22450 comes from the district office.\nBest wishes, Sami Castro",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Luca.\n- Only one person may claim Luca. Work through these steps in order.\n- Step one: only people who filed a claim for Luca are considered.\n- Step two: of those, only people with whom Luca lived for in excess of 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Luca lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Luca.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Farrowby Moorland Parish Credit, which person, if any, gets to claim Luca under these rules?",
  "options": [
   "Hiroko Nguyen",
   "Fatima Tanaka"
  ]
 },
 {
  "qid": "qa275c3e5b8",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Ali; the reference is CR-33598.\nKind regards, Jules Shrestha\n\nPeople who asked to claim Ali (2026):\n- Pavel Bergstrom: relationship to Ali: father; months lived with Ali: 5 months; annual income: $87,493.86; filed a claim: yes\n- Yasmin Dragic: relationship to Ali: mother; months lived with Ali: 11 months; annual income: $60,294.00; filed a claim: yes",
  "question": "Under these rules, is Pavel Bergstrom excluded from claiming Ali for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2026: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for equal to or greater than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ali lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd2b5c46489",
  "kind": "yes/no",
  "text": "[help_desk_entry] ref=HR-35542 by=Tomi Eklund about=Xavier Nakamura\n\nFacts for Xavier Nakamura (2027):\n| fact | value |\n| --- | --- |\n| time employed | 5 months |\n| hours worked in the past year | 910 hours |\n| employees at the worksite | 73 employees |\n| gross annual pay | $49,970.30 |\n| take-home annual pay | $35,000.01 |\n| enrolled in | Dorrane Parental Leave |",
  "question": "For Tovardine Seed Caregiver Leave, is Xavier Nakamura ineligible under the stated rules?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly over 54 employees.\n- Gate B: passed when hours worked in the past year are above 910 hours.\n- Gate C: passed when take-home annual pay is strictly lower than $35,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7ceb611883",
  "kind": "yes/no",
  "text": "Quick ticket: CR-30646\nRaised by: Kiran Morales\nAbout: Omar\n\nInterview notes for Omar (2027):\nCaseworker: Emeka Ruiz, your relation to Omar?\nEmeka Ruiz: I am Omar's father.\nCaseworker: Months Omar lived with you?\nEmeka Ruiz: eight months.\nCaseworker: Annual income?\nEmeka Ruiz: 70,531.87 USD.\nCaseworker: Filed a claim for Omar?\nEmeka Ruiz: yes.\nCaseworker: Hamid Russell, your relation to Omar?\nHamid Russell: I am Omar's uncle.\nCaseworker: Months Omar lived with you?\nHamid Russell: three months.\nCaseworker: Annual income?\nHamid Russell: $89,448.\nCaseworker: Filed a claim for Omar?\nHamid Russell: yes.\nCaseworker: Mariam Mensah, your relation to Omar?\nMariam Mensah: I am Omar's mother.\nCaseworker: Months Omar lived with you?\nMariam Mensah: two months.\nCaseworker: Annual income?\nMariam Mensah: $24,112.\nCaseworker: Filed a claim for Omar?\nMariam Mensah: yes.",
  "question": "According to these rules, is Hamid Russell the person who ends up holding the right to claim Omar for Stonevale Delta Child Allowance?",
  "definitions": "Stonevale Delta Child Allowance rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for a minimum of seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9595cc4cc2",
  "kind": "yes/no",
  "text": "Facts for Jamie Kelly (2025):\n| fact | value |\n| --- | --- |\n| time employed | 42 months |\n| hours worked in the past year | 1140 hours |\n| employees at the worksite | 385 employees |\n| gross annual pay | $119,853.62 |\n| take-home annual pay | $75,864.82 |\n| enrolled in | Pellbrook Staff Tool Allowance |\n\nTicket: district office desk review, case HR-88837\nRaised by: Jules Shrestha\nAbout: Jamie Kelly",
  "question": "Going by the listed rules, is Jamie Kelly not eligible for Drummock Robotics Workshop Training Fund?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is $78,500.00 or lower.\n- Gate B: passed when hours worked in the past year are greater than 1140 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4a2113abb4",
  "kind": "choice",
  "text": "Riley Watanabe: outreach list has CR-93869 for Eva.\n\nPeople who asked to claim Eva (2026):\n- Fatima Yilmaz: relationship to Eva: mother; months lived with Eva: 7 months; annual income: 83,912.00 USD; filed a claim: yes\n- Quentin Ilunga: relationship to Eva: father; months lived with Eva: 9 months; annual income: 22,300.00 USD; filed a claim: yes",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for strictly greater than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Eva lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Eva for Tollmere Lakeside Family Payment?",
  "options": [
   "Fatima Yilmaz",
   "Quentin Ilunga"
  ]
 },
 {
  "qid": "q8dec6aff4e",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CR-65804\nRaised by: Sasha Okonkwo\nAbout: Theo\n\nPeople who asked to claim Theo (2025):\n| person | relationship to Theo | months lived with Theo | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dario Okafor | grandfather | 11 months | $38,241.04 | yes |\n| Matias Dragic | father | 5 months | $43,020.00 | yes |",
  "question": "Does the right to claim Theo for Ostrowan Prairie Grant pass to a different person from Dario Okafor, or stay unclaimed under these rules?",
  "definitions": "Ostrowan Prairie Grant rules for 2025: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for 5 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Theo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7b7b0f4f0a",
  "kind": "choice",
  "text": "Facts for Emeka Kimura (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,358.59 USD |\n| net monthly income | 1,527.19 USD |\n| countable assets | $4,650 |\n| time in the service area | 7 months |\n| age | 35 years |\n| enrolled in | Tessaly Housing Aid |\n\nCase note: the help desk has Avery Obradovic on file CASE-98228 for Emeka Kimura.",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or under $3,160.\n- Gate B: passed when the applicant has lived in the service area for strictly over 5 months.\n- Gate C: passed when countable assets are lower than or equal to $4,650.\n- Route: an applicant enrolled in Tessaly Housing Aid skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Wyndholm Forest Fuel Support, which outcome does the application of Emeka Kimura get?",
  "options": [
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q97272b62db",
  "kind": "yes/no",
  "text": "[team_note] Ezra Rosales keeps file CASE-11004 with kind care\n[about] Cyril Ilic is the focus\n\nIntake interview with Cyril Ilic (2026):\nCaseworker: Gross monthly income?\nCyril Ilic: $4,828.66.\nCaseworker: Net monthly income?\nCyril Ilic: $3,094.99.\nCaseworker: Countable assets?\nCyril Ilic: $1,877.24.\nCaseworker: Time in the service area?\nCyril Ilic: 32 months.\nCaseworker: Age?\nCyril Ilic: 46 years.\nCaseworker: Other programme enrolled in?\nCyril Ilic: Quenmoor Emergency Loan.",
  "question": "Is Cyril Ilic not eligible for Ostermere Delta Flood Repair Support as the rules stand?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under the amount of $4,105.\n- Gate B: passed when the applicant's age is a minimum of 63 years.\n- Gate C: passed when net monthly income is strictly lower than $3,095.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf56c7ff48d",
  "kind": "choice",
  "text": "People who asked to claim Ezra (2025):\n| person | relationship to Ezra | months lived with Ezra | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Imani Esposito | grandmother | six months | $35,958 | yes |\n| Hana Lehmann | mother | six months | $64,211 | yes |\n| Elias Mwangi | uncle | six months | $64,211 | yes |\n\nTicket CR-98316\nWith: Alex Lindgren\nAbout: Ezra",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for strictly over five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Ezra for Brellow Orchard Family Credit?",
  "options": [
   "Imani Esposito",
   "Hana Lehmann"
  ]
 }
]
