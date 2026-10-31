# G5-H blind read T15-blind_read-251c30af-000 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/pilot/g5h/answers/T15-blind_read-251c30af-000.json

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
  "qid": "q42805fe83a",
  "kind": "yes/no",
  "text": "Internal note: Quinn Pavlenko looks after case CASE-55272 in the regional service team, about Jakub Abebe.\n\nFacts for Jakub Abebe (2026):\n- gross monthly income: 2,420.91 USD\n- net monthly income: 2,175.00 USD\n- countable assets: 3,213.44 USD\n- time in the service area: 10 months\n- age: 62 years\n- enrolled in: Tallow Ridge Commuter Permit",
  "question": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 10 months.\n- Gate B: passed when net monthly income is at or below 2,175.00 USD.\n- Route: an applicant enrolled in Ambermoor Water Rebate skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Jakub Abebe meet the rules for Sennamoor River Rent Support by passing every gate that applies?"
 },
 {
  "qid": "q9f07ffcf96",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CR-21117, handled by Mika Zamora\n[subject_line] Liam is at the heart of it\n\nPeople who asked to claim Liam (2025):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hamid Sullivan | father | 12 months | 77,719.94 USD | no |\n| Galina Becker | aunt | 7 months | 15,880.00 USD | yes |\n| Yara Douglas | aunt | 12 months | 54,991.85 USD | no |\n| Gustav Gordon | grandfather | 6 months | 30,293.55 USD | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for strictly higher than 7 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Liam lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is Galina Becker the person who ends up with the right to claim Liam for Tessenvale Valley Child Credit?"
 },
 {
  "qid": "qd2065b8884",
  "kind": "choice",
  "text": "People who asked to claim Remi (2027), as JSON:\n{\"people\": [{\"name\": \"Ingrid Tanaka\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"3 months\", \"annual_income\": \"$19,696.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Gabriel Dragic\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"0 months\", \"annual_income\": \"$38,555.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nikolai Singh\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"$49,286.90\", \"filed_a_claim\": \"no\"}, {\"name\": \"Amara Robinson\", \"relationship\": \"mother\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"$71,530.00\", \"filed_a_claim\": \"no\"}]}\n\n{\"case\": \"CR-14033\", \"caseworker\": \"Blair Xiong\", \"about\": \"Remi\", \"line\": \"help\"}",
  "question": "Sorrenby Island Family Payment rules for 2027: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for strictly over 6 months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Remi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Remi for Sorrenby Island Family Payment?",
  "options": [
   "Nobody may claim the child",
   "Amara Robinson"
  ]
 },
 {
  "qid": "q490443b803",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CR-21117, handled by Mika Zamora\n[subject_line] Liam is at the heart of it\n\nPeople who asked to claim Liam (2025):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hamid Sullivan | father | 12 months | 77,719.94 USD | no |\n| Galina Becker | aunt | 8 months | 15,880.00 USD | yes |\n| Yara Douglas | aunt | 12 months | 54,991.85 USD | no |\n| Gustav Gordon | grandfather | 6 months | 30,293.55 USD | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for strictly higher than 7 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Liam lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is Galina Becker the person who ends up with the right to claim Liam for Tessenvale Valley Child Credit?"
 },
 {
  "qid": "qe7dd9de581",
  "kind": "choice",
  "text": "Case note: Casey Kaplan holds case file CR-48663 about Elif. The record sits at the town hall desk.\n\nPeople who asked to claim Elif (2027):\n- Mateo Watson: relationship to Elif: uncle; months lived with Elif: nine months; annual income: $72,323; filed a claim: yes\n- Oskar Demir: relationship to Elif: grandfather; months lived with Elif: four months; annual income: $63,929; filed a claim: yes\n- Ilse Esposito: relationship to Elif: grandmother; months lived with Elif: eight months; annual income: $64,988; filed a claim: yes\n- Juliana Kelly: relationship to Elif: mother; months lived with Elif: eight months; annual income: $36,088.88; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for a minimum of five months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Elif lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Elif for Ostrowan Prairie Grant?",
  "options": [
   "Mateo Watson",
   "Nobody may claim the child",
   "Juliana Kelly"
  ]
 },
 {
  "qid": "q639f453b56",
  "kind": "choice",
  "text": "Front counter intake form\nReference: CASE-37940\nCaseworker: Ari Benali\nPerson: Zofia Gordon\n\nFacts for Zofia Gordon (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,260.45 |\n| net monthly income | $2,804.36 |\n| countable assets | $7,900 |\n| time in the service area | 8 months |\n| age | 21 years |\n| enrolled in | Velgate Pantry Voucher |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly beneath the level of $7,900.\n- Gate B: passed when net monthly income is at or under $3,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Zofia Gordon for Corrivale Valley Childcare Grant come out?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q0ebe666d12",
  "kind": "choice",
  "text": "Internal case note for CR-38582.\nSet down by Avery Obradovic at the town hall office, for Ami.\n\nPeople who asked to claim Ami (2025):\n- Xavier Dlamini: relationship to Ami: father; months lived with Ami: 9 months; annual income: 40,128.00 USD; filed a claim: no\n- Freya Sharma: relationship to Ami: mother; months lived with Ami: 3 months; annual income: 63,923.77 USD; filed a claim: yes\n- Nkechi Lindqvist: relationship to Ami: grandmother; months lived with Ami: 3 months; annual income: 45,509.91 USD; filed a claim: yes\n- Anjali Sokolov: relationship to Ami: grandmother; months lived with Ami: 9 months; annual income: 49,483.00 USD; filed a claim: yes",
  "question": "Tollmere Lakeside Family Payment rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for a minimum of 5 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Ami for Tollmere Lakeside Family Payment, who is it?",
  "options": [
   "Freya Sharma",
   "Anjali Sokolov",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q4afd54e42c",
  "kind": "yes/no",
  "text": "Regional service office intake\nCase reference: HR-00259\nCaseworker: Ren Dvorak\nSubject: Ivo Petrov\n\nIntake interview with Ivo Petrov (2025):\nCaseworker: How long have you been employed here?\nIvo Petrov: 65 months.\nCaseworker: How many hours did you work in the past year?\nIvo Petrov: 737 hours.\nCaseworker: How many employees work at your worksite?\nIvo Petrov: 72 employees.\nCaseworker: What is your gross annual pay?\nIvo Petrov: $87,861.70.\nCaseworker: And your take-home annual pay?\nIvo Petrov: $75,933.62.\nCaseworker: Which other programme are you enrolled in?\nIvo Petrov: Heldane Transit Pass.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or under the amount of $60,500.00.\n- Gate B: passed when the worksite has equal to or above 72 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, does a gate that applies end the application of Ivo Petrov to Quenhollow Brewery Bereavement Leave?"
 },
 {
  "qid": "q8b8a1a6f36",
  "kind": "yes/no",
  "text": "ref: CASE-57690\nowner: Kazu Yousef\nabout: Ren Demir\nteam: outreach\n\nFacts for Ren Demir (2025):\n- gross monthly income: 1,478.80 USD\n- net monthly income: 1,200.65 USD\n- countable assets: 12,493.86 USD\n- time in the service area: 11 months\n- age: 46 years\n- enrolled in: Vellmar Transit Card",
  "question": "Ostmere Lakeside Winter Energy Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for 11 months at minimum.\n- Gate B: passed when net monthly income is strictly lower than $1,935.\n- Route: an applicant enrolled in Dunmarrow Housing Repair skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is Ren Demir eligible for Ostmere Lakeside Winter Energy Support given every gate that applies is passed?"
 },
 {
  "qid": "q39816d4c51",
  "kind": "yes/no",
  "text": "desk: community help\ncase: HR-11145\ncaseworker: Ezra Rosales\nabout: Priya Stewart\n\nFacts for Priya Stewart (2027):\n- time employed: 28 months\n- hours worked in the past year: 809 hours\n- employees at the worksite: 178 employees\n- gross annual pay: $15,595.33\n- take-home annual pay: $11,458.57\n- enrolled in: Gerrondale Tenant Aid",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for greater than or equal to 19 months.\n- Gate B: passed when gross annual pay is at or less than $30,500.00.\n- Gate C: passed when hours worked in the past year are equal to or greater than 810 hours.\n- Route: an applicant enrolled in Selwick Fresh Box skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is Priya Stewart ineligible for Marrowby Bakery Family Leave?"
 },
 {
  "qid": "q9aab5b0703",
  "kind": "yes/no",
  "text": "Outreach sheet\nReference: HR-76610\nWorker: Yuki Adeyemi\nAbout: Ilse Hamilton\n\nFacts for Ilse Hamilton (2027):\n| fact | value |\n| --- | --- |\n| time employed | 50 months |\n| hours worked in the past year | 460 hours |\n| employees at the worksite | 319 employees |\n| gross annual pay | 39,594.37 USD |\n| take-home annual pay | 28,000.01 USD |\n| enrolled in | Lumenfold Skills Voucher |",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than or equal to $36,500.\n- Gate B: passed when take-home annual pay is at or below the level of $28,000.\n- Route: an applicant enrolled in Lumenfold Skills Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is Ilse Hamilton ineligible for Halvorne Shipyard Tuition Assistance?"
 },
 {
  "qid": "q05e6dd01cc",
  "kind": "yes/no",
  "text": "Facts for Ibrahim Patterson (2026), as JSON:\n{\"gross_monthly_income\": \"3,829.99 USD\", \"net_monthly_income\": \"2,408.50 USD\", \"countable_assets\": \"5,011.87 USD\", \"time_in_the_service_area\": \"26 months\", \"age\": \"37 years\", \"enrolled_in\": \"Ellisford Winter Supplement\"}\n\n{\"caseworker\": \"Jules Shrestha\", \"about\": \"Ibrahim Patterson\", \"case\": \"CASE-23455\", \"desk\": \"community\"}",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $8,350 or less.\n- Gate B: passed when gross monthly income is strictly under $3,830.\n- Gate C: passed when the applicant's age is strictly more than 36 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Ibrahim Patterson fail to qualify for admission to Wyndholm Forest Fuel Support?"
 },
 {
  "qid": "q6aa0a37a30",
  "kind": "choice",
  "text": "Facts for Tomas Zielinski (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $1,085.76 |\n| net monthly income | $776.94 |\n| countable assets | $5,999.99 |\n| time in the service area | 5 months |\n| age | 25 years |\n| enrolled in | Mirrowen Transit Voucher |\n\nteam: casework\ncase: CASE-63330\ncaseworker: Tomi Eklund\nabout: Tomas Zielinski",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than or equal to 62 years.\n- Gate B: passed when the applicant has lived in the service area for greater than 4 months.\n- Gate C: passed when countable assets are at or under $6,000.00.\n- Route: an applicant enrolled in Mirrowen Transit Voucher skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Tomas Zielinski to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q568d01e8e4",
  "kind": "choice",
  "text": "[support_hub] case_ref=HR-56101\n[support_hub] handler=Teo Quintero subject=Xavier Gallegos\n\nIntake interview with Xavier Gallegos (2025):\nCaseworker: How long have you been employed here?\nXavier Gallegos: 36 months.\nCaseworker: How many hours did you work in the past year?\nXavier Gallegos: 1,024 hours.\nCaseworker: How many employees work at your worksite?\nXavier Gallegos: 83 employees.\nCaseworker: What is your gross annual pay?\nXavier Gallegos: 87,287.15 USD.\nCaseworker: And your take-home annual pay?\nXavier Gallegos: 60,662.62 USD.\nCaseworker: Which other programme are you enrolled in?\nXavier Gallegos: Wendle Trade Pilot.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are above 1,023 hours.\n- Gate B: passed when the worksite has 73 employees or above.\n- Route: an applicant enrolled in Wendle Trade Pathway skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Xavier Gallegos for Brenwold Timber Apprentice Support come out?",
  "options": [
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Eligible"
  ]
 },
 {
  "qid": "qe9c7845afb",
  "kind": "yes/no",
  "text": "Routine note: CASE-75032\nFrom Avery Obradovic for the call centre, about Bruno Tanaka.\n\nFacts for Bruno Tanaka (2026):\n- gross monthly income: $2,584.81\n- net monthly income: $2,159.69\n- countable assets: $7,949.99\n- time in the service area: 8 months\n- age: 85 years\n- enrolled in: Tallow Ridge Commuter Permit",
  "question": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the level of $7,950.\n- Gate B: passed when the applicant's age is greater than or equal to 62 years.\n- Gate C: passed when net monthly income is strictly below $2,260.\n- Gate D: passed when gross monthly income is at or under the amount of $2,675.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Bruno Tanaka ineligible for Sennamoor River Rent Support given the listed gates?"
 },
 {
  "qid": "qb2ea11e250",
  "kind": "choice",
  "text": "case: HR-57972\ncentre: contact\nhandler: Avery Obradovic\nperson: Avery Sullivan\n\nFacts for Avery Sullivan (2026):\n- time employed: 78 months\n- hours worked in the past year: 1400 hours\n- employees at the worksite: 28 employees\n- gross annual pay: $57,240.80\n- take-home annual pay: $46,444.40\n- enrolled in: Corrivale Welding Bursary",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has greater than 27 employees.\n- Gate B: passed when hours worked in the past year are at or greater than 1400 hours.\n- Gate C: passed when take-home annual pay is $36,500.00 at the most.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Avery Sullivan to Halvorne Shipyard Tuition Assistance lead to?",
  "options": [
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qa75b6196ea",
  "kind": "yes/no",
  "text": "{\"case\": \"HR-57252\", \"caseworker\": \"Kazu Yousef\", \"about\": \"Dmitri Okafor\", \"line\": \"help\"}\n\nIntake interview with Dmitri Okafor (2027):\nCaseworker: How long have you been employed here?\nDmitri Okafor: 25 months.\nCaseworker: How many hours did you work in the past year?\nDmitri Okafor: 1,847 hours.\nCaseworker: How many employees work at your worksite?\nDmitri Okafor: 99 employees.\nCaseworker: What is your gross annual pay?\nDmitri Okafor: 53,793.93 USD.\nCaseworker: And your take-home annual pay?\nDmitri Okafor: 51,069.49 USD.\nCaseworker: Which other programme are you enrolled in?\nDmitri Okafor: Ellerwick Trainee Stream.",
  "question": "Sorrelby Child Care Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or less than 45,500.00 USD.\n- Gate B: passed when the applicant has been employed for strictly over 24 months.\n- Gate C: passed when the worksite has 64 employees or above.\n- Gate D: passed when gross annual pay is 58,000.00 USD or under.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, does Dmitri Okafor meet the rules for Sorrelby Child Care Support?"
 },
 {
  "qid": "qcbf180277b",
  "kind": "yes/no",
  "text": "[review_desk] case=CR-02714 caseworker=Yuki Adeyemi\n[about] subject=Uri thanks_for_patience\n\nPeople who asked to claim Uri (2025):\n| person | relationship to Uri | months lived with Uri | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Elias Delgado | father | 3 months | 18,655.00 USD | yes |\n| Cyril Russell | grandfather | 8 months | 69,405.00 USD | yes |\n| Felix Schultz | uncle | 10 months | 18,655.00 USD | yes |",
  "question": "Tollmere Lakeside Family Payment rules for 2025: who may claim Uri.\n- Only one person may claim Uri. Work through these steps in order.\n- Step one: only people who filed a claim for Uri are considered.\n- Step two: of those, only people with whom Uri lived for over 5 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Uri lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Uri.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is Cyril Russell the person who ends up with the right to claim Uri for Tollmere Lakeside Family Payment?"
 },
 {
  "qid": "q6439319371",
  "kind": "yes/no",
  "text": "Facts for Vesna Iyer (2026):\n| fact | value |\n| --- | --- |\n| time employed | 11 months |\n| hours worked in the past year | 176 hours |\n| employees at the worksite | 66 employees |\n| gross annual pay | 87,021.81 USD |\n| take-home annual pay | 65,731.65 USD |\n| enrolled in | Ostermere Skills Scholarship |\n\nNote for the intake desk: Vesna Iyer is named on case HR-97021, which Jules Shrestha keeps.",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for above 10 months.\n- Gate B: passed when the worksite has a minimum of 39 employees.\n- Route: an applicant enrolled in Ostermere Skills Bursary skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder the rules for Drummock Robotics Workshop Training Fund, is Vesna Iyer not eligible?"
 },
 {
  "qid": "q89ac372b4e",
  "kind": "choice",
  "text": "Facts for Bianca Zielinski (2026):\n| fact | value |\n| --- | --- |\n| time employed | 105 months |\n| hours worked in the past year | 1,032 hours |\n| employees at the worksite | 34 employees |\n| gross annual pay | 31,000.01 USD |\n| take-home annual pay | 29,009.83 USD |\n| enrolled in | Stonevale Staff Nursery Grant |\n\nEzra Rosales: for the record, file HR-17663 belongs to Bianca Zielinski.",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has equal to or above 35 employees.\n- Gate B: passed when gross annual pay is $31,000 or under.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, how does the application of Bianca Zielinski to Orrendale Printworks Sick Leave Supplement turn out?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qf8545f3bc4",
  "kind": "yes/no",
  "text": "{\"record\": \"case\", \"reference\": \"CR-13951\", \"caseworker\": \"Kazu Yousef\", \"about\": \"Bao\"}\n\nInterview notes for Bao (2027):\nCaseworker: Ubah Esposito, how are you related to Bao?\nUbah Esposito: I am Bao's aunt.\nCaseworker: How long did Bao live with you in 2027?\nUbah Esposito: 7 months.\nCaseworker: What was your annual income?\nUbah Esposito: $17,995.97.\nCaseworker: Did you file a claim for Bao?\nUbah Esposito: yes.\nCaseworker: Juliana Nilsen, how are you related to Bao?\nJuliana Nilsen: I am Bao's mother.\nCaseworker: How long did Bao live with you in 2027?\nJuliana Nilsen: 10 months.\nCaseworker: What was your annual income?\nJuliana Nilsen: $87,405.86.\nCaseworker: Did you file a claim for Bao?\nJuliana Nilsen: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2027: who may claim Bao.\n- Only one person may claim Bao. Work through these steps in order.\n- Step one: only people who filed a claim for Bao are considered.\n- Step two: of those, only people with whom Bao lived for a minimum of 6 months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Bao lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Bao.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Juliana Nilsen end up as the sole person who may claim Bao for Kelmstone Mountain Family Grant?"
 },
 {
  "qid": "q550f165d7a",
  "kind": "yes/no",
  "text": "case_id: HR-58613\nworker_name: Kiran Morales\nsubject_name: Esra Hudson\n\nFacts for Esra Hudson (2026):\n- time employed: 7 months\n- hours worked in the past year: 1,177 hours\n- employees at the worksite: 102 employees\n- gross annual pay: $28,412.68\n- take-home annual pay: $24,417.82\n- enrolled in: Idrane Tuition Grant",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly in excess of 920 hours.\n- Gate B: passed when the applicant has been employed for strictly above 6 months.\n- Gate C: passed when the worksite has equal to or greater than 59 employees.\n- Route: an applicant enrolled in Idrane Tuition Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is Esra Hudson eligible for Wendmoor Mill Parental Leave?"
 },
 {
  "qid": "q4031efcdbf",
  "kind": "yes/no",
  "text": "Dear colleague,\nPlease see CASE-50833 about Ilse Campbell on the queue.\nThanks, Casey Kaplan\n\nFacts for Ilse Campbell (2027):\n- gross monthly income: 4,550.03 USD\n- net monthly income: 3,897.08 USD\n- countable assets: 2,394.78 USD\n- time in the service area: 16 months\n- age: 62 years\n- enrolled in: Pellbrook Heating Grant",
  "question": "Tarrowick Food Basket Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or greater than 10 months.\n- Gate B: passed when gross monthly income is strictly under 3,980.00 USD.\n- Gate C: passed when countable assets are strictly below the level of 3,650.00 USD.\n- Gate D: passed when the applicant's age is 57 years or more.\n- Route: an applicant enrolled in Pellbrook Heating Grant skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tarrowick Food Basket Support, does a gate that applies halt the application made by Ilse Campbell?"
 },
 {
  "qid": "q1d985c3bfc",
  "kind": "choice",
  "text": "Facts for Esra Bergstrom (2026):\n| fact | value |\n| --- | --- |\n| time employed | 4 months |\n| hours worked in the past year | 2,053 hours |\n| employees at the worksite | 252 employees |\n| gross annual pay | $45,465.88 |\n| take-home annual pay | $33,500 |\n| enrolled in | Tundale Care Voucher |\n\nCounter ticket: HR-92420\nRaised by: Riley Watanabe\nAbout: Esra Bergstrom",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for at or greater than 15 months.\n- Gate B: passed when take-home annual pay is at or under $33,500.\n- Route: an applicant enrolled in Tundale Care Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Esra Bergstrom to Pelmoor Ceramics Carer Support get?",
  "options": [
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)"
  ]
 },
 {
  "qid": "qb6a75839b9",
  "kind": "yes/no",
  "text": "Outreach sheet\nReference: HR-76610\nWorker: Yuki Adeyemi\nAbout: Ilse Hamilton\n\nFacts for Ilse Hamilton (2027):\n| fact | value |\n| --- | --- |\n| time employed | 50 months |\n| hours worked in the past year | 460 hours |\n| employees at the worksite | 319 employees |\n| gross annual pay | 39,594.37 USD |\n| take-home annual pay | 28,000.01 USD |\n| enrolled in | Lumenfold Skills Voucher |",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than or equal to $36,500.\n- Gate B: passed when take-home annual pay is at or below the level of 28,000.01 USD.\n- Route: an applicant enrolled in Lumenfold Skills Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is Ilse Hamilton ineligible for Halvorne Shipyard Tuition Assistance?"
 },
 {
  "qid": "q4ba3ca8a9c",
  "kind": "yes/no",
  "text": "Routine note: CASE-75032\nFrom Avery Obradovic for the call centre, about Bruno Tanaka.\n\nFacts for Bruno Tanaka (2026):\n- gross monthly income: $2,584.81\n- net monthly income: $2,159.69\n- countable assets: $7,949.99\n- time in the service area: 8 months\n- age: 85 years\n- enrolled in: Tallow Ridge Commuter Permit",
  "question": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the level of $7,950.\n- Gate B: passed when the applicant's age is greater than or equal to 62 years.\n- Gate C: passed when net monthly income is strictly below $2,260.\n- Gate D: passed when gross monthly income is at or under the amount of $2,675.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, does Bruno Tanaka qualify for Sennamoor River Rent Support?"
 },
 {
  "qid": "q2507a40b34",
  "kind": "yes/no",
  "text": "Help ticket: HR-97900\nWho: Quinn Pavlenko\nAbout: Toni Lindqvist\n\nIntake interview with Toni Lindqvist (2027):\nCaseworker: How long have you been employed here?\nToni Lindqvist: 109 months.\nCaseworker: How many hours did you work in the past year?\nToni Lindqvist: 851 hours.\nCaseworker: How many employees work at your worksite?\nToni Lindqvist: 61 employees.\nCaseworker: What is your gross annual pay?\nToni Lindqvist: 62,499.24 USD.\nCaseworker: And your take-home annual pay?\nToni Lindqvist: 48,758.23 USD.\nCaseworker: Which other programme are you enrolled in?\nToni Lindqvist: none.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly more than 850 hours.\n- Gate B: passed when the worksite has a minimum of 60 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is Toni Lindqvist eligible for Quenhollow Brewery Bereavement Leave overall?"
 },
 {
  "qid": "qae330fb495",
  "kind": "yes/no",
  "text": "Ticket: people services case CR-00914\nRaised by: Dani Ishikawa\nAbout: Rafi\n\nInterview notes for Rafi (2025):\nCaseworker: Matias Wojcik, how are you related to Rafi?\nMatias Wojcik: I am Rafi's uncle.\nCaseworker: How long did Rafi live with you in 2025?\nMatias Wojcik: 12 months.\nCaseworker: What was your annual income?\nMatias Wojcik: 72,113.66 USD.\nCaseworker: Did you file a claim for Rafi?\nMatias Wojcik: yes.\nCaseworker: Farid Haddad, how are you related to Rafi?\nFarid Haddad: I am Rafi's father.\nCaseworker: How long did Rafi live with you in 2025?\nFarid Haddad: 11 months.\nCaseworker: What was your annual income?\nFarid Haddad: $17,663.\nCaseworker: Did you file a claim for Rafi?\nFarid Haddad: yes.\nCaseworker: Dmitri Dubois, how are you related to Rafi?\nDmitri Dubois: I am Rafi's grandfather.\nCaseworker: How long did Rafi live with you in 2025?\nDmitri Dubois: 9 months.\nCaseworker: What was your annual income?\nDmitri Dubois: $88,260.\nCaseworker: Did you file a claim for Rafi?\nDmitri Dubois: yes.\nCaseworker: Luka Patterson, how are you related to Rafi?\nLuka Patterson: I am Rafi's uncle.\nCaseworker: How long did Rafi live with you in 2025?\nLuka Patterson: 0 months.\nCaseworker: What was your annual income?\nLuka Patterson: $81,821.\nCaseworker: Did you file a claim for Rafi?\nLuka Patterson: yes.",
  "question": "Sallowmere Family Payment rules for 2025: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for larger than 7 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Rafi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is Dmitri Dubois excluded from claiming Rafi for Sallowmere Family Payment?"
 },
 {
  "qid": "q355b654ca6",
  "kind": "choice",
  "text": "{\"about\": \"Nika Ferreira\", \"case\": \"CASE-98161\", \"caseworker\": \"Sami Castro\", \"team\": \"help line\"}\n\nIntake interview with Nika Ferreira (2025):\nCaseworker: What is your gross monthly income?\nNika Ferreira: 4,799.49 USD.\nCaseworker: And your net monthly income, after deductions?\nNika Ferreira: 3,633.95 USD.\nCaseworker: What are your countable assets worth?\nNika Ferreira: 13,217.63 USD.\nCaseworker: How long have you lived in the service area?\nNika Ferreira: ten months.\nCaseworker: How old are you?\nNika Ferreira: nineteen years.\nCaseworker: Which other programme are you enrolled in?\nNika Ferreira: Aldervale Meal Basket.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or above nine months.\n- Gate B: passed when the applicant's age is at or over 63 years.\n- Gate C: passed when net monthly income is strictly below 2,580.00 USD.\n- Gate D: passed when gross monthly income is strictly smaller than 3,410.00 USD.\n- Route: an applicant enrolled in Aldervale Meal Basket skips Gate B, Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tamsfell Senior Home Support, which outcome does the application submitted by Nika Ferreira get?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate D is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q1c9cf2311f",
  "kind": "choice",
  "text": "Routine ticket: CR-23595\nRaised by: Blair Xiong\nAbout: Tove\n\nPeople who asked to claim Tove (2025):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ugo Reynolds | father | one month | $70,951.39 | yes |\n| Fatima Russell | mother | four months | $47,572.81 | yes |\n| Dmitri Singh | grandfather | three months | $35,298 | no |\n| Dagny Ferreira | grandmother | four months | $65,596 | yes |",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for strictly more than five months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Tove lived for more months comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Tove for Corrowby Family Supplement?",
  "options": [
   "Nobody may claim the child",
   "Ugo Reynolds"
  ]
 },
 {
  "qid": "q9db7940368",
  "kind": "choice",
  "text": "Facts for Greta Kelly (2027):\n| fact | value |\n| --- | --- |\n| time employed | 13 months |\n| hours worked in the past year | 312 hours |\n| employees at the worksite | 30 employees |\n| gross annual pay | 88,111.14 USD |\n| take-home annual pay | 65,133.42 USD |\n| enrolled in | Hathermoor Relief Leave |\n\nref: HR-56537\noffice: branch\nlead: Quinn Pavlenko\nperson: Greta Kelly",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or under the amount of 47,000.00 USD.\n- Gate B: passed when hours worked in the past year are at or above 810 hours.\n- Gate C: passed when the applicant has been employed for at or over 14 months.\n- Gate D: passed when the worksite has strictly in excess of 25 employees.\n- Route: an applicant enrolled in Hathermoor Relief Leave skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Greta Kelly to Pelmoor Ceramics Carer Support?",
  "options": [
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (time employed)",
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate D is the reason (employees at the worksite)"
  ]
 },
 {
  "qid": "q0381e8e9b7",
  "kind": "yes/no",
  "text": "People who asked to claim Amir (2025):\n| person | relationship to Amir | months lived with Amir | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gabriel Eriksen | grandfather | 1 month | 81,409.57 USD | yes |\n| Cyril Zielinski | father | 5 months | $30,615 | no |\n| Mateo Evans | grandfather | 8 months | $70,551 | no |\n\n[front_counter] reference=CR-63869 caseworker=Sami Castro person=Amir",
  "question": "Mollenby Canal Child Supplement rules for 2025: who may claim Amir.\n- Only one person may claim Amir. Work through these steps in order.\n- Step one: only people who filed a claim for Amir are considered.\n- Step two: of those, only people with whom Amir lived for a minimum of 6 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Amir lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Amir.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs it not true that Gabriel Eriksen may not claim Amir for Mollenby Canal Child Supplement?"
 },
 {
  "qid": "q94d3955f4e",
  "kind": "yes/no",
  "text": "Front counter ticket: CASE-30397\nWarm hello from: Toni Lazar\nPerson: Felix Murphy\n\nFacts for Felix Murphy (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,727.82 |\n| net monthly income | $1,940.01 |\n| countable assets | $2,871.56 |\n| time in the service area | 47 months |\n| age | twenty years |\n| enrolled in | Ruddock Shuttle Card |",
  "question": "Corvane Transit Fare Discount eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under the amount of $2,285.00.\n- Gate B: passed when net monthly income is $1,940.00 or under.\n- Route: an applicant enrolled in Ruddock Shuttle Card skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Felix Murphy not eligible for Corvane Transit Fare Discount as the rules stand?"
 },
 {
  "qid": "q9bf35c3863",
  "kind": "choice",
  "text": "Facts for Wanjiru Okoro (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,968.68 |\n| net monthly income | $4,049.81 |\n| countable assets | $4,990.28 |\n| time in the service area | 13 months |\n| age | 64 years |\n| enrolled in | Kelder Veterans Pension |\n\nTicket CASE-08394\nWith: Morgan Mendoza\nAbout: Wanjiru Okoro",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 64 years or greater.\n- Gate B: passed when the applicant has lived in the service area for over 8 months.\n- Route: an applicant enrolled in Kelder Veterans Pension skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat does Wanjiru Okoro get from the application to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "q0e78e0d985",
  "kind": "yes/no",
  "text": "Facts for Bianca Anderson (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,743.72 USD |\n| net monthly income | 1,969.71 USD |\n| countable assets | 4,650.00 USD |\n| time in the service area | 2 months |\n| age | 49 years |\n| enrolled in | Velden Transit Pass |\n\nCase note: CASE-91786 for Bianca Anderson. Handled by Remy Tran.",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than 4 months.\n- Gate B: passed when countable assets are strictly under 4,650.00 USD.\n- Gate C: passed when gross monthly income is strictly under 3,635.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Bianca Anderson fail to qualify for Sallowick Ward Home Repair Grant on these rules?"
 },
 {
  "qid": "qa269c32ecb",
  "kind": "yes/no",
  "text": "Jamie Jorgensen: file CR-44991 about Isla is on my list.\n\nInterview notes for Isla (2026):\nCaseworker: Ivo Mensah, how are you related to Isla?\nIvo Mensah: I am Isla's father.\nCaseworker: How long did Isla live with you in 2026?\nIvo Mensah: 7 months.\nCaseworker: What was your annual income?\nIvo Mensah: $64,041.00.\nCaseworker: Did you file a claim for Isla?\nIvo Mensah: yes.\nCaseworker: Yasmin Haddad, how are you related to Isla?\nYasmin Haddad: I am Isla's grandmother.\nCaseworker: How long did Isla live with you in 2026?\nYasmin Haddad: 7 months.\nCaseworker: What was your annual income?\nYasmin Haddad: $72,151.67.\nCaseworker: Did you file a claim for Isla?\nYasmin Haddad: yes.\nCaseworker: Juliana Hudson, how are you related to Isla?\nJuliana Hudson: I am Isla's mother.\nCaseworker: How long did Isla live with you in 2026?\nJuliana Hudson: 0 months.\nCaseworker: What was your annual income?\nJuliana Hudson: $64,041.00.\nCaseworker: Did you file a claim for Isla?\nJuliana Hudson: no.",
  "question": "Stonevale Delta Child Allowance rules for 2026: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for above 5 months in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Isla lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, is it true that Yasmin Haddad does not get to claim Isla for Stonevale Delta Child Allowance?"
 },
 {
  "qid": "q1259da4ad4",
  "kind": "choice",
  "text": "Facts for Nikolai Ramirez (2025), as JSON:\n{\"time_employed\": \"10 months\", \"hours_worked_in_the_past_year\": \"1311 hours\", \"employees_at_the_worksite\": \"56 employees\", \"gross_annual_pay\": \"83,647.74 USD\", \"take-home_annual_pay\": \"53,852.22 USD\", \"enrolled_in\": \"Vellan Travel Discount\"}\n\n{\"case\": \"HR-52384\", \"caseworker\": \"Riley Watanabe\", \"about\": \"Nikolai Ramirez\"}",
  "question": "Orrendale Printworks Sick Leave Supplement eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has over 56 employees.\n- Gate B: passed when the applicant has been employed for 20 months or more.\n- Gate C: passed when hours worked in the past year are 1310 hours or more.\n- Route: an applicant enrolled in Vellan Travel Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Nikolai Ramirez for Orrendale Printworks Sick Leave Supplement come out?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "qfd54a2d983",
  "kind": "choice",
  "text": "People who asked to claim Milo (2025), as JSON:\n{\"people\": [{\"name\": \"Mirela Sorensen\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"$28,007\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Anjali Robinson\", \"relationship\": \"mother\", \"months_lived_with_child\": \"4 months\", \"annual_income\": \"46,192.81 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Kofi Nilsen\", \"relationship\": \"father\", \"months_lived_with_child\": \"11 months\", \"annual_income\": \"$28,007\", \"filed_a_claim\": \"yes\"}]}\n\n{\"reference\": \"CR-68601\", \"held_by\": \"Teo Quintero\", \"about\": \"Milo\", \"unit\": \"district\"}",
  "question": "Farrowby Moorland Parish Credit rules for 2025: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for greater than 6 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Milo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Milo for Farrowby Moorland Parish Credit?",
  "options": [
   "Mirela Sorensen",
   "Kofi Nilsen",
   "Anjali Robinson"
  ]
 },
 {
  "qid": "qe40dd5645a",
  "kind": "choice",
  "text": "{\"case\": \"CASE-88248\", \"worker\": \"Kazu Yousef\", \"about\": \"Hana Demir\", \"office\": \"town hall\"}\n\nIntake interview with Hana Demir (2026):\nCaseworker: What is your gross monthly income?\nHana Demir: 2,469.77 USD.\nCaseworker: And your net monthly income, after deductions?\nHana Demir: 1,526.11 USD.\nCaseworker: What are your countable assets worth?\nHana Demir: 13,625.77 USD.\nCaseworker: How long have you lived in the service area?\nHana Demir: 18 months.\nCaseworker: How old are you?\nHana Demir: 60 years.\nCaseworker: Which other programme are you enrolled in?\nHana Demir: Yarrowdean Bus Pass.",
  "question": "Fennick School Meal Supplement eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than 59 years.\n- Gate B: passed when net monthly income is strictly beneath $1,820.\n- Gate C: passed when the applicant has lived in the service area for at or beyond 9 months.\n- Gate D: passed when gross monthly income is $2,325 or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hana Demir to Fennick School Meal Supplement get?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Eligible",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate D is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q25a6c5fb66",
  "kind": "choice",
  "text": "Ticket: HR-18932, front counter\nRaised by: Ari Benali\nAbout: Dagny Kelly\n\nFacts for Dagny Kelly (2025):\n| fact | value |\n| --- | --- |\n| time employed | 55 months |\n| hours worked in the past year | 1,001 hours |\n| employees at the worksite | 232 employees |\n| gross annual pay | 103,949.83 USD |\n| take-home annual pay | 67,999.99 USD |\n| enrolled in | Lindcombe Care Leave Fund |",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly above 1,000 hours.\n- Gate B: passed when gross annual pay is strictly under the value of 84,500.00 USD.\n- Gate C: passed when take-home annual pay is 68,000.00 USD at the most.\n- Route: an applicant enrolled in Lindcombe Care Leave Fund skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Dagny Kelly to Morrowdene Hospital Group Return Support get?",
  "options": [
   "Not eligible: Gate A is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "q911559aa5c",
  "kind": "choice",
  "text": "Review desk form\nCase reference: CR-42383\nFor: Ami\nCaseworker: Ezra Rosales\n\nInterview notes for Ami (2027):\nCaseworker: Kenji Hoffman, how are you related to Ami?\nKenji Hoffman: I am Ami's grandfather.\nCaseworker: How long did Ami live with you in 2027?\nKenji Hoffman: 8 months.\nCaseworker: What was your annual income?\nKenji Hoffman: 54,114.00 USD.\nCaseworker: Did you file a claim for Ami?\nKenji Hoffman: yes.\nCaseworker: Farid Ramirez, how are you related to Ami?\nFarid Ramirez: I am Ami's father.\nCaseworker: How long did Ami live with you in 2027?\nFarid Ramirez: 7 months.\nCaseworker: What was your annual income?\nFarid Ramirez: 94,746.78 USD.\nCaseworker: Did you file a claim for Ami?\nFarid Ramirez: yes.\nCaseworker: Mateo Okoro, how are you related to Ami?\nMateo Okoro: I am Ami's grandfather.\nCaseworker: How long did Ami live with you in 2027?\nMateo Okoro: 2 months.\nCaseworker: What was your annual income?\nMateo Okoro: 93,967.00 USD.\nCaseworker: Did you file a claim for Ami?\nMateo Okoro: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for 7 months or greater in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Ami lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, gets to claim Ami for Stonevale Delta Child Allowance under these rules?",
  "options": [
   "Kenji Hoffman",
   "Nobody may claim the child",
   "Farid Ramirez"
  ]
 },
 {
  "qid": "qd8acfebee8",
  "kind": "choice",
  "text": "Facts for Nikolai Abara (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 4,059.99 USD |\n| net monthly income | 3,609.87 USD |\n| countable assets | 857.81 USD |\n| time in the service area | 4 months |\n| age | 81 years |\n| enrolled in | Sallafell Bus Credit |\n\nreference: CASE-39032\nworker: Avery Obradovic\nabout: Nikolai Abara",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under 4,060.00 USD.\n- Gate B: passed when the applicant has lived in the service area for at or over 5 months.\n- Route: an applicant enrolled in Kelder Veterans Pension skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Nikolai Abara to Tollsey Island Ferry Discount receive?",
  "options": [
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qb12da35bfb",
  "kind": "yes/no",
  "text": "Mika Zamora: Lovely to see you, Ami; the staff desk has case CR-42709 in good hands.\n\nPeople who asked to claim Ami (2025):\n- Mirela Dragic: relationship to Ami: aunt; months lived with Ami: 10 months; annual income: $57,021.00; filed a claim: yes\n- Juliana Lehmann: relationship to Ami: mother; months lived with Ami: 12 months; annual income: $63,016.00; filed a claim: no\n- Tomas Dlamini: relationship to Ami: father; months lived with Ami: 10 months; annual income: $35,430.00; filed a claim: yes",
  "question": "Ferrowby Forest Credit rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for in excess of 7 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ami lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Ferrowby Forest Credit, is Tomas Dlamini barred from claiming Ami under the listed rules?"
 },
 {
  "qid": "q4339ff3626",
  "kind": "choice",
  "text": "{\"ref\": \"CR-04208\", \"handled_by\": \"Sami Castro\", \"about\": \"Kai\", \"setting\": \"walk-in\"}\n\nPeople who asked to claim Kai (2026), as JSON:\n{\"people\": [{\"name\": \"Ingrid Delgado\", \"relationship\": \"mother\", \"months_lived_with_child\": \"ten months\", \"annual_income\": \"57,314.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Ilse Jovanovic\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"nine months\", \"annual_income\": \"81,865.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nikolai Mensah\", \"relationship\": \"father\", \"months_lived_with_child\": \"twelve months\", \"annual_income\": \"25,464.00 USD\", \"filed_a_claim\": \"no\"}]}",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for a minimum of seven months in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Kai for Tollmere Lakeside Family Payment?",
  "options": [
   "Ingrid Delgado",
   "Ilse Jovanovic",
   "Nikolai Mensah"
  ]
 },
 {
  "qid": "q9cae8b2d28",
  "kind": "choice",
  "text": "Staff support form\nReference: CR-97409\nName: Amir\nHeld by: Lior Grigoryan\n\nInterview notes for Amir (2026):\nCaseworker: Gustav Lehmann, how are you related to Amir?\nGustav Lehmann: I am Amir's grandfather.\nCaseworker: How long did Amir live with you in 2026?\nGustav Lehmann: 8 months.\nCaseworker: What was your annual income?\nGustav Lehmann: 35,392.00 USD.\nCaseworker: Did you file a claim for Amir?\nGustav Lehmann: yes.\nCaseworker: Mateo Mwangi, how are you related to Amir?\nMateo Mwangi: I am Amir's father.\nCaseworker: How long did Amir live with you in 2026?\nMateo Mwangi: 6 months.\nCaseworker: What was your annual income?\nMateo Mwangi: 91,888.00 USD.\nCaseworker: Did you file a claim for Amir?\nMateo Mwangi: yes.\nCaseworker: Xavier Ortega, how are you related to Amir?\nXavier Ortega: I am Amir's uncle.\nCaseworker: How long did Amir live with you in 2026?\nXavier Ortega: 7 months.\nCaseworker: What was your annual income?\nXavier Ortega: 47,027.00 USD.\nCaseworker: Did you file a claim for Amir?\nXavier Ortega: yes.\nCaseworker: Yara Yamazaki, how are you related to Amir?\nYara Yamazaki: I am Amir's mother.\nCaseworker: How long did Amir live with you in 2026?\nYara Yamazaki: 9 months.\nCaseworker: What was your annual income?\nYara Yamazaki: 48,542.00 USD.\nCaseworker: Did you file a claim for Amir?\nYara Yamazaki: no.",
  "question": "Gristmere Child Credit rules for 2026: who may claim Amir.\n- Only one person may claim Amir. Work through these steps in order.\n- Step one: only people who filed a claim for Amir are considered.\n- Step two: of those, only people with whom Amir lived for greater than 6 months in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Amir lived for more months comes first.\n- If nobody is left after step two, nobody may claim Amir.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is allowed to claim Amir for Gristmere Child Credit?",
  "options": [
   "Nobody may claim the child",
   "Xavier Ortega"
  ]
 },
 {
  "qid": "q3f85f7d936",
  "kind": "choice",
  "text": "[counter_log] file CASE-48321 is with Adi Chandra at the counter\n[about] Lior Nguyen is the subject here\n\nFacts for Lior Nguyen (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,022.44 USD |\n| net monthly income | 1,772.66 USD |\n| countable assets | 9,017.68 USD |\n| time in the service area | six months |\n| age | 50 years |\n| enrolled in | none |",
  "question": "Corvane Transit Fare Discount eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for in excess of five months.\n- Gate B: passed when gross monthly income is at or below the level of $2,455.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Lior Nguyen to Corvane Transit Fare Discount receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "q3f2daa93de",
  "kind": "yes/no",
  "text": "Dear colleague,\nPlease see HR-04711 about Freya Demir on the queue.\nThanks, Sasha Okonkwo\n\nFacts for Freya Demir (2027):\n- time employed: 41 months\n- hours worked in the past year: 2,115 hours\n- employees at the worksite: 178 employees\n- gross annual pay: 61,499.99 USD\n- take-home annual pay: 52,000.00 USD\n- enrolled in: Corrivale Welding Bursary",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than 52,000.00 USD.\n- Gate B: passed when gross annual pay is at or below the level of 61,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is Freya Demir plainly not eligible for Halvorne Shipyard Tuition Assistance?"
 },
 {
  "qid": "q85bf587056",
  "kind": "choice",
  "text": "Adi Chandra: CASE-56712 for Quentin Hamilton is on my list, moving fast.\n\nFacts for Quentin Hamilton (2025):\n- gross monthly income: 4,581.97 USD\n- net monthly income: 3,874.37 USD\n- countable assets: 13,219.44 USD\n- time in the service area: 8 months\n- age: 51 years\n- enrolled in: Stonevale Housing Loan",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for 8 months or above.\n- Gate B: passed when net monthly income is lower than or equal to 3,395.00 USD.\n- Gate C: passed when countable assets are strictly smaller than 8,550.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Quentin Hamilton to Corrivale Valley Childcare Grant receive?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate C is the reason (countable assets)"
  ]
 },
 {
  "qid": "q58d28eaaa3",
  "kind": "choice",
  "text": "Yuki Adeyemi: counter queue has CASE-71597, and it is about Amara Hudson.\n\nFacts for Amara Hudson (2025):\n- gross monthly income: 1,400.74 USD\n- net monthly income: 1,305.32 USD\n- countable assets: 5,419.68 USD\n- time in the service area: 55 months\n- age: 56 years\n- enrolled in: Feldane Childcare Credit",
  "question": "Sennamoor River Rent Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is smaller than 1,465.00 USD.\n- Gate B: passed when gross monthly income is lower than 1,890.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, how is the application of Amara Hudson to Sennamoor River Rent Support resolved?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qa28ebac90e",
  "kind": "choice",
  "text": "[routine_check] case=HR-91728 about=Aiko Delgado by=Morgan Mendoza\n\nIntake interview with Aiko Delgado (2025):\nCaseworker: How long have you been employed here?\nAiko Delgado: nine months.\nCaseworker: How many hours did you work in the past year?\nAiko Delgado: 1575 hours.\nCaseworker: How many employees work at your worksite?\nAiko Delgado: 36 employees.\nCaseworker: What is your gross annual pay?\nAiko Delgado: 77,723.80 USD.\nCaseworker: And your take-home annual pay?\nAiko Delgado: 55,536.81 USD.\nCaseworker: Which other programme are you enrolled in?\nAiko Delgado: Wendle Trade Pilot.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for 9 months at minimum.\n- Gate B: passed when the worksite has at or above 33 employees.\n- Gate C: passed when gross annual pay is strictly below the level of $71,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Aiko Delgado to Brenwold Timber Apprentice Support land?",
  "options": [
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate B is the reason (employees at the worksite)"
  ]
 }
]
