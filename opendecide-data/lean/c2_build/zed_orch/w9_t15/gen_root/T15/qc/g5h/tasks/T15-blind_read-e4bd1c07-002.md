# G5-H blind read T15-blind_read-e4bd1c07-002 (family T15)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/zed_orch/w9_t15/gen_root/T15/qc/g5h/answers/T15-blind_read-e4bd1c07-002.json

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
  "qid": "q3465589d29",
  "kind": "choice",
  "text": "[casework_team] case_id=HR-92047\n[casework_team] worker=Casey Kaplan about=Lior Hudson\n\nFacts for Lior Hudson (2026):\n| fact | value |\n| --- | --- |\n| time employed | 34 months |\n| hours worked in the past year | 2170 hours |\n| employees at the worksite | 53 employees |\n| gross annual pay | 82,561.33 USD |\n| take-home annual pay | 67,201.26 USD |\n| enrolled in | Idrane Tuition Grant |",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for higher than 22 months.\n- Gate B: passed when gross annual pay is 82,561.34 USD or under.\n- Gate C: passed when the worksite has at or beyond 54 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat comes of the application of Lior Hudson to Wendmoor Mill Parental Leave?",
  "options": [
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Eligible",
   "Not eligible: Gate A is the reason (time employed)"
  ]
 },
 {
  "qid": "q23ae1badab",
  "kind": "yes/no",
  "text": "reference: HR-41566\nhandler: Kendall Umarov\nsubject: Kiran Kovacs\n\nFacts for Kiran Kovacs (2027):\n- time employed: 111 months\n- hours worked in the past year: 1,945 hours\n- employees at the worksite: 226 employees\n- gross annual pay: 62,175.28 USD\n- take-home annual pay: 30,666.09 USD\n- enrolled in: Quillmere Apprentice Pilot",
  "question": "Under these rules, does Kiran Kovacs fail to qualify for Halvorne Shipyard Tuition Assistance?",
  "definitions": "Halvorne Shipyard Tuition Assistance eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of 62,175.29 USD.\n- Gate B: passed when take-home annual pay is equal to or below 45,273.69 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q48dc394f79",
  "kind": "yes/no",
  "text": "case: CASE-28730\nhub: support\ncaseworker: Remy Tran\nabout: Ari Hamilton\n\nFacts for Ari Hamilton (2025):\n- gross monthly income: 4,833.78 USD\n- net monthly income: 3,567.54 USD\n- countable assets: 7,384.70 USD\n- time in the service area: thirteen months\n- age: 59 years\n- enrolled in: Crannock Food Pantry",
  "question": "According to these rules, does Ari Hamilton qualify for Ostmere Lakeside Winter Energy Support?",
  "definitions": "Ostmere Lakeside Winter Energy Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is larger than 57 years.\n- Gate B: passed when countable assets are at or below 9,451.98 USD.\n- Route: an applicant enrolled in Crannock Food Pantry skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5de9a38626",
  "kind": "yes/no",
  "text": "Dear colleague,\nThe record CR-72853 for Joon has been sent to the front counter.\nRegards, Kazu Yousef\n\nInterview notes for Joon (2027):\nCaseworker: Fatima Kaur, your relation to Joon?\nFatima Kaur: I am Joon's mother.\nCaseworker: Months Joon lived with you?\nFatima Kaur: five months.\nCaseworker: Annual income?\nFatima Kaur: $16,997.\nCaseworker: Filed a claim for Joon?\nFatima Kaur: yes.\nCaseworker: Hiro Vasquez, your relation to Joon?\nHiro Vasquez: I am Joon's uncle.\nCaseworker: Months Joon lived with you?\nHiro Vasquez: six months.\nCaseworker: Annual income?\nHiro Vasquez: $16,997.\nCaseworker: Filed a claim for Joon?\nHiro Vasquez: yes.\nCaseworker: Jakub Tesfaye, your relation to Joon?\nJakub Tesfaye: I am Joon's grandfather.\nCaseworker: Months Joon lived with you?\nJakub Tesfaye: nine months.\nCaseworker: Annual income?\nJakub Tesfaye: $31,337.90.\nCaseworker: Filed a claim for Joon?\nJakub Tesfaye: no.",
  "question": "According to these rules, does Jakub Tesfaye fail to earn a claim on Joon for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2027: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for in excess of five months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Joon lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q77e8a7b578",
  "kind": "yes/no",
  "text": "{\"caseworker\": \"Quinn Pavlenko\", \"case\": \"CR-36477\", \"about\": \"Joon\", \"hub\": \"support\"}\n\nPeople who asked to claim Joon (2025), as JSON:\n{\"people\": [{\"name\": \"Nikolai Choi\", \"relationship\": \"father\", \"months_lived_with_child\": \"seven months\", \"annual_income\": \"$17,175.29\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Leila Choi\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"eleven months\", \"annual_income\": \"$16,107.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Priya Robinson\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"twelve months\", \"annual_income\": \"$83,545.00\", \"filed_a_claim\": \"no\"}]}",
  "question": "According to these rules, will the right to claim Joon for Kelvery Market Credit go to a different person from Priya Robinson, or stay unclaimed?",
  "definitions": "Kelvery Market Credit rules for 2025: who may claim Joon.\n- Only one person may claim Joon. Work through these steps in order.\n- Step one: only people who filed a claim for Joon are considered.\n- Step two: of those, only people with whom Joon lived for a minimum of seven months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Joon lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Joon.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7b21c45ab6",
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
  "qid": "q13a21a4766",
  "kind": "yes/no",
  "text": "Ticket: casework note for case CASE-45697\nRaised by: Ezra Rosales\nAbout: Gabriel Becker\n\nFacts for Gabriel Becker (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $2,347.47 |\n| net monthly income | $1,517.60 |\n| countable assets | $5,719.34 |\n| time in the service area | five months |\n| age | 33 years |\n| enrolled in | Velgate Pantry Voucher |",
  "question": "Under these rules, does a gate that applies end the application of Gabriel Becker to Corrivale Valley Childcare Grant?",
  "definitions": "Corrivale Valley Childcare Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for larger than five months.\n- Gate B: passed when countable assets are equal to or below $8,163.49.\n- Gate C: passed when the applicant's age is over 60 years.\n- Gate D: passed when gross monthly income is strictly below the amount of $2,347.48.\n- Route: an applicant enrolled in Velgate Pantry Voucher skips Gate C and Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qf62e6e8d90",
  "kind": "choice",
  "text": "{\"case\": \"CASE-15187\", \"caseworker\": \"Morgan Mendoza\", \"about\": \"Sofia Lehmann\"}\n\nIntake interview with Sofia Lehmann (2025):\nCaseworker: Gross monthly income?\nSofia Lehmann: 5,174.77 USD.\nCaseworker: Net monthly income?\nSofia Lehmann: 4,051.21 USD.\nCaseworker: Countable assets?\nSofia Lehmann: 7,972.40 USD.\nCaseworker: Time in the service area?\nSofia Lehmann: 7 months.\nCaseworker: Age?\nSofia Lehmann: 69 years.\nCaseworker: Other programme enrolled in?\nSofia Lehmann: Lowmarsh Heating Aid.",
  "question": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are strictly below 7,972.40 USD.\n- Gate B: passed when the applicant has lived in the service area for above 3 months.\n- Gate C: passed when the applicant's age is over 58 years.\n- Route: an applicant enrolled in Brindlemoor Repair Fund skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Sofia Lehmann to Tamsfell Senior Home Support receive?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (countable assets)",
   "Eligible"
  ]
 },
 {
  "qid": "q6d2bd8e5db",
  "kind": "yes/no",
  "text": "[hello_intake] welcome to file CASE-35915, handled by Quinn Pavlenko\n[subject_line] Priya Mensah is at the heart of it\n\nFacts for Priya Mensah (2026):\n| fact | value |\n| --- | --- |\n| gross monthly income | $927.52 |\n| net monthly income | $711.89 |\n| countable assets | $6,970.43 |\n| time in the service area | 35 months |\n| age | 85 years |\n| enrolled in | none |",
  "question": "Does a gate that applies halt the application of Priya Mensah to Corvane Transit Fare Discount?",
  "definitions": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is a minimum of 67 years.\n- Gate B: passed when gross monthly income is strictly beneath the level of $1,938.19.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q84bb52b2e3",
  "kind": "choice",
  "text": "{\"case\": \"CR-01075\", \"caseworker\": \"Ezra Rosales\", \"about\": \"Kira\", \"team\": \"casework\"}\n\nPeople who asked to claim Kira (2026), as JSON:\n{\"people\": [{\"name\": \"Olena Murphy\", \"relationship\": \"mother\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"$27,417.00\", \"filed_a_claim\": \"yes\"}, {\"name\": \"Hana Sokolov\", \"relationship\": \"aunt\", \"months_lived_with_child\": \"10 months\", \"annual_income\": \"$19,986.00\", \"filed_a_claim\": \"no\"}, {\"name\": \"Juliana Dragic\", \"relationship\": \"grandmother\", \"months_lived_with_child\": \"8 months\", \"annual_income\": \"$52,256.00\", \"filed_a_claim\": \"yes\"}]}",
  "question": "Corrowby Family Supplement rules for 2026: who may claim Kira.\n- Only one person may claim Kira. Work through these steps in order.\n- Step one: only people who filed a claim for Kira are considered.\n- Step two: of those, only people with whom Kira lived for 5 months at minimum in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Kira lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Kira.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is allowed to claim Kira for Corrowby Family Supplement?",
  "options": [
   "Juliana Dragic",
   "Hana Sokolov",
   "Olena Murphy"
  ]
 },
 {
  "qid": "qac66d4f2c4",
  "kind": "choice",
  "text": "reference: HR-75056\ncaseworker: Kendall Umarov\nabout: Hiro Halvorsen\ntone: warm\n\nFacts for Hiro Halvorsen (2026):\n- time employed: 81 months\n- hours worked in the past year: 657 hours\n- employees at the worksite: 62 employees\n- gross annual pay: $55,906.77\n- take-home annual pay: $36,646.62\n- enrolled in: Selwick Fresh Crate",
  "question": "Marrowby Bakery Family Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has 51 employees or greater.\n- Gate B: passed when hours worked in the past year are strictly greater than 740 hours.\n- Gate C: passed when gross annual pay is strictly beneath the level of $66,614.72.\n- Route: an applicant enrolled in Selwick Fresh Box skips Gate B and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Hiro Halvorsen to Marrowby Bakery Family Leave get?",
  "options": [
   "Not eligible: Gate A is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "q9f623490aa",
  "kind": "choice",
  "text": "Quinn Pavlenko: outreach list has CASE-83485 for Bruno Kimura.\n\nIntake interview with Bruno Kimura (2027):\nCaseworker: Gross monthly income?\nBruno Kimura: $2,451.14.\nCaseworker: Net monthly income?\nBruno Kimura: $2,062.35.\nCaseworker: Countable assets?\nBruno Kimura: $2,187.14.\nCaseworker: Time in the service area?\nBruno Kimura: 11 months.\nCaseworker: Age?\nBruno Kimura: 74 years.\nCaseworker: Other programme enrolled in?\nBruno Kimura: Ormsby Housing Aid.",
  "question": "Fennick School Meal Supplement eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant's age is greater than 56 years.\n- Gate B: passed when the applicant has lived in the service area for 7 months or greater.\n- Gate C: passed when gross monthly income is at or below the level of $2,451.13.\n- Gate D: passed when net monthly income is $1,971.14 at the most.\n- Route: an applicant enrolled in Ormsby Housing Aid skips Gate D; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Bruno Kimura to Fennick School Meal Supplement receive?",
  "options": [
   "Not eligible: Gate B is the reason (time in the service area)",
   "Not eligible: Gate A is the reason (age)",
   "Not eligible: Gate D is the reason (net monthly income)",
   "Eligible",
   "Not eligible: Gate C is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "qdc27b1ac74",
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
  "qid": "q5d3807f4f5",
  "kind": "choice",
  "text": "Mika Zamora: HR-38235 is up on the desk, about Ren Kovacs.\n\nIntake interview with Ren Kovacs (2027):\nCaseworker: Time employed?\nRen Kovacs: 42 months.\nCaseworker: Hours worked in the past year?\nRen Kovacs: 1,397 hours.\nCaseworker: Employees at your worksite?\nRen Kovacs: 132 employees.\nCaseworker: Gross annual pay?\nRen Kovacs: 54,048.22 USD.\nCaseworker: Take-home annual pay?\nRen Kovacs: 45,612.81 USD.\nCaseworker: Other programme enrolled in?\nRen Kovacs: Yeldham Retirement Bonus.",
  "question": "Quenhollow Brewery Bereavement Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is strictly under the amount of 54,048.23 USD.\n- Gate B: passed when hours worked in the past year are equal to or greater than 1,030 hours.\n- Gate C: passed when take-home annual pay is strictly beneath the level of 43,894.12 USD.\n- Route: an applicant enrolled in Yeldham Retirement Bonus skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat outcome does the application of Ren Kovacs to Quenhollow Brewery Bereavement Leave receive?",
  "options": [
   "Not eligible: Gate A is the reason (gross annual pay)",
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (take-home annual pay)"
  ]
 },
 {
  "qid": "qf26a26b53f",
  "kind": "yes/no",
  "text": "[busy_queue] case=CR-69539 worker=Dani Ishikawa subject=Finn\n\nPeople who asked to claim Finn (2026):\n| person | relationship to Finn | months lived with Finn | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hiro Ilunga | father | 8 months | 48,581.00 USD | no |\n| Waleed Douglas | uncle | 6 months | 79,541.00 USD | yes |",
  "question": "Under these rules, is Waleed Douglas excluded from claiming Finn for Ferrowby Forest Credit?",
  "definitions": "Ferrowby Forest Credit rules for 2026: who may claim Finn.\n- Only one person may claim Finn. Work through these steps in order.\n- Step one: only people who filed a claim for Finn are considered.\n- Step two: of those, only people with whom Finn lived for strictly higher than 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Finn lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Finn.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q6ab814903d",
  "kind": "yes/no",
  "text": "[help_desk_entry] ref=CR-99689 by=Blair Xiong about=Ines\n\nPeople who asked to claim Ines (2025):\n| person | relationship to Ines | months lived with Ines | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Kwame Kelly | uncle | 4 months | $51,380.85 | no |\n| Mirela Gallegos | mother | 5 months | $36,317 | yes |",
  "question": "According to these rules, is Mirela Gallegos the person who ends up holding the right to claim Ines for Corrowby Family Supplement?",
  "definitions": "Corrowby Family Supplement rules for 2025: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for 6 months or more in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ines lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa6a858ab1a",
  "kind": "yes/no",
  "text": "reference: CASE-39971\nhandler: Emi Figueroa\nsubject: Elias Lindqvist\n\nFacts for Elias Lindqvist (2025):\n- gross monthly income: $2,151.79\n- net monthly income: $1,618.67\n- countable assets: $2,517.98\n- time in the service area: 12 months\n- age: 50 years\n- enrolled in: Feldane Childcare Credit",
  "question": "Going by the listed rules, is Elias Lindqvist eligible for Sennamoor River Rent Support?",
  "definitions": "Sennamoor River Rent Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are at or below the level of $4,862.03.\n- Gate B: passed when the applicant has lived in the service area for over 6 months.\n- Gate C: passed when gross monthly income is strictly under the amount of $2,174.65.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qacbdf70b98",
  "kind": "yes/no",
  "text": "Dear Mirela Evans,\nPlease find HR-87957 logged with the help line team.\nYours faithfully, Kiran Morales\n\nFacts for Mirela Evans (2027):\n- time employed: 79 months\n- hours worked in the past year: 1,260 hours\n- employees at the worksite: 30 employees\n- gross annual pay: 31,255.13 USD\n- take-home annual pay: 23,731.11 USD\n- enrolled in: Rickmere Night School Fund",
  "question": "Is Mirela Evans eligible for Hallowdene Logistics Study Grant by passing every gate that applies?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are in excess of 1,260 hours.\n- Gate B: passed when take-home annual pay is strictly below the level of 40,996.42 USD.\n- Gate C: passed when the worksite has strictly higher than sixteen employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qc5275e9d1f",
  "kind": "yes/no",
  "text": "[case_record] ref=CR-01207 worker=Mika Zamora about=Mia\n\nPeople who asked to claim Mia (2025):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anjali Eriksen | mother | 5 months | 90,875.00 USD | no |\n| Felix Nilsen | father | 3 months | 64,636.39 USD | yes |\n| Idris Ilic | uncle | 12 months | 61,134.77 USD | yes |",
  "question": "For Tessenvale Valley Child Credit, is Anjali Eriksen barred from claiming Mia under the listed rules?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for greater than or equal to 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Mia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5033e393b1",
  "kind": "yes/no",
  "text": "Ticket: casework note for case CASE-75172\nRaised by: Dani Ishikawa\nAbout: Yusuf Sorensen\n\nIntake interview with Yusuf Sorensen (2027):\nCaseworker: Gross monthly income?\nYusuf Sorensen: 3,266.79 USD.\nCaseworker: Net monthly income?\nYusuf Sorensen: 1,748.14 USD.\nCaseworker: Countable assets?\nYusuf Sorensen: 6,542.99 USD.\nCaseworker: Time in the service area?\nYusuf Sorensen: nine months.\nCaseworker: Age?\nYusuf Sorensen: 29 years.\nCaseworker: Other programme enrolled in?\nYusuf Sorensen: Quenmoor Emergency Fund.",
  "question": "Under these rules, is Yusuf Sorensen eligible for Ostermere Delta Flood Repair Support given every gate that applies is passed?",
  "definitions": "Ostermere Delta Flood Repair Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for in excess of nine months.\n- Gate B: passed when net monthly income is strictly beneath the level of 2,166.21 USD.\n- Gate C: passed when gross monthly income is strictly below 2,767.83 USD.\n- Route: an applicant enrolled in Quenmoor Emergency Fund skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q30dc6f7231",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-09477\", \"caseworker\": \"Ezra Rosales\", \"about\": \"Yara Yilmaz\", \"desk\": \"call centre\"}\n\nFacts for Yara Yilmaz (2027), as JSON:\n{\"gross_monthly_income\": \"$3,830.88\", \"net_monthly_income\": \"$2,499.68\", \"countable_assets\": \"$8,626.98\", \"time_in_the_service_area\": \"16 months\", \"age\": \"30 years\", \"enrolled_in\": \"Ambermoor Water Rebate\"}",
  "question": "Under these rules, is Yara Yilmaz eligible for Sennamoor River Rent Support given every gate that applies is passed?",
  "definitions": "Sennamoor River Rent Support eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is smaller than $4,092.71.\n- Gate B: passed when the applicant has lived in the service area for above 8 months.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q2a06efb6c8",
  "kind": "yes/no",
  "text": "People who asked to claim Vida (2026):\n| person | relationship to Vida | months lived with Vida | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anjali Ueda | grandmother | 4 months | 67,482.00 USD | yes |\n| Olena Ramirez | aunt | 6 months | 74,505.00 USD | yes |\n| Mariam Abara | grandmother | 5 months | 74,505.00 USD | yes |\n\ncase_ref: CR-78385\nlead: Avery Obradovic\nperson: Vida",
  "question": "Does the right to claim Vida for Brellow Orchard Family Credit pass to a different person from Mariam Abara, or stay unclaimed?",
  "definitions": "Brellow Orchard Family Credit rules for 2026: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for in excess of 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Vida lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q74562ae497",
  "kind": "yes/no",
  "text": "[case_record] ref=CR-01207 worker=Mika Zamora about=Mia\n\nPeople who asked to claim Mia (2025):\n| person | relationship to Mia | months lived with Mia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Anjali Eriksen | mother | 5 months | 90,875.00 USD | yes |\n| Felix Nilsen | father | 3 months | 64,636.39 USD | yes |\n| Idris Ilic | uncle | 12 months | 61,134.77 USD | yes |",
  "question": "For Tessenvale Valley Child Credit, is Anjali Eriksen barred from claiming Mia under the listed rules?",
  "definitions": "Tessenvale Valley Child Credit rules for 2025: who may claim Mia.\n- Only one person may claim Mia. Work through these steps in order.\n- Step one: only people who filed a claim for Mia are considered.\n- Step two: of those, only people with whom Mia lived for greater than or equal to 5 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Mia lived for more months comes first.\n- If nobody is left after step two, nobody may claim Mia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q5b0703fe72",
  "kind": "yes/no",
  "text": "Hi Vida,\nThis is a routine update on case CR-03480.\nBest, Shay Bekele\n\nPeople who asked to claim Vida (2027):\n- Jelena Kelly: relationship to Vida: aunt; months lived with Vida: twelve months; annual income: $35,298.00; filed a claim: yes\n- Viktor Ruiz: relationship to Vida: father; months lived with Vida: seven months; annual income: $35,298.00; filed a claim: yes",
  "question": "According to these rules, is Jelena Kelly barred from claiming Vida for Ostrowan Prairie Grant?",
  "definitions": "Ostrowan Prairie Grant rules for 2027: who may claim Vida.\n- Only one person may claim Vida. Work through these steps in order.\n- Step one: only people who filed a claim for Vida are considered.\n- Step two: of those, only people with whom Vida lived for seven months or above in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Vida lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Vida.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qca168ac46d",
  "kind": "yes/no",
  "text": "A quick note for the district team: Remy Tran is taking care of HR-91933 for Ubah Castellano.\n\nFacts for Ubah Castellano (2026):\n- time employed: 4 months\n- hours worked in the past year: 542 hours\n- employees at the worksite: 198 employees\n- gross annual pay: 72,985.66 USD\n- take-home annual pay: 50,624.86 USD\n- enrolled in: Ferrin Exam Stipend",
  "question": "Is Ubah Castellano formally ineligible for Hallowdene Logistics Study Grant under these rules?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is lower than or equal to 50,624.85 USD.\n- Gate B: passed when the applicant has been employed for greater than or equal to 7 months.\n- Route: an applicant enrolled in Ferrin Exam Bursary skips Gate A; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q64068743c3",
  "kind": "yes/no",
  "text": "Routine note: HR-60137\nFrom Kiran Morales for the call centre, about Gabriel Watson.\n\nFacts for Gabriel Watson (2025):\n- time employed: 27 months\n- hours worked in the past year: 1,689 hours\n- employees at the worksite: 27 employees\n- gross annual pay: 55,121.14 USD\n- take-home annual pay: 38,833.89 USD\n- enrolled in: Gerrondale Tenant Loan",
  "question": "Does Gabriel Watson fail to qualify for Marrowby Bakery Family Leave on these rules?",
  "definitions": "Marrowby Bakery Family Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the worksite has higher than 27 employees.\n- Gate B: passed when take-home annual pay is equal to or below 62,270.30 USD.\n- Route: an applicant enrolled in Gerrondale Tenant Aid skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q7db5a598ea",
  "kind": "yes/no",
  "text": "Remy Tran: back office has Ana down for CR-92183, just routine stuff.\n\nInterview notes for Ana (2026):\nCaseworker: Bianca Dragic, your relation to Ana?\nBianca Dragic: I am Ana's grandmother.\nCaseworker: Months Ana lived with you?\nBianca Dragic: 9 months.\nCaseworker: Annual income?\nBianca Dragic: 54,605.05 USD.\nCaseworker: Filed a claim for Ana?\nBianca Dragic: yes.\nCaseworker: Jiro Sokolov, your relation to Ana?\nJiro Sokolov: I am Ana's father.\nCaseworker: Months Ana lived with you?\nJiro Sokolov: 2 months.\nCaseworker: Annual income?\nJiro Sokolov: $55,542.\nCaseworker: Filed a claim for Ana?\nJiro Sokolov: yes.",
  "question": "Under these rules, is Bianca Dragic the person who gets to claim Ana for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2026: who may claim Ana.\n- Only one person may claim Ana. Work through these steps in order.\n- Step one: only people who filed a claim for Ana are considered.\n- Step two: of those, only people with whom Ana lived for over 7 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: the person with whom Ana lived for more months comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ana.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q4db88a571b",
  "kind": "yes/no",
  "text": "[welcome_file] thanks to Sami Castro for case CASE-90632\n[about_person] Ravi Murphy is the warm focus here.\n\nIntake interview with Ravi Murphy (2025):\nCaseworker: Gross monthly income?\nRavi Murphy: $3,638.76.\nCaseworker: Net monthly income?\nRavi Murphy: $2,459.25.\nCaseworker: Countable assets?\nRavi Murphy: $11,048.56.\nCaseworker: Time in the service area?\nRavi Murphy: five months.\nCaseworker: Age?\nRavi Murphy: 85 years.\nCaseworker: Other programme enrolled in?\nRavi Murphy: Lowmarsh Heating Loan.",
  "question": "Going by the listed rules, does a gate that applies end the application of Ravi Murphy to Tamsfell Senior Home Support?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when countable assets are $9,217.39 or lower.\n- Gate B: passed when the applicant has lived in the service area for a minimum of three months.\n- Gate C: passed when the applicant's age is above 57 years.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q938ec9b5f3",
  "kind": "choice",
  "text": "[town_hall_log] case=HR-26163 worker=Avery Obradovic\n[town_hall_log] about=Leila Nguyen\n\nFacts for Leila Nguyen (2026):\n| fact | value |\n| --- | --- |\n| time employed | 3 months |\n| hours worked in the past year | 2061 hours |\n| employees at the worksite | 53 employees |\n| gross annual pay | $56,251.21 |\n| take-home annual pay | $35,286.11 |\n| enrolled in | Pratchell Caregiver Stipend |",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly smaller than $42,284.21.\n- Gate B: passed when the applicant has been employed for 3 months or above.\n- Route: an applicant enrolled in Pratchell Caregiver Allowance skips Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Leila Nguyen to Wendmoor Mill Parental Leave receive?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Eligible",
   "Not eligible: Gate B is the reason (time employed)"
  ]
 },
 {
  "qid": "qcf1ce3b4de",
  "kind": "yes/no",
  "text": "Hello Zara,\nQuick update: the staff support desk has CR-69078 in view.\nRegards, Avery Obradovic\n\nPeople who asked to claim Zara (2027):\n- Zainab Ruiz: relationship to Zara: aunt; months lived with Zara: 7 months; annual income: $62,274.00; filed a claim: yes\n- Tamar Lehmann: relationship to Zara: aunt; months lived with Zara: 8 months; annual income: $62,274.00; filed a claim: yes\n- Dmitri Johnson: relationship to Zara: uncle; months lived with Zara: 8 months; annual income: $55,550.00; filed a claim: yes",
  "question": "Going by the listed rules, does Zainab Ruiz fail to win the right to claim Zara for Kelvery Market Credit?",
  "definitions": "Kelvery Market Credit rules for 2027: who may claim Zara.\n- Only one person may claim Zara. Work through these steps in order.\n- Step one: only people who filed a claim for Zara are considered.\n- Step two: of those, only people with whom Zara lived for equal to or greater than 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Zara lived for more months comes first.\n- If nobody is left after step two, nobody may claim Zara.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q39d2e5221e",
  "kind": "choice",
  "text": "Kazu Yousef: back office has Pia down for CR-25595, just routine stuff.\n\nPeople who asked to claim Pia (2026):\n- Bianca Evans: relationship to Pia: grandmother; months lived with Pia: seven months; annual income: 59,889.42 USD; filed a claim: yes\n- Luka Ilunga: relationship to Pia: father; months lived with Pia: nine months; annual income: 61,092.00 USD; filed a claim: no",
  "question": "Ostrowan Prairie Grant rules for 2026: who may claim Pia.\n- Only one person may claim Pia. Work through these steps in order.\n- Step one: only people who filed a claim for Pia are considered.\n- Step two: of those, only people with whom Pia lived for strictly in excess of six months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Pia lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Pia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, if anyone may claim Pia for Ostrowan Prairie Grant, who is it?",
  "options": [
   "Luka Ilunga",
   "Nobody may claim the child",
   "Bianca Evans"
  ]
 },
 {
  "qid": "qebc1202395",
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
  "qid": "q1907fc4ac5",
  "kind": "yes/no",
  "text": "People who asked to claim Ali (2027):\n| person | relationship to Ali | months lived with Ali | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Elias Lindqvist | father | two months | $38,450 | no |\n| Priya Reynolds | aunt | nine months | $48,964 | yes |\n| Hiroko Okafor | mother | nine months | $30,697 | no |\n\nHi team,\nCase CR-41341 for Ali has gone to the desk.\nThanks, Kendall Umarov",
  "question": "According to these rules, does Priya Reynolds fail to earn a claim on Ali for Mollenby Canal Child Supplement?",
  "definitions": "Mollenby Canal Child Supplement rules for 2027: who may claim Ali.\n- Only one person may claim Ali. Work through these steps in order.\n- Step one: only people who filed a claim for Ali are considered.\n- Step two: of those, only people with whom Ali lived for strictly higher than seven months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with whom Ali lived for more months comes first.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ali.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0ed86a5e9d",
  "kind": "yes/no",
  "text": "People who asked to claim Tove (2025):\n| person | relationship to Tove | months lived with Tove | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Hamid Dlamini | father | 6 months | $17,631.00 | yes |\n| Fatima Becker | mother | 6 months | $87,092.00 | yes |\n| Jelena Medina | grandmother | 6 months | $65,401.00 | yes |\n\nFront counter intake form\nReference: CR-94729\nCaseworker: Sami Castro\nPerson: Tove",
  "question": "According to these rules, does Fatima Becker fail to earn a claim on Tove for Brellow Orchard Family Credit?",
  "definitions": "Brellow Orchard Family Credit rules for 2025: who may claim Tove.\n- Only one person may claim Tove. Work through these steps in order.\n- Step one: only people who filed a claim for Tove are considered.\n- Step two: of those, only people with whom Tove lived for equal to or greater than 6 months in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Tove lived for more months comes first.\n- If nobody is left after step two, nobody may claim Tove.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q98e92e4e56",
  "kind": "yes/no",
  "text": "Nika Hernandez: file CR-49299 about Ezra is on my list.\n\nInterview notes for Ezra (2027):\nCaseworker: Xenia Rahimi, your relation to Ezra?\nXenia Rahimi: I am Ezra's mother.\nCaseworker: Months Ezra lived with you?\nXenia Rahimi: 9 months.\nCaseworker: Annual income?\nXenia Rahimi: 45,721.29 USD.\nCaseworker: Filed a claim for Ezra?\nXenia Rahimi: yes.\nCaseworker: Rafael Eriksen, your relation to Ezra?\nRafael Eriksen: I am Ezra's father.\nCaseworker: Months Ezra lived with you?\nRafael Eriksen: 9 months.\nCaseworker: Annual income?\nRafael Eriksen: 58,537.00 USD.\nCaseworker: Filed a claim for Ezra?\nRafael Eriksen: no.",
  "question": "Following the listed rules, is it true that Rafael Eriksen does not get to claim Ezra for Sallowmere Family Payment?",
  "definitions": "Sallowmere Family Payment rules for 2027: who may claim Ezra.\n- Only one person may claim Ezra. Work through these steps in order.\n- Step one: only people who filed a claim for Ezra are considered.\n- Step two: of those, only people with whom Ezra lived for a minimum of 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ezra lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ezra.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q53b4e3bcbb",
  "kind": "yes/no",
  "text": "[queue_desk] case=CASE-05919 staff=Kendall Umarov person=Juliana Sorensen\n\nIntake interview with Juliana Sorensen (2026):\nCaseworker: Gross monthly income?\nJuliana Sorensen: $3,799.51.\nCaseworker: Net monthly income?\nJuliana Sorensen: $2,713.50.\nCaseworker: Countable assets?\nJuliana Sorensen: $1,431.53.\nCaseworker: Time in the service area?\nJuliana Sorensen: twelve months.\nCaseworker: Age?\nJuliana Sorensen: 58 years.\nCaseworker: Other programme enrolled in?\nJuliana Sorensen: Lowmarsh Heating Aid.",
  "question": "Does Juliana Sorensen fully qualify for Tamsfell Senior Home Support under these rules?",
  "definitions": "Tamsfell Senior Home Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is lower than or equal to $3,799.51.\n- Gate B: passed when the applicant's age is larger than 58 years.\n- Gate C: passed when net monthly income is at or under the amount of $2,713.49.\n- Route: an applicant enrolled in Lowmarsh Heating Aid skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q041f9c7ea4",
  "kind": "yes/no",
  "text": "Records office ticket: CR-50068\nRaised by: Adi Chandra\nAbout: Ivan\n\nInterview notes for Ivan (2026):\nCaseworker: Luka Ilic, your relation to Ivan?\nLuka Ilic: I am Ivan's father.\nCaseworker: Months Ivan lived with you?\nLuka Ilic: 8 months.\nCaseworker: Annual income?\nLuka Ilic: $79,613.\nCaseworker: Filed a claim for Ivan?\nLuka Ilic: yes.\nCaseworker: Yasmin Russell, your relation to Ivan?\nYasmin Russell: I am Ivan's mother.\nCaseworker: Months Ivan lived with you?\nYasmin Russell: 0 months.\nCaseworker: Annual income?\nYasmin Russell: 87,687.91 USD.\nCaseworker: Filed a claim for Ivan?\nYasmin Russell: yes.\nCaseworker: Cyril Nilsen, your relation to Ivan?\nCyril Nilsen: I am Ivan's uncle.\nCaseworker: Months Ivan lived with you?\nCyril Nilsen: 6 months.\nCaseworker: Annual income?\nCyril Nilsen: 36,858.17 USD.\nCaseworker: Filed a claim for Ivan?\nCyril Nilsen: yes.",
  "question": "For Kelmstone Mountain Family Grant, is Cyril Nilsen the person who is left holding the right to claim Ivan?",
  "definitions": "Kelmstone Mountain Family Grant rules for 2026: who may claim Ivan.\n- Only one person may claim Ivan. Work through these steps in order.\n- Step one: only people who filed a claim for Ivan are considered.\n- Step two: of those, only people with whom Ivan lived for at or over 5 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: the person with whom Ivan lived for more months comes first.\n- If nobody is left after step two, nobody may claim Ivan.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8d8bf09f30",
  "kind": "choice",
  "text": "Intake form: call centre\nCase reference: HR-16230\nCaseworker: Quinn Pavlenko\nAbout: Ren Watson\n\nFacts for Ren Watson (2025):\n| fact | value |\n| --- | --- |\n| time employed | 6 months |\n| hours worked in the past year | 556 hours |\n| employees at the worksite | 46 employees |\n| gross annual pay | $66,897.58 |\n| take-home annual pay | $15,331.97 |\n| enrolled in | Pellwick Bereavement Leave |",
  "question": "Tovardine Seed Caregiver Leave eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is strictly smaller than $32,956.28.\n- Gate B: passed when gross annual pay is $45,229.88 or less.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhat comes of the application of Ren Watson to Tovardine Seed Caregiver Leave?",
  "options": [
   "Not eligible: Gate A is the reason (take-home annual pay)",
   "Not eligible: Gate B is the reason (gross annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "qee509c72c8",
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
  "qid": "q2ee7e4d9ac",
  "kind": "yes/no",
  "text": "Front counter ticket: HR-94827\nWarm hello from: Riley Watanabe\nPerson: Kenji Halvorsen\n\nIntake interview with Kenji Halvorsen (2027):\nCaseworker: Time employed?\nKenji Halvorsen: five months.\nCaseworker: Hours worked in the past year?\nKenji Halvorsen: 2177 hours.\nCaseworker: Employees at your worksite?\nKenji Halvorsen: 22 employees.\nCaseworker: Gross annual pay?\nKenji Halvorsen: 79,488.26 USD.\nCaseworker: Take-home annual pay?\nKenji Halvorsen: 26,825.34 USD.\nCaseworker: Other programme enrolled in?\nKenji Halvorsen: Myrren Study Grant.",
  "question": "Is Kenji Halvorsen ineligible for Quenhollow Brewery Bereavement Leave given the listed gates?",
  "definitions": "Quenhollow Brewery Bereavement Leave eligibility rules for 2027:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross annual pay is 79,488.26 USD or lower.\n- Gate B: passed when take-home annual pay is strictly smaller than 59,371.05 USD.\n- Gate C: passed when the worksite has a minimum of 21 employees.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qdca9929a1e",
  "kind": "choice",
  "text": "People who asked to claim Nia (2026):\n| person | relationship to Nia | months lived with Nia | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Galina Russell | grandmother | 9 months | $81,895.00 | yes |\n| Tomas Okafor | grandfather | 11 months | $81,895.00 | yes |\n| Yasmin Gashi | grandmother | 2 months | $42,277.34 | yes |\n\nDear Nia,\nThis reply concerns case CR-64448.\nYours sincerely, Nika Hernandez",
  "question": "Mollenby Canal Child Supplement rules for 2026: who may claim Nia.\n- Only one person may claim Nia. Work through these steps in order.\n- Step one: only people who filed a claim for Nia are considered.\n- Step two: of those, only people with whom Nia lived for higher than 6 months in 2026 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Nia lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Nia.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which person, if any, is the sole person who may claim Nia for Mollenby Canal Child Supplement?",
  "options": [
   "Tomas Okafor",
   "Galina Russell"
  ]
 },
 {
  "qid": "qbbf1c61bfa",
  "kind": "yes/no",
  "text": "case_ref: HR-05668\nhandled_by: Kazu Yousef\nperson: Hana Douglas\ndesk: intake\n\nFacts for Hana Douglas (2026):\n- time employed: 7 months\n- hours worked in the past year: 751 hours\n- employees at the worksite: 368 employees\n- gross annual pay: $46,040.21\n- take-home annual pay: $34,503.09\n- enrolled in: Sarrowby Mentor Stipend",
  "question": "Is Hana Douglas not eligible for Hallowdene Logistics Study Grant under these rules?",
  "definitions": "Hallowdene Logistics Study Grant eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when hours worked in the past year are larger than 750 hours.\n- Gate B: passed when take-home annual pay is lower than or equal to $27,562.98.\n- Gate C: passed when the applicant has been employed for 8 months or more.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q0c5bb3427f",
  "kind": "yes/no",
  "text": "Kendall Umarov: back office has Xenia Dubois down for HR-18689, just routine stuff.\n\nIntake interview with Xenia Dubois (2026):\nCaseworker: Time employed?\nXenia Dubois: 13 months.\nCaseworker: Hours worked in the past year?\nXenia Dubois: 2,117 hours.\nCaseworker: Employees at your worksite?\nXenia Dubois: 100 employees.\nCaseworker: Gross annual pay?\nXenia Dubois: $76,767.20.\nCaseworker: Take-home annual pay?\nXenia Dubois: $59,343.56.\nCaseworker: Other programme enrolled in?\nXenia Dubois: Ellerwick Trainee Stream.",
  "question": "Under these rules, is Xenia Dubois eligible for Sorrelby Child Care Support overall?",
  "definitions": "Sorrelby Child Care Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for 14 months or above.\n- Gate B: passed when the worksite has at or beyond 64 employees.\n- Gate C: passed when gross annual pay is $76,767.20 or lower.\n- Route: an applicant enrolled in Ivormoor Shift Supplement skips Gate A and Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qe89ab16fce",
  "kind": "choice",
  "text": "Ezra Rosales: routine check on Nika Murphy under CASE-06747.\n\nIntake interview with Nika Murphy (2025):\nCaseworker: Gross monthly income?\nNika Murphy: 4,430.06 USD.\nCaseworker: Net monthly income?\nNika Murphy: 3,235.12 USD.\nCaseworker: Countable assets?\nNika Murphy: 8,394.14 USD.\nCaseworker: Time in the service area?\nNika Murphy: 52 months.\nCaseworker: Age?\nNika Murphy: 59 years.\nCaseworker: Other programme enrolled in?\nNika Murphy: Ormsby Housing Aid.",
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
  "qid": "qa47bce3ab3",
  "kind": "choice",
  "text": "Case note: Avery Obradovic picks up file CASE-34407, about Esra Castellano, at the counter.\n\nIntake interview with Esra Castellano (2026):\nCaseworker: Gross monthly income?\nEsra Castellano: $5,125.52.\nCaseworker: Net monthly income?\nEsra Castellano: $3,195.43.\nCaseworker: Countable assets?\nEsra Castellano: $9,713.64.\nCaseworker: Time in the service area?\nEsra Castellano: three months.\nCaseworker: Age?\nEsra Castellano: 66 years.\nCaseworker: Other programme enrolled in?\nEsra Castellano: Quenmoor Emergency Fund.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly over eight months.\n- Gate B: passed when gross monthly income is strictly smaller than $3,237.95.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which result does the application of Esra Castellano to Ostermere Delta Flood Repair Support receive?",
  "options": [
   "Not eligible: Gate B is the reason (gross monthly income)",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Eligible"
  ]
 },
 {
  "qid": "qdad80c65ab",
  "kind": "choice",
  "text": "Hi Ailsa Kimura,\nBrief update on case HR-89802 below.\nThanks, Emi Figueroa\n\nIntake interview with Ailsa Kimura (2026):\nCaseworker: Time employed?\nAilsa Kimura: 10 months.\nCaseworker: Hours worked in the past year?\nAilsa Kimura: 1,128 hours.\nCaseworker: Employees at your worksite?\nAilsa Kimura: 23 employees.\nCaseworker: Gross annual pay?\nAilsa Kimura: 96,619.70 USD.\nCaseworker: Take-home annual pay?\nAilsa Kimura: 64,669.83 USD.\nCaseworker: Other programme enrolled in?\nAilsa Kimura: Wendle Trade Pilot.",
  "question": "Brenwold Timber Apprentice Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has been employed for larger than 10 months.\n- Gate B: passed when take-home annual pay is 65,151.41 USD or lower.\n- Gate C: passed when the worksite has in excess of 37 employees.\n- Route: an applicant enrolled in Pendrick Training Grant skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, which outcome does the application of Ailsa Kimura to Brenwold Timber Apprentice Support produce?",
  "options": [
   "Not eligible: Gate A is the reason (time employed)",
   "Not eligible: Gate C is the reason (employees at the worksite)",
   "Not eligible: Gate B is the reason (take-home annual pay)",
   "Eligible"
  ]
 },
 {
  "qid": "qcbfece21ab",
  "kind": "yes/no",
  "text": "Shay Bekele: At the regional service office, case CR-10938 concerns Ines.\n\nPeople who asked to claim Ines (2027):\n- Hugo Murphy: relationship to Ines: father; months lived with Ines: 10 months; annual income: 31,119.75 USD; filed a claim: yes\n- Jakub Johnson: relationship to Ines: grandfather; months lived with Ines: 7 months; annual income: $63,812; filed a claim: yes\n- Rania Wojcik: relationship to Ines: mother; months lived with Ines: 7 months; annual income: 31,119.75 USD; filed a claim: yes",
  "question": "Is Hugo Murphy the person who comes out with the right to claim Ines for Tollmere Lakeside Family Payment?",
  "definitions": "Tollmere Lakeside Family Payment rules for 2027: who may claim Ines.\n- Only one person may claim Ines. Work through these steps in order.\n- Step one: only people who filed a claim for Ines are considered.\n- Step two: of those, only people with whom Ines lived for over 7 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ines lived for more months comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with the higher annual income comes first.\n- If nobody is left after step two, nobody may claim Ines.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "qa8f865b121",
  "kind": "yes/no",
  "text": "{\"case\": \"CASE-70270\", \"caseworker\": \"Cameron Vargas\", \"about\": \"Greta Johnson\", \"desk\": \"call centre\"}\n\nFacts for Greta Johnson (2025), as JSON:\n{\"gross_monthly_income\": \"3,547.29 USD\", \"net_monthly_income\": \"2,209.44 USD\", \"countable_assets\": \"1,774.96 USD\", \"time_in_the_service_area\": \"6 months\", \"age\": \"73 years\", \"enrolled_in\": \"Brackenholm Housing Loan\"}",
  "question": "Under these rules, is Greta Johnson ineligible for Tarrowick Food Basket Support as a whole?",
  "definitions": "Tarrowick Food Basket Support eligibility rules for 2025:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for equal to or greater than 6 months.\n- Gate B: passed when net monthly income is strictly below the level of 1,576.51 USD.\n- Gate C: passed when countable assets are at or beneath 3,006.34 USD.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome."
 },
 {
  "qid": "q8e1bef0e8b",
  "kind": "choice",
  "text": "Ticket: district office desk review, case CR-34217\nRaised by: Dani Ishikawa\nAbout: Remi\n\nInterview notes for Remi (2027):\nCaseworker: Rania Halvorsen, your relation to Remi?\nRania Halvorsen: I am Remi's grandmother.\nCaseworker: Months Remi lived with you?\nRania Halvorsen: 8 months.\nCaseworker: Annual income?\nRania Halvorsen: $61,640.41.\nCaseworker: Filed a claim for Remi?\nRania Halvorsen: yes.\nCaseworker: Dmitri Hamilton, your relation to Remi?\nDmitri Hamilton: I am Remi's grandfather.\nCaseworker: Months Remi lived with you?\nDmitri Hamilton: 2 months.\nCaseworker: Annual income?\nDmitri Hamilton: $61,391.00.\nCaseworker: Filed a claim for Remi?\nDmitri Hamilton: no.\nCaseworker: Idris Sokolov, your relation to Remi?\nIdris Sokolov: I am Remi's father.\nCaseworker: Months Remi lived with you?\nIdris Sokolov: 5 months.\nCaseworker: Annual income?\nIdris Sokolov: $61,639.41.\nCaseworker: Filed a claim for Remi?\nIdris Sokolov: yes.",
  "question": "Kelmstone Mountain Family Grant rules for 2027: who may claim Remi.\n- Only one person may claim Remi. Work through these steps in order.\n- Step one: only people who filed a claim for Remi are considered.\n- Step two: of those, only people with whom Remi lived for at or greater than 5 months in 2027 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with the higher annual income comes first.\n- Second tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- Third tie-breaker: the person with whom Remi lived for more months comes first.\n- If nobody is left after step two, nobody may claim Remi.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nAccording to these rules, which person, if any, is the sole person entitled to claim Remi for Kelmstone Mountain Family Grant?",
  "options": [
   "Rania Halvorsen",
   "Idris Sokolov"
  ]
 },
 {
  "qid": "qdbc2c0409d",
  "kind": "choice",
  "text": "case_ref: HR-48777\nworker: Mika Zamora\nsubject: Quinn Dubois\n\nFacts for Quinn Dubois (2026):\n- time employed: 116 months\n- hours worked in the past year: 1,070 hours\n- employees at the worksite: 109 employees\n- gross annual pay: $119,717.06\n- take-home annual pay: $63,750.22\n- enrolled in: Dunnamore Retraining Bonus",
  "question": "Wendmoor Mill Parental Leave eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when take-home annual pay is $63,750.21 or lower.\n- Gate B: passed when hours worked in the past year are strictly in excess of 1,070 hours.\n- Gate C: passed when gross annual pay is smaller than $86,820.10.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nWhich outcome does the application of Quinn Dubois to Wendmoor Mill Parental Leave receive?",
  "options": [
   "Not eligible: Gate B is the reason (hours worked in the past year)",
   "Eligible",
   "Not eligible: Gate C is the reason (gross annual pay)",
   "Not eligible: Gate A is the reason (take-home annual pay)"
  ]
 }
]
