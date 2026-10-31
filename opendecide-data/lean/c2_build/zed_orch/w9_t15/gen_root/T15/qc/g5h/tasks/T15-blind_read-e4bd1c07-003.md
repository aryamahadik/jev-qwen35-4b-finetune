# G5-H blind read T15-blind_read-e4bd1c07-003 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t15/gen_root/T15/qc/g5h/answers/T15-blind_read-e4bd1c07-003.json

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
  "qid": "qdd6c69c4e4",
  "kind": "choice",
  "text": "[casework_team] case_id=HR-92047\n[casework_team] worker=Casey Kaplan about=Lior Hudson\n\nFacts for Lior Hudson (2026):\n| fact | value |\n| --- | --- |\n| time employed | 34 months |\n| hours worked in the past year | 2170 hours |\n| employees at the worksite | 54 employees |\n| gross annual pay | 82,561.33 USD |\n| take-home annual pay | 67,201.26 USD |\n| enrolled in | Idrane Tuition Grant |",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for higher than 22 months.\n- Gate B: passed when gross annual pay is 82,561.34 USD or under.\n- Gate C: passed when the worksite has at or beyond 54 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat comes of the application of Lior Hudson to Wendmoor Mill Parental Leave?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)"
  ]
 },
 {
  "qid": "q009054902a",
  "kind": "choice",
  "text": "Quick intake form\nCase reference: CR-98541\nCaseworker: Cameron Vargas\nAbout: Eva\n\nPeople who asked to claim Eva (2027):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Yasmin Ilunga | mother | four months | $74,192.00 | yes |\n| Emeka Esposito | father | twelve months | $50,082.29 | no |\n| Mariam Gordon | aunt | eleven months | $74,192.00 | yes |",
  "question": "Dunmarrow Hill Allowance rules for 2027: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for five months or greater in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Eva for Dunmarrow Hill Allowance?",
  "options": [
   "Emeka Esposito",
   "Mariam Gordon",
   "Yasmin Ilunga"
  ]
 },
 {
  "qid": "qf5ce6d92db",
  "kind": "choice",
  "text": "Quick note: Avery Obradovic is running CR-24321 for Sora. Outreach is moving fast.\n\nInterview notes for Sora (2026):\nCaseworker: Kavita Hudson, your relation to Sora?\nKavita Hudson: I am Sora's grandmother.\nCaseworker: Months Sora lived with you?\nKavita Hudson: 10 months.\nCaseworker: Annual income?\nKavita Hudson: 15,886.00 USD.\nCaseworker: Filed a claim for Sora?\nKavita Hudson: yes.\nCaseworker: Tariq Choi, your relation to Sora?\nTariq Choi: I am Sora's uncle.\nCaseworker: Months Sora lived with you?\nTariq Choi: 8 months.\nCaseworker: Annual income?\nTariq Choi: 89,375.00 USD.\nCaseworker: Filed a claim for Sora?\nTariq Choi: yes.",
  "question": "Gristmere Child Credit rules for 2026: who may claim Sora.\n- Only one person may claim Sora. Work through these steps in order.\n- Step one: only people who filed a claim for Sora are considered.\n- Step two: of those, only people with whom Sora lived for 7 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Sora lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Sora.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Sora for Gristmere Child Credit?",
  "options": [
   "Kavita Hudson",
   "Tariq Choi"
  ]
 },
 {
  "qid": "qa9e93474c1",
  "kind": "yes/no",
  "text": "unit: busy support hub\nticket: CR-61736\nhandling: Nika Hernandez\nregards: Ezra\n\nInterview notes for Ezra (2027):\nCaseworker: Ubah Hakimi, your relation to Ezra?\nUbah Hakimi: I am Ezra's aunt.\nCaseworker: Months Ezra lived with you?\nUbah Hakimi: four months.\nCaseworker: Annual income?\nUbah Hakimi: $20,241.\nCaseworker: Filed a claim for Ezra?\nUbah Hakimi: yes.\nCaseworker: Felix Haddad, your relation to Ezra?\nFelix Haddad: I am Ezra's grandfather.\nCaseworker: Months Ezra lived with you?\nFelix Haddad: three months.\nCaseworker: Annual income?\nFelix Haddad: $19,157.\nCaseworker: Filed a claim for Ezra?\nFelix Haddad: yes.\nCaseworker: Quentin Nilsen, your relation to Ezra?\nQuentin Nilsen: I am Ezra's grandfather.\nCaseworker: Months Ezra lived with you?\nQuentin Nilsen: one month.\nCaseworker: Annual income?\nQuentin Nilsen: $20,241.\nCaseworker: Filed a claim for Ezra?\nQuentin Nilsen: no.",
  "question": "Under these rules, is Ubah Hakimi the person who gets to claim Ezra for Gristmere Child Credit?",
  "definitions": "Gristmere Child Credit rules for 2027: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for over five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ezra lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0f75c13e3b",
  "kind": "yes/no",
  "text": "Facts for Viktor Haddad (2025):\n| fact | value |\n| --- | --- |\n| time employed | sixteen months |\n| hours worked in the past year | 393 hours |\n| employees at the worksite | 57 employees |\n| gross annual pay | $33,267.95 |\n| take-home annual pay | $28,402.20 |\n| enrolled in | Stonevale Staff Nursery Grant |\n\ncase_ref: HR-26148\nhandled_by: Sasha Okonkwo\nperson: Viktor Haddad\ndesk: intake",
  "question": "Is Viktor Haddad formally ineligible for Orrendale Printworks Sick Leave Supplement under these rules?",
  "definitions": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is $34,433.97 at the most.\n- Gate B: passed when the applicant has been employed for equal to or above sixteen months.\n- Gate C: passed when take-home annual pay is at or under the amount of $25,584.45.\n- Gate D: passed when the worksite has over 31 employees.\n- Route: an applicant enrolled in Stonevale Staff Nursery Grant skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q37314f8ecb",
  "kind": "yes/no",
  "text": "[case_file] ref=HR-11043 worker=Avery Obradovic\n[about] subject=Ubah Johnson\n\nIntake interview with Ubah Johnson (2025):\nCaseworker: Time employed?\nUbah Johnson: 27 months.\nCaseworker: Hours worked in the past year?\nUbah Johnson: 512 hours.\nCaseworker: Employees at your worksite?\nUbah Johnson: 99 employees.\nCaseworker: Gross annual pay?\nUbah Johnson: $28,623.30.\nCaseworker: Take-home annual pay?\nUbah Johnson: $21,294.67.\nCaseworker: Other programme enrolled in?\nUbah Johnson: Quelmere Lunch Card.",
  "question": "Going by the listed rules, is Ubah Johnson ineligible for Sorrelby Child Care Support?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for higher than sixteen months.\n- Gate B: passed when the worksite has strictly above 74 employees.\n- Gate C: passed when take-home annual pay is strictly smaller than $45,293.75.\n- Route: an applicant enrolled in Quelmere Lunch Card skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9a72a645da",
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
  "qid": "q27be00cc8a",
  "kind": "yes/no",
  "text": "Shay Bekele: At the regional service office, case CR-10938 concerns Ines.\n\nPeople who asked to claim Ines (2027):\n- Hugo Murphy: relationship to Ines: father; months lived with Ines: 7 months; annual income: 31,119.75 USD; filed a claim: yes\n- Jakub Johnson: relationship to Ines: grandfather; months lived with Ines: 7 months; annual income: $63,812; filed a claim: yes\n- Rania Wojcik: relationship to Ines: mother; months lived with Ines: 7 months; annual income: 31,119.75 USD; filed a claim: yes",
  "question": "Is Hugo Murphy the person who comes out with the right to claim Ines for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for over 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ines lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7765287f82",
  "kind": "choice",
  "text": "Ticket: staff support desk, case HR-27201\nFrom: Alex Lindgren\nAbout: Farid Johnson\n\nFacts for Farid Johnson (2025):\n| fact | value |\n| --- | --- |\n| time employed | 23 months |\n| hours worked in the past year | 1,803 hours |\n| employees at the worksite | 63 employees |\n| gross annual pay | 34,526.56 USD |\n| take-home annual pay | 24,624.07 USD |\n| enrolled in | Corranmere Flexi Hours |",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or above 64 employees.\n- Gate B: passed when the applicant has been employed for seventeen months or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Farid Johnson to Marrowby Bakery Family Leave receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)",
   "Not eligible: Gate A is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "qe3dd0bab73",
  "kind": "choice",
  "text": "Ticket: people services case CR-49338\nRaised by: Kiran Morales\nAbout: Tove\n\nPeople who asked to claim Tove (2026):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Pavel Kowalski | grandfather | 4 months | $49,075.66 | yes |\n| Zofia Ilic | aunt | 12 months | $42,892.00 | yes |\n| Wanjiru Halvorsen | aunt | 3 months | $89,215.00 | yes |",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for 5 months or more in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Tove lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Tove for Tollmere Lakeside Family Payment?",
  "options": [
   "Pavel Kowalski",
   "Zofia Ilic"
  ]
 },
 {
  "qid": "qc806574701",
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
  "qid": "qc744817dba",
  "kind": "choice",
  "text": "People who asked to claim Ana (2025):\n| person | relationship to Ana | months lived with Ana | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Nkechi Nguyen | mother | eight months | $46,140.00 | yes |\n| Ibrahim Yamazaki | father | ten months | $82,028.00 | yes |\n\ncase_ref: CR-60806\nworker: Dani Ishikawa\nsubject: Ana",
  "question": "Mollenby Canal Child Supplement rules for 2025: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for above six months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ana lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, has the right to claim Ana for Mollenby Canal Child Supplement?",
  "options": [
   "Nkechi Nguyen",
   "Ibrahim Yamazaki",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q0fc0281779",
  "kind": "choice",
  "text": "case_ref: CR-24001\nworker: Morgan Mendoza\nsubject: Ada\n\nPeople who asked to claim Ada (2027):\n- Sofia Ferreira: relationship to Ada: aunt; months lived with Ada: eight months; annual income: 63,721.00 USD; filed a claim: yes\n- Amara Medina: relationship to Ada: mother; months lived with Ada: seven months; annual income: 19,467.72 USD; filed a claim: yes\n- Felix Demir: relationship to Ada: father; months lived with Ada: eight months; annual income: 63,721.00 USD; filed a claim: no",
  "question": "Caddowen Harbour Family Allowance rules for 2027: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for strictly greater than six months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Ada for Caddowen Harbour Family Allowance?",
  "options": [
   "Felix Demir",
   "Sofia Ferreira",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q6847ea2f5d",
  "kind": "choice",
  "text": "Cameron Vargas: file CASE-33886 about Juliana Ramirez is on my list.\n\nFacts for Juliana Ramirez (2025):\n- gross monthly income: 3,347.57 USD\n- net monthly income: 3,031.68 USD\n- countable assets: 4,967.88 USD\n- time in the service area: 51 months\n- age: 60 years\n- enrolled in: Pellbrook Heating Fund",
  "question": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is lower than or equal to 2,574.57 USD.\n- Gate B: passed when countable assets are strictly beneath 4,967.89 USD.\n- Gate C: passed when gross monthly income is at or below 3,347.57 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Juliana Ramirez to Tarrowick Food Basket Support resolved?",
  "options": [
   "Not eligible: Gate C is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate B is the reason (countable assets)"
  ]
 },
 {
  "qid": "q7c5acebd3a",
  "kind": "choice",
  "text": "Hi Matias Castellano,\nBrief update on case CASE-09199 below.\nThanks, Teo Quintero\n\nIntake interview with Matias Castellano (2025):\nCaseworker: Gross monthly income?\nMatias Castellano: 2,079.12 USD.\nCaseworker: Net monthly income?\nMatias Castellano: 1,367.52 USD.\nCaseworker: Countable assets?\nMatias Castellano: 15,506.49 USD.\nCaseworker: Time in the service area?\nMatias Castellano: 12 months.\nCaseworker: Age?\nMatias Castellano: 49 years.\nCaseworker: Other programme enrolled in?\nMatias Castellano: Velgate Pump Loan.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is lower than or equal to 2,063.42 USD.\n- Gate B: passed when the applicant's age is 66 years or more.\n- Gate C: passed when the applicant has lived in the service area for strictly over 11 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does Matias Castellano get on the application to Ostermere Delta Flood Repair Support under these rules?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qcd85eac737",
  "kind": "choice",
  "text": "Emi Figueroa: Warm thanks to Tomas Abebe for case HR-89899, handled with care.\n\nFacts for Tomas Abebe (2026):\n- time employed: sixteen months\n- hours worked in the past year: 691 hours\n- employees at the worksite: 168 employees\n- gross annual pay: $81,837.08\n- take-home annual pay: $67,012.56\n- enrolled in: Ferrin Exam Stipend",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or over 691 hours.\n- Gate B: passed when the applicant has been employed for strictly higher than fifteen months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Hallowdene Logistics Study Grant, which outcome does the application submitted by Tomas Abebe get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "q7cadc26dce",
  "kind": "choice",
  "text": "Internal case note for CASE-85580.\nSet down by Jules Shrestha at the town hall office, for Rania Gashi.\n\nFacts for Rania Gashi (2027):\n- gross monthly income: 2,609.29 USD\n- net monthly income: 1,889.10 USD\n- countable assets: 2,959.17 USD\n- time in the service area: 11 months\n- age: 67 years\n- enrolled in: Sorrenby Tenancy Deposit Loan",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for higher than 5 months.\n- Gate B: passed when net monthly income is at or beneath 2,356.15 USD.\n- Gate C: passed when the applicant's age is over 67 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Rania Gashi to Tesslow Prairie Water Bill Assistance resolved?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate C is the reason (age)"
  ]
 },
 {
  "qid": "q2976b11809",
  "kind": "yes/no",
  "text": "Routine desk intake record\nCase reference: CR-16934\nHandled by: Riley Watanabe\nAbout: Uri\n\nPeople who asked to claim Uri (2027):\n| person | relationship to Uri | months lived with Uri | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ibrahim Mensah | father | seven months | 38,260.00 USD | yes |\n| Leila Gallegos | mother | seven months | 35,973.18 USD | yes |\n| Viktor Johnson | grandfather | six months | 38,260.00 USD | yes |",
  "question": "For Corrowby Family Supplement, will the right to claim Uri go to a different person from Viktor Johnson, or stay unclaimed?",
  "definitions": "Corrowby Family Supplement rules for 2027: who may claim Uri.\n- Only one person may claim Uri. Work through these steps in order.\n- Step one: only people who filed a claim for Uri are considered.\n- Step two: of those, only people with whom Uri lived for strictly more than five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Uri lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Uri.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf7271665fa",
  "kind": "yes/no",
  "text": "People who asked to claim Ali (2026):\n| person | relationship to Ali | months lived with Ali | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Rafael Tanaka | father | 2 months | $59,025.69 | yes |\n| Jelena Ilunga | mother | 11 months | $72,206.00 | yes |\n| Wanjiru Russell | aunt | 9 months | $46,791.95 | yes |\n\nBack office ticket: CR-72622\nRaised by: Blair Xiong\nAbout: Ali",
  "question": "For Sorrenby Island Family Payment, does Rafael Tanaka fail to secure the right to claim Ali under these rules?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for equal to or greater than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ali lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7a18abf0df",
  "kind": "yes/no",
  "text": "Friendly front counter slip\nTicket: HR-03299\nDealt with by: Cameron Vargas\nNamed person: Yara Lindqvist\n\nFacts for Yara Lindqvist (2025):\n| fact | value |\n| --- | --- |\n| time employed | 11 months |\n| hours worked in the past year | 1066 hours |\n| employees at the worksite | 232 employees |\n| gross annual pay | $46,302.03 |\n| take-home annual pay | $30,182.64 |\n| enrolled in | Quillmere Apprentice Pathway |",
  "question": "According to these rules, does a gate that applies end the application of Yara Lindqvist to Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly more than 10 months.\n- Gate B: passed when hours worked in the past year are 1040 hours or above.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9c2bdde370",
  "kind": "yes/no",
  "text": "case: CASE-86359\ncaseworker: Kendall Umarov\nabout: Quentin Lehmann\n\nFacts for Quentin Lehmann (2026):\n- gross monthly income: $4,589.06\n- net monthly income: $2,949.33\n- countable assets: $5,214.92\n- time in the service area: fifteen months\n- age: 65 years\n- enrolled in: Corrivale Meal Voucher",
  "question": "Going by the listed rules, does a gate that applies end the application of Quentin Lehmann to Tesslow Prairie Water Bill Assistance?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly beneath the level of $2,949.32.\n- Gate B: passed when the applicant's age is equal to or above 59 years.\n- Gate C: passed when countable assets are at or below the level of $5,214.91.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8ba143ca5c",
  "kind": "choice",
  "text": "Tomi Eklund: Lovely to see you, Cyril Castellano; the staff desk has case HR-71161 in good hands.\n\nFacts for Cyril Castellano (2025):\n- time employed: 48 months\n- hours worked in the past year: 292 hours\n- employees at the worksite: 372 employees\n- gross annual pay: 58,630.02 USD\n- take-home annual pay: 46,426.41 USD\n- enrolled in: Rickmere Night Course Fund",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 940 hours.\n- Gate B: passed when gross annual pay is strictly below the amount of 46,888.38 USD.\n- Route: an applicant enrolled in Rickmere Night Course Fund skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Hallowdene Logistics Study Grant, which outcome does the application of Cyril Castellano get?",
  "options": [
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q6e71abc555",
  "kind": "yes/no",
  "text": "Case file intake form\nCase reference: CASE-35053\nCaseworker: Riley Watanabe\nAbout: Jiro Esposito\n\nFacts for Jiro Esposito (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,073.84 |\n| net monthly income | $3,632.02 |\n| countable assets | $5,517.97 |\n| time in the service area | 10 months |\n| age | 47 years |\n| enrolled in | Ambermoor Water Rebate |",
  "question": "Does Jiro Esposito fail to qualify for Sennamoor River Rent Support under these rules?",
  "definitions": "Sennamoor River Rent Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or under $9,017.05.\n- Gate B: passed when gross monthly income is strictly beneath the level of $4,073.85.\n- Gate C: passed when net monthly income is lower than or equal to $3,302.89.\n- Route: an applicant enrolled in Ambermoor Water Rebate skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qba1c7f997f",
  "kind": "choice",
  "text": "Quick intake form\nCase reference: CR-51055\nCaseworker: Dani Ishikawa\nAbout: Liam\n\nPeople who asked to claim Liam (2025):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Freya Vasquez | mother | 9 months | $75,777 | no |\n| Xavier Russell | father | 9 months | $22,365 | yes |\n| Ugo Bergstrom | grandfather | 8 months | $61,222 | yes |",
  "question": "Kelvery Market Credit rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for strictly in excess of 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Liam lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, can claim Liam for Kelvery Market Credit?",
  "options": [
   "Xavier Russell",
   "Ugo Bergstrom"
  ]
 },
 {
  "qid": "q998e0a1f90",
  "kind": "yes/no",
  "text": "Ticket: regional case record HR-99450\nRaised by: Lior Grigoryan\nAbout: Imani Hoffman\n\nFacts for Imani Hoffman (2025):\n| fact | value |\n| --- | --- |\n| time employed | 31 months |\n| hours worked in the past year | 1699 hours |\n| employees at the worksite | 75 employees |\n| gross annual pay | $25,619.00 |\n| take-home annual pay | $18,435.57 |\n| enrolled in | Selwick Fresh Crate |",
  "question": "Is Imani Hoffman really eligible for Marrowby Bakery Family Leave under these rules?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 74 employees at minimum.\n- Gate B: passed when hours worked in the past year are at or greater than 1220 hours.\n- Gate C: passed when gross annual pay is strictly below $44,660.14.\n- Route: an applicant enrolled in Corranmere Flexi Hours skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qcafd34366b",
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
  "qid": "q6198036d24",
  "kind": "choice",
  "text": "district_ref: CR-63829\nhandled_by: Quinn Pavlenko\nabout: Ada\n\nPeople who asked to claim Ada (2027):\n- Farid Thompson: relationship to Ada: father; months lived with Ada: 12 months; annual income: $37,469; filed a claim: yes\n- Felix Ilunga: relationship to Ada: uncle; months lived with Ada: 2 months; annual income: $83,077; filed a claim: yes\n- Greta Okafor: relationship to Ada: mother; months lived with Ada: 5 months; annual income: $81,823.85; filed a claim: no\n- Ubah Jovanovic: relationship to Ada: aunt; months lived with Ada: 5 months; annual income: $63,557; filed a claim: yes",
  "question": "Kelvery Market Credit rules for 2027: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for 5 months at minimum in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ada lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Ada for Kelvery Market Credit?",
  "options": [
   "Felix Ilunga",
   "Farid Thompson"
  ]
 },
 {
  "qid": "qf4472c43de",
  "kind": "choice",
  "text": "People who asked to claim Joon (2027):\n| person | relationship to Joon | months lived with Joon | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Jakub Lehmann | uncle | 5 months | $78,033 | yes |\n| Hugo Rahimi | father | 7 months | $53,989 | yes |\n\n[case_file] ref=CR-58282 worker=Avery Obradovic\n[about] subject=Joon",
  "question": "Mollenby Canal Child Supplement rules for 2027: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for at or greater than 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Joon lived for more months comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, can claim Joon for Mollenby Canal Child Supplement under these rules?",
  "options": [
   "Nobody may claim the child",
   "Hugo Rahimi",
   "Jakub Lehmann"
  ]
 },
 {
  "qid": "qf1ae437439",
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
  "qid": "q404ffca9c5",
  "kind": "choice",
  "text": "[town_hall_log] case=CR-14151 worker=Casey Kaplan\n[town_hall_log] about=Lara\n\nPeople who asked to claim Lara (2027):\n| person | relationship to Lara | months lived with Lara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anjali Becker | mother | eleven months | 36,568.33 USD | no |\n| Emeka Nguyen | father | seven months | 36,568.33 USD | yes |\n| Ugo Stewart | grandfather | twelve months | 39,083.93 USD | no |",
  "question": "Dunmarrow Hill Allowance rules for 2027: who may claim Lara.\n- Only one person may claim Lara. Work through these steps in order.\n- Step one: only people who filed a claim for Lara are considered.\n- Step two: of those, only people with whom Lara lived for greater than or equal to six months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Lara lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Lara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, is the sole person who may claim Lara for Dunmarrow Hill Allowance?",
  "options": [
   "Ugo Stewart",
   "Nobody may claim the child",
   "Emeka Nguyen"
  ]
 },
 {
  "qid": "qb035830eb3",
  "kind": "yes/no",
  "text": "Hello,\nYour details for Gia are with the intake desk under CR-15598.\nWarm regards, Ezra Rosales\n\nPeople who asked to claim Gia (2025):\n- Dmitri Iyer: relationship to Gia: father; months lived with Gia: 5 months; annual income: $26,017; filed a claim: yes\n- Zainab Ueda: relationship to Gia: grandmother; months lived with Gia: 6 months; annual income: $37,791.53; filed a claim: no\n- Sofia Fujimoto: relationship to Gia: mother; months lived with Gia: 3 months; annual income: $67,143.22; filed a claim: yes",
  "question": "Does Dmitri Iyer end up as the sole person who may claim Gia for Caddowen Harbour Family Allowance?",
  "definitions": "Caddowen Harbour Family Allowance rules for 2025: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for a minimum of 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Gia lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdd707d1d6b",
  "kind": "choice",
  "text": "Work ticket CR-30567\nLogged by: Cameron Vargas\nAbout: Vida\n\nInterview notes for Vida (2025):\nCaseworker: Gabriel Sharma, your relation to Vida?\nGabriel Sharma: I am Vida's uncle.\nCaseworker: Months Vida lived with you?\nGabriel Sharma: 2 months.\nCaseworker: Annual income?\nGabriel Sharma: 92,353.62 USD.\nCaseworker: Filed a claim for Vida?\nGabriel Sharma: yes.\nCaseworker: Olena Abara, your relation to Vida?\nOlena Abara: I am Vida's grandmother.\nCaseworker: Months Vida lived with you?\nOlena Abara: 6 months.\nCaseworker: Annual income?\nOlena Abara: 28,994.00 USD.\nCaseworker: Filed a claim for Vida?\nOlena Abara: no.\nCaseworker: Felix Bergstrom, your relation to Vida?\nFelix Bergstrom: I am Vida's uncle.\nCaseworker: Months Vida lived with you?\nFelix Bergstrom: 7 months.\nCaseworker: Annual income?\nFelix Bergstrom: 40,864.00 USD.\nCaseworker: Filed a claim for Vida?\nFelix Bergstrom: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2025: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for 7 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Vida lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Vida for Kelmstone Mountain Family Grant?",
  "options": [
   "Gabriel Sharma",
   "Nobody may claim the child",
   "Felix Bergstrom"
  ]
 },
 {
  "qid": "q1c031ba350",
  "kind": "choice",
  "text": "Counter ticket: CR-17449\nRaised by: Nika Hernandez\nAbout: Lina\n\nInterview notes for Lina (2026):\nCaseworker: Ibrahim Zielinski, your relation to Lina?\nIbrahim Zielinski: I am Lina's father.\nCaseworker: Months Lina lived with you?\nIbrahim Zielinski: five months.\nCaseworker: Annual income?\nIbrahim Zielinski: 39,484.00 USD.\nCaseworker: Filed a claim for Lina?\nIbrahim Zielinski: yes.\nCaseworker: Hamid Vasquez, your relation to Lina?\nHamid Vasquez: I am Lina's grandfather.\nCaseworker: Months Lina lived with you?\nHamid Vasquez: six months.\nCaseworker: Annual income?\nHamid Vasquez: 15,287.88 USD.\nCaseworker: Filed a claim for Lina?\nHamid Vasquez: yes.\nCaseworker: Nkechi Douglas, your relation to Lina?\nNkechi Douglas: I am Lina's mother.\nCaseworker: Months Lina lived with you?\nNkechi Douglas: twelve months.\nCaseworker: Annual income?\nNkechi Douglas: 26,480.00 USD.\nCaseworker: Filed a claim for Lina?\nNkechi Douglas: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Lina.\n- Only one person may claim Lina. Work through these steps in order.\n- Step one: only people who filed a claim for Lina are considered.\n- Step two: of those, only people with whom Lina lived for five months or above in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Lina lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Lina.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Lina for Stonevale Delta Child Allowance?",
  "options": [
   "Ibrahim Zielinski",
   "Nkechi Douglas"
  ]
 },
 {
  "qid": "qeab2eb9f6d",
  "kind": "yes/no",
  "text": "reference: CR-10458\nhandler: Quinn Pavlenko\nsubject: Dara\n\nPeople who asked to claim Dara (2025):\n- Hiro Petrov: relationship to Dara: father; months lived with Dara: 12 months; annual income: 33,076.31 USD; filed a claim: yes\n- Sabine Zielinski: relationship to Dara: aunt; months lived with Dara: 0 months; annual income: 53,941.00 USD; filed a claim: no",
  "question": "Does the right to claim Dara for Tollmere Lakeside Family Payment pass to a different person from Hiro Petrov, or stay unclaimed under these rules?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2025: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for at or above 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q022e4af421",
  "kind": "yes/no",
  "text": "case: CASE-15023\ncaseworker: Kendall Umarov\nabout: Xenia Dubois\nkind: file\n\nFacts for Xenia Dubois (2025):\n- gross monthly income: 3,435.64 USD\n- net monthly income: 3,323.64 USD\n- countable assets: 7,482.93 USD\n- time in the service area: seventeen months\n- age: 88 years\n- enrolled in: Vellmar Transit Pass",
  "question": "Is Xenia Dubois eligible for Ostmere Lakeside Winter Energy Support with every applicable gate passed?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or under 7,482.94 USD.\n- Gate B: passed when the applicant's age is greater than or equal to 57 years.\n- Gate C: passed when the applicant has lived in the service area for at or above eleven months.\n- Gate D: passed when gross monthly income is strictly under the value of 3,435.64 USD.\n- Route: an applicant enrolled in Vellmar Transit Pass skips Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfa8266caf9",
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
  "qid": "q7a77a23967",
  "kind": "choice",
  "text": "Case note: routine check on CR-37735, held by Toni Lazar for Ada.\n\nPeople who asked to claim Ada (2026):\n- Greta Ivanova: relationship to Ada: mother; months lived with Ada: 6 months; annual income: 80,066.00 USD; filed a claim: no\n- Kenji Begum: relationship to Ada: father; months lived with Ada: 7 months; annual income: 53,081.00 USD; filed a claim: yes\n- Rania Choi: relationship to Ada: grandmother; months lived with Ada: 9 months; annual income: 76,918.00 USD; filed a claim: no\n- Bruno Fujimoto: relationship to Ada: uncle; months lived with Ada: 7 months; annual income: 80,066.00 USD; filed a claim: yes",
  "question": "Kelvery Market Credit rules for 2026: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for larger than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, is the sole person who may claim Ada for Kelvery Market Credit?",
  "options": [
   "Rania Choi",
   "Kenji Begum",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qfdefd09cca",
  "kind": "choice",
  "text": "Kendall Umarov: back office log for CR-68074, a plain entry about Milo.\n\nPeople who asked to claim Milo (2026):\n- Matias Kimura: relationship to Milo: uncle; months lived with Milo: 11 months; annual income: $30,816; filed a claim: yes\n- Bianca Dragic: relationship to Milo: mother; months lived with Milo: 2 months; annual income: $17,264; filed a claim: yes\n- Ugo Dubois: relationship to Milo: father; months lived with Milo: 7 months; annual income: $17,264; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2026: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for 7 months or more in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Milo lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Ostrowan Prairie Grant, which person, if any, may claim Milo?",
  "options": [
   "Ugo Dubois",
   "Matias Kimura",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qea6adf85d1",
  "kind": "yes/no",
  "text": "{\"case\": \"CR-01974\", \"caseworker\": \"Kendall Umarov\", \"about\": \"Gia\", \"desk\": \"internal\"}\n\nPeople who asked to claim Gia (2027), as JSON:\n{\"people\": [{\"name\": \"Esra Okafor\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"$46,756\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Farid Nilsen\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"$66,348\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nkechi Bergstrom\", \"relationship\": \"mother\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"$42,466\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Following the listed rules, is Esra Okafor the person who winds up with the claim on Gia for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for at or above 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Gia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe66e7a7975",
  "kind": "yes/no",
  "text": "case: CASE-28730\nhub: support\ncaseworker: Remy Tran\nabout: Ari Hamilton\n\nFacts for Ari Hamilton (2025):\n- gross monthly income: 4,833.78 USD\n- net monthly income: 3,567.54 USD\n- countable assets: 7,384.70 USD\n- time in the service area: thirteen months\n- age: 59 years\n- enrolled in: Crannock Food Pantry",
  "question": "Going by the listed rules, is Ari Hamilton ineligible for Ostmere Lakeside Winter Energy Support?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is larger than 57 years.\n- Gate B: passed when countable assets are at or below 9,451.98 USD.\n- Route: an applicant enrolled in Crannock Food Pantry skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb71672914f",
  "kind": "choice",
  "text": "[hub_entry] ref=CASE-74434 handler=Kendall Umarov subject=Cyril Anderson\n\nIntake interview with Cyril Anderson (2027):\nCaseworker: Gross monthly income?\nCyril Anderson: 2,955.21 USD.\nCaseworker: Net monthly income?\nCyril Anderson: 1,679.68 USD.\nCaseworker: Countable assets?\nCyril Anderson: 13,344.08 USD.\nCaseworker: Time in the service area?\nCyril Anderson: three months.\nCaseworker: Age?\nCyril Anderson: 38 years.\nCaseworker: Other programme enrolled in?\nCyril Anderson: none.",
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
  "qid": "q51b3731060",
  "kind": "yes/no",
  "text": "desk: community help\ncase: CASE-71613\ncaseworker: Mika Zamora\nabout: Kazu Choi\n\nFacts for Kazu Choi (2025):\n- gross monthly income: 3,789.46 USD\n- net monthly income: 2,874.94 USD\n- countable assets: 4,512.97 USD\n- time in the service area: 5 months\n- age: 39 years\n- enrolled in: Stennet Commuter Pass",
  "question": "Going by the listed rules, does a gate that applies end the application of Kazu Choi to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are lower than or equal to 4,512.96 USD.\n- Gate B: passed when the applicant's age is 64 years or greater.\n- Gate C: passed when the applicant has lived in the service area for strictly in excess of 4 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q98eab5406d",
  "kind": "yes/no",
  "text": "Case note: the intake desk has Hugo Yilmaz on case CASE-98717, with Alex Lindgren in charge.\n\nFacts for Hugo Yilmaz (2026):\n- gross monthly income: $5,052.93\n- net monthly income: $4,426.91\n- countable assets: $7,159.37\n- time in the service area: 10 months\n- age: 73 years\n- enrolled in: Stennet Commuter Pass",
  "question": "For Corvane Transit Fare Discount, does Hugo Yilmaz qualify under the listed rules?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or under $7,159.36.\n- Gate B: passed when the applicant has lived in the service area for above 11 months.\n- Gate C: passed when the applicant's age is strictly over 66 years.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q64ebbf71d1",
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
  "qid": "q1ebc871c01",
  "kind": "choice",
  "text": "Mika Zamora: outreach list has CASE-95347 for Yusuf Patterson.\n\nFacts for Yusuf Patterson (2027):\n- gross monthly income: $4,602.45\n- net monthly income: $3,241.53\n- countable assets: $12,314.93\n- time in the service area: 11 months\n- age: 57 years\n- enrolled in: Sorrenby Tenancy Deposit Loan",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for above 10 months.\n- Gate B: passed when net monthly income is lower than or equal to $3,241.53.\n- Gate C: passed when the applicant's age is 65 years or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Yusuf Patterson to Tesslow Prairie Water Bill Assistance get?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qdfe5971e57",
  "kind": "choice",
  "text": "[case_index] ref=HR-99711 worker=Kazu Yousef subject=Dario Esposito\n\nFacts for Dario Esposito (2025):\n| fact | value |\n| --- | --- |\n| time employed | 23 months |\n| hours worked in the past year | 381 hours |\n| employees at the worksite | 41 employees |\n| gross annual pay | 77,653.78 USD |\n| take-home annual pay | 56,158.24 USD |\n| enrolled in | Dorrane Parental Leave |",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 41 employees or more.\n- Gate B: passed when hours worked in the past year are strictly more than 910 hours.\n- Gate C: passed when the applicant has been employed for in excess of twenty months.\n- Route: an applicant enrolled in Dorrane Parental Leave skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Dario Esposito to Tovardine Seed Caregiver Leave gets which outcome?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (time employed)"
  ]
 },
 {
  "qid": "q4341cd70ba",
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
  "qid": "qf5b60102d3",
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
  "qid": "q7c92e24d6a",
  "kind": "yes/no",
  "text": "Town hall intake header\nCase reference: CASE-29875\nCaseworker: Dani Ishikawa\nAbout: Dario Wojcik\n\nIntake interview with Dario Wojcik (2025):\nCaseworker: Gross monthly income?\nDario Wojcik: $2,927.28.\nCaseworker: Net monthly income?\nDario Wojcik: $2,448.65.\nCaseworker: Countable assets?\nDario Wojcik: $17,300.22.\nCaseworker: Time in the service area?\nDario Wojcik: 26 months.\nCaseworker: Age?\nDario Wojcik: 65 years.\nCaseworker: Other programme enrolled in?\nDario Wojcik: Aldervale Meal Basket.",
  "question": "Does Dario Wojcik meet the rules for Tamsfell Senior Home Support by passing every gate that applies?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 59 years or more.\n- Gate B: passed when gross monthly income is equal to or below $3,176.39.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q73a33ca0d7",
  "kind": "choice",
  "text": "Quick note: Quinn Pavlenko is running HR-23404 for Rania Hoffman. Outreach is moving fast.\n\nFacts for Rania Hoffman (2027):\n- time employed: 8 months\n- hours worked in the past year: 976 hours\n- employees at the worksite: 123 employees\n- gross annual pay: $82,389.79\n- take-home annual pay: $65,184.42\n- enrolled in: Drummock Nurse Bursary",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $82,389.78.\n- Gate B: passed when hours worked in the past year are 1360 hours or greater.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Morrowdene Hospital Group Return Support, which outcome does the application submitted by Rania Hoffman get?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible"
  ]
 }
]
