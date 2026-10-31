# G5-H blind read T15-blind_read-619ba0ed-001 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t15/gen_root/T15/qc/g5h/answers/T15-blind_read-619ba0ed-001.json

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
  "qid": "qbd126dde51",
  "kind": "yes/no",
  "text": "[case_file] ref=HR-11043 worker=Avery Obradovic\n[about] subject=Ubah Johnson\n\nIntake interview with Ubah Johnson (2025):\nCaseworker: Time employed?\nUbah Johnson: 27 months.\nCaseworker: Hours worked in the past year?\nUbah Johnson: 512 hours.\nCaseworker: Employees at your worksite?\nUbah Johnson: 99 employees.\nCaseworker: Gross annual pay?\nUbah Johnson: $28,623.30.\nCaseworker: Take-home annual pay?\nUbah Johnson: $21,294.67.\nCaseworker: Other programme enrolled in?\nUbah Johnson: Quelmere Lunch Card.",
  "question": "Going by the listed rules, is Ubah Johnson ineligible for Sorrelby Child Care Support?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for higher than sixteen months.\n- Gate B: passed when the worksite has strictly above 74 employees.\n- Gate C: passed when take-home annual pay is strictly smaller than $45,293.75.\n- Route: an applicant enrolled in Quelmere Lunch Card skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa360e0a295",
  "kind": "choice",
  "text": "Case note: Shay Bekele is glad to take on the matter of Joon, reference CR-37261.\n\nPeople who asked to claim Joon (2027):\n- Elias Campbell: relationship to Joon: father; months lived with Joon: 9 months; annual income: 82,026.00 USD; filed a claim: no\n- Nadia Kovacs: relationship to Joon: mother; months lived with Joon: 2 months; annual income: 38,615.00 USD; filed a claim: yes\n- Amara Murphy: relationship to Joon: aunt; months lived with Joon: 10 months; annual income: 50,369.00 USD; filed a claim: yes",
  "question": "Kelvery Market Credit rules for 2027: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for above 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Joon lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Joon for Kelvery Market Credit?",
  "options": [
   "Elias Campbell",
   "Amara Murphy"
  ]
 },
 {
  "qid": "q3a60e9e5c3",
  "kind": "choice",
  "text": "{\"team\": \"casework\", \"case_ref\": \"CASE-29955\", \"worker\": \"Avery Obradovic\", \"about\": \"Kiran Jovanovic\"}\n\nIntake interview with Kiran Jovanovic (2026):\nCaseworker: Gross monthly income?\nKiran Jovanovic: $3,407.29.\nCaseworker: Net monthly income?\nKiran Jovanovic: $2,209.90.\nCaseworker: Countable assets?\nKiran Jovanovic: $17,721.28.\nCaseworker: Time in the service area?\nKiran Jovanovic: 7 months.\nCaseworker: Age?\nKiran Jovanovic: 22 years.\nCaseworker: Other programme enrolled in?\nKiran Jovanovic: Quenmoor Emergency Fund.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for greater than or equal to 3 months.\n- Gate B: passed when net monthly income is at or less than $2,209.89.\n- Gate C: passed when the applicant's age is strictly above 59 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Kiran Jovanovic to Ostermere Delta Flood Repair Support land?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qce69621ef4",
  "kind": "choice",
  "text": "Facts for Hugo Sokolov (2026):\n| fact | value |\n| --- | --- |\n| time employed | 18 months |\n| hours worked in the past year | 1505 hours |\n| employees at the worksite | 18 employees |\n| gross annual pay | 93,912.57 USD |\n| take-home annual pay | 59,273.12 USD |\n| enrolled in | Tallowmere Wellbeing Fund |\n\nQuinn Pavlenko: help line has Hugo Sokolov on HR-41993.",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has greater than 18 employees.\n- Gate B: passed when gross annual pay is at or under 63,609.73 USD.\n- Gate C: passed when hours worked in the past year are 1030 hours or above.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Hugo Sokolov for Orrendale Printworks Sick Leave Supplement come out?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate C is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q8ff354e9c1",
  "kind": "yes/no",
  "text": "reference: CR-10458\nhandler: Quinn Pavlenko\nsubject: Dara\n\nPeople who asked to claim Dara (2025):\n- Hiro Petrov: relationship to Dara: father; months lived with Dara: 12 months; annual income: 33,076.31 USD; filed a claim: yes\n- Sabine Zielinski: relationship to Dara: aunt; months lived with Dara: 0 months; annual income: 53,941.00 USD; filed a claim: no",
  "question": "Does the right to claim Dara for Tollmere Lakeside Family Payment pass to a different person from Hiro Petrov, or stay unclaimed under these rules?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2025: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for at or above 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q37af72285b",
  "kind": "yes/no",
  "text": "Internal note for the branch desk. HR-08537 rests with Avery Obradovic and concerns Priya Evans.\n\nFacts for Priya Evans (2026):\n- time employed: 76 months\n- hours worked in the past year: 1410 hours\n- employees at the worksite: 257 employees\n- gross annual pay: 75,190.17 USD\n- take-home annual pay: 62,070.49 USD\n- enrolled in: Fallowden Retraining Bursary",
  "question": "According to these rules, does Priya Evans qualify for Tovardine Seed Caregiver Leave?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or greater than 1410 hours.\n- Gate B: passed when take-home annual pay is strictly under the amount of 54,873.43 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3e5ef660b1",
  "kind": "yes/no",
  "text": "People who asked to claim Ali (2027):\n| person | relationship to Ali | months lived with Ali | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Elias Lindqvist | father | two months | $38,450 | no |\n| Priya Reynolds | aunt | nine months | $48,964 | yes |\n| Hiroko Okafor | mother | nine months | $30,697 | no |\n\nHi team,\nCase CR-41341 for Ali has gone to the desk.\nThanks, Kendall Umarov",
  "question": "According to these rules, does Priya Reynolds fail to earn a claim on Ali for Mollenby Canal Child Supplement?",
  "definitions": "Mollenby Canal Child Supplement rules for 2027: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for strictly higher than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ali lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf0af84deae",
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
  "qid": "q778804213e",
  "kind": "yes/no",
  "text": "Facts for Kofi Demir (2027), as JSON:\n{\"gross_monthly_income\": \"$3,636.90\", \"net_monthly_income\": \"$2,734.54\", \"countable_assets\": \"$17,853.04\", \"time_in_the_service_area\": \"51 months\", \"age\": \"83 years\", \"enrolled_in\": \"Velden Transit Badge\"}\n\n{\"record\": \"case\", \"reference\": \"CASE-09703\", \"caseworker\": \"Kendall Umarov\", \"about\": \"Kofi Demir\"}",
  "question": "Under these rules, does Kofi Demir meet the rules for Sallowick Ward Home Repair Grant across every applicable gate?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are equal to or below $11,962.62.\n- Gate B: passed when net monthly income is at or under $2,734.55.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7d00b36ec2",
  "kind": "choice",
  "text": "Case note: CASE-93775 for Kiran Nilsen. Handled by Alex Lindgren.\n\nIntake interview with Kiran Nilsen (2027):\nCaseworker: Gross monthly income?\nKiran Nilsen: $3,502.57.\nCaseworker: Net monthly income?\nKiran Nilsen: $2,179.14.\nCaseworker: Countable assets?\nKiran Nilsen: $2,943.22.\nCaseworker: Time in the service area?\nKiran Nilsen: nine months.\nCaseworker: Age?\nKiran Nilsen: 80 years.\nCaseworker: Other programme enrolled in?\nKiran Nilsen: Kelmstone Drainage Subsidy.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or less than $2,195.23.\n- Gate B: passed when the applicant has lived in the service area for at or over nine months.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Kiran Nilsen for Ostermere Delta Flood Repair Support come out?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q9b63057fbb",
  "kind": "yes/no",
  "text": "[help_line] case_ref=CR-41711 staff=Shay Bekele about=Gia\n\nInterview notes for Gia (2026):\nCaseworker: Kiara Moreau, your relation to Gia?\nKiara Moreau: I am Gia's mother.\nCaseworker: Months Gia lived with you?\nKiara Moreau: 9 months.\nCaseworker: Annual income?\nKiara Moreau: $16,923.65.\nCaseworker: Filed a claim for Gia?\nKiara Moreau: yes.\nCaseworker: Kenji Esposito, your relation to Gia?\nKenji Esposito: I am Gia's grandfather.\nCaseworker: Months Gia lived with you?\nKenji Esposito: 5 months.\nCaseworker: Annual income?\nKenji Esposito: $90,467.00.\nCaseworker: Filed a claim for Gia?\nKenji Esposito: yes.\nCaseworker: Priya Gutierrez, your relation to Gia?\nPriya Gutierrez: I am Gia's aunt.\nCaseworker: Months Gia lived with you?\nPriya Gutierrez: 1 month.\nCaseworker: Annual income?\nPriya Gutierrez: $23,925.00.\nCaseworker: Filed a claim for Gia?\nPriya Gutierrez: yes.\nCaseworker: Hiro Yamazaki, your relation to Gia?\nHiro Yamazaki: I am Gia's uncle.\nCaseworker: Months Gia lived with you?\nHiro Yamazaki: 10 months.\nCaseworker: Annual income?\nHiro Yamazaki: $28,218.00.\nCaseworker: Filed a claim for Gia?\nHiro Yamazaki: no.",
  "question": "Under these rules, does Kiara Moreau fail to gain the right to claim Gia for Stonevale Delta Child Allowance?",
  "definitions": "Stonevale Delta Child Allowance rules for 2026: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for at or over 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Gia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qbf4250d599",
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
  "qid": "qc94d70ee0c",
  "kind": "choice",
  "text": "Dear team,\nPlease see the attached summary on case CR-61106 for Uri.\nYours sincerely, Sasha Okonkwo\n\nPeople who asked to claim Uri (2027):\n- Leila Lindqvist: relationship to Uri: mother; months lived with Uri: zero months; annual income: $40,326.00; filed a claim: yes\n- Cyril Nguyen: relationship to Uri: father; months lived with Uri: six months; annual income: $83,835.00; filed a claim: yes\n- Bruno Reynolds: relationship to Uri: grandfather; months lived with Uri: seven months; annual income: $26,009.00; filed a claim: yes\n- Nadia Dragic: relationship to Uri: aunt; months lived with Uri: eleven months; annual income: $87,114.00; filed a claim: yes",
  "question": "Kelvery Market Credit rules for 2027: who may claim Uri.\n- Only one person may claim Uri. Work through these steps in order.\n- Step one: only people who filed a claim for Uri are considered.\n- Step two: of those, only people with whom Uri lived for six months or more in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Uri lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Uri.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, has the right to claim Uri for Kelvery Market Credit?",
  "options": [
   "Nadia Dragic",
   "Leila Lindqvist",
   "Cyril Nguyen"
  ]
 },
 {
  "qid": "qa8f492a42c",
  "kind": "yes/no",
  "text": "Facts for Nika Mensah (2025):\n| fact | value |\n| --- | --- |\n| time employed | 84 months |\n| hours worked in the past year | 1389 hours |\n| employees at the worksite | 40 employees |\n| gross annual pay | 68,557.20 USD |\n| take-home annual pay | 31,834.44 USD |\n| enrolled in | Tallowmere Wellbeing Fund |\n\nCase note: Kiran Morales holds case file HR-83245 about Nika Mensah. The record sits at the town hall desk.",
  "question": "Following the listed rules, is Nika Mensah not eligible for Orrendale Printworks Sick Leave Supplement?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly higher than 32 employees.\n- Gate B: passed when take-home annual pay is strictly under the value of 31,834.44 USD.\n- Gate C: passed when gross annual pay is at or less than 43,493.69 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe5ed668c47",
  "kind": "choice",
  "text": "Ticket: staff support desk, case HR-27201\nFrom: Alex Lindgren\nAbout: Farid Johnson\n\nFacts for Farid Johnson (2025):\n| fact | value |\n| --- | --- |\n| time employed | 23 months |\n| hours worked in the past year | 1,803 hours |\n| employees at the worksite | 63 employees |\n| gross annual pay | 34,526.56 USD |\n| take-home annual pay | 24,624.07 USD |\n| enrolled in | Corranmere Flexi Hours |",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or above 46 employees.\n- Gate B: passed when the applicant has been employed for seventeen months or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Farid Johnson to Marrowby Bakery Family Leave receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "q60f873ca05",
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
  "qid": "q03d0ec9eea",
  "kind": "yes/no",
  "text": "[help_desk_entry] ref=CR-99689 by=Blair Xiong about=Ines\n\nPeople who asked to claim Ines (2025):\n| person | relationship to Ines | months lived with Ines | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kwame Kelly | uncle | 4 months | $51,380.85 | no |\n| Mirela Gallegos | mother | 5 months | $36,317 | yes |",
  "question": "According to these rules, is Mirela Gallegos the person who ends up holding the right to claim Ines for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2025: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for 6 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ines lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc864c9e79a",
  "kind": "choice",
  "text": "Service intake form\nCase reference: CR-74585\nCaseworker: Yuki Adeyemi\nAbout: Vida\n\nInterview notes for Vida (2025):\nCaseworker: Anjali Sokolov, your relation to Vida?\nAnjali Sokolov: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nAnjali Sokolov: 3 months.\nCaseworker: Annual income?\nAnjali Sokolov: 92,293.79 USD.\nCaseworker: Filed a claim for Vida?\nAnjali Sokolov: yes.\nCaseworker: Mirela Mwangi, your relation to Vida?\nMirela Mwangi: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nMirela Mwangi: 11 months.\nCaseworker: Annual income?\nMirela Mwangi: 76,578.00 USD.\nCaseworker: Filed a claim for Vida?\nMirela Mwangi: yes.\nCaseworker: Bruno Reynolds, your relation to Vida?\nBruno Reynolds: I am Vida's uncle.\nCaseworker: Months Vida lived with you?\nBruno Reynolds: 7 months.\nCaseworker: Annual income?\nBruno Reynolds: 83,266.00 USD.\nCaseworker: Filed a claim for Vida?\nBruno Reynolds: yes.\nCaseworker: Vesna Halvorsen, your relation to Vida?\nVesna Halvorsen: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nVesna Halvorsen: 5 months.\nCaseworker: Annual income?\nVesna Halvorsen: 52,869.00 USD.\nCaseworker: Filed a claim for Vida?\nVesna Halvorsen: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2025: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for in excess of 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Vida for Stonevale Delta Child Allowance?",
  "options": [
   "Mirela Mwangi",
   "Bruno Reynolds",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qfcad7520f7",
  "kind": "choice",
  "text": "Case note: CR-66147 sits with Toni Lazar and concerns Ana.\n\nPeople who asked to claim Ana (2025):\n- Greta Haddad: relationship to Ana: grandmother; months lived with Ana: 10 months; annual income: $82,799; filed a claim: no\n- Yasmin Ivanova: relationship to Ana: aunt; months lived with Ana: 4 months; annual income: $82,799; filed a claim: yes\n- Elias Kowalski: relationship to Ana: grandfather; months lived with Ana: 1 month; annual income: $26,121; filed a claim: no",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for 5 months or above in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, can claim Ana for Tessenvale Valley Child Credit under these rules?",
  "options": [
   "Yasmin Ivanova",
   "Greta Haddad",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qb6e7bafde9",
  "kind": "choice",
  "text": "case_ref: HR-71945\nhandler: Riley Watanabe\nsubject: Olena Abebe\nclass: file\n\nFacts for Olena Abebe (2025):\n- time employed: twelve months\n- hours worked in the past year: 308 hours\n- employees at the worksite: 48 employees\n- gross annual pay: $87,228.14\n- take-home annual pay: $70,349.74\n- enrolled in: Pratchell Caregiver Stipend",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of $87,228.14.\n- Gate B: passed when take-home annual pay is strictly lower than $70,349.75.\n- Gate C: passed when the worksite has strictly in excess of 47 employees.\n- Gate D: passed when the applicant has been employed for twelve months or greater.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Olena Abebe to Wendmoor Mill Parental Leave gets which outcome?",
  "options": [
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate D is the reason (time employed)",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qe66593f2ab",
  "kind": "choice",
  "text": "People who asked to claim Theo (2026):\n| person | relationship to Theo | months lived with Theo | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Cyril Delgado | father | 6 months | $68,983 | yes |\n| Rania Sorensen | grandmother | 10 months | $49,496 | yes |\n| Hiroko Choi | aunt | 0 months | 52,291.27 USD | yes |\n\nDear colleague,\nThis is a short outreach note on case CR-57391 for Theo.\nRegards, Nika Hernandez",
  "question": "Mollenby Canal Child Supplement rules for 2026: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for 6 months or more in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Theo lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Theo for Mollenby Canal Child Supplement under these rules?",
  "options": [
   "Cyril Delgado",
   "Rania Sorensen"
  ]
 },
 {
  "qid": "q9296162d2b",
  "kind": "yes/no",
  "text": "Services counter intake form\nCase reference: CR-37995\nCaseworker: Sasha Okonkwo\nAbout: Kai\n\nPeople who asked to claim Kai (2027):\n| person | relationship to Kai | months lived with Kai | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Zainab Rahimi | mother | zero months | 43,566.77 USD | no |\n| Jiro Hamilton | father | seven months | $24,273 | yes |\n| Dmitri Kimura | grandfather | nine months | $44,575 | yes |",
  "question": "According to these rules, is Jiro Hamilton the person who ends up with the right to claim Kai for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for strictly greater than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Kai lived for more months comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q503a57d1b4",
  "kind": "yes/no",
  "text": "Call centre ticket: CR-55672\nRaised by: Kazu Yousef\nAbout: Ada\n\nPeople who asked to claim Ada (2025):\n| person | relationship to Ada | months lived with Ada | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ilse Sharma | aunt | 5 months | $60,442.00 | yes |\n| Yasmin Haddad | mother | 7 months | $70,068.00 | yes |\n| Imani Hoffman | grandmother | 11 months | $75,323.00 | yes |",
  "question": "Under these rules, is it true that Yasmin Haddad may not claim Ada for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2025: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for equal to or greater than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8837cecd73",
  "kind": "yes/no",
  "text": "case_ref: HR-50887\nlead: Alex Lindgren\nperson: Gustav Stewart\n\nFacts for Gustav Stewart (2026):\n- time employed: 98 months\n- hours worked in the past year: 263 hours\n- employees at the worksite: 81 employees\n- gross annual pay: $66,514.14\n- take-home annual pay: $50,593.06\n- enrolled in: Corrivale Welding Bursary",
  "question": "For Halvorne Shipyard Tuition Assistance, does Gustav Stewart qualify under the listed rules?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 48 employees or above.\n- Gate B: passed when gross annual pay is $50,645.07 at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7a40438c6c",
  "kind": "choice",
  "text": "Note for CASE-11159, with thanks.\nTomi Eklund is looking after Sami Douglas at the district office.\n\nIntake interview with Sami Douglas (2026):\nCaseworker: Gross monthly income?\nSami Douglas: 2,999.09 USD.\nCaseworker: Net monthly income?\nSami Douglas: 1,978.73 USD.\nCaseworker: Countable assets?\nSami Douglas: 8,588.78 USD.\nCaseworker: Time in the service area?\nSami Douglas: five months.\nCaseworker: Age?\nSami Douglas: 70 years.\nCaseworker: Other programme enrolled in?\nSami Douglas: Ulverby Summer Meals.",
  "question": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly over four months.\n- Gate B: passed when countable assets are smaller than 8,778.36 USD.\n- Gate C: passed when the applicant's age is at or over 56 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Sami Douglas to Fennick School Meal Supplement produce?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (countable assets)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (age)"
  ]
 },
 {
  "qid": "q3bbe8eb9e9",
  "kind": "choice",
  "text": "case_ref: CASE-26780\nhandler: Toni Lazar\nsubject: Ivo Kowalski\nclass: file\n\nIntake interview with Ivo Kowalski (2027):\nCaseworker: Gross monthly income?\nIvo Kowalski: $2,136.58.\nCaseworker: Net monthly income?\nIvo Kowalski: $1,387.87.\nCaseworker: Countable assets?\nIvo Kowalski: $8,596.43.\nCaseworker: Time in the service area?\nIvo Kowalski: 59 months.\nCaseworker: Age?\nIvo Kowalski: 60 years.\nCaseworker: Other programme enrolled in?\nIvo Kowalski: Brindlemoor Repair Fund.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is equal to or below $2,670.10.\n- Gate B: passed when countable assets are at or below the level of $5,851.\n- Gate C: passed when the applicant's age is at or greater than 61 years.\n- Route: an applicant enrolled in Brindlemoor Repair Fund skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Ivo Kowalski to Tamsfell Senior Home Support resolved?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (countable assets)"
  ]
 },
 {
  "qid": "qb187ab0046",
  "kind": "yes/no",
  "text": "Morgan Mendoza: hi team, thread for CASE-15748 covers Freya Iyer, thanks!\n\nIntake interview with Freya Iyer (2027):\nCaseworker: Gross monthly income?\nFreya Iyer: 2,852.20 USD.\nCaseworker: Net monthly income?\nFreya Iyer: 1,802.27 USD.\nCaseworker: Countable assets?\nFreya Iyer: 17,515.26 USD.\nCaseworker: Time in the service area?\nFreya Iyer: 8 months.\nCaseworker: Age?\nFreya Iyer: 75 years.\nCaseworker: Other programme enrolled in?\nFreya Iyer: Ormsby Housing Plan.",
  "question": "Is Freya Iyer eligible for Fennick School Meal Supplement with every applicable gate passed?",
  "definitions": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or below 1,802.26 USD.\n- Gate B: passed when the applicant has lived in the service area for strictly higher than 7 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe809407860",
  "kind": "choice",
  "text": "Ezra Rosales: case reference CASE-06747 is held for Nika Murphy.\n\nIntake interview with Nika Murphy (2025):\nCaseworker: Gross monthly income?\nNika Murphy: 4,430.06 USD.\nCaseworker: Net monthly income?\nNika Murphy: 3,235.12 USD.\nCaseworker: Countable assets?\nNika Murphy: 8,394.14 USD.\nCaseworker: Time in the service area?\nNika Murphy: 52 months.\nCaseworker: Age?\nNika Murphy: 59 years.\nCaseworker: Other programme enrolled in?\nNika Murphy: Ormsby Housing Aid.",
  "question": "Fennick School Meal Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or below the level of 8,394.14 USD.\n- Gate B: passed when net monthly income is equal to or below 2,887.80 USD.\n- Gate C: passed when the applicant's age is greater than 58 years.\n- Gate D: passed when gross monthly income is at or under the amount of 4,027.40 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Nika Murphy to Fennick School Meal Supplement lead to?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate D is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate C is the reason (age)"
  ]
 },
 {
  "qid": "q4ddf02a616",
  "kind": "choice",
  "text": "Facts for Yasmin Demir (2025):\n| fact | value |\n| --- | --- |\n| time employed | 27 months |\n| hours worked in the past year | 859 hours |\n| employees at the worksite | 270 employees |\n| gross annual pay | 63,261.63 USD |\n| take-home annual pay | 47,435.81 USD |\n| enrolled in | Stonevale Staff Nursery Grant |\n\nRecords desk note. Yuki Adeyemi keeps HR-88182, which concerns Yasmin Demir.",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or greater than 23 months.\n- Gate B: passed when hours worked in the past year are 860 hours or more.\n- Gate C: passed when take-home annual pay is at or beneath 39,563.38 USD.\n- Route: an applicant enrolled in Stonevale Staff Nursery Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Yasmin Demir to Orrendale Printworks Sick Leave Supplement receive?",
  "options": [
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q59a25f9165",
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
  "qid": "q00f122d8da",
  "kind": "yes/no",
  "text": "Ticket: regional case record HR-99450\nRaised by: Lior Grigoryan\nAbout: Imani Hoffman\n\nFacts for Imani Hoffman (2025):\n| fact | value |\n| --- | --- |\n| time employed | 31 months |\n| hours worked in the past year | 1699 hours |\n| employees at the worksite | 75 employees |\n| gross annual pay | $25,619.00 |\n| take-home annual pay | $18,435.57 |\n| enrolled in | Selwick Fresh Crate |",
  "question": "Is Imani Hoffman really eligible for Marrowby Bakery Family Leave under these rules?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 74 employees at minimum.\n- Gate B: passed when hours worked in the past year are at or greater than 1220 hours.\n- Gate C: passed when gross annual pay is strictly below $44,660.14.\n- Route: an applicant enrolled in Corranmere Flexi Hours skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qef836622d5",
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
  "qid": "q7f49e1b14a",
  "kind": "choice",
  "text": "case_ref: HR-48777\nworker: Mika Zamora\nsubject: Quinn Dubois\n\nFacts for Quinn Dubois (2026):\n- time employed: 116 months\n- hours worked in the past year: 1,070 hours\n- employees at the worksite: 109 employees\n- gross annual pay: $119,717.06\n- take-home annual pay: $63,750.22\n- enrolled in: Dunnamore Retraining Bonus",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is $63,750.21 or lower.\n- Gate B: passed when hours worked in the past year are strictly in excess of 1,070 hours.\n- Gate C: passed when gross annual pay is smaller than $86,820.10.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Quinn Dubois to Wendmoor Mill Parental Leave receive?",
  "options": [
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qb930421dec",
  "kind": "yes/no",
  "text": "{\"ref\": \"CR-07664\", \"handled_by\": \"Quinn Pavlenko\", \"about\": \"Kai\", \"setting\": \"walk-in\"}\n\nPeople who asked to claim Kai (2025), as JSON:\n{\"people\": [{\"name\": \"Nikolai Dubois\", \"relationship\": \"father\", \"months_lived_with_child\": \"7 months\", \"annual_income\": \"74,121.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Yasmin Mitchell\", \"relationship\": \"mother\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"86,364.00 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Pavel Nakamura\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"86,364.00 USD\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Following the listed rules, does Nikolai Dubois fail to win the right to claim Kai for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for 6 months or above in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q08932a6dcc",
  "kind": "yes/no",
  "text": "reference: HR-41566\nhandler: Kendall Umarov\nsubject: Kiran Kovacs\n\nFacts for Kiran Kovacs (2027):\n- time employed: 111 months\n- hours worked in the past year: 1,945 hours\n- employees at the worksite: 226 employees\n- gross annual pay: 62,175.28 USD\n- take-home annual pay: 30,666.09 USD\n- enrolled in: Quillmere Apprentice Pilot",
  "question": "Under these rules, does Kiran Kovacs fail to qualify for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of 62,175.29 USD.\n- Gate B: passed when take-home annual pay is equal to or below 45,273.69 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q991e810d93",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CASE-35915, handled by Quinn Pavlenko\n[subject_line] Priya Mensah is at the heart of it\n\nFacts for Priya Mensah (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $927.52 |\n| net monthly income | $711.89 |\n| countable assets | $6,970.43 |\n| time in the service area | 35 months |\n| age | 85 years |\n| enrolled in | none |",
  "question": "Does a gate that applies halt the application of Priya Mensah to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is a minimum of 67 years.\n- Gate B: passed when gross monthly income is strictly beneath the level of $1,938.19.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe1f8bc44c2",
  "kind": "yes/no",
  "text": "[busy_queue] case=CR-69539 worker=Dani Ishikawa subject=Finn\n\nPeople who asked to claim Finn (2026):\n| person | relationship to Finn | months lived with Finn | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hiro Ilunga | father | 8 months | 48,581.00 USD | no |\n| Waleed Douglas | uncle | 6 months | 79,541.00 USD | yes |",
  "question": "Under these rules, is Waleed Douglas excluded from claiming Finn for Ferrowby Forest Credit?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Finn.\n- Only one person may claim Finn. Work through these steps in order.\n- Step one: only people who filed a claim for Finn are considered.\n- Step two: of those, only people with whom Finn lived for strictly higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Finn lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Finn.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc4220010f4",
  "kind": "choice",
  "text": "Dear colleague,\nPlease see HR-54798 about Gustav Sorensen on the queue.\nThanks, Ezra Rosales\n\nFacts for Gustav Sorensen (2027):\n- time employed: 94 months\n- hours worked in the past year: 365 hours\n- employees at the worksite: 69 employees\n- gross annual pay: 75,438.33 USD\n- take-home annual pay: 55,995.09 USD\n- enrolled in: Rickmere Night School Fund",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has above 69 employees.\n- Gate B: passed when hours worked in the past year are higher than 880 hours.\n- Gate C: passed when take-home annual pay is strictly below the amount of 55,995.09 USD.\n- Route: an applicant enrolled in Rickmere Night Course Fund skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Gustav Sorensen to Hallowdene Logistics Study Grant resolved?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q0b31d19cfd",
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
  "qid": "q38873db6af",
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
  "qid": "qba786e4ae9",
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
  "qid": "qf89e663556",
  "kind": "yes/no",
  "text": "record: CASE-49260\nlead: Morgan Mendoza\nsubject: Anton Becker\n\nFacts for Anton Becker (2027):\n- gross monthly income: 3,104.16 USD\n- net monthly income: 1,341.33 USD\n- countable assets: 707.59 USD\n- time in the service area: 47 months\n- age: 69 years\n- enrolled in: Sallowby Water Rebate",
  "question": "Is Anton Becker eligible for Ostmere Lakeside Winter Energy Support with every applicable gate passed?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly under 1,969.51 USD.\n- Gate B: passed when the applicant's age is at or over 57 years.\n- Gate C: passed when net monthly income is at or less than 1,401.88 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe0cd9aa36a",
  "kind": "choice",
  "text": "Welcome to the community help desk\nCase reference: CR-44090\nCaseworker: Nika Hernandez\nPerson: Ana\n\nInterview notes for Ana (2026):\nCaseworker: Yusuf Rahimi, your relation to Ana?\nYusuf Rahimi: I am Ana's uncle.\nCaseworker: Months Ana lived with you?\nYusuf Rahimi: 6 months.\nCaseworker: Annual income?\nYusuf Rahimi: 67,424.00 USD.\nCaseworker: Filed a claim for Ana?\nYusuf Rahimi: no.\nCaseworker: Ravi Delgado, your relation to Ana?\nRavi Delgado: I am Ana's uncle.\nCaseworker: Months Ana lived with you?\nRavi Delgado: 6 months.\nCaseworker: Annual income?\nRavi Delgado: 21,296.00 USD.\nCaseworker: Filed a claim for Ana?\nRavi Delgado: yes.\nCaseworker: Ivo Becker, your relation to Ana?\nIvo Becker: I am Ana's father.\nCaseworker: Months Ana lived with you?\nIvo Becker: 5 months.\nCaseworker: Annual income?\nIvo Becker: 86,152.00 USD.\nCaseworker: Filed a claim for Ana?\nIvo Becker: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for 6 months or greater in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Ana for Stonevale Delta Child Allowance?",
  "options": [
   "Yusuf Rahimi",
   "Ivo Becker",
   "Ravi Delgado"
  ]
 },
 {
  "qid": "qe240c13a46",
  "kind": "yes/no",
  "text": "Hi Mateo Campbell,\nQuick note on case HR-50756 follows.\nCheers, Sami Castro\n\nFacts for Mateo Campbell (2027):\n- time employed: 7 months\n- hours worked in the past year: 1150 hours\n- employees at the worksite: 20 employees\n- gross annual pay: $82,373.02\n- take-home annual pay: $51,245.74\n- enrolled in: Idrane Tuition Bursary",
  "question": "According to these rules, is Mateo Campbell not eligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of $82,373.03.\n- Gate B: passed when hours worked in the past year are 1150 hours or greater.\n- Gate C: passed when the worksite has strictly over 19 employees.\n- Gate D: passed when the applicant has been employed for strictly above 6 months.\n- Route: an applicant enrolled in Corrowell Sabbatical Fund skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q1a8db9c693",
  "kind": "yes/no",
  "text": "Shay Bekele: At the regional service office, case CR-10938 concerns Ines.\n\nPeople who asked to claim Ines (2027):\n- Hugo Murphy: relationship to Ines: father; months lived with Ines: 7 months; annual income: 31,119.75 USD; filed a claim: yes\n- Jakub Johnson: relationship to Ines: grandfather; months lived with Ines: 7 months; annual income: $63,812; filed a claim: yes\n- Rania Wojcik: relationship to Ines: mother; months lived with Ines: 7 months; annual income: 31,119.75 USD; filed a claim: yes",
  "question": "Is Hugo Murphy the person who comes out with the right to claim Ines for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for over 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ines lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q11cb5d6375",
  "kind": "yes/no",
  "text": "desk: community help\ncase: CASE-71613\ncaseworker: Mika Zamora\nabout: Kazu Choi\n\nFacts for Kazu Choi (2025):\n- gross monthly income: 3,789.46 USD\n- net monthly income: 2,874.94 USD\n- countable assets: 4,512.97 USD\n- time in the service area: 5 months\n- age: 39 years\n- enrolled in: Stennet Commuter Pass",
  "question": "Going by the listed rules, does a gate that applies end the application of Kazu Choi to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are lower than or equal to 4,512.96 USD.\n- Gate B: passed when the applicant's age is 64 years or greater.\n- Gate C: passed when the applicant has lived in the service area for strictly in excess of 4 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5e4e4b437f",
  "kind": "yes/no",
  "text": "Internal note: Jamie Jorgensen looks after case HR-93964 in the regional service team, about Sabine Campbell.\n\nFacts for Sabine Campbell (2027):\n- time employed: twelve months\n- hours worked in the past year: 821 hours\n- employees at the worksite: 371 employees\n- gross annual pay: $42,607.45\n- take-home annual pay: $34,983.86\n- enrolled in: Quarrowmere Childcare Voucher",
  "question": "Following the listed rules, does Sabine Campbell qualify for Tovardine Seed Caregiver Leave?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or above ten months.\n- Gate B: passed when take-home annual pay is at or below $42,832.21.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q162bc9bbd7",
  "kind": "choice",
  "text": "Facts for Felix Haddad (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,481.90 USD |\n| net monthly income | 2,197.29 USD |\n| countable assets | 11,687.83 USD |\n| time in the service area | 1 month |\n| age | 27 years |\n| enrolled in | Wenlow Housing Aid |\n\nWalk-in sheet\nCase: CASE-91844\nCaseworker: Alex Lindgren\nAbout: Felix Haddad",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for greater than or equal to 4 months.\n- Gate B: passed when the applicant's age is at or greater than 56 years.\n- Gate C: passed when net monthly income is at or under 2,319.59 USD.\n- Route: an applicant enrolled in Wenlow Housing Aid skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Felix Haddad to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "q973934230d",
  "kind": "choice",
  "text": "Emi Figueroa: Warm thanks to Tomas Abebe for case HR-89899, handled with care.\n\nFacts for Tomas Abebe (2026):\n- time employed: sixteen months\n- hours worked in the past year: 691 hours\n- employees at the worksite: 168 employees\n- gross annual pay: $81,837.08\n- take-home annual pay: $67,012.56\n- enrolled in: Ferrin Exam Stipend",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or over 970 hours.\n- Gate B: passed when the applicant has been employed for strictly higher than fifteen months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Hallowdene Logistics Study Grant, which outcome does the application submitted by Tomas Abebe get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "q480d849694",
  "kind": "yes/no",
  "text": "{\"case\": \"CR-01974\", \"caseworker\": \"Kendall Umarov\", \"about\": \"Gia\", \"desk\": \"internal\"}\n\nPeople who asked to claim Gia (2027), as JSON:\n{\"people\": [{\"name\": \"Esra Okafor\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"$46,756\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Farid Nilsen\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"$66,348\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nkechi Bergstrom\", \"relationship\": \"mother\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"$42,466\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Following the listed rules, is Esra Okafor the person who winds up with the claim on Gia for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for at or above 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Gia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 }
]
