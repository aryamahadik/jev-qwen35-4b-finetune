# G5-H blind read T15-blind_read-d59b2266-001 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/pilot_i2/g5h/answers/T15-blind_read-d59b2266-001.json

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
  "qid": "q7bd5868d1b",
  "kind": "choice",
  "text": "Records desk note. Ezra Rosales keeps CR-85975, which concerns Vida.\n\nInterview notes for Vida (2026):\nCaseworker: Kavita Kimura, your relation to Vida?\nKavita Kimura: I am Vida's grandmother.\nCaseworker: Months Vida lived with you?\nKavita Kimura: 9 months.\nCaseworker: Annual income?\nKavita Kimura: $24,722.00.\nCaseworker: Filed a claim for Vida?\nKavita Kimura: yes.\nCaseworker: Elias Ruiz, your relation to Vida?\nElias Ruiz: I am Vida's father.\nCaseworker: Months Vida lived with you?\nElias Ruiz: 1 month.\nCaseworker: Annual income?\nElias Ruiz: $24,722.00.\nCaseworker: Filed a claim for Vida?\nElias Ruiz: yes.\nCaseworker: Zofia Kaur, your relation to Vida?\nZofia Kaur: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nZofia Kaur: 7 months.\nCaseworker: Annual income?\nZofia Kaur: $90,761.27.\nCaseworker: Filed a claim for Vida?\nZofia Kaur: no.",
  "question": "Kelmstone Mountain Family Grant rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Vida for Kelmstone Mountain Family Grant?",
  "options": [
   "Zofia Kaur",
   "Kavita Kimura"
  ]
 },
 {
  "qid": "q9c47017eb7",
  "kind": "choice",
  "text": "Front counter intake form\nReference: CASE-00935\nCaseworker: Adi Chandra\nPerson: Jamie Ortega\n\nFacts for Jamie Ortega (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,838.97 USD |\n| net monthly income | 2,385.01 USD |\n| countable assets | 9,250.01 USD |\n| time in the service area | zero months |\n| age | 78 years |\n| enrolled in | Stonevale Housing Loan |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly smaller than 9,250.00 USD.\n- Gate B: passed when net monthly income is strictly smaller than 2,385.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which outcome does the application of Jamie Ortega to Corrivale Valley Childcare Grant get?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "q0d61736012",
  "kind": "yes/no",
  "text": "Facts for Jamie Kelly (2025):\n| fact | value |\n| --- | --- |\n| time employed | 42 months |\n| hours worked in the past year | 1140 hours |\n| employees at the worksite | 385 employees |\n| gross annual pay | $119,853.62 |\n| take-home annual pay | $75,864.82 |\n| enrolled in | Pellbrook Staff Tool Allowance |\n\nTicket: district office desk review, case HR-88837\nRaised by: Jules Shrestha\nAbout: Jamie Kelly",
  "question": "Going by the listed rules, is Jamie Kelly not eligible for Drummock Robotics Workshop Training Fund?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is $78,500.00 or lower.\n- Gate B: passed when hours worked in the past year are greater than 1140 hours.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q705e46054a",
  "kind": "yes/no",
  "text": "People who asked to claim Eva (2027):\n| person | relationship to Eva | months lived with Eva | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Lucia Abara | grandmother | 1 month | $74,507.40 | no |\n| Dmitri Mensah | father | 12 months | $63,869.00 | yes |\n\n[routine_check] case=CR-40285 about=Eva by=Jules Shrestha",
  "question": "Going by the listed rules, is Dmitri Mensah shut out from claiming Eva for Farrowby Moorland Parish Credit?",
  "definitions": "Farrowby Moorland Parish Credit rules for 2027: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for strictly above 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Eva lived for more months comes first.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q31d6f1ca1e",
  "kind": "yes/no",
  "text": "Welcome to your case file\nCase reference: CASE-39136\nCaseworker: Kiran Morales\nAbout: Anton Yamazaki\n\nFacts for Anton Yamazaki (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $992.90 |\n| net monthly income | $891.01 |\n| countable assets | $9,368.16 |\n| time in the service area | eleven months |\n| age | 59 years |\n| enrolled in | none |",
  "question": "Does Anton Yamazaki fail to qualify for admission to Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is at or above 58 years.\n- Gate B: passed when the applicant has lived in the service area for equal to or above eight months.\n- Gate C: passed when gross monthly income is $2,030.00 or under.\n- Route: an applicant enrolled in Hemmerly Nursery Place Fund skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdc226e2acc",
  "kind": "yes/no",
  "text": "{\"about\": \"Tove\", \"case\": \"CR-80635\", \"caseworker\": \"Sami Castro\", \"team\": \"help line\"}\n\nPeople who asked to claim Tove (2026), as JSON:\n{\"people\": [{\"name\": \"Farid Eriksen\", \"relationship\": \"father\", \"months_lived_with_child\": \"2 months\", \"annual_income\": \"64,181.64 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Sabine Dragic\", \"relationship\": \"mother\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"58,055.00 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Idris Anderson\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"56,245.00 USD\", \"filed_a_claim\": \"yes\"}]}",
  "question": "According to these rules, is Idris Anderson the person who ends up holding the right to claim Tove for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2026: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for strictly above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Tove lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb3212c249a",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CR-65804\nRaised by: Sasha Okonkwo\nAbout: Theo\n\nPeople who asked to claim Theo (2025):\n| person | relationship to Theo | months lived with Theo | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dario Okafor | grandfather | 11 months | $38,241.04 | yes |\n| Matias Dragic | father | 5 months | $43,020.00 | yes |",
  "question": "Does the right to claim Theo for Ostrowan Prairie Grant pass to a different person from Dario Okafor, or stay unclaimed under these rules?",
  "definitions": "Ostrowan Prairie Grant rules for 2025: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for 5 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Theo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qac88dd6ec6",
  "kind": "choice",
  "text": "ref: CR-62461\ncaseworker: Teo Quintero\nperson: Ana\n\nPeople who asked to claim Ana (2026):\n- Dagny Demir: relationship to Ana: aunt; months lived with Ana: 6 months; annual income: $49,074.00; filed a claim: yes\n- Xenia Bergstrom: relationship to Ana: mother; months lived with Ana: 5 months; annual income: $79,610.01; filed a claim: yes\n- Wanjiru Abara: relationship to Ana: grandmother; months lived with Ana: 3 months; annual income: $49,074.00; filed a claim: yes",
  "question": "Caddowen Harbour Family Allowance rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for 5 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ana lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if anyone, is entitled to claim Ana for Caddowen Harbour Family Allowance?",
  "options": [
   "Xenia Bergstrom",
   "Dagny Demir",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q33e665016e",
  "kind": "yes/no",
  "text": "{\"record\": \"CR-38896\", \"officer\": \"Quinn Pavlenko\", \"concerning\": \"Isla\"}\n\nInterview notes for Isla (2027):\nCaseworker: Anjali Ferreira, your relation to Isla?\nAnjali Ferreira: I am Isla's grandmother.\nCaseworker: Months Isla lived with you?\nAnjali Ferreira: 2 months.\nCaseworker: Annual income?\nAnjali Ferreira: $76,886.02.\nCaseworker: Filed a claim for Isla?\nAnjali Ferreira: yes.\nCaseworker: Fatima Bergstrom, your relation to Isla?\nFatima Bergstrom: I am Isla's mother.\nCaseworker: Months Isla lived with you?\nFatima Bergstrom: 3 months.\nCaseworker: Annual income?\nFatima Bergstrom: $60,435.07.\nCaseworker: Filed a claim for Isla?\nFatima Bergstrom: yes.\nCaseworker: Lucia Iyer, your relation to Isla?\nLucia Iyer: I am Isla's aunt.\nCaseworker: Months Isla lived with you?\nLucia Iyer: 6 months.\nCaseworker: Annual income?\nLucia Iyer: $66,229.00.\nCaseworker: Filed a claim for Isla?\nLucia Iyer: yes.\nCaseworker: Tariq Ilunga, your relation to Isla?\nTariq Ilunga: I am Isla's father.\nCaseworker: Months Isla lived with you?\nTariq Ilunga: 10 months.\nCaseworker: Annual income?\nTariq Ilunga: $43,376.92.\nCaseworker: Filed a claim for Isla?\nTariq Ilunga: no.",
  "question": "According to these rules, is Lucia Iyer the person who ends up with the right to claim Isla for Gristmere Child Credit?",
  "definitions": "Gristmere Child Credit rules for 2027: who may claim Isla.\n- Only one person may claim Isla. Work through these steps in order.\n- Step one: only people who filed a claim for Isla are considered.\n- Step two: of those, only people with whom Isla lived for 6 months or more in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Isla lived for more months comes first.\n- If nobody is left after step two, nobody may claim Isla.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfa2063a5fc",
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
  "qid": "q824afc3d18",
  "kind": "yes/no",
  "text": "Facts for Ugo Jovanovic (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,535.57 USD |\n| net monthly income | 2,029.99 USD |\n| countable assets | 7,642.12 USD |\n| time in the service area | 47 months |\n| age | 58 years |\n| enrolled in | none |\n\n[front_counter] case_ref=CASE-38558 staff=Jamie Jorgensen subject=Ugo Jovanovic",
  "question": "Under these rules, is it not true that Ugo Jovanovic is not eligible for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly lower than $2,030.\n- Gate B: passed when the applicant's age is greater than 57 years.\n- Gate C: passed when gross monthly income is strictly under $2,825.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qfcbbfbac20",
  "kind": "choice",
  "text": "Hello,\nThe casework team holds CR-16850 for Ada.\nBest, Shay Bekele\n\nPeople who asked to claim Ada (2025):\n- Kwame Thompson: relationship to Ada: grandfather; months lived with Ada: 7 months; annual income: $94,822.95; filed a claim: yes\n- Xavier Johnson: relationship to Ada: father; months lived with Ada: 11 months; annual income: $24,380.00; filed a claim: no",
  "question": "Kelvery Market Credit rules for 2025: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for strictly higher than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Kelvery Market Credit, which person, if any, gets to claim Ada under these rules?",
  "options": [
   "Xavier Johnson",
   "Kwame Thompson"
  ]
 },
 {
  "qid": "q2eefd4bcd5",
  "kind": "yes/no",
  "text": "Dear colleague,\nFor the record, HR-93726 concerning Galina Ueda is held by the desk.\nYours faithfully, Jamie Jorgensen\n\nFacts for Galina Ueda (2027):\n- time employed: 5 months\n- hours worked in the past year: 1502 hours\n- employees at the worksite: 11 employees\n- gross annual pay: 113,194.81 USD\n- take-home annual pay: 83,842.37 USD\n- enrolled in: Idrane Tuition Grant",
  "question": "Going by the listed rules, is Galina Ueda eligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for strictly above 19 months.\n- Gate B: passed when take-home annual pay is 57,000.00 USD or less.\n- Gate C: passed when the worksite has 36 employees at minimum.\n- Route: an applicant enrolled in Idrane Tuition Grant skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3d0eb120fc",
  "kind": "yes/no",
  "text": "Note for the intake desk: Mariam Kimura is named on case CASE-02795, which Kendall Umarov keeps.\n\nIntake interview with Mariam Kimura (2026):\nCaseworker: Gross monthly income?\nMariam Kimura: $2,261.39.\nCaseworker: Net monthly income?\nMariam Kimura: $1,925.81.\nCaseworker: Countable assets?\nMariam Kimura: $3,322.72.\nCaseworker: Time in the service area?\nMariam Kimura: 0 months.\nCaseworker: Age?\nMariam Kimura: 28 years.\nCaseworker: Other programme enrolled in?\nMariam Kimura: Lowmarsh Heating Aid.",
  "question": "Under these rules, is Mariam Kimura plainly not eligible for Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for greater than 3 months.\n- Gate B: passed when net monthly income is at or beneath $1,730.00.\n- Route: an applicant enrolled in Aldervale Meal Basket skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q37fcebdc32",
  "kind": "choice",
  "text": "Friendly ticket: CR-05822\nRaised by: Emi Figueroa\nAbout: Vida\n\nInterview notes for Vida (2026):\nCaseworker: Bruno Stewart, your relation to Vida?\nBruno Stewart: I am Vida's uncle.\nCaseworker: Months Vida lived with you?\nBruno Stewart: three months.\nCaseworker: Annual income?\nBruno Stewart: $45,083.42.\nCaseworker: Filed a claim for Vida?\nBruno Stewart: no.\nCaseworker: Gabriel Eriksen, your relation to Vida?\nGabriel Eriksen: I am Vida's grandfather.\nCaseworker: Months Vida lived with you?\nGabriel Eriksen: ten months.\nCaseworker: Annual income?\nGabriel Eriksen: $23,317.\nCaseworker: Filed a claim for Vida?\nGabriel Eriksen: yes.\nCaseworker: Imani Ruiz, your relation to Vida?\nImani Ruiz: I am Vida's aunt.\nCaseworker: Months Vida lived with you?\nImani Ruiz: seven months.\nCaseworker: Annual income?\nImani Ruiz: $93,976.\nCaseworker: Filed a claim for Vida?\nImani Ruiz: yes.",
  "question": "Gristmere Child Credit rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for greater than six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Vida for Gristmere Child Credit?",
  "options": [
   "Nobody may claim the child",
   "Gabriel Eriksen",
   "Imani Ruiz"
  ]
 },
 {
  "qid": "q5922ea9857",
  "kind": "yes/no",
  "text": "Riley Watanabe: Case CR-54498 is logged on the review desk for Milo.\n\nPeople who asked to claim Milo (2027):\n- Yasmin Sharma: relationship to Milo: mother; months lived with Milo: four months; annual income: $71,320.22; filed a claim: yes\n- Yusuf Hoffman: relationship to Milo: father; months lived with Milo: twelve months; annual income: $57,009; filed a claim: yes\n- Ingrid Anderson: relationship to Milo: grandmother; months lived with Milo: three months; annual income: $57,009; filed a claim: no",
  "question": "According to these rules, is Yusuf Hoffman the person who ends up holding the right to claim Milo for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for strictly greater than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Milo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4059eec982",
  "kind": "yes/no",
  "text": "Intake ticket: CR-14472\nRaised by: Adi Chandra\nAbout: Lara\n\nPeople who asked to claim Lara (2027):\n| person | relationship to Lara | months lived with Lara | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kenji Campbell | uncle | 10 months | $23,378.02 | yes |\n| Viktor Gashi | grandfather | 4 months | $87,623.00 | yes |\n| Mateo Rahimi | father | 6 months | $58,183.37 | yes |\n| Freya Choi | mother | 7 months | $58,183.37 | yes |",
  "question": "Is Freya Choi excluded from claiming Lara for Caddowen Harbour Family Allowance under these rules?",
  "definitions": "Caddowen Harbour Family Allowance rules for 2027: who may claim Lara.\n- Only one person may claim Lara. Work through these steps in order.\n- Step one: only people who filed a claim for Lara are considered.\n- Step two: of those, only people with whom Lara lived for greater than or equal to 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Lara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Lara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc6a8a9ef47",
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
  "qid": "qe9fe058f45",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-56894\", \"caseworker\": \"Remy Tran\", \"about\": \"Idris Medina\", \"desk\": \"services counter\"}\n\nIntake interview with Idris Medina (2025):\nCaseworker: Gross monthly income?\nIdris Medina: 3,087.84 USD.\nCaseworker: Net monthly income?\nIdris Medina: 2,599.99 USD.\nCaseworker: Countable assets?\nIdris Medina: 5,685.95 USD.\nCaseworker: Time in the service area?\nIdris Medina: 12 months.\nCaseworker: Age?\nIdris Medina: 18 years.\nCaseworker: Other programme enrolled in?\nIdris Medina: Kelmstone Drainage Subsidy.",
  "question": "Under these rules, does Idris Medina meet the rules for Ostermere Delta Flood Repair Support across every applicable gate?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly below the level of $3,575.\n- Gate B: passed when net monthly income is strictly lower than $2,600.\n- Gate C: passed when the applicant's age is higher than 61 years.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf6938dfdd6",
  "kind": "yes/no",
  "text": "Quick ticket: CR-30646\nRaised by: Kiran Morales\nAbout: Omar\n\nInterview notes for Omar (2027):\nCaseworker: Emeka Ruiz, your relation to Omar?\nEmeka Ruiz: I am Omar's father.\nCaseworker: Months Omar lived with you?\nEmeka Ruiz: eight months.\nCaseworker: Annual income?\nEmeka Ruiz: 70,531.87 USD.\nCaseworker: Filed a claim for Omar?\nEmeka Ruiz: yes.\nCaseworker: Hamid Russell, your relation to Omar?\nHamid Russell: I am Omar's uncle.\nCaseworker: Months Omar lived with you?\nHamid Russell: three months.\nCaseworker: Annual income?\nHamid Russell: $89,448.\nCaseworker: Filed a claim for Omar?\nHamid Russell: yes.\nCaseworker: Mariam Mensah, your relation to Omar?\nMariam Mensah: I am Omar's mother.\nCaseworker: Months Omar lived with you?\nMariam Mensah: two months.\nCaseworker: Annual income?\nMariam Mensah: $24,112.\nCaseworker: Filed a claim for Omar?\nMariam Mensah: yes.",
  "question": "According to these rules, is Hamid Russell the person who ends up holding the right to claim Omar for Stonevale Delta Child Allowance?",
  "definitions": "Stonevale Delta Child Allowance rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for a minimum of seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qb5086d9965",
  "kind": "yes/no",
  "text": "People who asked to claim Gia (2026):\n| person | relationship to Gia | months lived with Gia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kofi Petrov | uncle | 10 months | $35,617.24 | yes |\n| Hamid Choi | father | 0 months | $51,356.00 | yes |\n| Ravi Watson | grandfather | 12 months | $35,617.24 | yes |\n\n[casework_team] ref=CR-70531 caseworker=Morgan Mendoza about=Gia",
  "question": "For Sorrenby Island Family Payment, is Hamid Choi barred from claiming Gia under the listed rules?",
  "definitions": "Sorrenby Island Family Payment rules for 2026: who may claim Gia.\n- Only one person may claim Gia. Work through these steps in order.\n- Step one: only people who filed a claim for Gia are considered.\n- Step two: of those, only people with whom Gia lived for at or greater than 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Gia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Gia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd287bb6721",
  "kind": "yes/no",
  "text": "Records desk note. Nika Hernandez keeps HR-91668, which concerns Yasmin Johnson.\n\nFacts for Yasmin Johnson (2026):\n- time employed: 80 months\n- hours worked in the past year: 1,533 hours\n- employees at the worksite: 130 employees\n- gross annual pay: 47,610.95 USD\n- take-home annual pay: 33,500.01 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "For Morrowdene Hospital Group Return Support, does Yasmin Johnson fail to qualify under these rules?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are over 1,290 hours.\n- Gate B: passed when take-home annual pay is at or below $33,500.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q10e553334c",
  "kind": "yes/no",
  "text": "{\"caseworker\": \"Teo Quintero\", \"about\": \"Gustav Dubois\", \"case\": \"HR-27746\", \"office\": \"branch\"}\n\nFacts for Gustav Dubois (2025), as JSON:\n{\"time_employed\": \"70 months\", \"hours_worked_in_the_past_year\": \"514 hours\", \"employees_at_the_worksite\": \"85 employees\", \"gross_annual_pay\": \"64,609.26 USD\", \"take-home_annual_pay\": \"42,768.06 USD\", \"enrolled_in\": \"Gerrondale Tenant Aid\"}",
  "question": "Going by the listed rules, is Gustav Dubois not eligible for Marrowby Bakery Family Leave?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has a minimum of 58 employees.\n- Gate B: passed when take-home annual pay is at or beneath $40,500.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q47bc2c42b0",
  "kind": "yes/no",
  "text": "Dear Jakub Ueda,\nThis reply concerns case HR-96150.\nYours sincerely, Adi Chandra\n\nFacts for Jakub Ueda (2025):\n- time employed: 25 months\n- hours worked in the past year: 915 hours\n- employees at the worksite: 192 employees\n- gross annual pay: $85,499.99\n- take-home annual pay: $60,264.10\n- enrolled in: Corrowell Sabbatical Fund",
  "question": "Going by the listed rules, is Jakub Ueda ineligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or under the amount of $85,500.00.\n- Gate B: passed when the applicant has been employed for over 24 months.\n- Route: an applicant enrolled in Corrowell Sabbatical Fund skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q52901281a5",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Viktor Mensah; the reference is HR-03377.\nKind regards, Casey Kaplan\n\nFacts for Viktor Mensah (2027):\n- time employed: 9 months\n- hours worked in the past year: 664 hours\n- employees at the worksite: 36 employees\n- gross annual pay: 56,999.99 USD\n- take-home annual pay: 46,499.99 USD\n- enrolled in: Halvorne Sabbatical Fund",
  "question": "According to these rules, does Viktor Mensah fail to qualify for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 663 hours.\n- Gate B: passed when take-home annual pay is smaller than $46,500.\n- Gate C: passed when gross annual pay is $57,000 or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9969d3a468",
  "kind": "yes/no",
  "text": "Ticket: outreach team, with thanks, case CR-65804\nRaised by: Sasha Okonkwo\nAbout: Theo\n\nPeople who asked to claim Theo (2025):\n| person | relationship to Theo | months lived with Theo | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Dario Okafor | grandfather | 11 months | $38,241.04 | yes |\n| Matias Dragic | father | 5 months | $43,020.00 | yes |",
  "question": "According to these rules, is Dario Okafor the person who ends up with the right to claim Theo for Ostrowan Prairie Grant?",
  "definitions": "Ostrowan Prairie Grant rules for 2025: who may claim Theo.\n- Only one person may claim Theo. Work through these steps in order.\n- Step one: only people who filed a claim for Theo are considered.\n- Step two: of those, only people with whom Theo lived for 5 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Theo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Theo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2a621917bb",
  "kind": "choice",
  "text": "People who asked to claim Ezra (2025):\n| person | relationship to Ezra | months lived with Ezra | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Imani Esposito | grandmother | six months | $35,958 | yes |\n| Hana Lehmann | mother | six months | $64,211 | yes |\n| Elias Mwangi | uncle | six months | $64,211 | yes |\n\nTicket CR-98316\nWith: Alex Lindgren\nAbout: Ezra",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for strictly over five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Ezra for Brellow Orchard Family Credit?",
  "options": [
   "Imani Esposito",
   "Hana Lehmann"
  ]
 },
 {
  "qid": "q5baa00de93",
  "kind": "yes/no",
  "text": "ref: CR-19674\nhandler: Blair Xiong\nsubject: Omar\n\nInterview notes for Omar (2027):\nCaseworker: Dario Mwangi, your relation to Omar?\nDario Mwangi: I am Omar's father.\nCaseworker: Months Omar lived with you?\nDario Mwangi: 2 months.\nCaseworker: Annual income?\nDario Mwangi: 69,448.00 USD.\nCaseworker: Filed a claim for Omar?\nDario Mwangi: no.\nCaseworker: Amara Russell, your relation to Omar?\nAmara Russell: I am Omar's grandmother.\nCaseworker: Months Omar lived with you?\nAmara Russell: 12 months.\nCaseworker: Annual income?\nAmara Russell: 73,151.63 USD.\nCaseworker: Filed a claim for Omar?\nAmara Russell: yes.\nCaseworker: Vesna Becker, your relation to Omar?\nVesna Becker: I am Omar's mother.\nCaseworker: Months Omar lived with you?\nVesna Becker: 10 months.\nCaseworker: Annual income?\nVesna Becker: 90,988.00 USD.\nCaseworker: Filed a claim for Omar?\nVesna Becker: yes.",
  "question": "Under these rules, is Vesna Becker excluded from claiming Omar for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2027: who may claim Omar.\n- Only one person may claim Omar. Work through these steps in order.\n- Step one: only people who filed a claim for Omar are considered.\n- Step two: of those, only people with whom Omar lived for 7 months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Omar lived for more months comes first.\n- If nobody is left after step two, nobody may claim Omar.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2476561289",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-56894\", \"caseworker\": \"Remy Tran\", \"about\": \"Idris Medina\", \"desk\": \"services counter\"}\n\nIntake interview with Idris Medina (2025):\nCaseworker: Gross monthly income?\nIdris Medina: 3,087.84 USD.\nCaseworker: Net monthly income?\nIdris Medina: 2,599.99 USD.\nCaseworker: Countable assets?\nIdris Medina: 5,685.95 USD.\nCaseworker: Time in the service area?\nIdris Medina: 12 months.\nCaseworker: Age?\nIdris Medina: 18 years.\nCaseworker: Other programme enrolled in?\nIdris Medina: Kelmstone Drainage Subsidy.",
  "question": "Does a gate that applies halt the application of Idris Medina to Ostermere Delta Flood Repair Support?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly below the level of $3,575.\n- Gate B: passed when net monthly income is strictly lower than $2,600.\n- Gate C: passed when the applicant's age is higher than 17 years.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdc994bbbe4",
  "kind": "yes/no",
  "text": "Note for the intake desk: Mariam Kimura is named on case CASE-02795, which Kendall Umarov keeps.\n\nIntake interview with Mariam Kimura (2026):\nCaseworker: Gross monthly income?\nMariam Kimura: $2,261.39.\nCaseworker: Net monthly income?\nMariam Kimura: $1,925.81.\nCaseworker: Countable assets?\nMariam Kimura: $3,322.72.\nCaseworker: Time in the service area?\nMariam Kimura: 0 months.\nCaseworker: Age?\nMariam Kimura: 28 years.\nCaseworker: Other programme enrolled in?\nMariam Kimura: Lowmarsh Heating Aid.",
  "question": "Going by the listed rules, is it not the case that Mariam Kimura is not eligible for Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for greater than 3 months.\n- Gate B: passed when net monthly income is at or beneath $1,730.00.\n- Route: an applicant enrolled in Aldervale Meal Basket skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf6b6ebbd37",
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
  "qid": "qb1b872e76d",
  "kind": "choice",
  "text": "{\"case\": \"CR-19448\", \"lead\": \"Dani Ishikawa\", \"subject\": \"Vida\", \"office\": \"town_hall\"}\n\nPeople who asked to claim Vida (2027), as JSON:\n{\"people\": [{\"name\": \"Olena Nilsen\", \"relationship\": \"mother\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"$44,458.00\", \"filed_a_claim\": \"no\"}, {\"name\": \"Viktor Gashi\", \"relationship\": \"uncle\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"$56,563.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Zaid Schultz\", \"relationship\": \"father\", \"months_lived_with_child\": \"10 months\", \"annual_income\": \"$27,154.36\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for 6 months or more in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if any, ends up with the right to claim Vida for Ostrowan Prairie Grant?",
  "options": [
   "Viktor Gashi",
   "Zaid Schultz"
  ]
 },
 {
  "qid": "q42560ca832",
  "kind": "choice",
  "text": "Facts for Luka Ruiz (2027):\n| fact | value |\n| --- | --- |\n| time employed | 95 months |\n| hours worked in the past year | 1,371 hours |\n| employees at the worksite | 57 employees |\n| gross annual pay | 59,885.56 USD |\n| take-home annual pay | 37,374.48 USD |\n| enrolled in | Brumstead Wellbeing Grant |\n\nQuick intake form\nCase reference: HR-09870\nCaseworker: Kiran Morales\nAbout: Luka Ruiz",
  "question": "Pelmoor Ceramics Carer Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,370 hours.\n- Gate B: passed when the worksite has strictly more than 58 employees.\n- Gate C: passed when take-home annual pay is at or below the level of 70,000.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Luka Ruiz to Pelmoor Ceramics Carer Support receive?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (take-home annual pay)",
   "Not eligible: Gate A is the reason (hours worked in the past year)"
  ]
 },
 {
  "qid": "qa678ac8b74",
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
  "qid": "qb73b04a19b",
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
  "qid": "q4ed42a2023",
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
  "qid": "qe5e2a447cb",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Viktor Mensah; the reference is HR-03377.\nKind regards, Casey Kaplan\n\nFacts for Viktor Mensah (2027):\n- time employed: 9 months\n- hours worked in the past year: 664 hours\n- employees at the worksite: 36 employees\n- gross annual pay: 56,999.99 USD\n- take-home annual pay: 46,499.99 USD\n- enrolled in: Halvorne Sabbatical Fund",
  "question": "According to these rules, does Viktor Mensah fail to qualify for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,150 hours.\n- Gate B: passed when take-home annual pay is smaller than $46,500.\n- Gate C: passed when gross annual pay is $57,000 or lower.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q02dc21e994",
  "kind": "choice",
  "text": "Desk note: CR-71496\nQuick note by Mika Zamora at the community help desk, about Milo.\n\nInterview notes for Milo (2025):\nCaseworker: Wanjiru Nguyen, your relation to Milo?\nWanjiru Nguyen: I am Milo's mother.\nCaseworker: Months Milo lived with you?\nWanjiru Nguyen: 2 months.\nCaseworker: Annual income?\nWanjiru Nguyen: 26,718.74 USD.\nCaseworker: Filed a claim for Milo?\nWanjiru Nguyen: yes.\nCaseworker: Sergio Delgado, your relation to Milo?\nSergio Delgado: I am Milo's uncle.\nCaseworker: Months Milo lived with you?\nSergio Delgado: 6 months.\nCaseworker: Annual income?\nSergio Delgado: 89,326.18 USD.\nCaseworker: Filed a claim for Milo?\nSergio Delgado: yes.\nCaseworker: Dmitri Evans, your relation to Milo?\nDmitri Evans: I am Milo's uncle.\nCaseworker: Months Milo lived with you?\nDmitri Evans: 7 months.\nCaseworker: Annual income?\nDmitri Evans: 26,718.74 USD.\nCaseworker: Filed a claim for Milo?\nDmitri Evans: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2025: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for 5 months at minimum in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Milo lived for more months comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole individual who may claim Milo for Kelmstone Mountain Family Grant?",
  "options": [
   "Dmitri Evans",
   "Sergio Delgado"
  ]
 },
 {
  "qid": "q41eb547782",
  "kind": "yes/no",
  "text": "Facts for Kazu Wojcik (2025):\n| fact | value |\n| --- | --- |\n| time employed | 9 months |\n| hours worked in the past year | 326 hours |\n| employees at the worksite | 289 employees |\n| gross annual pay | 61,567.19 USD |\n| take-home annual pay | 38,255.22 USD |\n| enrolled in | Ostermere Skills Bursary |\n\nGreetings colleague,\nCase HR-42086 concerns Kazu Wojcik and sits with the records team.\nYours truly, Blair Xiong",
  "question": "Is Kazu Wojcik eligible for Drummock Robotics Workshop Training Fund with every applicable gate passed?",
  "definitions": "Drummock Robotics Workshop Training Fund eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is at or under the amount of 86,000.00 USD.\n- Gate B: passed when the applicant has been employed for strictly above 8 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8fce505b71",
  "kind": "choice",
  "text": "People who asked to claim Luca (2026):\n| person | relationship to Luca | months lived with Luca | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Fatima Tanaka | mother | 12 months | 17,369.00 USD | yes |\n| Hugo Mitchell | father | 1 month | 17,369.00 USD | yes |\n| Hiroko Nguyen | grandmother | 9 months | 79,104.00 USD | yes |\n\nHello Luca,\nA routine note about CR-22450 comes from the district office.\nBest wishes, Sami Castro",
  "question": "Farrowby Moorland Parish Credit rules for 2026: who may claim Luca.\n- Only one person may claim Luca. Work through these steps in order.\n- Step one: only people who filed a claim for Luca are considered.\n- Step two: of those, only people with whom Luca lived for in excess of 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Luca lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Luca.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Farrowby Moorland Parish Credit, which person, if any, gets to claim Luca under these rules?",
  "options": [
   "Hiroko Nguyen",
   "Fatima Tanaka"
  ]
 },
 {
  "qid": "q87adb5ef72",
  "kind": "yes/no",
  "text": "Facts for Freya Delgado (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 1,874.99 USD |\n| net monthly income | 1,349.11 USD |\n| countable assets | 7,049.99 USD |\n| time in the service area | twenty months |\n| age | 73 years |\n| enrolled in | Morvane Carers Allowance |\n\nDear team,\nPlease see the attached summary on case CASE-29998 for Freya Delgado.\nYours sincerely, Avery Obradovic",
  "question": "According to these rules, does Freya Delgado meet the rules for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly beneath $7,050.\n- Gate B: passed when gross monthly income is $1,875 or lower.\n- Gate C: passed when the applicant has lived in the service area for at or beyond ten months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q89b3daee6a",
  "kind": "yes/no",
  "text": "{\"case\": \"HR-47346\", \"caseworker\": \"Ezra Rosales\", \"about\": \"Kofi Hudson\", \"desk\": \"internal\"}\n\nFacts for Kofi Hudson (2026), as JSON:\n{\"time_employed\": \"67 months\", \"hours_worked_in_the_past_year\": \"1761 hours\", \"employees_at_the_worksite\": \"322 employees\", \"gross_annual_pay\": \"$90,440\", \"take-home_annual_pay\": \"62,257.10 USD\", \"enrolled_in\": \"Fallowden Retraining Bursary\"}",
  "question": "Following the listed rules, does Kofi Hudson fail to qualify for Tovardine Seed Caregiver Leave?",
  "definitions": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is lower than $82,500.\n- Gate B: passed when hours worked in the past year are at or beyond 1230 hours.\n- Route: an applicant enrolled in Dorrane Parental Leave skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q54cdbab5bc",
  "kind": "choice",
  "text": "[back_office] ref_code=CR-36949 held_by=Kazu Yousef concerns=Pia\n\nInterview notes for Pia (2027):\nCaseworker: Kwame Kimura, your relation to Pia?\nKwame Kimura: I am Pia's father.\nCaseworker: Months Pia lived with you?\nKwame Kimura: 1 month.\nCaseworker: Annual income?\nKwame Kimura: $61,480.81.\nCaseworker: Filed a claim for Pia?\nKwame Kimura: yes.\nCaseworker: Oskar Ramirez, your relation to Pia?\nOskar Ramirez: I am Pia's grandfather.\nCaseworker: Months Pia lived with you?\nOskar Ramirez: 3 months.\nCaseworker: Annual income?\nOskar Ramirez: $70,152.82.\nCaseworker: Filed a claim for Pia?\nOskar Ramirez: yes.\nCaseworker: Kenji Iyer, your relation to Pia?\nKenji Iyer: I am Pia's grandfather.\nCaseworker: Months Pia lived with you?\nKenji Iyer: 7 months.\nCaseworker: Annual income?\nKenji Iyer: $70,383.87.\nCaseworker: Filed a claim for Pia?\nKenji Iyer: yes.\nCaseworker: Vesna Sorensen, your relation to Pia?\nVesna Sorensen: I am Pia's mother.\nCaseworker: Months Pia lived with you?\nVesna Sorensen: 10 months.\nCaseworker: Annual income?\nVesna Sorensen: $73,259.46.\nCaseworker: Filed a claim for Pia?\nVesna Sorensen: no.",
  "question": "Gristmere Child Credit rules for 2027: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for equal to or greater than 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Pia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Pia for Gristmere Child Credit under these rules?",
  "options": [
   "Kwame Kimura",
   "Nobody may claim the child",
   "Kenji Iyer"
  ]
 },
 {
  "qid": "q4198001ff8",
  "kind": "choice",
  "text": "Friendly front counter slip\nTicket: CR-55084\nDealt with by: Blair Xiong\nNamed person: Tove\n\nPeople who asked to claim Tove (2027):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Galina Becker | mother | 9 months | 39,118.00 USD | yes |\n| Tomas Jovanovic | grandfather | 11 months | 28,081.00 USD | yes |\n| Kiara Lindqvist | aunt | 1 month | 20,256.00 USD | no |\n| Bruno Dlamini | father | 9 months | 64,650.13 USD | no |",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for over 6 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Tove lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, ends up with the right to claim Tove for Ostrowan Prairie Grant?",
  "options": [
   "Tomas Jovanovic",
   "Bruno Dlamini",
   "Galina Becker"
  ]
 },
 {
  "qid": "q4326b4100e",
  "kind": "yes/no",
  "text": "[case_log] staff_support_desk case=HR-76487 caseworker=Blair Xiong about=Jiro Ilunga\n\nIntake interview with Jiro Ilunga (2025):\nCaseworker: Time employed?\nJiro Ilunga: 21 months.\nCaseworker: Hours worked in the past year?\nJiro Ilunga: 2015 hours.\nCaseworker: Employees at your worksite?\nJiro Ilunga: 326 employees.\nCaseworker: Gross annual pay?\nJiro Ilunga: 56,046.78 USD.\nCaseworker: Take-home annual pay?\nJiro Ilunga: 36,625.95 USD.\nCaseworker: Other programme enrolled in?\nJiro Ilunga: Quelmere Lunch Card.",
  "question": "Does Jiro Ilunga fully qualify for Sorrelby Child Care Support under these rules?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are 1480 hours or greater.\n- Gate B: passed when gross annual pay is at or under the amount of $37,000.\n- Gate C: passed when the applicant has been employed for 11 months or above.\n- Route: an applicant enrolled in Quelmere Lunch Card skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q60037a8311",
  "kind": "choice",
  "text": "district_ref: HR-45230\nhandled_by: Kazu Yousef\nabout: Ivo Yamazaki\n\nFacts for Ivo Yamazaki (2027):\n- time employed: nine months\n- hours worked in the past year: 1649 hours\n- employees at the worksite: 225 employees\n- gross annual pay: $113,395.81\n- take-home annual pay: $97,351.95\n- enrolled in: Caddowen Veterans Pathway",
  "question": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly below the amount of $77,000.00.\n- Gate B: passed when the applicant has been employed for ten months or more.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, what outcome does the application of Ivo Yamazaki to Morrowdene Hospital Group Return Support receive?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "q3eabf1bf75",
  "kind": "yes/no",
  "text": "Facts for Kazu Medina (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,150.94 USD |\n| net monthly income | 2,566.99 USD |\n| countable assets | 12,597.83 USD |\n| time in the service area | 7 months |\n| age | 76 years |\n| enrolled in | Sallafell Bus Credit |\n\nTown hall intake header\nCase reference: CASE-39450\nCaseworker: Sasha Okonkwo\nAbout: Kazu Medina",
  "question": "For Tollsey Island Ferry Discount, does Kazu Medina qualify by passing every gate that applies?",
  "definitions": "Tollsey Island Ferry Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is lower than or equal to 3,240.00 USD.\n- Gate B: passed when the applicant has lived in the service area for 4 months at minimum.\n- Gate C: passed when the applicant's age is a minimum of 64 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc95d945ec8",
  "kind": "yes/no",
  "text": "reference: CR-87729\nworker: Morgan Mendoza\nabout: Dara\n\nPeople who asked to claim Dara (2025):\n- Xenia Bergstrom: relationship to Dara: aunt; months lived with Dara: ten months; annual income: 89,055.00 USD; filed a claim: yes\n- Ugo Gutierrez: relationship to Dara: father; months lived with Dara: nine months; annual income: 31,077.25 USD; filed a claim: yes\n- Zofia Ivanova: relationship to Dara: mother; months lived with Dara: five months; annual income: 41,304.58 USD; filed a claim: yes",
  "question": "Under these rules, is it true that Ugo Gutierrez may not claim Dara for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Dara.\n- Only one person may claim Dara. Work through these steps in order.\n- Step one: only people who filed a claim for Dara are considered.\n- Step two: of those, only people with whom Dara lived for at or greater than five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Dara lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Dara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3dd6286d8f",
  "kind": "choice",
  "text": "[record_entry] case_ref=CR-69834 worker=Dani Ishikawa\n[desk_queue] about=Remi queue=records_office\n\nPeople who asked to claim Remi (2026):\n| person | relationship to Remi | months lived with Remi | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ailsa Anderson | grandmother | 10 months | $56,481.49 | yes |\n| Jelena Bergstrom | mother | 7 months | $31,624.00 | yes |\n| Nkechi Evans | grandmother | 1 month | $63,931.00 | yes |",
  "question": "Ostrowan Prairie Grant rules for 2026: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for strictly greater than 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Remi lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, may claim Remi for Ostrowan Prairie Grant?",
  "options": [
   "Ailsa Anderson",
   "Jelena Bergstrom"
  ]
 },
 {
  "qid": "qf5dd2d18eb",
  "kind": "yes/no",
  "text": "Case note: the intake desk has Nia on case CR-38751, with Lior Grigoryan in charge.\n\nPeople who asked to claim Nia (2027):\n- Felix Rahimi: relationship to Nia: grandfather; months lived with Nia: 11 months; annual income: 79,618.12 USD; filed a claim: yes\n- Nkechi Eriksen: relationship to Nia: mother; months lived with Nia: 11 months; annual income: 79,618.12 USD; filed a claim: no\n- Bianca Ueda: relationship to Nia: grandmother; months lived with Nia: 11 months; annual income: 25,479.00 USD; filed a claim: yes",
  "question": "According to these rules, is Nkechi Eriksen the person who ends up holding the right to claim Nia for Dunmarrow Hill Allowance?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Nia.\n- Only one person may claim Nia. Work through these steps in order.\n- Step one: only people who filed a claim for Nia are considered.\n- Step two: of those, only people with whom Nia lived for strictly over 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Nia lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Nia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 }
]
