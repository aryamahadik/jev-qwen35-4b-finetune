# G5-H blind read T15-blind_read-251c30af-001 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/pilot/g5h/answers/T15-blind_read-251c30af-001.json

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
  "qid": "q4389c28b93",
  "kind": "choice",
  "text": "Facts for Aiko Tanaka (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,255.69 |\n| net monthly income | $3,226.23 |\n| countable assets | $4,287.35 |\n| time in the service area | zero months |\n| age | 25 years |\n| enrolled in | Ellisford Winter Supplement |\n\n[district_office] record_key=CASE-92241 owner=Remy Tran subject=Aiko Tanaka",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the level of $5,800.00.\n- Gate B: passed when net monthly income is strictly under the value of $3,115.00.\n- Gate C: passed when the applicant has lived in the service area for in excess of three months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Aiko Tanaka to Wyndholm Forest Fuel Support receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (countable assets)"
  ]
 },
 {
  "qid": "q0a2ea72be0",
  "kind": "yes/no",
  "text": "Dear colleague,\nThe record CASE-46244 for Juliana Becker has been sent to the front counter.\nRegards, Casey Kaplan\n\nIntake interview with Juliana Becker (2027):\nCaseworker: What is your gross monthly income?\nJuliana Becker: $2,468.50.\nCaseworker: And your net monthly income, after deductions?\nJuliana Becker: $2,012.58.\nCaseworker: What are your countable assets worth?\nJuliana Becker: $1,366.71.\nCaseworker: How long have you lived in the service area?\nJuliana Becker: 7 months.\nCaseworker: How old are you?\nJuliana Becker: 58 years.\nCaseworker: Which other programme are you enrolled in?\nJuliana Becker: Quarrowdale Food Parcel.",
  "question": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for higher than 6 months.\n- Gate B: passed when the applicant's age is equal to or greater than 58 years.\n- Gate C: passed when countable assets are strictly beneath the level of $2,200.00.\n- Gate D: passed when net monthly income is strictly lower than $2,185.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, does Juliana Becker fail to qualify for Fennick School Meal Supplement?"
 },
 {
  "qid": "qfc3f1c41dc",
  "kind": "yes/no",
  "text": "Yuki Adeyemi: help line has Esra Patterson on CASE-81739.\n\nFacts for Esra Patterson (2027):\n- gross monthly income: 4,930.11 USD\n- net monthly income: 3,111.02 USD\n- countable assets: 11,850.79 USD\n- time in the service area: 40 months\n- age: 55 years\n- enrolled in: Hallowby Utility Discount",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than or equal to 55 years.\n- Gate B: passed when gross monthly income is at or under the amount of 3,430.00 USD.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is Esra Patterson eligible for Tesslow Prairie Water Bill Assistance overall?"
 },
 {
  "qid": "qed1682c946",
  "kind": "yes/no",
  "text": "Routine desk intake record\nCase reference: CR-88093\nHandled by: Tomi Eklund\nAbout: Elif\n\nPeople who asked to claim Elif (2026):\n| person | relationship to Elif | months lived with Elif | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Zofia Medina | mother | two months | $64,844.00 | yes |\n| Yara Watson | aunt | eight months | $33,403.59 | yes |\n| Ubah Gallegos | aunt | three months | $73,659.35 | yes |",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for strictly over seven months in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Elif lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Ubah Gallegos fail to win the right to claim Elif for Tollmere Lakeside Family Payment?"
 },
 {
  "qid": "qd5d47ec963",
  "kind": "yes/no",
  "text": "Facts for Yusuf Anderson (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,011.27 |\n| net monthly income | $1,944.84 |\n| countable assets | $676.19 |\n| time in the service area | 50 months |\n| age | 63 years |\n| enrolled in | Velden Transit Pass |\n\nentry: CASE-81805\nheld_by: Emi Figueroa\nregarding: Yusuf Anderson\ndesk: community help",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or below the level of $3,970.00.\n- Gate B: passed when net monthly income is strictly under the amount of $3,120.00.\n- Route: an applicant enrolled in Ketteridge Veterans Scheme skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is it not the case that Yusuf Anderson is not eligible for Sallowick Ward Home Repair Grant?"
 },
 {
  "qid": "qd4ad2283d9",
  "kind": "yes/no",
  "text": "Facts for Kazu Hudson (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,990 |\n| net monthly income | 2,035.96 USD |\n| countable assets | 6,344.52 USD |\n| time in the service area | 18 months |\n| age | 57 years |\n| enrolled in | Morvane Carers Pension |\n\n[front_counter] case_ref=CASE-38558 staff=Jamie Jorgensen subject=Kazu Hudson",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly under $2,445.\n- Gate B: passed when the applicant's age is larger than 56 years.\n- Gate C: passed when gross monthly income is $2,990 at the most.\n- Gate D: passed when the applicant has lived in the service area for 19 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is it not true that Kazu Hudson is not eligible for Wyndholm Forest Fuel Support?"
 },
 {
  "qid": "q231e1c2ff4",
  "kind": "choice",
  "text": "record: CR-96070\ncaseworker: Jamie Jorgensen\nabout: Eva\ntone: warm\n\nPeople who asked to claim Eva (2025):\n- Jelena Reynolds: relationship to Eva: grandmother; months lived with Eva: nine months; annual income: $47,632.15; filed a claim: yes\n- Juliana Kaur: relationship to Eva: mother; months lived with Eva: twelve months; annual income: $15,815.00; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2025: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for strictly more than five months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Eva for Ostrowan Prairie Grant, who is it?",
  "options": [
   "Juliana Kaur",
   "Jelena Reynolds"
  ]
 },
 {
  "qid": "qed2606865b",
  "kind": "choice",
  "text": "Busy intake desk slip: CASE-17244\nTaken by: Sasha Okonkwo\nFor: Emi Watson\n\nIntake interview with Emi Watson (2026):\nCaseworker: What is your gross monthly income?\nEmi Watson: 2,837.26 USD.\nCaseworker: And your net monthly income, after deductions?\nEmi Watson: 1,990.28 USD.\nCaseworker: What are your countable assets worth?\nEmi Watson: 8,401.10 USD.\nCaseworker: How long have you lived in the service area?\nEmi Watson: 12 months.\nCaseworker: How old are you?\nEmi Watson: 80 years.\nCaseworker: Which other programme are you enrolled in?\nEmi Watson: Quenmoor Emergency Loan.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 8 months.\n- Gate B: passed when gross monthly income is strictly beneath the level of 2,415.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Emi Watson to Ostermere Delta Flood Repair Support receive?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q2e7db81a95",
  "kind": "yes/no",
  "text": "District office intake form\nReference: HR-73721\nCaseworker: Sasha Okonkwo\nAbout: Galina Hoffman\n\nFacts for Galina Hoffman (2025):\n| fact | value |\n| --- | --- |\n| time employed | 23 months |\n| hours worked in the past year | 1,324 hours |\n| employees at the worksite | 65 employees |\n| gross annual pay | 36,166.15 USD |\n| take-home annual pay | 28,057.95 USD |\n| enrolled in | Caddowen Veterans Pathway |",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly beneath the level of 46,000.00 USD.\n- Gate B: passed when hours worked in the past year are strictly above 850 hours.\n- Gate C: passed when the applicant has been employed for higher than 22 months.\n- Gate D: passed when the worksite has above 64 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, does Galina Hoffman qualify for Morrowdene Hospital Group Return Support?"
 },
 {
  "qid": "q086ed22bd5",
  "kind": "choice",
  "text": "[counter_log] file CASE-73422 is with Nika Hernandez at the counter\n[about] Xenia Eriksen is the subject here\n\nFacts for Xenia Eriksen (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,194.84 USD |\n| net monthly income | 2,484.97 USD |\n| countable assets | 7,100.01 USD |\n| time in the service area | eight months |\n| age | 45 years |\n| enrolled in | Corvasy Heating Charter |",
  "question": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for at or over nine months.\n- Gate B: passed when net monthly income is at or under the amount of $2,535.\n- Gate C: passed when countable assets are lower than or equal to $7,100.\n- Route: an applicant enrolled in Tallow Ridge Commuter Pass skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Xenia Eriksen to Sennamoor River Rent Support land?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate C is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q955923d012",
  "kind": "yes/no",
  "text": "Hi team,\nCase CASE-53402 for Emi Tanaka has gone to the desk.\nThanks, Jamie Jorgensen\n\nFacts for Emi Tanaka (2026):\n- gross monthly income: $2,595\n- net monthly income: 2,063.59 USD\n- countable assets: 10,549.99 USD\n- time in the service area: 11 months\n- age: 32 years\n- enrolled in: Stennet Commuter Pass",
  "question": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly smaller than 10,549.99 USD.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 10 months.\n- Gate C: passed when gross monthly income is equal to or below $2,595.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Emi Tanaka eligible for Corvane Transit Fare Discount by passing every gate that applies?"
 },
 {
  "qid": "q016e2e5fc4",
  "kind": "choice",
  "text": "Hi team,\nThanks for waiting, CASE-11244 about Esra Iyer is in good hands.\nWarm wishes, Jamie Jorgensen\n\nFacts for Esra Iyer (2025):\n- gross monthly income: 3,544.99 USD\n- net monthly income: 3,333.43 USD\n- countable assets: 5,659.04 USD\n- time in the service area: 30 months\n- age: 25 years\n- enrolled in: none",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly below $3,545.\n- Gate B: passed when net monthly income is smaller than $2,810.\n- Route: an applicant enrolled in Sorrenby Tenancy Deposit Loan skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Esra Iyer to Tesslow Prairie Water Bill Assistance land?",
  "options": [
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qcaa196241c",
  "kind": "choice",
  "text": "[case_log] staff_support_desk case=CASE-03190 caseworker=Teo Quintero about=Kavita Reynolds\n\nFacts for Kavita Reynolds (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,124.90 |\n| net monthly income | $2,129.99 |\n| countable assets | $5,566.60 |\n| time in the service area | 34 months |\n| age | 83 years |\n| enrolled in | Corrivale Meal Coupon |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below the amount of $10,600.00.\n- Gate B: passed when net monthly income is strictly under the amount of $2,130.00.\n- Gate C: passed when the applicant's age is above 83 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Kavita Reynolds to Tesslow Prairie Water Bill Assistance?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qb076052383",
  "kind": "yes/no",
  "text": "Facts for Olena Thompson (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,091.70 |\n| net monthly income | $2,624.49 |\n| countable assets | $9,799.99 |\n| time in the service area | 7 months |\n| age | 73 years |\n| enrolled in | Sallafell Bus Credit |\n\nFront counter ticket: CASE-48079\nWarm hello from: Blair Xiong\nPerson: Olena Thompson",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly under the value of $9,800.00.\n- Gate B: passed when net monthly income is at or below $2,705.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, does a gate that applies halt the application of Olena Thompson to Tollsey Island Ferry Discount?"
 },
 {
  "qid": "q6e937dded8",
  "kind": "yes/no",
  "text": "[record_entry] case_ref=CASE-66846 worker=Remy Tran\n[desk_queue] about=Farid Nguyen queue=records_office\n\nFacts for Farid Nguyen (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,810 |\n| net monthly income | 2,270.01 USD |\n| countable assets | 17,292.57 USD |\n| time in the service area | 12 months |\n| age | 56 years |\n| enrolled in | Hallowby Utility Supplement |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is $2,810 or under.\n- Gate B: passed when the applicant's age is at or beyond 56 years.\n- Gate C: passed when net monthly income is $2,270.01 or less.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is Farid Nguyen eligible for Tesslow Prairie Water Bill Assistance?"
 },
 {
  "qid": "q24b79ac03c",
  "kind": "choice",
  "text": "[queue_desk] case=CR-23915 staff=Toni Lazar person=Vida\n\nPeople who asked to claim Vida (2025):\n| person | relationship to Vida | months lived with Vida | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Farid Singh | uncle | 0 months | 58,876.00 USD | yes |\n| Sofia Reynolds | grandmother | 10 months | 43,978.00 USD | yes |\n| Waleed Ramirez | grandfather | 5 months | 84,027.00 USD | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for 5 months at minimum in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Vida for Tessenvale Valley Child Credit?",
  "options": [
   "Waleed Ramirez",
   "Farid Singh"
  ]
 },
 {
  "qid": "qf08d4e506d",
  "kind": "choice",
  "text": "[case_record] ref=CR-81946 worker=Kiran Morales about=Ezra\n\nPeople who asked to claim Ezra (2025):\n| person | relationship to Ezra | months lived with Ezra | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Nikolai Murphy | uncle | 3 months | $60,246 | yes |\n| Priya Gallegos | aunt | 6 months | $45,105 | yes |\n| Sergio Bergstrom | father | 8 months | $89,515 | yes |\n| Mirela Vasquez | aunt | 9 months | $83,734 | yes |",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for in excess of 5 months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ezra lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole person entitled to claim Ezra for Corrowby Family Supplement?",
  "options": [
   "Sergio Bergstrom",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qa4c0e0c810",
  "kind": "yes/no",
  "text": "Hello there,\nA short update on file HR-00798 for Kofi Abara follows below.\nBest, Avery Obradovic\n\nFacts for Kofi Abara (2026):\n- time employed: 12 months\n- hours worked in the past year: 1,504 hours\n- employees at the worksite: 67 employees\n- gross annual pay: 36,898.02 USD\n- take-home annual pay: 31,677.93 USD\n- enrolled in: Corrivale Welding Bursary",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has a minimum of 47 employees.\n- Gate B: passed when the applicant has been employed for above 11 months.\n- Gate C: passed when take-home annual pay is strictly under the amount of 54,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is Kofi Abara not eligible for Halvorne Shipyard Tuition Assistance?"
 },
 {
  "qid": "q648d90d520",
  "kind": "yes/no",
  "text": "Case note: Ren Dvorak is handling Milo on case CR-63984. Thanks for the help.\n\nInterview notes for Milo (2026):\nCaseworker: Quentin Yilmaz, how are you related to Milo?\nQuentin Yilmaz: I am Milo's father.\nCaseworker: How long did Milo live with you in 2026?\nQuentin Yilmaz: 9 months.\nCaseworker: What was your annual income?\nQuentin Yilmaz: 60,481.00 USD.\nCaseworker: Did you file a claim for Milo?\nQuentin Yilmaz: yes.\nCaseworker: Olena Ruiz, how are you related to Milo?\nOlena Ruiz: I am Milo's grandmother.\nCaseworker: How long did Milo live with you in 2026?\nOlena Ruiz: 2 months.\nCaseworker: What was your annual income?\nOlena Ruiz: 36,329.00 USD.\nCaseworker: Did you file a claim for Milo?\nOlena Ruiz: no.\nCaseworker: Anjali Halvorsen, how are you related to Milo?\nAnjali Halvorsen: I am Milo's mother.\nCaseworker: How long did Milo live with you in 2026?\nAnjali Halvorsen: 5 months.\nCaseworker: What was your annual income?\nAnjali Halvorsen: 93,202.00 USD.\nCaseworker: Did you file a claim for Milo?\nAnjali Halvorsen: no.\nCaseworker: Zofia Ramirez, how are you related to Milo?\nZofia Ramirez: I am Milo's aunt.\nCaseworker: How long did Milo live with you in 2026?\nZofia Ramirez: 10 months.\nCaseworker: What was your annual income?\nZofia Ramirez: 81,548.00 USD.\nCaseworker: Did you file a claim for Milo?\nZofia Ramirez: no.",
  "question": "Kelmstone Mountain Family Grant rules for 2026: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for at or above 7 months in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Milo lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is it true that Quentin Yilmaz may not claim Milo for Kelmstone Mountain Family Grant?"
 },
 {
  "qid": "q21f8b3d81b",
  "kind": "choice",
  "text": "Brisk help line note: Blair Xiong is running through CR-36743, which concerns Liam.\n\nInterview notes for Liam (2025):\nCaseworker: Nikolai Esposito, how are you related to Liam?\nNikolai Esposito: I am Liam's grandfather.\nCaseworker: How long did Liam live with you in 2025?\nNikolai Esposito: five months.\nCaseworker: What was your annual income?\nNikolai Esposito: $33,328.64.\nCaseworker: Did you file a claim for Liam?\nNikolai Esposito: yes.\nCaseworker: Leila Okoro, how are you related to Liam?\nLeila Okoro: I am Liam's mother.\nCaseworker: How long did Liam live with you in 2025?\nLeila Okoro: twelve months.\nCaseworker: What was your annual income?\nLeila Okoro: $40,299.00.\nCaseworker: Did you file a claim for Liam?\nLeila Okoro: no.\nCaseworker: Yusuf Esposito, how are you related to Liam?\nYusuf Esposito: I am Liam's uncle.\nCaseworker: How long did Liam live with you in 2025?\nYusuf Esposito: eight months.\nCaseworker: What was your annual income?\nYusuf Esposito: $29,553.00.\nCaseworker: Did you file a claim for Liam?\nYusuf Esposito: yes.",
  "question": "Stonevale Delta Child Allowance rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for a minimum of six months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Liam lived for more months comes first.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, holds the right to claim Liam for Stonevale Delta Child Allowance?",
  "options": [
   "Yusuf Esposito",
   "Nikolai Esposito"
  ]
 },
 {
  "qid": "q3833b54940",
  "kind": "choice",
  "text": "Outreach form\nCase: HR-88176\nCaseworker: Kendall Umarov\nAbout: Luka Russell\n\nFacts for Luka Russell (2026):\n| fact | value |\n| --- | --- |\n| time employed | fourteen months |\n| hours worked in the past year | 1,260 hours |\n| employees at the worksite | 154 employees |\n| gross annual pay | $82,395.50 |\n| take-home annual pay | $23,252.94 |\n| enrolled in | none |",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly under the value of $45,500.00.\n- Gate B: passed when the applicant has been employed for equal to or above fourteen months.\n- Gate C: passed when hours worked in the past year are greater than 1,260 hours.\n- Gate D: passed when gross annual pay is strictly under the amount of $59,000.00.\n- Route: an applicant enrolled in Sarrowby Mentor Stipend skips Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Luka Russell to Hallowdene Logistics Study Grant receive?",
  "options": [
   "Not eligible: Gate D is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (time employed)",
   "Eligible",
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate C is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q1a53b5ecf0",
  "kind": "yes/no",
  "text": "Facts for Kazu Singh (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,858.29 |\n| net monthly income | $2,277.65 |\n| countable assets | $12,521.47 |\n| time in the service area | 12 months |\n| age | 89 years |\n| enrolled in | Ketteridge Veterans Charter |\n\n[branch_queue] case=CASE-91383 by=Jamie Jorgensen about=Kazu Singh",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 55 years.\n- Gate B: passed when the applicant has lived in the service area for 12 months or more.\n- Gate C: passed when gross monthly income is strictly smaller than $2,395.00.\n- Route: an applicant enrolled in Ketteridge Veterans Scheme skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Kazu Singh not eligible for Sallowick Ward Home Repair Grant under these rules?"
 },
 {
  "qid": "q508f8dcf65",
  "kind": "choice",
  "text": "Front counter intake form\nReference: CASE-00935\nCaseworker: Adi Chandra\nPerson: Jamie Ortega\n\nFacts for Jamie Ortega (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,781.85 USD |\n| net monthly income | 2,385.01 USD |\n| countable assets | 4,700.99 USD |\n| time in the service area | 37 months |\n| age | nineteen years |\n| enrolled in | Stonevale Housing Loan |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are smaller than 9,250.00 USD.\n- Gate B: passed when net monthly income is strictly smaller than 2,385.02 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Jamie Ortega to Corrivale Valley Childcare Grant get?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qc909c97e18",
  "kind": "yes/no",
  "text": "Internal note: Ezra Rosales looks after case CR-92191 in the regional service team, about Ami.\n\nPeople who asked to claim Ami (2027):\n- Amara Kovacs: relationship to Ami: grandmother; months lived with Ami: 6 months; annual income: 56,572.37 USD; filed a claim: yes\n- Matias Hoffman: relationship to Ami: father; months lived with Ami: 0 months; annual income: 32,063.00 USD; filed a claim: no\n- Ailsa Begum: relationship to Ami: mother; months lived with Ami: 3 months; annual income: 79,442.00 USD; filed a claim: yes",
  "question": "Dunmarrow Hill Allowance rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for greater than or equal to 7 months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Dunmarrow Hill Allowance, is it not the case that Ailsa Begum may not claim Ami?"
 },
 {
  "qid": "q96c77fa784",
  "kind": "yes/no",
  "text": "Records desk note. Nika Hernandez keeps HR-91668, which concerns Yasmin Johnson.\n\nFacts for Yasmin Johnson (2026):\n- time employed: 80 months\n- hours worked in the past year: 1,533 hours\n- employees at the worksite: 130 employees\n- gross annual pay: 47,610.95 USD\n- take-home annual pay: 33,500.01 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are over 1,290 hours.\n- Gate B: passed when take-home annual pay is at or below $33,500.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Morrowdene Hospital Group Return Support, does Yasmin Johnson fail to qualify under these rules?"
 },
 {
  "qid": "q2bf49e2c8a",
  "kind": "yes/no",
  "text": "Case file intake form\nCase reference: CASE-61329\nCaseworker: Toni Lazar\nAbout: Jiro Delgado\n\nIntake interview with Jiro Delgado (2027):\nCaseworker: What is your gross monthly income?\nJiro Delgado: $5,333.\nCaseworker: And your net monthly income, after deductions?\nJiro Delgado: $4,049.81.\nCaseworker: What are your countable assets worth?\nJiro Delgado: $1,017.86.\nCaseworker: How long have you lived in the service area?\nJiro Delgado: 15 months.\nCaseworker: How old are you?\nJiro Delgado: 26 years.\nCaseworker: Which other programme are you enrolled in?\nJiro Delgado: Quenmoor Emergency Loan.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than 11 months.\n- Gate B: passed when net monthly income is $3,185 or lower.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes Jiro Delgado fail to qualify for Ostermere Delta Flood Repair Support under these rules?"
 },
 {
  "qid": "q765c47331e",
  "kind": "yes/no",
  "text": "Facts for Kazu Singh (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,858.29 |\n| net monthly income | $2,277.65 |\n| countable assets | $12,521.47 |\n| time in the service area | 12 months |\n| age | 89 years |\n| enrolled in | Ketteridge Veterans Charter |\n\n[branch_queue] case=CASE-91383 by=Jamie Jorgensen about=Kazu Singh",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 55 years.\n- Gate B: passed when the applicant has lived in the service area for 12 months or more.\n- Gate C: passed when gross monthly income is strictly smaller than $2,395.00.\n- Route: an applicant enrolled in Ketteridge Veterans Scheme skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, is it not true that Kazu Singh is not eligible for Sallowick Ward Home Repair Grant?"
 },
 {
  "qid": "q57885533b1",
  "kind": "yes/no",
  "text": "Hi team,\nCase CASE-53402 for Emi Tanaka has gone to the desk.\nThanks, Jamie Jorgensen\n\nFacts for Emi Tanaka (2026):\n- gross monthly income: $2,595\n- net monthly income: 2,063.59 USD\n- countable assets: 10,549.99 USD\n- time in the service area: 11 months\n- age: 32 years\n- enrolled in: Stennet Commuter Pass",
  "question": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly smaller than $10,550.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 10 months.\n- Gate C: passed when gross monthly income is equal to or below $2,595.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Emi Tanaka eligible for Corvane Transit Fare Discount by passing every gate that applies?"
 },
 {
  "qid": "q0ac0c7a29a",
  "kind": "choice",
  "text": "record: CR-19448\ncaseworker: Dani Ishikawa\nabout: Vida\ntone: warm\n\nPeople who asked to claim Vida (2027):\n- Olena Nilsen: relationship to Vida: mother; months lived with Vida: 12 months; annual income: $44,458.00; filed a claim: no\n- Viktor Gashi: relationship to Vida: uncle; months lived with Vida: 8 months; annual income: $56,563.00; filed a claim: no\n- Zaid Schultz: relationship to Vida: father; months lived with Vida: 10 months; annual income: $27,154.36; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for 6 months or more in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Vida for Ostrowan Prairie Grant?",
  "options": [
   "Zaid Schultz",
   "Viktor Gashi"
  ]
 },
 {
  "qid": "qf13e0096cb",
  "kind": "choice",
  "text": "[routine_check] case=HR-76596 about=Wanjiru Demir by=Emi Figueroa\n\nFacts for Wanjiru Demir (2027):\n| fact | value |\n| --- | --- |\n| time employed | 49 months |\n| hours worked in the past year | 1548 hours |\n| employees at the worksite | 77 employees |\n| gross annual pay | 31,687.32 USD |\n| take-home annual pay | $31,000 |\n| enrolled in | Fallowden Retraining Bounty |",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is $38,000 or under.\n- Gate B: passed when hours worked in the past year are at or greater than 1370 hours.\n- Gate C: passed when take-home annual pay is strictly under the value of $31,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what result does the application of Wanjiru Demir to Tovardine Seed Caregiver Leave produce?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qc2448e2f28",
  "kind": "choice",
  "text": "Town hall desk form\nCase reference: CR-23595\nHandled by: Blair Xiong\nFor: Tove\n\nPeople who asked to claim Tove (2025):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ugo Reynolds | father | one month | $70,951.39 | yes |\n| Fatima Russell | mother | four months | $47,572.81 | yes |\n| Dmitri Singh | grandfather | three months | $35,298 | no |\n| Dagny Ferreira | grandmother | six months | $65,596 | yes |",
  "question": "Corrowby Family Supplement rules for 2025: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for strictly more than five months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Tove lived for more months comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, may claim Tove for Corrowby Family Supplement?",
  "options": [
   "Dagny Ferreira",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q39c1595b8b",
  "kind": "yes/no",
  "text": "[casework_team] ref=HR-06778 caseworker=Avery Obradovic about=Kiara Becker\n\nFacts for Kiara Becker (2025):\n| fact | value |\n| --- | --- |\n| time employed | 104 months |\n| hours worked in the past year | 1159 hours |\n| employees at the worksite | 34 employees |\n| gross annual pay | $58,438.40 |\n| take-home annual pay | $47,229.33 |\n| enrolled in | Rickmere Night Course Fund |",
  "question": "Hallowdene Logistics Study Grant eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has over 34 employees.\n- Gate B: passed when take-home annual pay is strictly smaller than $60,000.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, does Kiara Becker meet the rules for Hallowdene Logistics Study Grant across every applicable gate?"
 },
 {
  "qid": "q9cdb15bfaa",
  "kind": "choice",
  "text": "Welcome to the community help desk\nCase reference: CASE-12797\nCaseworker: Lior Grigoryan\nPerson: Dario Mensah\n\nFacts for Dario Mensah (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,502.73 USD |\n| net monthly income | 2,624.99 USD |\n| countable assets | 5,374.07 USD |\n| time in the service area | 7 months |\n| age | 36 years |\n| enrolled in | Velgate Pantry Voucher |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly beneath the level of 2,625.00 USD.\n- Gate B: passed when the applicant has lived in the service area for greater than 7 months.\n- Gate C: passed when the applicant's age is at or beyond 57 years.\n- Gate D: passed when gross monthly income is at or less than 3,255.00 USD.\n- Route: an applicant enrolled in Velgate Pantry Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does Dario Mensah get on the application to Corrivale Valley Childcare Grant under these rules?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (net monthly income)",
   "Not eligible: Gate D is the reason (gross monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "q2966cdfcdf",
  "kind": "choice",
  "text": "Staff support desk ticket: CASE-63390\nLogged by: Ezra Rosales\nRegarding: Dagny Ortega\n\nFacts for Dagny Ortega (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,016.51 USD |\n| net monthly income | 2,673.28 USD |\n| countable assets | $5,350 |\n| time in the service area | 1 month |\n| age | 36 years |\n| enrolled in | Corrivale Meal Voucher |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for at or beyond 3 months.\n- Gate B: passed when countable assets are strictly lower than $5,350.\n- Gate C: passed when gross monthly income is at or less than $3,470.\n- Route: an applicant enrolled in Corrivale Meal Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tesslow Prairie Water Bill Assistance, which outcome does the application of Dagny Ortega get?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (gross monthly income)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qf9499447e5",
  "kind": "choice",
  "text": "Case note from the support hub: Ren Dvorak is handling case HR-62276 for Emeka Kelly.\n\nIntake interview with Emeka Kelly (2027):\nCaseworker: How long have you been employed here?\nEmeka Kelly: seventeen months.\nCaseworker: How many hours did you work in the past year?\nEmeka Kelly: 1379 hours.\nCaseworker: How many employees work at your worksite?\nEmeka Kelly: 141 employees.\nCaseworker: What is your gross annual pay?\nEmeka Kelly: 75,901.35 USD.\nCaseworker: And your take-home annual pay?\nEmeka Kelly: 57,500.00 USD.\nCaseworker: Which other programme are you enrolled in?\nEmeka Kelly: none.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or less than 76,500.00 USD.\n- Gate B: passed when the applicant has been employed for strictly over sixteen months.\n- Gate C: passed when hours worked in the past year are at or beyond 1380 hours.\n- Gate D: passed when take-home annual pay is lower than or equal to 57,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Emeka Kelly to Brenwold Timber Apprentice Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate D is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (time employed)",
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate C is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "q520817fe66",
  "kind": "choice",
  "text": "Review desk form\nCase reference: CR-79394\nFor: Rafi\nCaseworker: Remy Tran\n\nInterview notes for Rafi (2027):\nCaseworker: Hiro Ferreira, how are you related to Rafi?\nHiro Ferreira: I am Rafi's father.\nCaseworker: How long did Rafi live with you in 2027?\nHiro Ferreira: 8 months.\nCaseworker: What was your annual income?\nHiro Ferreira: $68,495.35.\nCaseworker: Did you file a claim for Rafi?\nHiro Ferreira: yes.\nCaseworker: Esra Lehmann, how are you related to Rafi?\nEsra Lehmann: I am Rafi's mother.\nCaseworker: How long did Rafi live with you in 2027?\nEsra Lehmann: 11 months.\nCaseworker: What was your annual income?\nEsra Lehmann: $68,495.35.\nCaseworker: Did you file a claim for Rafi?\nEsra Lehmann: yes.",
  "question": "Gristmere Child Credit rules for 2027: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for above 7 months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with whom Rafi lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Rafi for Gristmere Child Credit under these rules?",
  "options": [
   "Nobody may claim the child",
   "Esra Lehmann"
  ]
 },
 {
  "qid": "qe534787805",
  "kind": "yes/no",
  "text": "Hello there,\nThis note is about Ailsa Gallegos, under case reference CASE-86917.\nWarm regards, Toni Lazar\n\nFacts for Ailsa Gallegos (2026):\n- gross monthly income: 3,855.01 USD\n- net monthly income: 1,831.13 USD\n- countable assets: 17,952.27 USD\n- time in the service area: 50 months\n- age: 77 years\n- enrolled in: none",
  "question": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is higher than 62 years.\n- Gate B: passed when net monthly income is 3,115.00 USD at the most.\n- Gate C: passed when gross monthly income is at or under 3,855.00 USD.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, does Ailsa Gallegos fail to qualify for Corvane Transit Fare Discount?"
 },
 {
  "qid": "q415163a602",
  "kind": "yes/no",
  "text": "[welcome_file] thanks to Kendall Umarov for case CR-37473\n[about_person] Sora is the warm focus here.\n\nPeople who asked to claim Sora (2027):\n| person | relationship to Sora | months lived with Sora | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Mirela Tanaka | grandmother | six months | 75,262.00 USD | yes |\n| Cyril Moreau | father | five months | 79,069.00 USD | yes |\n| Felix Gallegos | uncle | ten months | 51,199.70 USD | yes |",
  "question": "Tollmere Lakeside Family Payment rules for 2027: who may claim Sora.\n- Only one person may claim Sora. Work through these steps in order.\n- Step one: only people who filed a claim for Sora are considered.\n- Step two: of those, only people with whom Sora lived for strictly higher than five months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Sora lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Sora.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, is Mirela Tanaka the person who ends up with the right to claim Sora for Tollmere Lakeside Family Payment?"
 },
 {
  "qid": "q0ff133cca9",
  "kind": "yes/no",
  "text": "People who asked to claim Nia (2027):\n| person | relationship to Nia | months lived with Nia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Imani Mitchell | aunt | seven months | $78,603.00 | no |\n| Ivo Halvorsen | grandfather | eight months | $42,530.00 | yes |\n\nref: CR-56360\noffice: branch\nlead: Riley Watanabe\nperson: Nia",
  "question": "Farrowby Moorland Parish Credit rules for 2027: who may claim Nia.\n- Only one person may claim Nia. Work through these steps in order.\n- Step one: only people who filed a claim for Nia are considered.\n- Step two: of those, only people with whom Nia lived for at or greater than seven months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Nia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Nia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, is it true that Ivo Halvorsen does not get to claim Nia for Farrowby Moorland Parish Credit?"
 },
 {
  "qid": "q2cd5a528e9",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-56894\", \"caseworker\": \"Remy Tran\", \"about\": \"Idris Medina\", \"desk\": \"services counter\"}\n\nIntake interview with Idris Medina (2025):\nCaseworker: What is your gross monthly income?\nIdris Medina: 3,087.84 USD.\nCaseworker: And your net monthly income, after deductions?\nIdris Medina: 2,599.99 USD.\nCaseworker: What are your countable assets worth?\nIdris Medina: 5,685.95 USD.\nCaseworker: How long have you lived in the service area?\nIdris Medina: 12 months.\nCaseworker: How old are you?\nIdris Medina: 18 years.\nCaseworker: Which other programme are you enrolled in?\nIdris Medina: Kelmstone Drainage Subsidy.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly below the level of $3,575.\n- Gate B: passed when net monthly income is strictly lower than $2,600.\n- Gate C: passed when the applicant's age is higher than 61 years.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nDoes a gate that applies halt the application of Idris Medina to Ostermere Delta Flood Repair Support?"
 },
 {
  "qid": "q7b41e3d0f9",
  "kind": "choice",
  "text": "Tomi Eklund: Warm thanks to Ali for case CR-48369, handled with care.\n\nPeople who asked to claim Ali (2026):\n- Juliana Ivanova: relationship to Ali: aunt; months lived with Ali: 1 month; annual income: 68,013.00 USD; filed a claim: yes\n- Idris Ilunga: relationship to Ali: uncle; months lived with Ali: 12 months; annual income: 55,444.00 USD; filed a claim: no\n- Sofia Lindqvist: relationship to Ali: mother; months lived with Ali: 2 months; annual income: 90,604.55 USD; filed a claim: no\n- Fatima Hudson: relationship to Ali: grandmother; months lived with Ali: 2 months; annual income: 61,100.43 USD; filed a claim: yes",
  "question": "Corrowby Family Supplement rules for 2026: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for 5 months or above in 2026 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ali lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if anyone, is entitled to claim Ali for Corrowby Family Supplement?",
  "options": [
   "Sofia Lindqvist",
   "Juliana Ivanova",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q71e27d1592",
  "kind": "choice",
  "text": "People who asked to claim Remi (2027):\n| person | relationship to Remi | months lived with Remi | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dagny Yilmaz | mother | 6 months | 45,429.31 USD | yes |\n| Hiroko Bergstrom | grandmother | 10 months | $58,934 | no |\n\ncase: CR-94161\ncaseworker: Alex Lindgren\nabout: Remi\nkind: file",
  "question": "Mollenby Canal Child Supplement rules for 2027: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for at or above 7 months in 2027 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Remi lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Remi for Mollenby Canal Child Supplement under these rules?",
  "options": [
   "Dagny Yilmaz",
   "Nobody may claim the child",
   "Hiroko Bergstrom"
  ]
 },
 {
  "qid": "q4c26722ae7",
  "kind": "yes/no",
  "text": "Records office ticket: CASE-52910\nRaised by: Dani Ishikawa\nAbout: Yuki Delgado\n\nFacts for Yuki Delgado (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,410.00 USD |\n| net monthly income | 3,211.27 USD |\n| countable assets | 9,894.70 USD |\n| time in the service area | 7 months |\n| age | 57 years |\n| enrolled in | Corrivale Meal Coupon |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for at or beyond 7 months.\n- Gate B: passed when the applicant's age is at or over 57 years.\n- Gate C: passed when gross monthly income is strictly under 3,410.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs it not true that Yuki Delgado is not eligible for Tesslow Prairie Water Bill Assistance?"
 },
 {
  "qid": "q06890d80dc",
  "kind": "choice",
  "text": "Internal case note for HR-57887.\nSet down by Yuki Adeyemi at the town hall office, for Aiko Gallegos.\n\nIntake interview with Aiko Gallegos (2026):\nCaseworker: How long have you been employed here?\nAiko Gallegos: 18 months.\nCaseworker: How many hours did you work in the past year?\nAiko Gallegos: 2,161 hours.\nCaseworker: How many employees work at your worksite?\nAiko Gallegos: 44 employees.\nCaseworker: What is your gross annual pay?\nAiko Gallegos: 79,553.19 USD.\nCaseworker: And your take-home annual pay?\nAiko Gallegos: 55,374.19 USD.\nCaseworker: Which other programme are you enrolled in?\nAiko Gallegos: Quelmere Lunch Card.",
  "question": "Sorrelby Child Care Support eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than $55,374.20.\n- Gate B: passed when the applicant has been employed for 22 months or greater.\n- Route: an applicant enrolled in Quelmere Lunch Card skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Aiko Gallegos to Sorrelby Child Care Support land?",
  "options": [
   "Eligible",
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "q542794a67c",
  "kind": "yes/no",
  "text": "Facts for Dario Dlamini (2025), as JSON:\n{\"time_employed\": \"93 months\", \"hours_worked_in_the_past_year\": \"1,900 hours\", \"employees_at_the_worksite\": \"330 employees\", \"gross_annual_pay\": \"40,890.92 USD\", \"take-home_annual_pay\": \"27,418.98 USD\", \"enrolled_in\": \"none\"}\n\n{\"record\": \"case\", \"reference\": \"HR-55039\", \"caseworker\": \"Alex Lindgren\", \"about\": \"Dario Dlamini\"}",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is 65,500.00 USD or lower.\n- Gate B: passed when take-home annual pay is strictly under 55,000.00 USD.\n- Gate C: passed when hours worked in the past year are a minimum of 1,110 hours.\n- Route: an applicant enrolled in Hathermoor Relief Leave skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, does a gate that applies end the application of Dario Dlamini to Pelmoor Ceramics Carer Support?"
 },
 {
  "qid": "q90b85079e9",
  "kind": "yes/no",
  "text": "Community help desk intake form\nCase reference: HR-37063\nCaseworker: Lior Grigoryan\nAbout: Casey Medina\n\nFacts for Casey Medina (2027):\n| fact | value |\n| --- | --- |\n| time employed | 110 months |\n| hours worked in the past year | 156 hours |\n| employees at the worksite | 249 employees |\n| gross annual pay | $61,375.59 |\n| take-home annual pay | $53,288.96 |\n| enrolled in | Drummock Nurse Stipend |",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly below $59,500.00.\n- Gate B: passed when gross annual pay is strictly under $73,500.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nIs Casey Medina not eligible for Morrowdene Hospital Group Return Support under these rules?"
 },
 {
  "qid": "q54f7fcd54f",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Priya Dlamini; the reference is HR-03377.\nKind regards, Casey Kaplan\n\nFacts for Priya Dlamini (2027):\n- time employed: 31 months\n- hours worked in the past year: 1,241 hours\n- employees at the worksite: 28 employees\n- gross annual pay: 63,499.99 USD\n- take-home annual pay: 61,502.74 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,240 hours.\n- Gate B: passed when take-home annual pay is at or less than $45,000.\n- Gate C: passed when gross annual pay is strictly under the amount of $63,500.\n- Gate D: passed when the worksite has equal to or greater than 63 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, does Priya Dlamini fail to qualify for Morrowdene Hospital Group Return Support?"
 },
 {
  "qid": "q8a87d7ce97",
  "kind": "yes/no",
  "text": "Support hub form\nCase reference: CR-54672\nCaseworker: Jamie Jorgensen\nSubject: Pia\n\nInterview notes for Pia (2025):\nCaseworker: Sofia Dlamini, how are you related to Pia?\nSofia Dlamini: I am Pia's mother.\nCaseworker: How long did Pia live with you in 2025?\nSofia Dlamini: twelve months.\nCaseworker: What was your annual income?\nSofia Dlamini: 45,456.56 USD.\nCaseworker: Did you file a claim for Pia?\nSofia Dlamini: yes.\nCaseworker: Matias Fujimoto, how are you related to Pia?\nMatias Fujimoto: I am Pia's grandfather.\nCaseworker: How long did Pia live with you in 2025?\nMatias Fujimoto: seven months.\nCaseworker: What was your annual income?\nMatias Fujimoto: 49,185.00 USD.\nCaseworker: Did you file a claim for Pia?\nMatias Fujimoto: yes.\nCaseworker: Oskar Russell, how are you related to Pia?\nOskar Russell: I am Pia's father.\nCaseworker: How long did Pia live with you in 2025?\nOskar Russell: ten months.\nCaseworker: What was your annual income?\nOskar Russell: 52,276.00 USD.\nCaseworker: Did you file a claim for Pia?\nOskar Russell: yes.",
  "question": "Gristmere Child Credit rules for 2025: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for strictly above seven months in 2025 stay in the running.\n- Step three: if more than one person is still in the running, apply the tie-breakers below in the order listed. Each tie-breaker keeps only those still in the running who come out best on it, and the tie-breakers stop as soon as one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Pia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, is it true that Oskar Russell may not claim Pia for Gristmere Child Credit?"
 },
 {
  "qid": "qb0bf64a396",
  "kind": "choice",
  "text": "Facts for Anjali Gordon (2025), as JSON:\n{\"time_employed\": \"44 months\", \"hours_worked_in_the_past_year\": \"1059 hours\", \"employees_at_the_worksite\": \"101 employees\", \"gross_annual_pay\": \"$60,955.96\", \"take-home_annual_pay\": \"$42,493.01\", \"enrolled_in\": \"Tesslow Engineering Traineeship\"}\n\n{\"caseworker\": \"Quinn Pavlenko\", \"about\": \"Anjali Gordon\", \"case\": \"HR-83772\", \"office\": \"branch\"}",
  "question": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly smaller than $71,000.\n- Gate B: passed when the worksite has 56 employees or above.\n- Route: an applicant enrolled in Tesslow Engineering Traineeship skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Drummock Robotics Workshop Training Fund, which outcome does the application of Anjali Gordon get?",
  "options": [
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate A is the reason (gross annual pay)"
  ]
 },
 {
  "qid": "qcc6866e989",
  "kind": "choice",
  "text": "Ticket: branch office, case CASE-11301\nRaised by: Riley Watanabe\nAbout: Nikolai Ueda\n\nFacts for Nikolai Ueda (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,054.04 USD |\n| net monthly income | 2,579.41 USD |\n| countable assets | 3,895.16 USD |\n| time in the service area | 13 months |\n| age | 34 years |\n| enrolled in | Kelmstone Parent Learning Grant |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed. An applicant must pass every gate that applies; testing stops at the first gate that fails, and that gate is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for above 13 months.\n- Gate B: passed when the applicant's age is at or greater than 57 years.\n- Gate C: passed when countable assets are 2,900.00 USD or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Nikolai Ueda to Corrivale Valley Childcare Grant receive?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (age)",
   "Eligible",
   "Not eligible: Gate C is the reason (countable assets)"
  ]
 }
]
