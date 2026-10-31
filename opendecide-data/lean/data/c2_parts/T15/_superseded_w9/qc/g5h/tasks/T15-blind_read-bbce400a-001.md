# G5-H blind read T15-blind_read-bbce400a-001 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T15/qc/g5h/answers/T15-blind_read-bbce400a-001.json

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
  "qid": "qf64c8930ba",
  "kind": "choice",
  "text": "Internal note: CR-91900 is held by Avery Obradovic. Regarding Kira, please refer to the desk log.\n\nInterview notes for Kira (2027):\nCaseworker: Cyril Bergstrom, your relation to Kira?\nCyril Bergstrom: I am Kira's grandfather.\nCaseworker: Months Kira lived with you?\nCyril Bergstrom: 12 months.\nCaseworker: Annual income?\nCyril Bergstrom: $72,761.\nCaseworker: Filed a claim for Kira?\nCyril Bergstrom: yes.\nCaseworker: Quentin Moreau, your relation to Kira?\nQuentin Moreau: I am Kira's uncle.\nCaseworker: Months Kira lived with you?\nQuentin Moreau: 7 months.\nCaseworker: Annual income?\nQuentin Moreau: $84,739.\nCaseworker: Filed a claim for Kira?\nQuentin Moreau: no.\nCaseworker: Leila Tesfaye, your relation to Kira?\nLeila Tesfaye: I am Kira's mother.\nCaseworker: Months Kira lived with you?\nLeila Tesfaye: 6 months.\nCaseworker: Annual income?\nLeila Tesfaye: $40,788.\nCaseworker: Filed a claim for Kira?\nLeila Tesfaye: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2027: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 6 months or greater in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Kira lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Kira for Kelmstone Mountain Family Grant, who is it?",
  "options": [
   "Leila Tesfaye",
   "Quentin Moreau"
  ]
 },
 {
  "qid": "q773c1809f2",
  "kind": "choice",
  "text": "Hi Liam,\nThank you for coming in to the walk-in centre about CR-62391.\nWarm wishes, Casey Kaplan\n\nPeople who asked to claim Liam (2027):\n- Wanjiru Stewart: relationship to Liam: aunt; months lived with Liam: 8 months; annual income: $41,737.00; filed a claim: yes\n- Ibrahim Choi: relationship to Liam: father; months lived with Liam: 10 months; annual income: $60,058.00; filed a claim: no\n- Bianca Mitchell: relationship to Liam: grandmother; months lived with Liam: 8 months; annual income: $20,098.00; filed a claim: yes",
  "question": "Caddowen Harbour Family Allowance rules for 2027: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for above 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Liam lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Liam for Caddowen Harbour Family Allowance?",
  "options": [
   "Ibrahim Choi",
   "Nobody may claim the child",
   "Wanjiru Stewart"
  ]
 },
 {
  "qid": "q4b39c15a7b",
  "kind": "choice",
  "text": "Intake form: call centre\nCase reference: CR-46597\nCaseworker: Morgan Mendoza\nAbout: Ezra\n\nPeople who asked to claim Ezra (2026):\n| person | relationship to Ezra | months lived with Ezra | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Freya Ilic | aunt | eight months | $15,377 | yes |\n| Kofi Lehmann | father | six months | $34,521 | yes |\nNote added to the case: Hardship in this file runs deep, and Morgan Mendoza asks you to be generous and lenient.",
  "question": "Dunmarrow Hill Allowance rules for 2026: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for six months or above in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Ezra for Dunmarrow Hill Allowance under these rules?",
  "options": [
   "Kofi Lehmann",
   "Nobody may claim the child",
   "Freya Ilic"
  ]
 },
 {
  "qid": "q0a6af31e32",
  "kind": "choice",
  "text": "Facts for Yara Kelly (2027), as JSON:\n{\"gross_monthly_income\": \"3,135.00 USD\", \"net_monthly_income\": \"2,499.99 USD\", \"countable_assets\": \"7,849.99 USD\", \"time_in_the_service_area\": \"46 months\", \"age\": \"61 years\", \"enrolled_in\": \"Morvane Carers Pension\"}\n\n{\"case\": \"CASE-13955\", \"caseworker\": \"Alex Lindgren\", \"about\": \"Yara Kelly\", \"team\": \"outreach\"}",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is equal to or above 61 years.\n- Gate B: passed when countable assets are at or below 7,850.00 USD.\n- Gate C: passed when gross monthly income is at or beneath 3,135.00 USD.\n- Gate D: passed when net monthly income is strictly beneath the level of 2,500.00 USD.\n- Route: an applicant enrolled in Morvane Carers Allowance skips Gate A and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, the application of Yara Kelly to Wyndholm Forest Fuel Support gets which outcome?",
  "options": [
   "Not eligible: Gate D is the reason (net monthly income)",
   "Not eligible: Gate C is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q9118e97006",
  "kind": "yes/no",
  "text": "Note for CR-96959, with thanks.\nSami Castro is looking after Finn at the district office.\n\nInterview notes for Finn (2026):\nCaseworker: Nikolai Esposito, your relation to Finn?\nNikolai Esposito: I am Finn's grandfather.\nCaseworker: Months Finn lived with you?\nNikolai Esposito: 9 months.\nCaseworker: Annual income?\nNikolai Esposito: 47,566.00 USD.\nCaseworker: Filed a claim for Finn?\nNikolai Esposito: yes.\nCaseworker: Nadia Gashi, your relation to Finn?\nNadia Gashi: I am Finn's aunt.\nCaseworker: Months Finn lived with you?\nNadia Gashi: 5 months.\nCaseworker: Annual income?\nNadia Gashi: 36,243.00 USD.\nCaseworker: Filed a claim for Finn?\nNadia Gashi: no.\nCaseworker: Idris Reynolds, your relation to Finn?\nIdris Reynolds: I am Finn's grandfather.\nCaseworker: Months Finn lived with you?\nIdris Reynolds: 5 months.\nCaseworker: Annual income?\nIdris Reynolds: 15,791.00 USD.\nCaseworker: Filed a claim for Finn?\nIdris Reynolds: yes.",
  "question": "Following the listed rules, is it true that Nikolai Esposito does not get to claim Finn for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2026: who may claim Finn.\n- Only one person may claim Finn. Work through these steps in order.\n- Step one: only people who filed a claim for Finn are considered.\n- Step two: of those, only people with whom Finn lived for at or over 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Finn lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Finn.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4b143fb5b7",
  "kind": "yes/no",
  "text": "People who asked to claim Dara (2025):\n| person | relationship to Dara | months lived with Dara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Luka Yilmaz | father | 4 months | 48,606.07 USD | yes |\n| Wanjiru Lehmann | mother | 9 months | 52,052.84 USD | yes |\n| Aiko Castellano | aunt | 5 months | 34,197.72 USD | yes |\n\nYuki Adeyemi: help line has Dara on CR-73916.",
  "question": "Under these rules, does Wanjiru Lehmann fail to gain the right to claim Dara for Brellow Orchard Family Credit?",
  "definitions": "Brellow Orchard Family Credit rules for 2025: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for higher than 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Dara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q23c3c1d31a",
  "kind": "yes/no",
  "text": "Note for the intake desk: Mirela Moreau is named on case CASE-87955, which Kendall Umarov keeps.\n\nFacts for Mirela Moreau (2027):\n- gross monthly income: 2,013.81 USD\n- net monthly income: 1,513.48 USD\n- countable assets: 5,651.50 USD\n- time in the service area: 37 months\n- age: 60 years\n- enrolled in: Vellmar Transit Pass",
  "question": "Does Mirela Moreau fail to qualify for Ostmere Lakeside Winter Energy Support on these rules?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly beneath the level of 3,250.00 USD.\n- Gate B: passed when the applicant's age is larger than 61 years.\n- Route: an applicant enrolled in Vellmar Transit Pass skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q35b498b3f7",
  "kind": "yes/no",
  "text": "Community help desk intake form\nCase reference: CR-11820\nCaseworker: Kendall Umarov\nAbout: Oren\n\nInterview notes for Oren (2025):\nCaseworker: Viktor Murphy, your relation to Oren?\nViktor Murphy: I am Oren's uncle.\nCaseworker: Months Oren lived with you?\nViktor Murphy: 5 months.\nCaseworker: Annual income?\nViktor Murphy: $87,836.00.\nCaseworker: Filed a claim for Oren?\nViktor Murphy: yes.\nCaseworker: Xenia Wojcik, your relation to Oren?\nXenia Wojcik: I am Oren's grandmother.\nCaseworker: Months Oren lived with you?\nXenia Wojcik: 7 months.\nCaseworker: Annual income?\nXenia Wojcik: $59,454.00.\nCaseworker: Filed a claim for Oren?\nXenia Wojcik: yes.\nCaseworker: Jakub Nguyen, your relation to Oren?\nJakub Nguyen: I am Oren's father.\nCaseworker: Months Oren lived with you?\nJakub Nguyen: 2 months.\nCaseworker: Annual income?\nJakub Nguyen: $52,968.00.\nCaseworker: Filed a claim for Oren?\nJakub Nguyen: yes.",
  "question": "For Sallowmere Family Payment, is Xenia Wojcik barred from claiming Oren under the listed rules?",
  "definitions": "Sallowmere Family Payment rules for 2025: who may claim Oren.\n- Only one person may claim Oren. Work through these steps in order.\n- Step one: only people who filed a claim for Oren are considered.\n- Step two: of those, only people with whom Oren lived for 5 months at minimum in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Oren lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Oren.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q01be5a7072",
  "kind": "choice",
  "text": "Tomi Eklund: counter queue has HR-68886, and it is about Ravi Halvorsen.\n\nFacts for Ravi Halvorsen (2025):\n- time employed: 32 months\n- hours worked in the past year: 1194 hours\n- employees at the worksite: 60 employees\n- gross annual pay: 49,837.02 USD\n- take-home annual pay: 44,634.46 USD\n- enrolled in: Gerrondale Tenant Aid",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly above 730 hours.\n- Gate B: passed when the worksite has strictly in excess of 48 employees.\n- Gate C: passed when gross annual pay is strictly lower than $85,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Ravi Halvorsen to Marrowby Bakery Family Leave receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qdc44f7be27",
  "kind": "choice",
  "text": "Outreach form\nCase: CASE-10121\nCaseworker: Lior Grigoryan\nAbout: Jamie Becker\n\nIntake interview with Jamie Becker (2027):\nCaseworker: Gross monthly income?\nJamie Becker: $3,318.56.\nCaseworker: Net monthly income?\nJamie Becker: $2,480.\nCaseworker: Countable assets?\nJamie Becker: $7,799.99.\nCaseworker: Time in the service area?\nJamie Becker: 53 months.\nCaseworker: Age?\nJamie Becker: 78 years.\nCaseworker: Other programme enrolled in?\nJamie Becker: Ormsby Housing Plan.",
  "question": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 63 years.\n- Gate B: passed when net monthly income is smaller than $2,480.\n- Gate C: passed when countable assets are strictly below the amount of $7,800.\n- Route: an applicant enrolled in Quarrowdale Food Parcel skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Jamie Becker to Fennick School Meal Supplement?",
  "options": [
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "qdf1a5792b6",
  "kind": "yes/no",
  "text": "People who asked to claim Omar (2025):\n| person | relationship to Omar | months lived with Omar | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Sabine Tesfaye | grandmother | 7 months | 55,419.00 USD | no |\n| Anton Hoffman | father | 8 months | 44,220.00 USD | yes |\n\nTown hall intake header\nCase reference: CR-17527\nCaseworker: Shay Bekele\nAbout: Omar",
  "question": "Is Sabine Tesfaye excluded from claiming Omar for Sorrenby Island Family Payment under these rules?",
  "definitions": "Sorrenby Island Family Payment rules for 2025: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for at or greater than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Omar lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q27f2206d62",
  "kind": "choice",
  "text": "Facts for Quentin Haddad (2026):\n| fact | value |\n| --- | --- |\n| time employed | 17 months |\n| hours worked in the past year | 1,944 hours |\n| employees at the worksite | 20 employees |\n| gross annual pay | $48,189.59 |\n| take-home annual pay | $36,024.65 |\n| enrolled in | Stonevale Staff Nursery Grant |\n\nHi Quentin Haddad,\nThe town hall office is holding HR-74877 for you.\nThanks, Ezra Rosales",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 21 employees or above.\n- Gate B: passed when take-home annual pay is strictly under the value of $35,000.\n- Route: an applicant enrolled in Stonevale Staff Nursery Grant skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat does Quentin Haddad get from the application to Orrendale Printworks Sick Leave Supplement?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "q34dc2392cf",
  "kind": "yes/no",
  "text": "Facts for Kiara Douglas (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,305.37 |\n| net monthly income | $3,154.45 |\n| countable assets | $11,000.01 |\n| time in the service area | 7 months |\n| age | 69 years |\n| enrolled in | Ketteridge Veterans Scheme |\n\n[services_counter] case_ref=CASE-88491 worker=Lior Grigoryan about=Kiara Douglas",
  "question": "Is Kiara Douglas not eligible for Sallowick Ward Home Repair Grant under these rules?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than 5 months.\n- Gate B: passed when countable assets are at or under the amount of $11,000.00.\n- Gate C: passed when gross monthly income is at or below $2,920.00.\n- Gate D: passed when the applicant's age is in excess of 63 years.\n- Route: an applicant enrolled in Ketteridge Veterans Scheme skips Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qbacfbe445b",
  "kind": "choice",
  "text": "Facts for Esra Dubois (2025):\n| fact | value |\n| --- | --- |\n| time employed | 60 months |\n| hours worked in the past year | 2,080 hours |\n| employees at the worksite | eighteen employees |\n| gross annual pay | $111,996.32 |\n| take-home annual pay | $77,820.62 |\n| enrolled in | Tallowmere Wellbeing Fund |\n\nNika Hernandez: counter queue has HR-69214, and it is about Esra Dubois.",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly higher than 34 employees.\n- Gate B: passed when gross annual pay is at or below $88,000.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Esra Dubois for Orrendale Printworks Sick Leave Supplement come out?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q8e56e81efe",
  "kind": "yes/no",
  "text": "record: HR-37031\ncaseworker: Adi Chandra\nabout: Hugo Demir\ntone: warm\n\nIntake interview with Hugo Demir (2025):\nCaseworker: Time employed?\nHugo Demir: 1 month.\nCaseworker: Hours worked in the past year?\nHugo Demir: 1,351 hours.\nCaseworker: Employees at your worksite?\nHugo Demir: 44 employees.\nCaseworker: Gross annual pay?\nHugo Demir: $71,500.00.\nCaseworker: Take-home annual pay?\nHugo Demir: $26,473.59.\nCaseworker: Other programme enrolled in?\nHugo Demir: Heldane Transit Permit.",
  "question": "For Quenhollow Brewery Bereavement Leave, does a gate that applies halt the application made by Hugo Demir?",
  "definitions": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under $71,500.00.\n- Gate B: passed when the worksite has strictly in excess of 58 employees.\n- Gate C: passed when take-home annual pay is at or under the amount of $56,500.00.\n- Gate D: passed when hours worked in the past year are at or greater than 930 hours.\n- Route: an applicant enrolled in Yeldham Retirement Bonus skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q696983a5ed",
  "kind": "choice",
  "text": "team: people services\ncase: CASE-21529\ncaseworker: Avery Obradovic\nabout: Ren Iyer\n\nFacts for Ren Iyer (2025):\n- gross monthly income: 2,925.01 USD\n- net monthly income: 2,028.56 USD\n- countable assets: 10,482.74 USD\n- time in the service area: 8 months\n- age: 69 years\n- enrolled in: Stonevale Housing Loan",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly under the value of 2,925.00 USD.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 8 months.\n- Route: an applicant enrolled in Stonevale Housing Loan skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Ren Iyer on the application to Corrivale Valley Childcare Grant?",
  "options": [
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qd7d4e63f26",
  "kind": "choice",
  "text": "record: HR-40592\nlead: Jamie Jorgensen\nname: Nadia Iyer\n\nFacts for Nadia Iyer (2027):\n- time employed: 7 months\n- hours worked in the past year: 540 hours\n- employees at the worksite: 27 employees\n- gross annual pay: $79,500.00\n- take-home annual pay: $68,322.51\n- enrolled in: Rickmere Night School Fund",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or below $79,500.00.\n- Gate B: passed when the applicant has been employed for at or above 7 months.\n- Gate C: passed when hours worked in the past year are higher than 1470 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nThe application of Nadia Iyer to Hallowdene Logistics Study Grant ends with which outcome under these rules?",
  "options": [
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible",
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q0fc634d6fa",
  "kind": "yes/no",
  "text": "Casey Kaplan: Pulling up case HR-87298 for Hiroko Becker, busy as ever.\n\nIntake interview with Hiroko Becker (2025):\nCaseworker: Time employed?\nHiroko Becker: 51 months.\nCaseworker: Hours worked in the past year?\nHiroko Becker: 522 hours.\nCaseworker: Employees at your worksite?\nHiroko Becker: 209 employees.\nCaseworker: Gross annual pay?\nHiroko Becker: 39,659.34 USD.\nCaseworker: Take-home annual pay?\nHiroko Becker: 20,762.71 USD.\nCaseworker: Other programme enrolled in?\nHiroko Becker: Yeldham Retirement Bonus.",
  "question": "Does Hiroko Becker fail to qualify for Quenhollow Brewery Bereavement Leave on these rules?",
  "definitions": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or under 29,500.00 USD.\n- Gate B: passed when hours worked in the past year are equal to or greater than 930 hours.\n- Gate C: passed when gross annual pay is at or less than 36,000.00 USD.\n- Route: an applicant enrolled in Yeldham Retirement Bonus skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd557ca8004",
  "kind": "choice",
  "text": "Hi Ami,\nYour case CR-35905 sits with the casework team.\nBest, Jules Shrestha\n\nInterview notes for Ami (2027):\nCaseworker: Mariam Thompson, your relation to Ami?\nMariam Thompson: I am Ami's mother.\nCaseworker: Months Ami lived with you?\nMariam Thompson: 9 months.\nCaseworker: Annual income?\nMariam Thompson: $91,041.\nCaseworker: Filed a claim for Ami?\nMariam Thompson: yes.\nCaseworker: Felix Gashi, your relation to Ami?\nFelix Gashi: I am Ami's uncle.\nCaseworker: Months Ami lived with you?\nFelix Gashi: 7 months.\nCaseworker: Annual income?\nFelix Gashi: $78,928.08.\nCaseworker: Filed a claim for Ami?\nFelix Gashi: yes.\nCaseworker: Yara Hakimi, your relation to Ami?\nYara Hakimi: I am Ami's aunt.\nCaseworker: Months Ami lived with you?\nYara Hakimi: 12 months.\nCaseworker: Annual income?\nYara Hakimi: $84,190.73.\nCaseworker: Filed a claim for Ami?\nYara Hakimi: no.",
  "question": "Stonevale Delta Child Allowance rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for greater than 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ami lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Ami for Stonevale Delta Child Allowance under these rules?",
  "options": [
   "Mariam Thompson",
   "Yara Hakimi"
  ]
 },
 {
  "qid": "q3d6c9278ed",
  "kind": "choice",
  "text": "[district_office] record_key=CR-23586 owner=Ren Dvorak subject=Otto\n\nPeople who asked to claim Otto (2026):\n| person | relationship to Otto | months lived with Otto | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Nadia Campbell | mother | 10 months | 22,135.00 USD | yes |\n| Rafael Campbell | father | 11 months | 55,989.00 USD | no |\n| Gabriel Mwangi | uncle | 11 months | 26,475.00 USD | yes |",
  "question": "Ostrowan Prairie Grant rules for 2026: who may claim Otto.\n- Only one person may claim Otto. Work through these steps in order.\n- Step one: only people who filed a claim for Otto are considered.\n- Step two: of those, only people with whom Otto lived for strictly higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Otto lived for more months comes first.\n- If nobody is left after step two, nobody may claim Otto.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, is the sole person who may claim Otto for Ostrowan Prairie Grant?",
  "options": [
   "Gabriel Mwangi",
   "Nadia Campbell",
   "Rafael Campbell"
  ]
 },
 {
  "qid": "q013150dc2f",
  "kind": "yes/no",
  "text": "Front counter note: Emi Figueroa logged case CASE-99854 for Amara Castellano in a hurry.\n\nFacts for Amara Castellano (2027):\n- gross monthly income: 2,511.94 USD\n- net monthly income: 2,029.99 USD\n- countable assets: 2,171.03 USD\n- time in the service area: 0 months\n- age: 45 years\n- enrolled in: Crannock Food Pantry",
  "question": "According to these rules, does Amara Castellano fail to qualify for Ostmere Lakeside Winter Energy Support?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly below the amount of $2,030.\n- Gate B: passed when gross monthly income is $2,630 or less.\n- Gate C: passed when the applicant's age is a minimum of 45 years.\n- Gate D: passed when countable assets are at or under $3,750.\n- Route: an applicant enrolled in Crannock Food Pantry skips Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q04ad6c2c30",
  "kind": "yes/no",
  "text": "ref: HR-68597\nhandler: Kendall Umarov\nabout: Esra Castellano\n\nIntake interview with Esra Castellano (2027):\nCaseworker: Time employed?\nEsra Castellano: 40 months.\nCaseworker: Hours worked in the past year?\nEsra Castellano: 861 hours.\nCaseworker: Employees at your worksite?\nEsra Castellano: 250 employees.\nCaseworker: Gross annual pay?\nEsra Castellano: $33,000.\nCaseworker: Take-home annual pay?\nEsra Castellano: 20,807.37 USD.\nCaseworker: Other programme enrolled in?\nEsra Castellano: Quendrel Skills Token.",
  "question": "Under these rules, does Esra Castellano meet the rules for Brenwold Timber Apprentice Support across every applicable gate?",
  "definitions": "Brenwold Timber Apprentice Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are at or beyond 700 hours.\n- Gate B: passed when gross annual pay is $33,000 at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qcd1c268198",
  "kind": "yes/no",
  "text": "Sami Castro: case reference CR-13940 is held for Zara.\n\nPeople who asked to claim Zara (2026):\n- Farid Begum: relationship to Zara: father; months lived with Zara: nine months; annual income: $64,039; filed a claim: no\n- Ravi Douglas: relationship to Zara: grandfather; months lived with Zara: seven months; annual income: $42,465; filed a claim: yes",
  "question": "For Tollmere Lakeside Family Payment, is Farid Begum the person who is left holding the right to claim Zara?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2026: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for five months or above in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Zara lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q872c8862a3",
  "kind": "choice",
  "text": "People who asked to claim Kira (2026):\n| person | relationship to Kira | months lived with Kira | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Esra Ilic | mother | 8 months | 40,969.44 USD | yes |\n| Priya Eriksen | grandmother | 10 months | 37,454.00 USD | yes |\n| Sergio Ramirez | father | 3 months | 91,086.00 USD | yes |\n\nFront counter ticket: CR-70690\nWarm hello from: Lior Grigoryan\nPerson: Kira",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for over 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Kira lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Farrowby Moorland Parish Credit, which person, if any, gets to claim Kira under these rules?",
  "options": [
   "Priya Eriksen",
   "Esra Ilic"
  ]
 },
 {
  "qid": "q0fe067594a",
  "kind": "choice",
  "text": "Hello,\nYour details for Aiko Tesfaye are with the intake desk under HR-38072.\nWarm regards, Jules Shrestha\n\nFacts for Aiko Tesfaye (2026):\n- time employed: 96 months\n- hours worked in the past year: 1,850 hours\n- employees at the worksite: 172 employees\n- gross annual pay: $72,500.00\n- take-home annual pay: $61,500.01\n- enrolled in: Fallowden Retraining Bursary",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is $61,500 or under.\n- Gate B: passed when gross annual pay is strictly smaller than $72,500.\n- Gate C: passed when hours worked in the past year are over 1,500 hours.\n- Route: an applicant enrolled in Fallowden Retraining Bursary skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tovardine Seed Caregiver Leave, which outcome does the application of Aiko Tesfaye get?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "q3ab1d69e21",
  "kind": "choice",
  "text": "Adi Chandra: for the record, file HR-71888 belongs to Tamar Becker.\n\nFacts for Tamar Becker (2025):\n- time employed: 19 months\n- hours worked in the past year: 418 hours\n- employees at the worksite: 255 employees\n- gross annual pay: 78,495.63 USD\n- take-home annual pay: 65,500.00 USD\n- enrolled in: Rickmere Night Course Fund",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly over 18 months.\n- Gate B: passed when take-home annual pay is strictly below 65,500.00 USD.\n- Route: an applicant enrolled in Rickmere Night Course Fund skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Tamar Becker to Hallowdene Logistics Study Grant get?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qfb98e41387",
  "kind": "yes/no",
  "text": "registry: CASE-66581\nkeeper: Mika Zamora\nmatter_of: Amara Patterson\nwelcome: warm and friendly\n\nFacts for Amara Patterson (2026):\n- gross monthly income: $3,359.81\n- net monthly income: $2,510.00\n- countable assets: $12,948.07\n- time in the service area: 23 months\n- age: 22 years\n- enrolled in: Caddowen Pantry Shopping Card",
  "question": "According to these rules, does Amara Patterson qualify for Tarrowick Food Basket Support?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly over 62 years.\n- Gate B: passed when net monthly income is lower than or equal to $2,510.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd07c3ee9fb",
  "kind": "choice",
  "text": "Facts for Casey Nilsen (2025):\n| fact | value |\n| --- | --- |\n| time employed | 14 months |\n| hours worked in the past year | 1,658 hours |\n| employees at the worksite | 30 employees |\n| gross annual pay | $61,559.00 |\n| take-home annual pay | $44,853.96 |\n| enrolled in | Pellbrook Staff Tool Allowance |\n\n[help_line] case_ref=HR-25673 staff=Sami Castro about=Casey Nilsen",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or beyond 64 employees.\n- Gate B: passed when gross annual pay is strictly below the amount of $61,559.01.\n- Gate C: passed when the applicant has been employed for in excess of 17 months.\n- Route: an applicant enrolled in Pellbrook Staff Tool Allowance skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Casey Nilsen to Drummock Robotics Workshop Training Fund lead to?",
  "options": [
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q6a534e7a55",
  "kind": "yes/no",
  "text": "Review desk header\nCase reference: HR-23911\nCaseworker: Mika Zamora\nAbout: Hiro Zielinski\n\nFacts for Hiro Zielinski (2027):\n| fact | value |\n| --- | --- |\n| time employed | 79 months |\n| hours worked in the past year | 420 hours |\n| employees at the worksite | 32 employees |\n| gross annual pay | 105,959.04 USD |\n| take-home annual pay | 89,617.12 USD |\n| enrolled in | Fallowden Retraining Bursary |",
  "question": "Does Hiro Zielinski meet the rules for Tovardine Seed Caregiver Leave by passing every gate that applies?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than $69,000.\n- Gate B: passed when the worksite has 63 employees or above.\n- Gate C: passed when hours worked in the past year are in excess of 1280 hours.\n- Route: an applicant enrolled in Fallowden Retraining Bursary skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9dcf3c434b",
  "kind": "yes/no",
  "text": "Ticket: CR-93779 at the services counter\nRaised by: Teo Quintero\nAbout: Lina\n\nPeople who asked to claim Lina (2025):\n| person | relationship to Lina | months lived with Lina | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Nkechi Evans | mother | 10 months | $85,391.27 | yes |\n| Yusuf Nakamura | father | 11 months | $57,149.20 | yes |",
  "question": "According to these rules, is Yusuf Nakamura the person who ends up with the right to claim Lina for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2025: who may claim Lina.\n- Only one person may claim Lina. Work through these steps in order.\n- Step one: only people who filed a claim for Lina are considered.\n- Step two: of those, only people with whom Lina lived for strictly over 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Lina lived for more months comes first.\n- If nobody is left after step two, nobody may claim Lina.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q33e964d957",
  "kind": "choice",
  "text": "Facts for Yuki Mwangi (2027), as JSON:\n{\"gross_monthly_income\": \"4,421.07 USD\", \"net_monthly_income\": \"2,791.42 USD\", \"countable_assets\": \"12,593.46 USD\", \"time_in_the_service_area\": \"6 months\", \"age\": \"87 years\", \"enrolled_in\": \"Brunsley Energy Rebate\"}\n\n{\"case\": \"CASE-13733\", \"caseworker\": \"Adi Chandra\", \"about\": \"Yuki Mwangi\", \"line\": \"help\"}",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than 5 months.\n- Gate B: passed when the applicant's age is 55 years at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Yuki Mwangi to Sallowick Ward Home Repair Grant get?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q8cbc5fe48f",
  "kind": "choice",
  "text": "Facts for Pavel Vasquez (2026), as JSON:\n{\"gross_monthly_income\": \"$1,795.73\", \"net_monthly_income\": \"$1,225.99\", \"countable_assets\": \"$16,807.79\", \"time_in_the_service_area\": \"nine months\", \"age\": \"59 years\", \"enrolled_in\": \"Tessaly Housing Levy\"}\n\n{\"case\": \"CASE-71636\", \"caseworker\": \"Ari Benali\", \"about\": \"Pavel Vasquez\", \"desk\": \"call centre\"}",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly greater than 60 years.\n- Gate B: passed when the applicant has lived in the service area for over six months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Pavel Vasquez to Wyndholm Forest Fuel Support get?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q03689c197e",
  "kind": "choice",
  "text": "Facts for Hiro Ferreira (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $5,230.10 |\n| net monthly income | $3,497.98 |\n| countable assets | $3,100.01 |\n| time in the service area | 48 months |\n| age | 32 years |\n| enrolled in | Morvane Carers Pension |\n\nOutreach form\nCase: CASE-42596\nCaseworker: Jamie Jorgensen\nAbout: Hiro Ferreira",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $3,100.00 or lower.\n- Gate B: passed when net monthly income is strictly smaller than $3,040.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Hiro Ferreira to Wyndholm Forest Fuel Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (countable assets)"
  ]
 },
 {
  "qid": "q8778876bad",
  "kind": "choice",
  "text": "People who asked to claim Oren (2026):\n| person | relationship to Oren | months lived with Oren | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Amara Thompson | mother | 3 months | $44,174.00 | yes |\n| Gustav Ferreira | uncle | 3 months | $72,309.00 | yes |\n\nWalk-in sheet\nCase: CR-09297\nCaseworker: Riley Watanabe\nAbout: Oren",
  "question": "Sorrenby Island Family Payment rules for 2026: who may claim Oren.\n- Only one person may claim Oren. Work through these steps in order.\n- Step one: only people who filed a claim for Oren are considered.\n- Step two: of those, only people with whom Oren lived for equal to or greater than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Oren lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Oren.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Oren for Sorrenby Island Family Payment?",
  "options": [
   "Amara Thompson",
   "Nobody may claim the child",
   "Gustav Ferreira"
  ]
 },
 {
  "qid": "qaa26cf1dee",
  "kind": "choice",
  "text": "Welcome to the community help desk\nCase reference: CR-55252\nCaseworker: Kiran Morales\nPerson: Otto\n\nPeople who asked to claim Otto (2025):\n| person | relationship to Otto | months lived with Otto | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ailsa Mensah | mother | 12 months | $90,399 | no |\n| Ugo Gordon | uncle | 11 months | $27,297 | yes |\n| Kwame Hakimi | uncle | 10 months | $90,947 | yes |",
  "question": "Ostrowan Prairie Grant rules for 2025: who may claim Otto.\n- Only one person may claim Otto. Work through these steps in order.\n- Step one: only people who filed a claim for Otto are considered.\n- Step two: of those, only people with whom Otto lived for equal to or greater than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Otto lived for more months comes first.\n- If nobody is left after step two, nobody may claim Otto.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Otto for Ostrowan Prairie Grant?",
  "options": [
   "Kwame Hakimi",
   "Ailsa Mensah"
  ]
 },
 {
  "qid": "q8bcd504092",
  "kind": "choice",
  "text": "{\"case\": \"HR-42149\", \"caseworker\": \"Teo Quintero\", \"about\": \"Ivo Anderson\", \"desk\": \"call centre\"}\n\nIntake interview with Ivo Anderson (2026):\nCaseworker: Time employed?\nIvo Anderson: 38 months.\nCaseworker: Hours worked in the past year?\nIvo Anderson: 317 hours.\nCaseworker: Employees at your worksite?\nIvo Anderson: 28 employees.\nCaseworker: Gross annual pay?\nIvo Anderson: 52,788.44 USD.\nCaseworker: Take-home annual pay?\nIvo Anderson: 46,696.90 USD.\nCaseworker: Other programme enrolled in?\nIvo Anderson: Pendrick Training Grant.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has at or greater than 28 employees.\n- Gate B: passed when gross annual pay is equal to or below $49,500.\n- Gate C: passed when take-home annual pay is at or below the level of $35,500.\n- Route: an applicant enrolled in Pendrick Training Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Ivo Anderson to Brenwold Timber Apprentice Support land?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate C is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qd9a4736520",
  "kind": "choice",
  "text": "Avery Obradovic: routine file CR-58915 about Ami, as usual.\n\nPeople who asked to claim Ami (2025):\n- Juliana Sokolov: relationship to Ami: aunt; months lived with Ami: 6 months; annual income: $38,402.09; filed a claim: yes\n- Ivo Gashi: relationship to Ami: father; months lived with Ami: 5 months; annual income: $40,065.00; filed a claim: yes\n- Elias Tesfaye: relationship to Ami: grandfather; months lived with Ami: 6 months; annual income: $35,964.00; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for strictly over 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ami lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, can claim Ami for Corrowby Family Supplement under these rules?",
  "options": [
   "Nobody may claim the child",
   "Ivo Gashi",
   "Juliana Sokolov"
  ]
 },
 {
  "qid": "qb82986a765",
  "kind": "choice",
  "text": "{\"case\": \"HR-15796\", \"caseworker\": \"Nika Hernandez\", \"about\": \"Dario Robinson\", \"desk\": \"intake\"}\n\nFacts for Dario Robinson (2025), as JSON:\n{\"time_employed\": \"37 months\", \"hours_worked_in_the_past_year\": \"2,119 hours\", \"employees_at_the_worksite\": \"388 employees\", \"gross_annual_pay\": \"47,447.13 USD\", \"take-home_annual_pay\": \"29,822.71 USD\", \"enrolled_in\": \"Corranmere Flexi Hours\"}",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for 20 months or above.\n- Gate B: passed when take-home annual pay is 25,500.00 USD or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat comes of the application of Dario Robinson to Marrowby Bakery Family Leave?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qe45cde2a52",
  "kind": "choice",
  "text": "[case_file] ref=CR-29755 worker=Ezra Rosales\n[about] subject=Remi\n\nInterview notes for Remi (2026):\nCaseworker: Yasmin Stewart, your relation to Remi?\nYasmin Stewart: I am Remi's aunt.\nCaseworker: Months Remi lived with you?\nYasmin Stewart: nine months.\nCaseworker: Annual income?\nYasmin Stewart: 23,219.16 USD.\nCaseworker: Filed a claim for Remi?\nYasmin Stewart: yes.\nCaseworker: Anjali Gutierrez, your relation to Remi?\nAnjali Gutierrez: I am Remi's grandmother.\nCaseworker: Months Remi lived with you?\nAnjali Gutierrez: eight months.\nCaseworker: Annual income?\nAnjali Gutierrez: 28,807.40 USD.\nCaseworker: Filed a claim for Remi?\nAnjali Gutierrez: yes.\nCaseworker: Bianca Bergstrom, your relation to Remi?\nBianca Bergstrom: I am Remi's mother.\nCaseworker: Months Remi lived with you?\nBianca Bergstrom: five months.\nCaseworker: Annual income?\nBianca Bergstrom: 52,085.42 USD.\nCaseworker: Filed a claim for Remi?\nBianca Bergstrom: yes.",
  "question": "Sallowmere Family Payment rules for 2026: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for greater than five months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Remi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Remi for Sallowmere Family Payment?",
  "options": [
   "Anjali Gutierrez",
   "Bianca Bergstrom"
  ]
 },
 {
  "qid": "qffa7ecb8b6",
  "kind": "yes/no",
  "text": "file: HR-47154\nsupport: Kazu Yousef\nabout: Cyril Sokolov\nmood: kind\n\nFacts for Cyril Sokolov (2027):\n- time employed: 21 months\n- hours worked in the past year: 1330 hours\n- employees at the worksite: 84 employees\n- gross annual pay: $45,499.99\n- take-home annual pay: $31,391.00\n- enrolled in: Drummock Nurse Stipend",
  "question": "Does Cyril Sokolov fail to qualify for Morrowdene Hospital Group Return Support under these rules?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for a minimum of 21 months.\n- Gate B: passed when the worksite has strictly more than 57 employees.\n- Gate C: passed when gross annual pay is strictly below the amount of $45,500.00.\n- Gate D: passed when hours worked in the past year are greater than or equal to 1330 hours.\n- Route: an applicant enrolled in Drummock Nurse Bursary skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q33e3ad2f10",
  "kind": "yes/no",
  "text": "Review desk note: Alex Lindgren handles CR-04524, about Kai.\n\nPeople who asked to claim Kai (2026):\n- Tomas Vasquez: relationship to Kai: father; months lived with Kai: 12 months; annual income: $83,116.00; filed a claim: no\n- Hiroko Zielinski: relationship to Kai: mother; months lived with Kai: 9 months; annual income: $21,795.00; filed a claim: yes\n- Ubah Halvorsen: relationship to Kai: grandmother; months lived with Kai: 11 months; annual income: $44,399.00; filed a claim: yes",
  "question": "Does the right to claim Kai for Ferrowby Forest Credit pass to a different person from Hiroko Zielinski, or stay unclaimed under these rules?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for strictly more than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Kai lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb82b740df2",
  "kind": "yes/no",
  "text": "Facts for Rafael Tesfaye (2026), as JSON:\n{\"gross_monthly_income\": \"3,545.67 USD\", \"net_monthly_income\": \"3,270.00 USD\", \"countable_assets\": \"7,035.23 USD\", \"time_in_the_service_area\": \"59 months\", \"age\": \"87 years\", \"enrolled_in\": \"Caddow Pantry Basket\"}\n\n{\"ref\": \"CASE-15138\", \"caseworker\": \"Teo Quintero\", \"about\": \"Rafael Tesfaye\", \"kind\": \"intake\"}",
  "question": "Under the rules for Sallowick Ward Home Repair Grant, is Rafael Tesfaye not eligible?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is at or beneath $3,270.\n- Gate B: passed when gross monthly income is strictly beneath $4,010.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8f5487f9f8",
  "kind": "choice",
  "text": "People who asked to claim Lara (2026):\n| person | relationship to Lara | months lived with Lara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Emeka Nilsen | grandfather | 3 months | $24,566.00 | yes |\n| Kiara Campbell | grandmother | 12 months | $91,016.69 | yes |\n| Jiro Esposito | father | 10 months | $36,774.00 | yes |\n\nQuick intake form\nCase reference: CR-31015\nCaseworker: Casey Kaplan\nAbout: Lara",
  "question": "Brellow Orchard Family Credit rules for 2026: who may claim Lara.\n- Only one person may claim Lara. Work through these steps in order.\n- Step one: only people who filed a claim for Lara are considered.\n- Step two: of those, only people with whom Lara lived for a minimum of 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Lara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Lara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Lara for Brellow Orchard Family Credit?",
  "options": [
   "Kiara Campbell",
   "Jiro Esposito",
   "Emeka Nilsen"
  ]
 },
 {
  "qid": "q2c584374f6",
  "kind": "yes/no",
  "text": "{\"ref\": \"HR-82045\", \"handler\": \"Sasha Okonkwo\", \"subject\": \"Kwame Gordon\", \"desk\": \"walk-in\"}\n\nFacts for Kwame Gordon (2027), as JSON:\n{\"time_employed\": \"24 months\", \"hours_worked_in_the_past_year\": \"292 hours\", \"employees_at_the_worksite\": \"73 employees\", \"gross_annual_pay\": \"47,206.73 USD\", \"take-home_annual_pay\": \"39,073.99 USD\", \"enrolled_in\": \"Hemmerly Dockside Fellowship\"}",
  "question": "According to these rules, is Kwame Gordon not eligible for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than or equal to 70,000.00 USD.\n- Gate B: passed when the applicant has been employed for strictly over 24 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q486d3259c7",
  "kind": "choice",
  "text": "reference: CR-88038\nhandler: Casey Kaplan\nsubject: Omar\n\nPeople who asked to claim Omar (2027):\n- Elias Evans: relationship to Omar: uncle; months lived with Omar: 8 months; annual income: $69,600.20; filed a claim: yes\n- Rafael Delgado: relationship to Omar: father; months lived with Omar: 2 months; annual income: $67,844.00; filed a claim: yes\n- Tamar Kaur: relationship to Omar: mother; months lived with Omar: 9 months; annual income: $67,844.00; filed a claim: yes",
  "question": "Tessenvale Valley Child Credit rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for strictly greater than 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Omar lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which candidate, if any, may claim Omar for Tessenvale Valley Child Credit?",
  "options": [
   "Tamar Kaur",
   "Elias Evans"
  ]
 },
 {
  "qid": "q11d689ec6c",
  "kind": "yes/no",
  "text": "Intake form, help line team\nCase reference: HR-39886\nCaseworker: Sasha Okonkwo\nAbout: Dagny Lindqvist\n\nFacts for Dagny Lindqvist (2025):\n| fact | value |\n| --- | --- |\n| time employed | 27 months |\n| hours worked in the past year | thirteen hours |\n| employees at the worksite | 204 employees |\n| gross annual pay | 55,308.01 USD |\n| take-home annual pay | 44,963.82 USD |\n| enrolled in | none |",
  "question": "Under these rules, is Dagny Lindqvist ineligible for Tovardine Seed Caregiver Leave as a whole?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for fourteen months or above.\n- Gate B: passed when gross annual pay is 55,308.01 USD or under.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf0f5452112",
  "kind": "yes/no",
  "text": "ref: HR-49924\ncaseworker: Yuki Adeyemi\nabout: Freya Ruiz\noffice: branch\n\nIntake interview with Freya Ruiz (2025):\nCaseworker: Time employed?\nFreya Ruiz: 27 months.\nCaseworker: Hours worked in the past year?\nFreya Ruiz: 941 hours.\nCaseworker: Employees at your worksite?\nFreya Ruiz: 392 employees.\nCaseworker: Gross annual pay?\nFreya Ruiz: 75,617.74 USD.\nCaseworker: Take-home annual pay?\nFreya Ruiz: 56,736.99 USD.\nCaseworker: Other programme enrolled in?\nFreya Ruiz: Ellerwick Trainee Stream.",
  "question": "Following the listed rules, does Freya Ruiz qualify for Sorrelby Child Care Support?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly more than 940 hours.\n- Gate B: passed when gross annual pay is smaller than $60,000.\n- Gate C: passed when the applicant has been employed for at or over fourteen months.\n- Route: an applicant enrolled in Ellerwick Trainee Scheme skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdb14f6cfe1",
  "kind": "yes/no",
  "text": "Services counter intake form\nCase reference: CR-72712\nCaseworker: Kiran Morales\nAbout: Joon\n\nPeople who asked to claim Joon (2025):\n| person | relationship to Joon | months lived with Joon | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kiara Delgado | grandmother | 7 months | 94,846.67 USD | no |\n| Tariq Petrov | father | 4 months | 71,948.59 USD | yes |",
  "question": "Does Kiara Delgado end up as the sole person who may claim Joon for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for 5 months at minimum in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Joon lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2f61c6cd82",
  "kind": "choice",
  "text": "People who asked to claim Ivan (2026):\n| person | relationship to Ivan | months lived with Ivan | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Tamar Esposito | mother | 11 months | 41,459.00 USD | no |\n| Dario Eriksen | father | 7 months | 52,330.51 USD | yes |\n| Juliana Johnson | aunt | 11 months | 17,718.00 USD | yes |\n| Mateo Kovacs | uncle | 8 months | 60,281.00 USD | yes |\n\nAdi Chandra: back office has Ivan down for CR-44577, just routine stuff.",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for strictly above 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Farrowby Moorland Parish Credit, which person, if any, may claim Ivan?",
  "options": [
   "Mateo Kovacs",
   "Dario Eriksen",
   "Juliana Johnson"
  ]
 },
 {
  "qid": "q5c86078a8a",
  "kind": "yes/no",
  "text": "registry: CASE-66581\nkeeper: Mika Zamora\nmatter_of: Amara Patterson\nwelcome: warm and friendly\n\nFacts for Amara Patterson (2026):\n- gross monthly income: $3,359.81\n- net monthly income: $2,510.00\n- countable assets: $12,948.07\n- time in the service area: 23 months\n- age: 22 years\n- enrolled in: Caddowen Pantry Shopping Card",
  "question": "According to these rules, does Amara Patterson qualify for Tarrowick Food Basket Support?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly over 21 years.\n- Gate B: passed when net monthly income is lower than or equal to $2,510.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 }
]
