# G5-H blind read T15-blind_read-18dfa75d-000 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/pilot_i1/g5h/answers/T15-blind_read-18dfa75d-000.json

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
  "qid": "q2539eccf88",
  "kind": "choice",
  "text": "Ticket: HR-22208 at the services counter\nRaised by: Kazu Yousef\nAbout: Luka Okafor\n\nFacts for Luka Okafor (2026):\n| fact | value |\n| --- | --- |\n| time employed | 37 months |\n| hours worked in the past year | 1831 hours |\n| employees at the worksite | 247 employees |\n| gross annual pay | 79,889.86 USD |\n| take-home annual pay | 32,207.44 USD |\n| enrolled in | Lumenfold Skills Voucher |",
  "question": "Halvorne Shipyard Tuition Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for equal to or greater than 23 months.\n- Gate B: passed when take-home annual pay is at or under 53,000.00 USD.\n- Gate C: passed when gross annual pay is at or less than 73,500.00 USD.\n- Route: an applicant enrolled in Lumenfold Skills Voucher skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Luka Okafor to Halvorne Shipyard Tuition Assistance land?",
  "options": [
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)"
  ]
 },
 {
  "qid": "q59989d716f",
  "kind": "yes/no",
  "text": "Facts for Kazu Hudson (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,990 |\n| net monthly income | 2,035.96 USD |\n| countable assets | 6,344.52 USD |\n| time in the service area | 18 months |\n| age | 57 years |\n| enrolled in | Morvane Carers Pension |\n\n[front_counter] case_ref=CASE-38558 staff=Jamie Jorgensen subject=Kazu Hudson",
  "question": "Under these rules, is it not true that Kazu Hudson is not eligible for Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when net monthly income is strictly under $2,445.\n- Gate B: passed when the applicant's age is larger than 56 years.\n- Gate C: passed when gross monthly income is $2,990 at the most.\n- Gate D: passed when the applicant has lived in the service area for 19 months at minimum.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q44205572d1",
  "kind": "yes/no",
  "text": "Case note: Ren Dvorak is handling Milo on case CR-63984. Thanks for the help.\n\nInterview notes for Milo (2026):\nCaseworker: Quentin Yilmaz, your relation to Milo?\nQuentin Yilmaz: I am Milo's father.\nCaseworker: Months Milo lived with you?\nQuentin Yilmaz: 9 months.\nCaseworker: Annual income?\nQuentin Yilmaz: 60,481.00 USD.\nCaseworker: Filed a claim for Milo?\nQuentin Yilmaz: yes.\nCaseworker: Olena Ruiz, your relation to Milo?\nOlena Ruiz: I am Milo's grandmother.\nCaseworker: Months Milo lived with you?\nOlena Ruiz: 2 months.\nCaseworker: Annual income?\nOlena Ruiz: 36,329.00 USD.\nCaseworker: Filed a claim for Milo?\nOlena Ruiz: no.\nCaseworker: Anjali Halvorsen, your relation to Milo?\nAnjali Halvorsen: I am Milo's mother.\nCaseworker: Months Milo lived with you?\nAnjali Halvorsen: 5 months.\nCaseworker: Annual income?\nAnjali Halvorsen: 93,202.00 USD.\nCaseworker: Filed a claim for Milo?\nAnjali Halvorsen: no.\nCaseworker: Zofia Ramirez, your relation to Milo?\nZofia Ramirez: I am Milo's aunt.\nCaseworker: Months Milo lived with you?\nZofia Ramirez: 10 months.\nCaseworker: Annual income?\nZofia Ramirez: 81,548.00 USD.\nCaseworker: Filed a claim for Milo?\nZofia Ramirez: no.",
  "question": "Going by the listed rules, is it true that Quentin Yilmaz may not claim Milo for Kelmstone Mountain Family Grant?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2026: who may claim Milo.\n- Only one person may claim Milo. Work through these steps in order.\n- Step one: only people who filed a claim for Milo are considered.\n- Step two: of those, only people with whom Milo lived for at or above 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Milo lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Milo.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa2de0939ef",
  "kind": "yes/no",
  "text": "[casework_team] ref=HR-06778 caseworker=Avery Obradovic about=Kiara Becker\n\nFacts for Kiara Becker (2025):\n| fact | value |\n| --- | --- |\n| time employed | 104 months |\n| hours worked in the past year | 1159 hours |\n| employees at the worksite | 34 employees |\n| gross annual pay | $58,438.40 |\n| take-home annual pay | $47,229.33 |\n| enrolled in | Rickmere Night Course Fund |",
  "question": "Under these rules, does Kiara Becker meet the rules for Hallowdene Logistics Study Grant across every applicable gate?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has over 34 employees.\n- Gate B: passed when take-home annual pay is strictly smaller than $60,000.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qeae6694176",
  "kind": "yes/no",
  "text": "Yuki Adeyemi: help line has Esra Patterson on CASE-81739.\n\nFacts for Esra Patterson (2027):\n- gross monthly income: 4,930.11 USD\n- net monthly income: 3,111.02 USD\n- countable assets: 11,850.79 USD\n- time in the service area: 40 months\n- age: 55 years\n- enrolled in: Hallowby Utility Discount",
  "question": "Under these rules, is Esra Patterson eligible for Tesslow Prairie Water Bill Assistance overall?",
  "definitions": "Tesslow Prairie Water Bill Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than or equal to 55 years.\n- Gate B: passed when gross monthly income is at or under the amount of 3,430.00 USD.\n- Route: an applicant enrolled in Hallowby Utility Discount skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6c3acb33e9",
  "kind": "choice",
  "text": "Front counter intake form\nReference: CASE-37940\nCaseworker: Ari Benali\nPerson: Zofia Gordon\n\nFacts for Zofia Gordon (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $3,487.45 |\n| net monthly income | $3,000.01 |\n| countable assets | $4,799.34 |\n| time in the service area | 41 months |\n| age | 35 years |\n| enrolled in | Velgate Pantry Voucher |",
  "question": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly lower than $7,900.\n- Gate B: passed when net monthly income is at or beneath $3,000.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich way does the application of Zofia Gordon for Corrivale Valley Childcare Grant come out?",
  "options": [
   "Not eligible: Gate B is the reason (net monthly income)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "qc7be8c759e",
  "kind": "yes/no",
  "text": "People who asked to claim Amir (2025):\n| person | relationship to Amir | months lived with Amir | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Gabriel Eriksen | grandfather | 1 month | 81,409.57 USD | yes |\n| Cyril Zielinski | father | 5 months | $30,615 | no |\n| Mateo Evans | grandfather | 8 months | $70,551 | no |\n\n[front_counter] reference=CR-63869 caseworker=Sami Castro person=Amir",
  "question": "Is it not true that Gabriel Eriksen may not claim Amir for Mollenby Canal Child Supplement?",
  "definitions": "Mollenby Canal Child Supplement rules for 2025: who may claim Amir.\n- Only one person may claim Amir. Work through these steps in order.\n- Step one: only people who filed a claim for Amir are considered.\n- Step two: of those, only people with whom Amir lived for a minimum of 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Amir lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Amir.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd8ebf14967",
  "kind": "yes/no",
  "text": "Front counter ticket: CASE-30397\nWarm hello from: Toni Lazar\nPerson: Felix Murphy\n\nFacts for Felix Murphy (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,727.82 |\n| net monthly income | $1,940.01 |\n| countable assets | $2,871.56 |\n| time in the service area | 47 months |\n| age | twenty years |\n| enrolled in | Ruddock Shuttle Card |",
  "question": "Is Felix Murphy not eligible for Corvane Transit Fare Discount as the rules stand?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is at or under the amount of $2,285.00.\n- Gate B: passed when net monthly income is $1,940.00 or under.\n- Route: an applicant enrolled in Ruddock Shuttle Card skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qded64e9a15",
  "kind": "choice",
  "text": "{\"record\": \"CR-46458\", \"handler\": \"Ezra Rosales\", \"subject\": \"Ivan\"}\n\nPeople who asked to claim Ivan (2025), as JSON:\n{\"people\": [{\"name\": \"Kwame Okafor\", \"relationship\": \"father\", \"months_lived_with_child\": \"7 months\", \"annual_income\": \"25,542.51 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Kavita Demir\", \"relationship\": \"mother\", \"months_lived_with_child\": \"9 months\", \"annual_income\": \"91,453.60 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nadia Kowalski\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"6 months\", \"annual_income\": \"50,376.80 USD\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Dunmarrow Hill Allowance rules for 2025: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for equal to or greater than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ivan lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Dunmarrow Hill Allowance, which person, if any, gets to claim Ivan under these rules?",
  "options": [
   "Kavita Demir",
   "Kwame Okafor",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qe581b0ab78",
  "kind": "choice",
  "text": "Ezra Rosales: Lovely to see you, Ailsa Halvorsen; the staff desk has case CASE-13965 in good hands.\n\nFacts for Ailsa Halvorsen (2026):\n- gross monthly income: $2,481.53\n- net monthly income: $1,950.20\n- countable assets: $6,701.51\n- time in the service area: 21 months\n- age: 27 years\n- enrolled in: Crannock Food Pantry",
  "question": "Ostmere Lakeside Winter Energy Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $6,450.00 or lower.\n- Gate B: passed when gross monthly income is strictly smaller than $2,155.00.\n- Route: an applicant enrolled in Crannock Food Pantry skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Ailsa Halvorsen to Ostmere Lakeside Winter Energy Support get under these rules?",
  "options": [
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible",
   "Not eligible: Gate B is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q2aed89d70e",
  "kind": "yes/no",
  "text": "Records desk note. Nika Hernandez keeps HR-91668, which concerns Yasmin Johnson.\n\nFacts for Yasmin Johnson (2026):\n- time employed: 80 months\n- hours worked in the past year: 1,533 hours\n- employees at the worksite: 130 employees\n- gross annual pay: 47,610.95 USD\n- take-home annual pay: 33,500.01 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "For Morrowdene Hospital Group Return Support, does Yasmin Johnson fail to qualify under these rules?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are over 1,290 hours.\n- Gate B: passed when take-home annual pay is at or below $33,500.\n- Route: an applicant enrolled in Caddowen Veterans Pathway skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q700aec5a49",
  "kind": "yes/no",
  "text": "Internal note: Ezra Rosales looks after case CR-92191 in the regional service team, about Ami.\n\nPeople who asked to claim Ami (2027):\n- Amara Kovacs: relationship to Ami: grandmother; months lived with Ami: 6 months; annual income: 56,572.37 USD; filed a claim: yes\n- Matias Hoffman: relationship to Ami: father; months lived with Ami: 0 months; annual income: 32,063.00 USD; filed a claim: no\n- Ailsa Begum: relationship to Ami: mother; months lived with Ami: 3 months; annual income: 79,442.00 USD; filed a claim: yes",
  "question": "For Dunmarrow Hill Allowance, is it not the case that Ailsa Begum may not claim Ami?",
  "definitions": "Dunmarrow Hill Allowance rules for 2027: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for greater than or equal to 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5ff6ab13ea",
  "kind": "yes/no",
  "text": "case_id: HR-58613\nworker_name: Kiran Morales\nsubject_name: Esra Hudson\n\nFacts for Esra Hudson (2026):\n- time employed: 7 months\n- hours worked in the past year: 1,177 hours\n- employees at the worksite: 102 employees\n- gross annual pay: $28,412.68\n- take-home annual pay: $24,417.82\n- enrolled in: Idrane Tuition Grant",
  "question": "Going by the listed rules, is Esra Hudson eligible for Wendmoor Mill Parental Leave?",
  "definitions": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly in excess of 920 hours.\n- Gate B: passed when the applicant has been employed for strictly above 6 months.\n- Gate C: passed when the worksite has equal to or greater than 59 employees.\n- Route: an applicant enrolled in Idrane Tuition Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q122bca459b",
  "kind": "choice",
  "text": "record: CR-96070\ncaseworker: Jamie Jorgensen\nabout: Eva\ntone: warm\n\nPeople who asked to claim Eva (2025):\n- Jelena Reynolds: relationship to Eva: grandmother; months lived with Eva: nine months; annual income: $47,632.15; filed a claim: yes\n- Juliana Kaur: relationship to Eva: mother; months lived with Eva: twelve months; annual income: $15,815.00; filed a claim: yes",
  "question": "Ostrowan Prairie Grant rules for 2025: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for strictly more than five months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Eva for Ostrowan Prairie Grant, who is it?",
  "options": [
   "Juliana Kaur",
   "Jelena Reynolds"
  ]
 },
 {
  "qid": "qac5eca84d3",
  "kind": "yes/no",
  "text": "Ticket: people services case CR-00914\nRaised by: Dani Ishikawa\nAbout: Rafi\n\nInterview notes for Rafi (2025):\nCaseworker: Matias Wojcik, your relation to Rafi?\nMatias Wojcik: I am Rafi's uncle.\nCaseworker: Months Rafi lived with you?\nMatias Wojcik: 12 months.\nCaseworker: Annual income?\nMatias Wojcik: 72,113.66 USD.\nCaseworker: Filed a claim for Rafi?\nMatias Wojcik: yes.\nCaseworker: Farid Haddad, your relation to Rafi?\nFarid Haddad: I am Rafi's father.\nCaseworker: Months Rafi lived with you?\nFarid Haddad: 11 months.\nCaseworker: Annual income?\nFarid Haddad: $17,663.\nCaseworker: Filed a claim for Rafi?\nFarid Haddad: yes.\nCaseworker: Dmitri Dubois, your relation to Rafi?\nDmitri Dubois: I am Rafi's grandfather.\nCaseworker: Months Rafi lived with you?\nDmitri Dubois: 9 months.\nCaseworker: Annual income?\nDmitri Dubois: $88,260.\nCaseworker: Filed a claim for Rafi?\nDmitri Dubois: yes.\nCaseworker: Luka Patterson, your relation to Rafi?\nLuka Patterson: I am Rafi's uncle.\nCaseworker: Months Rafi lived with you?\nLuka Patterson: 0 months.\nCaseworker: Annual income?\nLuka Patterson: $81,821.\nCaseworker: Filed a claim for Rafi?\nLuka Patterson: yes.",
  "question": "Under these rules, is Dmitri Dubois excluded from claiming Rafi for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2025: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for larger than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Rafi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0b3d909403",
  "kind": "choice",
  "text": "Facts for Wanjiru Okoro (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | $4,968.68 |\n| net monthly income | $4,049.81 |\n| countable assets | $10,926.67 |\n| time in the service area | 5 months |\n| age | 64 years |\n| enrolled in | Kelder Veterans Pension |\n\nTicket CASE-08394\nWith: Morgan Mendoza\nAbout: Wanjiru Okoro",
  "question": "Tollsey Island Ferry Discount eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is 64 years or greater.\n- Gate B: passed when the applicant has lived in the service area for over 8 months.\n- Route: an applicant enrolled in Kelder Veterans Pension skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat does Wanjiru Okoro get from the application to Tollsey Island Ferry Discount?",
  "options": [
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "qbb75c91d48",
  "kind": "choice",
  "text": "case_id: CASE-93505\nworker_name: Kendall Umarov\nsubject_name: Imani Fujimoto\n\nFacts for Imani Fujimoto (2027):\n- gross monthly income: $1,785.80\n- net monthly income: $1,280.30\n- countable assets: $2,922.85\n- time in the service area: ten months\n- age: 23 years\n- enrolled in: Ruddock Shuttle Card",
  "question": "Corvane Transit Fare Discount eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or greater than ten months.\n- Gate B: passed when the applicant's age is greater than 60 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which outcome does the application of Imani Fujimoto to Corvane Transit Fare Discount get?",
  "options": [
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "q00470e1c80",
  "kind": "choice",
  "text": "[intake_route] case_ref=HR-84523\n[desk_note] handler=Ari Benali about=Ailsa Yilmaz\n\nFacts for Ailsa Yilmaz (2026):\n| fact | value |\n| --- | --- |\n| time employed | 78 months |\n| hours worked in the past year | 1173 hours |\n| employees at the worksite | 23 employees |\n| gross annual pay | 56,183.87 USD |\n| take-home annual pay | 47,000.01 USD |\n| enrolled in | Pellwick Bereavement Leave |",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has strictly higher than 22 employees.\n- Gate B: passed when gross annual pay is equal to or below 62,000.00 USD.\n- Gate C: passed when hours worked in the past year are greater than 1480 hours.\n- Gate D: passed when take-home annual pay is lower than or equal to 47,000.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, what decision does the application of Ailsa Yilmaz to Tovardine Seed Caregiver Leave receive?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate C is the reason (hours worked in the past year)",
   "Not eligible: Gate D is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "qd8af57370f",
  "kind": "yes/no",
  "text": "Dear colleague,\nPlease see CASE-50833 about Ilse Campbell on the queue.\nThanks, Casey Kaplan\n\nFacts for Ilse Campbell (2027):\n- gross monthly income: 4,550.03 USD\n- net monthly income: 3,897.08 USD\n- countable assets: 2,394.78 USD\n- time in the service area: 16 months\n- age: 62 years\n- enrolled in: Pellbrook Heating Grant",
  "question": "For Tarrowick Food Basket Support, does a gate that applies halt the application made by Ilse Campbell?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or greater than 10 months.\n- Gate B: passed when gross monthly income is strictly under 3,980.00 USD.\n- Gate C: passed when countable assets are strictly below the level of 3,650.00 USD.\n- Gate D: passed when the applicant's age is 57 years or more.\n- Route: an applicant enrolled in Pellbrook Heating Grant skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7504aecc37",
  "kind": "choice",
  "text": "Review desk form\nCase reference: CR-79394\nFor: Rafi\nCaseworker: Remy Tran\n\nInterview notes for Rafi (2027):\nCaseworker: Hiro Ferreira, your relation to Rafi?\nHiro Ferreira: I am Rafi's father.\nCaseworker: Months Rafi lived with you?\nHiro Ferreira: 8 months.\nCaseworker: Annual income?\nHiro Ferreira: $68,495.35.\nCaseworker: Filed a claim for Rafi?\nHiro Ferreira: yes.\nCaseworker: Esra Lehmann, your relation to Rafi?\nEsra Lehmann: I am Rafi's mother.\nCaseworker: Months Rafi lived with you?\nEsra Lehmann: 11 months.\nCaseworker: Annual income?\nEsra Lehmann: $68,495.35.\nCaseworker: Filed a claim for Rafi?\nEsra Lehmann: yes.",
  "question": "Gristmere Child Credit rules for 2027: who may claim Rafi.\n- Only one person may claim Rafi. Work through these steps in order.\n- Step one: only people who filed a claim for Rafi are considered.\n- Step two: of those, only people with whom Rafi lived for above 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Rafi lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Rafi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, is allowed to claim Rafi for Gristmere Child Credit under these rules?",
  "options": [
   "Hiro Ferreira",
   "Esra Lehmann"
  ]
 },
 {
  "qid": "qf9e871abcd",
  "kind": "choice",
  "text": "[queue_desk] case=CR-23915 staff=Toni Lazar person=Vida\n\nPeople who asked to claim Vida (2025):\n| person | relationship to Vida | months lived with Vida | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Farid Singh | uncle | 0 months | 58,876.00 USD | yes |\n| Sofia Reynolds | grandmother | 10 months | 43,978.00 USD | yes |\n| Waleed Ramirez | grandfather | 5 months | 84,027.00 USD | yes |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for 5 months at minimum in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Vida lived for more months comes first.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Vida for Tessenvale Valley Child Credit?",
  "options": [
   "Waleed Ramirez",
   "Farid Singh"
  ]
 },
 {
  "qid": "qfbbc102bd7",
  "kind": "choice",
  "text": "People who asked to claim Eva (2025), as JSON:\n{\"people\": [{\"name\": \"Tariq Haddad\", \"relationship\": \"father\", \"months_lived_with_child\": \"7 months\", \"annual_income\": \"52,489.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Jelena Lindqvist\", \"relationship\": \"mother\", \"months_lived_with_child\": \"12 months\", \"annual_income\": \"75,369.54 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Galina Ortega\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"4 months\", \"annual_income\": \"20,735.00 USD\", \"filed_a_claim\": \"no\"}, {\"name\": \"Yusuf Dragic\", \"relationship\": \"grandfather\", \"months_lived_with_child\": \"2 months\", \"annual_income\": \"35,398.00 USD\", \"filed_a_claim\": \"yes\"}]}\n\n{\"reference\": \"CR-11027\", \"caseworker\": \"Avery Obradovic\", \"about\": \"Eva\", \"office\": \"district\"}",
  "question": "Brellow Orchard Family Credit rules for 2025: who may claim Eva.\n- Only one person may claim Eva. Work through these steps in order.\n- Step one: only people who filed a claim for Eva are considered.\n- Step two: of those, only people with whom Eva lived for a minimum of 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Eva lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Eva.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Brellow Orchard Family Credit, which person, if any, gets to claim Eva under these rules?",
  "options": [
   "Nobody may claim the child",
   "Jelena Lindqvist",
   "Tariq Haddad"
  ]
 },
 {
  "qid": "qe6293fc7ae",
  "kind": "choice",
  "text": "District office intake form\nCase reference: CASE-51987\nHandled by: Kiran Morales\nAbout: Zofia Jovanovic\n\nIntake interview with Zofia Jovanovic (2027):\nCaseworker: Gross monthly income?\nZofia Jovanovic: $4,807.47.\nCaseworker: Net monthly income?\nZofia Jovanovic: $3,433.63.\nCaseworker: Countable assets?\nZofia Jovanovic: $14,607.31.\nCaseworker: Time in the service area?\nZofia Jovanovic: 20 months.\nCaseworker: Age?\nZofia Jovanovic: 24 years.\nCaseworker: Other programme enrolled in?\nZofia Jovanovic: Lowmarsh Heating Aid.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly over 12 months.\n- Gate B: passed when the applicant's age is in excess of 56 years.\n- Gate C: passed when net monthly income is strictly below $2,880.\n- Gate D: passed when countable assets are at or under the amount of $10,250.\n- Route: an applicant enrolled in Lowmarsh Heating Aid skips Gate A, Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what is the fate of the application of Zofia Jovanovic to Tamsfell Senior Home Support?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Not eligible: Gate D is the reason (countable assets)",
   "Not eligible: Gate B is the reason (age)",
   "Eligible"
  ]
 },
 {
  "qid": "qc2c7fa6d1f",
  "kind": "choice",
  "text": "Review ticket: CR-41957\nOwner: Avery Obradovic\nAbout: Nia\n\nPeople who asked to claim Nia (2026):\n| person | relationship to Nia | months lived with Nia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Ravi Okoro | grandfather | 7 months | 18,028.00 USD | yes |\n| Olena Ruiz | aunt | 5 months | 42,367.00 USD | no |",
  "question": "Ferrowby Forest Credit rules for 2026: who may claim Nia.\n- Only one person may claim Nia. Work through these steps in order.\n- Step one: only people who filed a claim for Nia are considered.\n- Step two: of those, only people with whom Nia lived for greater than or equal to 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Nia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Nia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if anyone, would be permitted to claim Nia for Ferrowby Forest Credit?",
  "options": [
   "Nobody may claim the child",
   "Olena Ruiz",
   "Ravi Okoro"
  ]
 },
 {
  "qid": "q3049e92577",
  "kind": "choice",
  "text": "{\"ref\": \"CR-04208\", \"handled_by\": \"Sami Castro\", \"about\": \"Kai\", \"setting\": \"walk-in\"}\n\nPeople who asked to claim Kai (2026), as JSON:\n{\"people\": [{\"name\": \"Ingrid Delgado\", \"relationship\": \"mother\", \"months_lived_with_child\": \"ten months\", \"annual_income\": \"57,314.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Ilse Jovanovic\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"nine months\", \"annual_income\": \"81,865.00 USD\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Nikolai Mensah\", \"relationship\": \"father\", \"months_lived_with_child\": \"twelve months\", \"annual_income\": \"25,464.00 USD\", \"filed_a_claim\": \"no\"}]}",
  "question": "Tollmere Lakeside Family Payment rules for 2026: who may claim Kai.\n- Only one person may claim Kai. Work through these steps in order.\n- Step one: only people who filed a claim for Kai are considered.\n- Step two: of those, only people with whom Kai lived for a minimum of seven months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kai lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kai.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if anyone, may claim Kai for Tollmere Lakeside Family Payment?",
  "options": [
   "Ingrid Delgado",
   "Ilse Jovanovic",
   "Nikolai Mensah"
  ]
 },
 {
  "qid": "qd199baf9ec",
  "kind": "yes/no",
  "text": "Hello there,\nThanks for calling about Priya Dlamini; the reference is HR-03377.\nKind regards, Casey Kaplan\n\nFacts for Priya Dlamini (2027):\n- time employed: 31 months\n- hours worked in the past year: 1,241 hours\n- employees at the worksite: 28 employees\n- gross annual pay: 63,499.99 USD\n- take-home annual pay: 61,502.74 USD\n- enrolled in: Caddowen Veterans Pathway",
  "question": "According to these rules, does Priya Dlamini fail to qualify for Morrowdene Hospital Group Return Support?",
  "definitions": "Morrowdene Hospital Group Return Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are strictly greater than 1,240 hours.\n- Gate B: passed when take-home annual pay is at or less than $45,000.\n- Gate C: passed when gross annual pay is strictly under the amount of $63,500.\n- Gate D: passed when the worksite has equal to or greater than 63 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q3731783fdc",
  "kind": "choice",
  "text": "Intake header\nRef: CR-22388\nHandler: Teo Quintero\nAbout: Zara\n\nInterview notes for Zara (2027):\nCaseworker: Jiro Dragic, your relation to Zara?\nJiro Dragic: I am Zara's father.\nCaseworker: Months Zara lived with you?\nJiro Dragic: 0 months.\nCaseworker: Annual income?\nJiro Dragic: $65,312.\nCaseworker: Filed a claim for Zara?\nJiro Dragic: yes.\nCaseworker: Xenia Hoffman, your relation to Zara?\nXenia Hoffman: I am Zara's mother.\nCaseworker: Months Zara lived with you?\nXenia Hoffman: 0 months.\nCaseworker: Annual income?\nXenia Hoffman: $72,235.\nCaseworker: Filed a claim for Zara?\nXenia Hoffman: yes.\nCaseworker: Imani Okafor, your relation to Zara?\nImani Okafor: I am Zara's aunt.\nCaseworker: Months Zara lived with you?\nImani Okafor: 1 month.\nCaseworker: Annual income?\nImani Okafor: 56,596.48 USD.\nCaseworker: Filed a claim for Zara?\nImani Okafor: yes.\nCaseworker: Yasmin Delgado, your relation to Zara?\nYasmin Delgado: I am Zara's aunt.\nCaseworker: Months Zara lived with you?\nYasmin Delgado: 4 months.\nCaseworker: Annual income?\nYasmin Delgado: $79,287.\nCaseworker: Filed a claim for Zara?\nYasmin Delgado: yes.",
  "question": "Sallowmere Family Payment rules for 2027: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for at or over 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Zara lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if anyone, gets to claim Zara for Sallowmere Family Payment?",
  "options": [
   "Yasmin Delgado",
   "Xenia Hoffman",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "qf10d9420b7",
  "kind": "choice",
  "text": "Staff support desk ticket: CASE-63390\nLogged by: Ezra Rosales\nRegarding: Dagny Ortega\n\nFacts for Dagny Ortega (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | 3,016.51 USD |\n| net monthly income | 2,673.28 USD |\n| countable assets | 5,799.31 USD |\n| time in the service area | 1 month |\n| age | 36 years |\n| enrolled in | Corrivale Meal Voucher |",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for at or beyond 3 months.\n- Gate B: passed when countable assets are strictly lower than $5,350.\n- Gate C: passed when gross monthly income is at or less than $3,470.\n- Route: an applicant enrolled in Corrivale Meal Voucher skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tesslow Prairie Water Bill Assistance, which outcome does the application of Dagny Ortega get?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (gross monthly income)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Not eligible: Gate A is the reason (time in the service area)"
  ]
 },
 {
  "qid": "qf4ba4c6d88",
  "kind": "yes/no",
  "text": "Facts for Bianca Anderson (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,743.72 USD |\n| net monthly income | 1,969.71 USD |\n| countable assets | 4,650.00 USD |\n| time in the service area | 2 months |\n| age | 49 years |\n| enrolled in | Velden Transit Pass |\n\nCase note: CASE-91786 for Bianca Anderson. Handled by Remy Tran.",
  "question": "Does Bianca Anderson fail to qualify for Sallowick Ward Home Repair Grant on these rules?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than 4 months.\n- Gate B: passed when countable assets are strictly under 4,650.00 USD.\n- Gate C: passed when gross monthly income is strictly under 3,635.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0783348b3e",
  "kind": "yes/no",
  "text": "Hi team,\nCase CASE-53402 for Emi Tanaka has gone to the desk.\nThanks, Jamie Jorgensen\n\nFacts for Emi Tanaka (2026):\n- gross monthly income: $2,595\n- net monthly income: 2,063.59 USD\n- countable assets: 10,549.99 USD\n- time in the service area: 11 months\n- age: 32 years\n- enrolled in: Stennet Commuter Pass",
  "question": "Is Emi Tanaka eligible for Corvane Transit Fare Discount by passing every gate that applies?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly smaller than 10,549.99 USD.\n- Gate B: passed when the applicant has lived in the service area for equal to or above 10 months.\n- Gate C: passed when gross monthly income is equal to or below $2,595.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q9068d9f536",
  "kind": "yes/no",
  "text": "Case file intake form\nCase reference: CASE-61329\nCaseworker: Toni Lazar\nAbout: Jiro Delgado\n\nIntake interview with Jiro Delgado (2027):\nCaseworker: Gross monthly income?\nJiro Delgado: $5,333.\nCaseworker: Net monthly income?\nJiro Delgado: $4,049.81.\nCaseworker: Countable assets?\nJiro Delgado: $1,017.86.\nCaseworker: Time in the service area?\nJiro Delgado: 15 months.\nCaseworker: Age?\nJiro Delgado: 26 years.\nCaseworker: Other programme enrolled in?\nJiro Delgado: Quenmoor Emergency Loan.",
  "question": "Does Jiro Delgado fail to qualify for Ostermere Delta Flood Repair Support under these rules?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than 11 months.\n- Gate B: passed when net monthly income is $3,185 or lower.\n- Route: an applicant enrolled in Kelmstone Drainage Subsidy skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe17b2d6c9b",
  "kind": "yes/no",
  "text": "Dear colleague,\nThe record CASE-46244 for Juliana Becker has been sent to the front counter.\nRegards, Casey Kaplan\n\nIntake interview with Juliana Becker (2027):\nCaseworker: Gross monthly income?\nJuliana Becker: $2,468.50.\nCaseworker: Net monthly income?\nJuliana Becker: $2,012.58.\nCaseworker: Countable assets?\nJuliana Becker: $1,366.71.\nCaseworker: Time in the service area?\nJuliana Becker: 7 months.\nCaseworker: Age?\nJuliana Becker: 58 years.\nCaseworker: Other programme enrolled in?\nJuliana Becker: Quarrowdale Food Parcel.",
  "question": "According to these rules, does Juliana Becker fail to qualify for Fennick School Meal Supplement?",
  "definitions": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for higher than 6 months.\n- Gate B: passed when the applicant's age is equal to or greater than 58 years.\n- Gate C: passed when countable assets are strictly beneath the level of $2,200.00.\n- Gate D: passed when net monthly income is strictly lower than $2,185.00.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qadc63a0245",
  "kind": "choice",
  "text": "{\"about\": \"Nika Ferreira\", \"case\": \"CASE-98161\", \"caseworker\": \"Sami Castro\", \"team\": \"help line\"}\n\nIntake interview with Nika Ferreira (2025):\nCaseworker: Gross monthly income?\nNika Ferreira: 4,799.49 USD.\nCaseworker: Net monthly income?\nNika Ferreira: 3,633.95 USD.\nCaseworker: Countable assets?\nNika Ferreira: 13,217.63 USD.\nCaseworker: Time in the service area?\nNika Ferreira: ten months.\nCaseworker: Age?\nNika Ferreira: nineteen years.\nCaseworker: Other programme enrolled in?\nNika Ferreira: Aldervale Meal Basket.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or above nine months.\n- Gate B: passed when the applicant's age is at or over 63 years.\n- Gate C: passed when net monthly income is strictly below 2,580.00 USD.\n- Gate D: passed when gross monthly income is strictly smaller than 3,410.00 USD.\n- Route: an applicant enrolled in Aldervale Meal Basket skips Gate B, Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Tamsfell Senior Home Support, which outcome does the application submitted by Nika Ferreira get?",
  "options": [
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate C is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate D is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q281cc1e278",
  "kind": "choice",
  "text": "Facts for Ilse Schultz (2025):\n| fact | value |\n| --- | --- |\n| gross monthly income | 1,063.13 USD |\n| net monthly income | 771.46 USD |\n| countable assets | $8,350 |\n| time in the service area | 11 months |\n| age | 49 years |\n| enrolled in | Ketteridge Veterans Scheme |\n\nfile: CASE-07197\nsupport: Kazu Yousef\nabout: Ilse Schultz\nmood: kind",
  "question": "Sallowick Ward Home Repair Grant eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or below the level of $8,350.\n- Gate B: passed when the applicant's age is at or above 56 years.\n- Gate C: passed when the applicant has lived in the service area for a minimum of 11 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Ilse Schultz to Sallowick Ward Home Repair Grant get?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Eligible",
   "Not eligible: Gate A is the reason (countable assets)",
   "Not eligible: Gate C is the reason (time in the service area)"
  ]
 },
 {
  "qid": "q301d43dac8",
  "kind": "choice",
  "text": "Hi team,\nThanks for waiting, HR-69097 about Mirela Begum is in good hands.\nWarm wishes, Tomi Eklund\n\nFacts for Mirela Begum (2025):\n- time employed: 17 months\n- hours worked in the past year: 850 hours\n- employees at the worksite: 69 employees\n- gross annual pay: $88,905.78\n- take-home annual pay: $63,500.00\n- enrolled in: none",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than or equal to $63,500.\n- Gate B: passed when hours worked in the past year are greater than or equal to 850 hours.\n- Gate C: passed when the applicant has been employed for strictly greater than 11 months.\n- Route: an applicant enrolled in Fallowden Retraining Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Mirela Begum on the application to Tovardine Seed Caregiver Leave?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (time employed)"
  ]
 },
 {
  "qid": "qadb1e8bcda",
  "kind": "choice",
  "text": "Internal case note for CR-38582.\nSet down by Avery Obradovic at the town hall office, for Ami.\n\nPeople who asked to claim Ami (2025):\n- Xavier Dlamini: relationship to Ami: father; months lived with Ami: 9 months; annual income: 40,128.00 USD; filed a claim: no\n- Freya Sharma: relationship to Ami: mother; months lived with Ami: 3 months; annual income: 63,923.77 USD; filed a claim: yes\n- Nkechi Lindqvist: relationship to Ami: grandmother; months lived with Ami: 3 months; annual income: 45,509.91 USD; filed a claim: yes\n- Anjali Sokolov: relationship to Ami: grandmother; months lived with Ami: 9 months; annual income: 49,483.00 USD; filed a claim: yes",
  "question": "Tollmere Lakeside Family Payment rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for a minimum of 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Ami for Tollmere Lakeside Family Payment, who is it?",
  "options": [
   "Freya Sharma",
   "Anjali Sokolov",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q4c8688f520",
  "kind": "yes/no",
  "text": "Support hub form\nCase reference: CR-54672\nCaseworker: Jamie Jorgensen\nSubject: Pia\n\nInterview notes for Pia (2025):\nCaseworker: Sofia Dlamini, your relation to Pia?\nSofia Dlamini: I am Pia's mother.\nCaseworker: Months Pia lived with you?\nSofia Dlamini: twelve months.\nCaseworker: Annual income?\nSofia Dlamini: 45,456.56 USD.\nCaseworker: Filed a claim for Pia?\nSofia Dlamini: yes.\nCaseworker: Matias Fujimoto, your relation to Pia?\nMatias Fujimoto: I am Pia's grandfather.\nCaseworker: Months Pia lived with you?\nMatias Fujimoto: seven months.\nCaseworker: Annual income?\nMatias Fujimoto: 49,185.00 USD.\nCaseworker: Filed a claim for Pia?\nMatias Fujimoto: yes.\nCaseworker: Oskar Russell, your relation to Pia?\nOskar Russell: I am Pia's father.\nCaseworker: Months Pia lived with you?\nOskar Russell: ten months.\nCaseworker: Annual income?\nOskar Russell: 52,276.00 USD.\nCaseworker: Filed a claim for Pia?\nOskar Russell: yes.",
  "question": "Going by the listed rules, is it true that Oskar Russell may not claim Pia for Gristmere Child Credit?",
  "definitions": "Gristmere Child Credit rules for 2025: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for strictly above seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Pia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa0fa3bc3f2",
  "kind": "choice",
  "text": "Case note: Casey Kaplan holds case file CR-48663 about Elif. The record sits at the town hall desk.\n\nPeople who asked to claim Elif (2027):\n- Kenji Kovacs: relationship to Elif: uncle; months lived with Elif: five months; annual income: $64,126.79; filed a claim: no\n- Nadia Gashi: relationship to Elif: grandmother; months lived with Elif: five months; annual income: $31,180; filed a claim: no\n- Juliana Halvorsen: relationship to Elif: aunt; months lived with Elif: three months; annual income: $49,991; filed a claim: no\n- Ingrid Sullivan: relationship to Elif: grandmother; months lived with Elif: eleven months; annual income: $23,968; filed a claim: no",
  "question": "Ostrowan Prairie Grant rules for 2027: who may claim Elif.\n- Only one person may claim Elif. Work through these steps in order.\n- Step one: only people who filed a claim for Elif are considered.\n- Step two: of those, only people with whom Elif lived for at or greater than five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Elif lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Elif.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Elif for Ostrowan Prairie Grant?",
  "options": [
   "Nobody may claim the child",
   "Kenji Kovacs",
   "Ingrid Sullivan"
  ]
 },
 {
  "qid": "qfe1eb6ace7",
  "kind": "choice",
  "text": "Counter ticket: CR-45907\nRaised by: Toni Lazar\nAbout: Ezra\n\nPeople who asked to claim Ezra (2027):\n| person | relationship to Ezra | months lived with Ezra | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Nikolai Ueda | uncle | ten months | $49,046.00 | no |\n| Hiroko Nakamura | mother | eight months | $21,720.00 | yes |",
  "question": "Dunmarrow Hill Allowance rules for 2027: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for strictly greater than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ezra lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which person, if any, gets to claim Ezra for Dunmarrow Hill Allowance?",
  "options": [
   "Nikolai Ueda",
   "Hiroko Nakamura",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q1a478b1382",
  "kind": "choice",
  "text": "Hi team,\nThanks for waiting, CASE-11244 about Esra Iyer is in good hands.\nWarm wishes, Jamie Jorgensen\n\nFacts for Esra Iyer (2025):\n- gross monthly income: 3,544.99 USD\n- net monthly income: 3,333.43 USD\n- countable assets: 5,659.04 USD\n- time in the service area: 30 months\n- age: 25 years\n- enrolled in: none",
  "question": "Tesslow Prairie Water Bill Assistance eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly below $3,545.\n- Gate B: passed when net monthly income is smaller than $2,810.\n- Route: an applicant enrolled in Sorrenby Tenancy Deposit Loan skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, where does the application of Esra Iyer to Tesslow Prairie Water Bill Assistance land?",
  "options": [
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible",
   "Not eligible: Gate B is the reason (net monthly income)"
  ]
 },
 {
  "qid": "qa72da0c04a",
  "kind": "yes/no",
  "text": "Facts for Kazu Singh (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,858.29 |\n| net monthly income | $2,277.65 |\n| countable assets | $12,521.47 |\n| time in the service area | 12 months |\n| age | 89 years |\n| enrolled in | Ketteridge Veterans Charter |\n\n[branch_queue] case=CASE-91383 by=Jamie Jorgensen about=Kazu Singh",
  "question": "Under these rules, is it not true that Kazu Singh is not eligible for Sallowick Ward Home Repair Grant?",
  "definitions": "Sallowick Ward Home Repair Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is strictly above 55 years.\n- Gate B: passed when the applicant has lived in the service area for 12 months or more.\n- Gate C: passed when gross monthly income is strictly smaller than $2,395.00.\n- Route: an applicant enrolled in Ketteridge Veterans Scheme skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd2e27d4a87",
  "kind": "choice",
  "text": "Review desk form\nCase reference: CR-38582\nFor: Ami\nCaseworker: Avery Obradovic\n\nPeople who asked to claim Ami (2025):\n| person | relationship to Ami | months lived with Ami | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Xavier Dlamini | father | 9 months | 40,128.00 USD | no |\n| Freya Sharma | mother | 5 months | 63,923.77 USD | yes |\n| Nkechi Lindqvist | grandmother | 3 months | 45,509.91 USD | yes |\n| Anjali Sokolov | grandmother | 9 months | 49,483.00 USD | yes |",
  "question": "Tollmere Lakeside Family Payment rules for 2025: who may claim Ami.\n- Only one person may claim Ami. Work through these steps in order.\n- Step one: only people who filed a claim for Ami are considered.\n- Step two: of those, only people with whom Ami lived for a minimum of 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ami lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ami.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Ami for Tollmere Lakeside Family Payment, who is it?",
  "options": [
   "Anjali Sokolov",
   "Freya Sharma",
   "Nobody may claim the child"
  ]
 },
 {
  "qid": "q289e453a4c",
  "kind": "yes/no",
  "text": "Internal note: Quinn Pavlenko looks after case CASE-55272 in the regional service team, about Jakub Abebe.\n\nFacts for Jakub Abebe (2026):\n- gross monthly income: 2,420.91 USD\n- net monthly income: 2,175.00 USD\n- countable assets: 3,213.44 USD\n- time in the service area: 10 months\n- age: 62 years\n- enrolled in: Tallow Ridge Commuter Permit",
  "question": "Does Jakub Abebe meet the rules for Sennamoor River Rent Support by passing every gate that applies?",
  "definitions": "Sennamoor River Rent Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly in excess of 10 months.\n- Gate B: passed when net monthly income is at or below 2,175.00 USD.\n- Route: an applicant enrolled in Ambermoor Water Rebate skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa3c048d5ed",
  "kind": "choice",
  "text": "Riley Watanabe: back office log for CR-34362, a plain entry about Sora.\n\nInterview notes for Sora (2026):\nCaseworker: Yara Robinson, your relation to Sora?\nYara Robinson: I am Sora's mother.\nCaseworker: Months Sora lived with you?\nYara Robinson: 3 months.\nCaseworker: Annual income?\nYara Robinson: 68,194.00 USD.\nCaseworker: Filed a claim for Sora?\nYara Robinson: yes.\nCaseworker: Hiro Dubois, your relation to Sora?\nHiro Dubois: I am Sora's father.\nCaseworker: Months Sora lived with you?\nHiro Dubois: 3 months.\nCaseworker: Annual income?\nHiro Dubois: 36,139.08 USD.\nCaseworker: Filed a claim for Sora?\nHiro Dubois: no.\nCaseworker: Tomas Douglas, your relation to Sora?\nTomas Douglas: I am Sora's grandfather.\nCaseworker: Months Sora lived with you?\nTomas Douglas: 12 months.\nCaseworker: Annual income?\nTomas Douglas: 25,400.13 USD.\nCaseworker: Filed a claim for Sora?\nTomas Douglas: yes.",
  "question": "Gristmere Child Credit rules for 2026: who may claim Sora.\n- Only one person may claim Sora. Work through these steps in order.\n- Step one: only people who filed a claim for Sora are considered.\n- Step two: of those, only people with whom Sora lived for greater than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Sora lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Sora.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich person, if any, is the sole person who may claim Sora for Gristmere Child Credit under these rules?",
  "options": [
   "Yara Robinson",
   "Tomas Douglas"
  ]
 },
 {
  "qid": "q344ed1c054",
  "kind": "choice",
  "text": "Facts for Hamid Delgado (2027):\n| fact | value |\n| --- | --- |\n| gross monthly income | 2,828.86 USD |\n| net monthly income | 1,829.06 USD |\n| countable assets | 5,984.04 USD |\n| time in the service area | 54 months |\n| age | 42 years |\n| enrolled in | Tessaly Housing Levy |\n\nDear colleague,\nThis is a short outreach note on case CASE-31006 for Hamid Delgado.\nRegards, Sasha Okonkwo",
  "question": "Wyndholm Forest Fuel Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly smaller than 3,710.00 USD.\n- Gate B: passed when the applicant's age is strictly more than 63 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hamid Delgado to Wyndholm Forest Fuel Support lead to?",
  "options": [
   "Not eligible: Gate B is the reason (age)",
   "Not eligible: Gate A is the reason (gross monthly income)",
   "Eligible"
  ]
 },
 {
  "qid": "q61e7fe5a70",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CR-21117, handled by Mika Zamora\n[subject_line] Liam is at the heart of it\n\nPeople who asked to claim Liam (2025):\n| person | relationship to Liam | months lived with Liam | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hamid Sullivan | father | 12 months | 77,719.94 USD | no |\n| Galina Becker | aunt | 8 months | 15,880.00 USD | yes |\n| Yara Douglas | aunt | 12 months | 54,991.85 USD | no |\n| Gustav Gordon | grandfather | 6 months | 30,293.55 USD | yes |",
  "question": "According to these rules, is Galina Becker the person who ends up with the right to claim Liam for Tessenvale Valley Child Credit?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Liam.\n- Only one person may claim Liam. Work through these steps in order.\n- Step one: only people who filed a claim for Liam are considered.\n- Step two: of those, only people with whom Liam lived for strictly higher than 7 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Liam lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Liam.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q144de4c9e8",
  "kind": "yes/no",
  "text": "Facts for Ibrahim Patterson (2026), as JSON:\n{\"gross_monthly_income\": \"3,829.99 USD\", \"net_monthly_income\": \"2,408.50 USD\", \"countable_assets\": \"5,011.87 USD\", \"time_in_the_service_area\": \"26 months\", \"age\": \"37 years\", \"enrolled_in\": \"Ellisford Winter Supplement\"}\n\n{\"caseworker\": \"Jules Shrestha\", \"about\": \"Ibrahim Patterson\", \"case\": \"CASE-23455\", \"desk\": \"community\"}",
  "question": "Does Ibrahim Patterson fail to qualify for admission to Wyndholm Forest Fuel Support?",
  "definitions": "Wyndholm Forest Fuel Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $8,350 or less.\n- Gate B: passed when gross monthly income is strictly under $3,830.\n- Gate C: passed when the applicant's age is strictly more than 36 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qd55730e828",
  "kind": "choice",
  "text": "Back office note: Morgan Mendoza is moving case CR-61745 for Ali.\n\nInterview notes for Ali (2026):\nCaseworker: Idris Nilsen, your relation to Ali?\nIdris Nilsen: I am Ali's uncle.\nCaseworker: Months Ali lived with you?\nIdris Nilsen: 2 months.\nCaseworker: Annual income?\nIdris Nilsen: $66,090.\nCaseworker: Filed a claim for Ali?\nIdris Nilsen: yes.\nCaseworker: Hugo Begum, your relation to Ali?\nHugo Begum: I am Ali's father.\nCaseworker: Months Ali lived with you?\nHugo Begum: 7 months.\nCaseworker: Annual income?\nHugo Begum: 28,405.64 USD.\nCaseworker: Filed a claim for Ali?\nHugo Begum: yes.\nCaseworker: Greta Gallegos, your relation to Ali?\nGreta Gallegos: I am Ali's mother.\nCaseworker: Months Ali lived with you?\nGreta Gallegos: 4 months.\nCaseworker: Annual income?\nGreta Gallegos: 67,543.10 USD.\nCaseworker: Filed a claim for Ali?\nGreta Gallegos: no.",
  "question": "Kelmstone Mountain Family Grant rules for 2026: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for equal to or greater than 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ali lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFor Kelmstone Mountain Family Grant, which person, if any, gets the right to claim Ali?",
  "options": [
   "Greta Gallegos",
   "Idris Nilsen",
   "Hugo Begum"
  ]
 },
 {
  "qid": "qba576226b5",
  "kind": "yes/no",
  "text": "Regional service office intake\nCase reference: HR-00259\nCaseworker: Ren Dvorak\nSubject: Ivo Petrov\n\nIntake interview with Ivo Petrov (2025):\nCaseworker: Time employed?\nIvo Petrov: 65 months.\nCaseworker: Hours worked in the past year?\nIvo Petrov: 737 hours.\nCaseworker: Employees at your worksite?\nIvo Petrov: 72 employees.\nCaseworker: Gross annual pay?\nIvo Petrov: $87,861.70.\nCaseworker: Take-home annual pay?\nIvo Petrov: $75,933.62.\nCaseworker: Other programme enrolled in?\nIvo Petrov: Heldane Transit Pass.",
  "question": "Under these rules, does a gate that applies end the application of Ivo Petrov to Quenhollow Brewery Bereavement Leave?",
  "definitions": "Quenhollow Brewery Bereavement Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is at or under the amount of $60,500.00.\n- Gate B: passed when the worksite has equal to or above 72 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe73fe95d7c",
  "kind": "yes/no",
  "text": "Dear colleague,\nPlease see HR-04711 about Freya Demir on the queue.\nThanks, Sasha Okonkwo\n\nFacts for Freya Demir (2027):\n- time employed: 41 months\n- hours worked in the past year: 2,115 hours\n- employees at the worksite: 178 employees\n- gross annual pay: 61,499.99 USD\n- take-home annual pay: 52,000.00 USD\n- enrolled in: Corrivale Welding Bursary",
  "question": "Under these rules, is Freya Demir plainly not eligible for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than 52,000.00 USD.\n- Gate B: passed when gross annual pay is at or below the level of 61,500.00 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 }
]
