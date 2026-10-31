# G5-H blind read T15-blind_read-8379fede-005 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-8379fede-005.json

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
  "qid": "qd80440a80a",
  "kind": "yes/no",
  "text": "Ref: CR-80088\nAbout: Gia\nRaised by: Nika Hernandez\n\nPeople who asked to claim Gia (2026):\n| person | relationship to Gia | months lived with Gia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anton Nguyen | father | eight months | 23,179.92 USD | yes |\n| Farid Mitchell | grandfather | nine months | 50,472.39 USD | yes |\n| Leila Moreau | mother | twelve months | 80,922.06 USD | yes |\n| Xavier Sokolov | grandfather | six months | $47,980 | no |",
  "question": "Under these rules, does Leila Moreau fail to gain the right to claim Gia for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2026: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for seven months or above in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Gia lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q520c830e1d",
  "kind": "yes/no",
  "text": "[records_office] tag_case=CR-64325 worker=Kazu Yousef about=Kira\n\nPeople who asked to claim Kira (2026):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hana Sokolov | aunt | 12 months | 25,553.37 USD | yes |\n| Farid Ilic | father | 5 months | 85,116.62 USD | no |",
  "question": "Is Hana Sokolov the person who gets to claim Kira for Kelvery Market Credit under these rules?",
  "definitions": "Kelvery Market Credit rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 6 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Kira lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q473d89b49a",
  "kind": "choice",
  "text": "Facts for Kazu Yamazaki (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,636.21 |\n| net monthly income | $2,406.30 |\n| countable assets | $1,936.93 |\n| time in the service area | 47 months |\n| age | 45 years |\n| enrolled in | Tessaly Housing Levy |\n\nDistrict office intake form\nReference: CASE-94402\nCaseworker: Quinn Pavlenko\nAbout: Kazu Yamazaki",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly lower than $3,636.22.\n- Gate B: passed when countable assets are strictly beneath $3,250.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Wyndholm Forest Fuel Support, which outcome does the application submitted by Kazu Yamazaki get?",
  "options": [
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qc9a613c1ca",
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
  "qid": "q8942c6be57",
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
  "qid": "qf2f0fbe807",
  "kind": "yes/no",
  "text": "Ren Dvorak: quick update, case CR-24628 is up for Remi.\n\nInterview notes for Remi (2027):\nCaseworker: Pavel Hamilton, your relation to Remi?\nPavel Hamilton: I am Remi's uncle.\nCaseworker: Months Remi lived with you?\nPavel Hamilton: 7 months.\nCaseworker: Annual income?\nPavel Hamilton: 24,404.00 USD.\nCaseworker: Filed a claim for Remi?\nPavel Hamilton: no.\nCaseworker: Oskar Begum, your relation to Remi?\nOskar Begum: I am Remi's father.\nCaseworker: Months Remi lived with you?\nOskar Begum: 9 months.\nCaseworker: Annual income?\nOskar Begum: 24,404.00 USD.\nCaseworker: Filed a claim for Remi?\nOskar Begum: yes.\nCaseworker: Vesna Kimura, your relation to Remi?\nVesna Kimura: I am Remi's mother.\nCaseworker: Months Remi lived with you?\nVesna Kimura: 4 months.\nCaseworker: Annual income?\nVesna Kimura: 32,509.00 USD.\nCaseworker: Filed a claim for Remi?\nVesna Kimura: yes.",
  "question": "According to these rules, will the right to claim Remi for Stonevale Delta Child Allowance go to a different person from Vesna Kimura, or stay unclaimed?",
  "definitions": "Stonevale Delta Child Allowance rules for 2027: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for at or above 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Remi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2931fd9a08",
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
  "qid": "q1578d1b21a",
  "kind": "yes/no",
  "text": "Jules Shrestha: for the record, file CASE-69895 belongs to Ingrid Ruiz.\n\nFacts for Ingrid Ruiz (2025):\n- gross monthly income: 4,748.20 USD\n- net monthly income: 3,172.83 USD\n- countable assets: 4,858.89 USD\n- time in the service area: 8 months\n- age: 72 years\n- enrolled in: Brackenholm Housing Loan",
  "question": "Following the listed rules, does Ingrid Ruiz fail to qualify for Tarrowick Food Basket Support?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is above 59 years.\n- Gate B: passed when the applicant has lived in the service area for 8 months or above.\n- Route: an applicant enrolled in Brackenholm Housing Aid skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q84f44b6322",
  "kind": "yes/no",
  "text": "Branch intake sheet\nReference: HR-06980\nHandled by: Jamie Jorgensen\nAbout: Tariq Wojcik\n\nFacts for Tariq Wojcik (2027):\n| fact | value |\n| --- | --- |\n| time employed | 24 months |\n| hours worked in the past year | 1080 hours |\n| employees at the worksite | 80 employees |\n| gross annual pay | $73,098.40 |\n| take-home annual pay | $52,290.63 |\n| enrolled in | none |",
  "question": "Under these rules, is Tariq Wojcik eligible for Hallowdene Logistics Study Grant given every gate that applies is passed?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are equal to or greater than 1080 hours.\n- Gate B: passed when the applicant has been employed for 23 months or greater.\n- Gate C: passed when take-home annual pay is strictly lower than $66,500.00.\n- Route: an applicant enrolled in Sarrowby Mentor Stipend skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q04b1f96952",
  "kind": "choice",
  "text": "Internal note: Morgan Mendoza handles case CASE-92319 about Sabine Yamazaki.\n\nFacts for Sabine Yamazaki (2026):\n- gross monthly income: $3,301.20\n- net monthly income: $2,393.77\n- countable assets: $616.76\n- time in the service area: three months\n- age: 84 years\n- enrolled in: Sorrenby Tenancy Deposit Loan",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than 62 years.\n- Gate B: passed when the applicant has lived in the service area for at or above three months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Sabine Yamazaki to Tesslow Prairie Water Bill Assistance receive?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "q2ad71e6d2b",
  "kind": "yes/no",
  "text": "[help_line] case_ref=CASE-76099 staff=Tomi Eklund about=Amara Gutierrez\n\nIntake interview with Amara Gutierrez (2025):\nCaseworker: Gross monthly income?\nAmara Gutierrez: $2,411.68.\nCaseworker: Net monthly income?\nAmara Gutierrez: $1,988.31.\nCaseworker: Countable assets?\nAmara Gutierrez: $9,089.79.\nCaseworker: Time in the service area?\nAmara Gutierrez: thirteen months.\nCaseworker: Age?\nAmara Gutierrez: 57 years.\nCaseworker: Other programme enrolled in?\nAmara Gutierrez: Velgate Pump Loan.",
  "question": "Going by the listed rules, is Amara Gutierrez ineligible for Ostermere Delta Flood Repair Support?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than twelve months.\n- Gate B: passed when net monthly income is equal to or below $2,310.00.\n- Gate C: passed when countable assets are $9,500.00 or under.\n- Route: an applicant enrolled in Quenmoor Emergency Fund skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5731c30888",
  "kind": "yes/no",
  "text": "Intake form, records office\nCase reference: CR-73905\nSubject: Dara\nHandled by: Tomi Eklund\n\nPeople who asked to claim Dara (2026):\n| person | relationship to Dara | months lived with Dara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Leila Wojcik | aunt | 10 months | $31,652 | yes |\n| Matias Douglas | uncle | 7 months | $78,967 | yes |\n| Freya Zielinski | aunt | 4 months | 93,683.17 USD | yes |",
  "question": "Following the listed rules, is Matias Douglas barred from claiming Dara for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for strictly above 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q966c464993",
  "kind": "choice",
  "text": "People who asked to claim Omar (2025):\n| person | relationship to Omar | months lived with Omar | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Sergio Kelly | father | 12 months | 47,214.00 USD | no |\n| Mariam Tanaka | mother | 12 months | 22,656.00 USD | yes |\n| Matias Sullivan | grandfather | 8 months | 90,364.82 USD | yes |\n\n[services_counter] case_ref=CR-92074 worker=Nika Hernandez about=Omar",
  "question": "Farrowby Moorland Parish Credit rules for 2025: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for equal to or greater than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Omar for Farrowby Moorland Parish Credit?",
  "options": [
   "Sergio Kelly",
   "Nobody may claim the child",
   "Mariam Tanaka"
  ]
 },
 {
  "qid": "q39d68afd3d",
  "kind": "choice",
  "text": "Internal note: CASE-21737 is held by Ren Dvorak. Regarding Jamie Nakamura, please refer to the desk log.\n\nIntake interview with Jamie Nakamura (2027):\nCaseworker: Gross monthly income?\nJamie Nakamura: 3,459.99 USD.\nCaseworker: Net monthly income?\nJamie Nakamura: 2,424.97 USD.\nCaseworker: Countable assets?\nJamie Nakamura: 1,820.39 USD.\nCaseworker: Time in the service area?\nJamie Nakamura: 9 months.\nCaseworker: Age?\nJamie Nakamura: 50 years.\nCaseworker: Other programme enrolled in?\nJamie Nakamura: Quenmoor Emergency Loan.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below 3,350.00 USD.\n- Gate B: passed when gross monthly income is strictly under the value of 3,460.00 USD.\n- Gate C: passed when the applicant has lived in the service area for above 11 months.\n- Route: an applicant enrolled in Tallowmere Roof Grant skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Jamie Nakamura to Ostermere Delta Flood Repair Support ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qb8792ff088",
  "kind": "yes/no",
  "text": "[records_office] tag_case=CR-64325 worker=Kazu Yousef about=Kira\n\nPeople who asked to claim Kira (2026):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hana Sokolov | aunt | 12 months | 25,553.37 USD | no |\n| Farid Ilic | father | 5 months | 85,116.62 USD | no |",
  "question": "Is Hana Sokolov the person who gets to claim Kira for Kelvery Market Credit under these rules?",
  "definitions": "Kelvery Market Credit rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 6 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Kira lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q039d96e3f8",
  "kind": "choice",
  "text": "Case note: the staff support desk holds the record for Ezra. Case CR-76136, handled by Nika Hernandez.\n\nPeople who asked to claim Ezra (2026):\n- Tomas Douglas: relationship to Ezra: uncle; months lived with Ezra: 12 months; annual income: 84,425.00 USD; filed a claim: yes\n- Ivo Abebe: relationship to Ezra: father; months lived with Ezra: 1 month; annual income: 22,300.50 USD; filed a claim: yes\n- Hana Halvorsen: relationship to Ezra: mother; months lived with Ezra: 8 months; annual income: 48,899.00 USD; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2026: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Ezra for Corrowby Family Supplement?",
  "options": [
   "Tomas Douglas",
   "Hana Halvorsen"
  ]
 },
 {
  "qid": "q8ca29d0660",
  "kind": "yes/no",
  "text": "People who asked to claim Rafi (2027):\n| person | relationship to Rafi | months lived with Rafi | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Juliana Patterson | aunt | 9 months | 78,868.90 USD | yes |\n| Mirela Bergstrom | grandmother | 11 months | 84,716.07 USD | no |\n| Freya Anderson | mother | 3 months | 54,509.00 USD | yes |\n\n[help_line] case_ref=CR-49644 staff=Mika Zamora about=Rafi",
  "question": "Under these rules, is Juliana Patterson the person who gets to claim Rafi for Brellow Orchard Family Credit?",
  "definitions": "Brellow Orchard Family Credit rules for 2027: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for at or above 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Rafi lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q341ccb240d",
  "kind": "yes/no",
  "text": "Facts for Yara Gashi (2026):\n| fact | value |\n| --- | --- |\n| time employed | six months |\n| hours worked in the past year | 1,219 hours |\n| employees at the worksite | 58 employees |\n| gross annual pay | $68,000 |\n| take-home annual pay | $47,908.70 |\n| enrolled in | Tundale Care Coupon |\n\nteam: people services\ncase: HR-10645\ncaseworker: Lior Grigoryan\nabout: Yara Gashi",
  "question": "Does Yara Gashi fail to qualify for Pelmoor Ceramics Carer Support on these rules?",
  "definitions": "Pelmoor Ceramics Carer Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly greater than 58 employees.\n- Gate B: passed when gross annual pay is $68,000 at the most.\n- Gate C: passed when hours worked in the past year are 1,220 hours at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfdfff54b1f",
  "kind": "yes/no",
  "text": "Quinn Pavlenko: quick check on file CR-71438 for Dara, at the counter.\n\nPeople who asked to claim Dara (2026):\n- Zainab Dlamini: relationship to Dara: aunt; months lived with Dara: 10 months; annual income: $92,534.00; filed a claim: yes\n- Viktor Campbell: relationship to Dara: father; months lived with Dara: 0 months; annual income: $82,556.00; filed a claim: yes\n- Freya Gutierrez: relationship to Dara: mother; months lived with Dara: 5 months; annual income: $35,668.00; filed a claim: yes",
  "question": "Is it true that Zainab Dlamini may not claim Dara for Ferrowby Forest Credit?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2ba8ed63f9",
  "kind": "yes/no",
  "text": "Quick note: Ezra Rosales is running HR-11924 for Aiko Gordon. Outreach is moving fast.\n\nIntake interview with Aiko Gordon (2025):\nCaseworker: Time employed?\nAiko Gordon: 14 months.\nCaseworker: Hours worked in the past year?\nAiko Gordon: 416 hours.\nCaseworker: Employees at your worksite?\nAiko Gordon: 319 employees.\nCaseworker: Gross annual pay?\nAiko Gordon: $64,448.19.\nCaseworker: Take-home annual pay?\nAiko Gordon: $43,678.50.\nCaseworker: Other programme enrolled in?\nAiko Gordon: Ellerwick Trainee Stream.",
  "question": "Going by the listed rules, is Aiko Gordon eligible for Sorrelby Child Care Support?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for at or over 14 months.\n- Gate B: passed when take-home annual pay is strictly beneath $48,000.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q379e5ecd02",
  "kind": "yes/no",
  "text": "Dear colleague,\nThis is a short outreach note on case CASE-65257 for Zofia Kimura.\nRegards, Alex Lindgren\n\nIntake interview with Zofia Kimura (2026):\nCaseworker: Gross monthly income?\nZofia Kimura: $1,156.44.\nCaseworker: Net monthly income?\nZofia Kimura: $864.86.\nCaseworker: Countable assets?\nZofia Kimura: $12,578.41.\nCaseworker: Time in the service area?\nZofia Kimura: 13 months.\nCaseworker: Age?\nZofia Kimura: 86 years.\nCaseworker: Other programme enrolled in?\nZofia Kimura: Ormsby Housing Plan.",
  "question": "Does Zofia Kimura meet the rules for Fennick School Meal Supplement by passing every gate that applies?",
  "definitions": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or below $2,395.00.\n- Gate B: passed when the applicant has lived in the service area for at or over 9 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8133553c31",
  "kind": "choice",
  "text": "People who asked to claim Mia (2025):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ingrid Hudson | mother | 8 months | $80,826.00 | yes |\n| Priya Eriksen | aunt | 9 months | $84,529.00 | no |\n\nFront counter ticket: CR-38932\nWarm hello from: Kiran Morales\nPerson: Mia",
  "question": "Sorrenby Island Family Payment rules for 2025: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for 7 months at minimum in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Mia lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Sorrenby Island Family Payment, which person, if any, may claim Mia?",
  "options": [
   "Ingrid Hudson",
   "Priya Eriksen"
  ]
 },
 {
  "qid": "q1ca694c39b",
  "kind": "yes/no",
  "text": "[help_line] case_ref=CASE-76099 staff=Tomi Eklund about=Amara Gutierrez\n\nIntake interview with Amara Gutierrez (2025):\nCaseworker: Gross monthly income?\nAmara Gutierrez: $2,411.68.\nCaseworker: Net monthly income?\nAmara Gutierrez: $1,988.31.\nCaseworker: Countable assets?\nAmara Gutierrez: $9,089.79.\nCaseworker: Time in the service area?\nAmara Gutierrez: thirteen months.\nCaseworker: Age?\nAmara Gutierrez: 57 years.\nCaseworker: Other programme enrolled in?\nAmara Gutierrez: Velgate Pump Loan.",
  "question": "Does Amara Gutierrez fully qualify for Ostermere Delta Flood Repair Support under these rules?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than twelve months.\n- Gate B: passed when net monthly income is equal to or below $2,310.00.\n- Gate C: passed when countable assets are $9,500.00 or under.\n- Route: an applicant enrolled in Quenmoor Emergency Fund skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4d6505e63c",
  "kind": "yes/no",
  "text": "Casey Kaplan: Noted, CASE-85127 for Amara Lindqvist sits with the intake desk.\n\nFacts for Amara Lindqvist (2027):\n- gross monthly income: 1,995.52 USD\n- net monthly income: 1,777.63 USD\n- countable assets: 7,800.01 USD\n- time in the service area: 27 months\n- age: 61 years\n- enrolled in: Feldane Childcare Credit",
  "question": "Is Amara Lindqvist eligible for Sennamoor River Rent Support by passing every gate that applies?",
  "definitions": "Sennamoor River Rent Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or beneath 7,800.00 USD.\n- Gate B: passed when net monthly income is strictly below the amount of 2,420.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc5729cbcb9",
  "kind": "yes/no",
  "text": "Quinn Pavlenko: quick check on file CR-71438 for Dara, at the counter.\n\nPeople who asked to claim Dara (2026):\n- Zainab Dlamini: relationship to Dara: aunt; months lived with Dara: 5 months; annual income: $92,534.00; filed a claim: yes\n- Viktor Campbell: relationship to Dara: father; months lived with Dara: 0 months; annual income: $82,556.00; filed a claim: yes\n- Freya Gutierrez: relationship to Dara: mother; months lived with Dara: 5 months; annual income: $35,668.00; filed a claim: yes",
  "question": "Going by the listed rules, is Zainab Dlamini the person who wins the right to claim Dara for Ferrowby Forest Credit?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qea721957d4",
  "kind": "choice",
  "text": "[branch_desk] ref=CASE-34660 worker=Tomi Eklund about=Mateo Hoffman\n\nFacts for Mateo Hoffman (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,353.78 |\n| net monthly income | $2,145.18 |\n| countable assets | $3,689.52 |\n| time in the service area | eleven months |\n| age | 80 years |\n| enrolled in | Caddowen Pantry Shopping Card |",
  "question": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or less than $2,160.00.\n- Gate B: passed when the applicant has lived in the service area for twelve months at minimum.\n- Route: an applicant enrolled in Caddowen Pantry Shopping Card skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Mateo Hoffman to Tarrowick Food Basket Support receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qe6ff87cf75",
  "kind": "choice",
  "text": "Staff support form\nRef: CASE-58824\nOwner: Lior Grigoryan\nPerson: Tomi Nilsen\n\nIntake interview with Tomi Nilsen (2027):\nCaseworker: Gross monthly income?\nTomi Nilsen: 1,310.52 USD.\nCaseworker: Net monthly income?\nTomi Nilsen: 873.39 USD.\nCaseworker: Countable assets?\nTomi Nilsen: 2,977.63 USD.\nCaseworker: Time in the service area?\nTomi Nilsen: 9 months.\nCaseworker: Age?\nTomi Nilsen: 44 years.\nCaseworker: Other programme enrolled in?\nTomi Nilsen: Quenmoor Emergency Fund.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly under 4,100.00 USD.\n- Gate B: passed when the applicant's age is strictly in excess of 55 years.\n- Gate C: passed when the applicant has lived in the service area for above 10 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Tomi Nilsen on the application to Ostermere Delta Flood Repair Support?",
  "options": [
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q8e6b7271b3",
  "kind": "yes/no",
  "text": "People who asked to claim Liam (2026), as JSON:\n{\"people\": [{\"name\": \"Kenji Douglas\", \"relationship\": \"father\", \"months_lived_with_child\": \"7 months\", \"annual_income\": \"94,463.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Ravi Ilic\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"5 months\", \"annual_income\": \"22,925.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Hiroko Sullivan\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"21,352.13 USD\", \"filed_a_claim\": \"yes\"}]}\n\n{\"ref\": \"CR-54322\", \"lead\": \"Sasha Okonkwo\", \"person\": \"Liam\"}",
  "question": "For Sorrenby Island Family Payment, does Kenji Douglas fail to secure the right to claim Liam under these rules?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Liam lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa3b8aebeee",
  "kind": "choice",
  "text": "Dani Ishikawa: cheers, the staff support desk has HR-07286 for Zaid Dragic.\n\nIntake interview with Zaid Dragic (2025):\nCaseworker: Time employed?\nZaid Dragic: 16 months.\nCaseworker: Hours worked in the past year?\nZaid Dragic: 1,685 hours.\nCaseworker: Employees at your worksite?\nZaid Dragic: 36 employees.\nCaseworker: Gross annual pay?\nZaid Dragic: $64,026.94.\nCaseworker: Take-home annual pay?\nZaid Dragic: $48,492.65.\nCaseworker: Other programme enrolled in?\nZaid Dragic: Myrren Study Grant.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly beneath $52,000.\n- Gate B: passed when hours worked in the past year are above 1,130 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Zaid Dragic to Quenhollow Brewery Bereavement Leave?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q74cdf315d3",
  "kind": "choice",
  "text": "Facts for Nadia Vasquez (2025):\n| fact | value |\n| --- | --- |\n| time employed | 105 months |\n| hours worked in the past year | 710 hours |\n| employees at the worksite | 226 employees |\n| gross annual pay | 34,676.03 USD |\n| take-home annual pay | 24,315.61 USD |\n| enrolled in | Stonevale Staff Nursery Grant |\n\nSasha Okonkwo: Quick call from the district office on case HR-25024 for Nadia Vasquez.",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are higher than 710 hours.\n- Gate B: passed when take-home annual pay is lower than $52,500.\n- Route: an applicant enrolled in Stonevale Staff Nursery Grant skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Nadia Vasquez to Orrendale Printworks Sick Leave Supplement get under these rules?",
  "options": [
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q963226091f",
  "kind": "choice",
  "text": "Case note: Adi Chandra covers case CASE-08226 for Kwame Hoffman, with thanks.\n\nFacts for Kwame Hoffman (2026):\n- gross monthly income: $1,411.75\n- net monthly income: $1,203.74\n- countable assets: $7,705.30\n- time in the service area: 8 months\n- age: 61 years\n- enrolled in: Hemmerly Nursery Place Fund",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly higher than 62 years.\n- Gate B: passed when the applicant has lived in the service area for strictly more than 7 months.\n- Route: an applicant enrolled in Hemmerly Nursery Place Fund skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Kwame Hoffman to Corrivale Valley Childcare Grant land?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "qaabfd39417",
  "kind": "choice",
  "text": "[outreach] file=CR-76263 handled_by=Cameron Vargas\n[about] subject=Ada\n\nPeople who asked to claim Ada (2026):\n| person | relationship to Ada | months lived with Ada | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Viktor Gashi | grandfather | 9 months | 50,017.00 USD | yes |\n| Amara Anderson | aunt | 11 months | 50,017.00 USD | no |\n| Dmitri Vasquez | father | 6 months | 50,042.00 USD | yes |",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for greater than or equal to 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Ada for Ferrowby Forest Credit?",
  "options": [
   "Viktor Gashi",
   "Dmitri Vasquez"
  ]
 },
 {
  "qid": "qa5f889d63e",
  "kind": "choice",
  "text": "Dani Ishikawa: quick update, case HR-25717 is up for Anton Delgado.\n\nFacts for Anton Delgado (2027):\n- time employed: 17 months\n- hours worked in the past year: 224 hours\n- employees at the worksite: 82 employees\n- gross annual pay: 33,723.23 USD\n- take-home annual pay: 24,659.11 USD\n- enrolled in: none",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has larger than 56 employees.\n- Gate B: passed when take-home annual pay is strictly under the amount of 44,500.00 USD.\n- Gate C: passed when the applicant has been employed for strictly higher than 16 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Anton Delgado to Marrowby Bakery Family Leave produce?",
  "options": [
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "q5f4e63462f",
  "kind": "choice",
  "text": "People who asked to claim Joon (2026):\n| person | relationship to Joon | months lived with Joon | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Leila Russell | mother | 3 months | $32,423 | yes |\n| Matias Ruiz | father | 7 months | $77,526 | no |\n\nCase file intake form\nCase reference: CR-43930\nCaseworker: Ren Dvorak\nAbout: Joon",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for greater than or equal to 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Joon lived for more months comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Joon for Farrowby Moorland Parish Credit?",
  "options": [
   "Leila Russell",
   "Nobody may claim the child",
   "Matias Ruiz"
  ]
 },
 {
  "qid": "q44b0cfa78e",
  "kind": "choice",
  "text": "{\"case\": \"HR-82429\", \"caseworker\": \"Emi Figueroa\", \"about\": \"Pavel Zielinski\", \"team\": \"outreach\"}\n\nIntake interview with Pavel Zielinski (2026):\nCaseworker: Time employed?\nPavel Zielinski: 14 months.\nCaseworker: Hours worked in the past year?\nPavel Zielinski: 1141 hours.\nCaseworker: Employees at your worksite?\nPavel Zielinski: 19 employees.\nCaseworker: Gross annual pay?\nPavel Zielinski: $26,896.19.\nCaseworker: Take-home annual pay?\nPavel Zielinski: $24,197.04.\nCaseworker: Other programme enrolled in?\nPavel Zielinski: Osterlin Tool Allowance.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or over 20 employees.\n- Gate B: passed when hours worked in the past year are 1210 hours or greater.\n- Gate C: passed when take-home annual pay is strictly under the value of $29,500.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Pavel Zielinski to Brenwold Timber Apprentice Support get?",
  "options": [
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "q0cf75cd98d",
  "kind": "yes/no",
  "text": "Facts for Kofi Fujimoto (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,115.47 USD |\n| net monthly income | 3,570.41 USD |\n| countable assets | 10,517.22 USD |\n| time in the service area | five months |\n| age | 48 years |\n| enrolled in | Brunsley Energy Rebate |\n\nteam: casework\ncase: CASE-23228\ncaseworker: Ezra Rosales\nabout: Kofi Fujimoto",
  "question": "Going by the listed rules, is Kofi Fujimoto ineligible for Sallowick Ward Home Repair Grant?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is smaller than 2,850.00 USD.\n- Gate B: passed when the applicant has lived in the service area for equal to or greater than six months.\n- Gate C: passed when countable assets are 7,500.00 USD or lower.\n- Route: an applicant enrolled in Brunsley Energy Rebate skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd7c1ba2219",
  "kind": "yes/no",
  "text": "People who asked to claim Pia (2026):\n| person | relationship to Pia | months lived with Pia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Juliana Hakimi | mother | 7 months | 58,888.41 USD | yes |\n| Hamid Reynolds | father | 12 months | 58,888.41 USD | yes |\n| Tariq Dlamini | uncle | 12 months | 17,103.39 USD | yes |\n\nCase note: thanks for your patience. Blair Xiong has CR-06391 in hand for Pia.",
  "question": "Going by the listed rules, is Hamid Reynolds the person who secures the right to claim Pia for Sorrenby Island Family Payment?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for strictly in excess of 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Pia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q28fe9afc1a",
  "kind": "yes/no",
  "text": "District office intake form\nCase reference: CR-22468\nHandled by: Lior Grigoryan\nAbout: Remi\n\nPeople who asked to claim Remi (2026):\n| person | relationship to Remi | months lived with Remi | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kavita Tanaka | aunt | 0 months | $86,550 | yes |\n| Rania Reynolds | mother | 10 months | $73,480.52 | yes |\n| Mateo Zielinski | grandfather | 11 months | $47,280 | yes |",
  "question": "According to these rules, is Rania Reynolds the person who ends up with the right to claim Remi for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2026: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for at or beyond 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Remi lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q000e69710a",
  "kind": "choice",
  "text": "Records desk note. Dani Ishikawa keeps CASE-22007, which concerns Yuki Bergstrom.\n\nFacts for Yuki Bergstrom (2027):\n- gross monthly income: $2,403.39\n- net monthly income: $2,060.00\n- countable assets: $11,449.99\n- time in the service area: 18 months\n- age: 65 years\n- enrolled in: Vellmar Transit Pass",
  "question": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or below $2,060.00.\n- Gate B: passed when the applicant's age is 65 years or above.\n- Gate C: passed when countable assets are strictly lower than $11,450.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Yuki Bergstrom on the application to Ostmere Lakeside Winter Energy Support?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate C is the reason (countable assets)"
  ]
 },
 {
  "qid": "qefe12969ac",
  "kind": "yes/no",
  "text": "People who asked to claim Eva (2027):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Waleed Robinson | grandfather | 5 months | $20,077.02 | yes |\n| Greta Delgado | aunt | 10 months | $49,198 | yes |\n| Freya Nakamura | grandmother | 0 months | $44,183 | yes |\n| Hamid Rahimi | father | 9 months | $49,198 | yes |\n\n[desk_sweep] ref=CR-92244 by=Morgan Mendoza subject=Eva",
  "question": "Does Waleed Robinson end up as the sole person who may claim Eva for Farrowby Moorland Parish Credit?",
  "definitions": "Farrowby Moorland Parish Credit rules for 2027: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for in excess of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf7020dca1e",
  "kind": "choice",
  "text": "People who asked to claim Zara (2026), as JSON:\n{\"people\": [{\"name\": \"Sofia Johnson\", \"relationship\": \"mother\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"$27,723\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Tomas Anderson\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"3 months\", \"annual_income\": \"$53,225\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Pavel Johnson\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"7 months\", \"annual_income\": \"$86,452\", \"filed_a_claim\": \"yes\"}]}\n\n{\"caseworker\": \"Toni Lazar\", \"about\": \"Zara\", \"case\": \"CR-97625\", \"desk\": \"community\"}",
  "question": "Mollenby Canal Child Supplement rules for 2026: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for strictly above 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Zara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Zara for Mollenby Canal Child Supplement?",
  "options": [
   "Sofia Johnson",
   "Pavel Johnson",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q8498a6cb02",
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
  "qid": "q674977c7ca",
  "kind": "choice",
  "text": "Dear Liam,\nPlease find CR-02406 logged with the help line team.\nYours faithfully, Emi Figueroa\n\nInterview notes for Liam (2027):\nCaseworker: Emeka Bergstrom, your relation to Liam?\nEmeka Bergstrom: I am Liam's father.\nCaseworker: Months Liam lived with you?\nEmeka Bergstrom: twelve months.\nCaseworker: Annual income?\nEmeka Bergstrom: $62,025.00.\nCaseworker: Filed a claim for Liam?\nEmeka Bergstrom: yes.\nCaseworker: Nkechi Anderson, your relation to Liam?\nNkechi Anderson: I am Liam's aunt.\nCaseworker: Months Liam lived with you?\nNkechi Anderson: seven months.\nCaseworker: Annual income?\nNkechi Anderson: $64,319.24.\nCaseworker: Filed a claim for Liam?\nNkechi Anderson: yes.\nCaseworker: Tomas Gashi, your relation to Liam?\nTomas Gashi: I am Liam's grandfather.\nCaseworker: Months Liam lived with you?\nTomas Gashi: eleven months.\nCaseworker: Annual income?\nTomas Gashi: $75,315.00.\nCaseworker: Filed a claim for Liam?\nTomas Gashi: yes.",
  "question": "Gristmere Child Credit rules for 2027: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for five months at minimum in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Liam lived for more months comes first.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Liam for Gristmere Child Credit under these rules?",
  "options": [
   "Tomas Gashi",
   "Emeka Bergstrom",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qe66092b584",
  "kind": "choice",
  "text": "case: HR-56391\nlead: Avery Obradovic\nperson: Rania Abebe\n\nFacts for Rania Abebe (2026):\n- time employed: 29 months\n- hours worked in the past year: 128 hours\n- employees at the worksite: 74 employees\n- gross annual pay: $57,500.01\n- take-home annual pay: $41,499.99\n- enrolled in: Caddowen Veterans Pathway",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or below $57,500.00.\n- Gate B: passed when take-home annual pay is $41,500.00 or less.\n- Gate C: passed when the worksite has equal to or greater than 75 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Rania Abebe to Morrowdene Hospital Group Return Support receive?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q97b3de86a8",
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
  "qid": "qab04aed6a9",
  "kind": "choice",
  "text": "Work ticket CASE-61035\nLogged by: Morgan Mendoza\nAbout: Kazu Douglas\n\nFacts for Kazu Douglas (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,614.89 USD |\n| net monthly income | 2,852.14 USD |\n| countable assets | 7,599.99 USD |\n| time in the service area | 25 months |\n| age | 26 years |\n| enrolled in | Hallowby Utility Discount |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the amount of 7,600.00 USD.\n- Gate B: passed when the applicant's age is greater than 63 years.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Kazu Douglas to Tesslow Prairie Water Bill Assistance land?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (countable assets)"
  ]
 },
 {
  "qid": "qed5cdef01d",
  "kind": "yes/no",
  "text": "[branch_queue] case=CR-80501 by=Emi Figueroa about=Mia\n\nPeople who asked to claim Mia (2025):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gabriel Johnson | father | seven months | $94,171.00 | yes |\n| Wanjiru Mwangi | aunt | six months | $91,707.00 | yes |\n| Fatima Petrov | mother | eight months | $54,035.00 | no |\n| Tamar Murphy | grandmother | ten months | $51,540.10 | yes |",
  "question": "Following the listed rules, is Gabriel Johnson the person who winds up with the claim on Mia for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2025: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for at or greater than five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Mia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q73960ecc86",
  "kind": "yes/no",
  "text": "Work ticket HR-92224\nLogged by: Ezra Rosales\nAbout: Hugo Gallegos\n\nIntake interview with Hugo Gallegos (2025):\nCaseworker: Time employed?\nHugo Gallegos: 59 months.\nCaseworker: Hours worked in the past year?\nHugo Gallegos: 1,160 hours.\nCaseworker: Employees at your worksite?\nHugo Gallegos: 321 employees.\nCaseworker: Gross annual pay?\nHugo Gallegos: $56,832.31.\nCaseworker: Take-home annual pay?\nHugo Gallegos: $37,979.08.\nCaseworker: Other programme enrolled in?\nHugo Gallegos: Quendrel Skills Voucher.",
  "question": "Does Hugo Gallegos fail to qualify for Brenwold Timber Apprentice Support under these rules?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $43,500.00.\n- Gate B: passed when hours worked in the past year are equal to or greater than 1,160 hours.\n- Gate C: passed when take-home annual pay is strictly under the amount of $33,000.00.\n- Route: an applicant enrolled in Quendrel Skills Voucher skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4cae3bf547",
  "kind": "yes/no",
  "text": "Hi team,\nThanks for waiting, CR-24666 about Lara is in good hands.\nWarm wishes, Kendall Umarov\n\nPeople who asked to claim Lara (2027):\n- Amara Lindqvist: relationship to Lara: mother; months lived with Lara: 6 months; annual income: 76,364.00 USD; filed a claim: yes\n- Zainab Gallegos: relationship to Lara: aunt; months lived with Lara: 12 months; annual income: 76,364.00 USD; filed a claim: yes",
  "question": "For Ferrowby Forest Credit, is Amara Lindqvist the person who is left holding the right to claim Lara?",
  "definitions": "Ferrowby Forest Credit rules for 2027: who may claim Lara.\n- Only one person may claim Lara. Work through these steps in order.\n- Step one: only people who filed a claim for Lara are considered.\n- Step two: of those, only people with whom Lara lived for in excess of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Lara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Lara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q66a7ed027a",
  "kind": "choice",
  "text": "Dear Idris Okafor,\nThis concerns case HR-41875 with the outreach team.\nYours faithfully, Nika Hernandez\n\nFacts for Idris Okafor (2026):\n- time employed: six months\n- hours worked in the past year: 1,361 hours\n- employees at the worksite: 61 employees\n- gross annual pay: 50,656.25 USD\n- take-home annual pay: 44,500.00 USD\n- enrolled in: Sarrowby Mentor Stipend",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is smaller than 44,500.00 USD.\n- Gate B: passed when the worksite has at or over 42 employees.\n- Gate C: passed when the applicant has been employed for strictly greater than eight months.\n- Route: an applicant enrolled in Sarrowby Mentor Stipend skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Idris Okafor to Hallowdene Logistics Study Grant receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (employees at the worksite)"
  ]
 }
]
