# A46 replay label-noise blind read RSAM43-blind_read-3a26a22d-008

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAM43-blind_read-3a26a22d-008.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 40. Answers expected: 40 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q848eecb8ff",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nUnited States in 1987, where he returned to Colombia to avoid deportation, and resided in Colombia for 13 or 14 months until he returned to the United States as a tourist, constitutes an abandonment of his lawful, permanent resident status in the United States.” {Id. at 13.) In reaching his conclusions, the IJ noted, among other things, petitioner’s testimony that when he left the United States in 1987, he had no intention of returning'to the United States and that he returned to the United States with a fraudulent passport and a tourist visa. (Id. at 12-13.) Petitioner argues that his leaving the United States in 1987 was not voluntary and was induced by misinformation provided to him by the Immigration and Naturalization Service. See Tejeda v. INS, 346 F.2d 389, 393 (9th Cir.1965) (<HOLDING>); McLeod v. Peterson, 283 F.2d 180, 184 (3d\n\nCandidate holding for <HOLDING>: holding that iirira and aedpa are not applicable to criminal alien who entered a guilty plea at a time when alien was eligible for 212c relief",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "qff74baf998",
  "kind": "choice",
  "text": "Question: Most common complication of acute Otitis media in children:\nOptions: (A) Deafness (B) Mastoiditis (C) Cholesteatoma (D) Facial nerve palsy",
  "question": "Which medical subject does this exam question belong to?",
  "options": [
   "ENT (otorhinolaryngology)",
   "anaesthesia",
   "anatomy",
   "biochemistry",
   "dermatology",
   "forensic medicine and toxicology",
   "internal medicine",
   "microbiology",
   "obstetrics and gynaecology",
   "ophthalmology",
   "orthopaedics",
   "paediatrics",
   "pathology",
   "pharmacology",
   "physiology",
   "psychiatry",
   "radiology",
   "social and preventive medicine",
   "surgery"
  ],
  "definitions": "- ENT (otorhinolaryngology): Diseases and surgery of the ear, nose, paranasal sinuses, pharynx and larynx, hearing and vestibular tests, and head-neck conditions treated by ENT surgeons.\n- anaesthesia: Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, regional blocks and pain or ICU management as practised by anaesthetists.\n- anatomy: Normal structure of the body: gross anatomy, relations, nerve and blood supply, embryology, histology and neuroanatomy; not how organs function (physiology) or disease (pathology).\n- biochemistry: Molecules and metabolism: enzymes, vitamins, metabolic pathways and their inborn errors, molecular biology and genetics techniques, lipids, proteins and nutrition chemistry.\n- dermatology: Skin, hair and nail diseases, their lesions and treatment, and sexually transmitted diseases and leprosy as taught in dermatology (venereology).\n- forensic medicine and toxicology: Medico-legal practice: injuries and wounds, death and post-mortem changes, identification, sexual offences, legal procedures, and poisons with their antidotes (toxicology).\n- internal medicine: Diagnosis and non-surgical management of adult systemic diseases (cardiac, renal, endocrine, infectious, neurological...); drug mechanism questions go to pharmacology, tissue-level mechanisms to pathology.\n- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation.\n- obstetrics and gynaecology: Pregnancy, labour, puerperium and their complications, contraception, and diseases of the female reproductive organs, including gynaecological cancers.\n- ophthalmology: Eye diseases, their signs, investigations and treatment, optics and refraction, and eye surgery.\n- orthopaedics: Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and their orthopaedic management.\n- paediatrics: Child health: growth and development milestones, neonatal care, immunisation schedules, nutrition and diseases of infants and children.\n- pathology: Mechanisms and morphology of disease: cell injury, inflammation, neoplasia, haematology, and the gross/microscopic features and lab findings of diseases.\n- pharmacology: Drugs: mechanisms of action, pharmacokinetics, adverse effects, interactions, drug of choice and classification of drugs.\n- physiology: Normal function of the body's systems (nerve, muscle, blood, heart, lungs, kidney, endocrine, special senses) and their regulation, not their structure or disease.\n- psychiatry: Mental disorders, their symptoms, classification and treatment (including psychotropic therapy choices), psychology and substance-use disorders.\n- radiology: Imaging and radiation: X-ray, CT, MRI, ultrasound and nuclear-medicine signs and choice of investigation, radiation physics, radiotherapy and radiation protection.\n- social and preventive medicine: Community medicine: epidemiology, biostatistics, national health programmes, screening, nutrition and environmental and occupational health at population level.\n- surgery: Surgical diseases and their operative management: trauma, GI and hepatobiliary surgery, breast, thyroid, vascular, urology, neurosurgery and surgical oncology."
 },
 {
  "qid": "q55ada6a400",
  "kind": "choice",
  "text": "the storm drain inside our complex is clogged",
  "question": "Which City of San Diego 311 request type (and so which crew) should this resident's report be routed to?",
  "options": [
   "clogged or damaged storm drain",
   "dead animal pickup",
   "flooded street",
   "graffiti on private property",
   "graffiti on public property",
   "homeless encampment",
   "illegal dumping",
   "lane striping, curb paint or guardrail repair",
   "missed trash or recycling pickup",
   "new sign, crosswalk or traffic-calming request",
   "overgrown weeds",
   "parking violation",
   "pavement repair or resurfacing",
   "polluted runoff or illegal discharge",
   "pothole repair",
   "shared scooter or bike problem",
   "sidewalk repair",
   "street light repair",
   "street sweeping",
   "traffic sign repair",
   "traffic signal malfunction",
   "traffic signal timing",
   "tree trimming or fallen tree",
   "vegetation blocking the sidewalk",
   "waste on private property"
  ],
  "definitions": "- clogged or damaged storm drain: A storm drain, inlet, grate, culvert or drainage channel that is clogged, full of debris or damaged.\n- dead animal pickup: A dead animal on a street, sidewalk or public area that needs to be picked up.\n- flooded street: Water standing or flowing across a street or intersection (ponding, flooding, a water break) rather than a blocked drain being the reported issue.\n- graffiti on private property: Graffiti on a private business, building, home, fence or dumpster, handled by code enforcement so the property owner removes it.\n- graffiti on public property: Graffiti on public right-of-way property (streets, sidewalks, curbs, signs, poles, utility boxes, bridges, alleys), removed by the City's graffiti crew, when the report does not place it on private property.\n- homeless encampment: People camping or living in tents, structures or on sidewalks, canyons or parks with belongings, reported for outreach and clean-up.\n- illegal dumping: Trash, furniture, mattresses, appliances or debris left on a public street, sidewalk, alley or lot by someone, not bins awaiting pickup.\n- lane striping, curb paint or guardrail repair: Upkeep of road markings and roadside hardware: faded lane striping or curb paint, damaged guardrails, barriers or city fences.\n- missed trash or recycling pickup: The City's scheduled collection skipped a household's trash, recycling or green-waste container on its collection day.\n- new sign, crosswalk or traffic-calming request: A request for something new: a stop sign, crosswalk, speed hump, signage or other traffic-safety change to be evaluated by traffic engineers.\n- overgrown weeds: Weeds, tall grass or dry brush growing on public land (medians, canyons, city lots, road edges) that need clearing, often as a fire risk.\n- parking violation: A vehicle parked illegally or stored on the street: over 72 hours, in a red or other restricted zone, blocking a driveway, or abandoned.\n- pavement repair or resurfacing: Street or alley surface that is cracked, crumbling, sunken, uneven or worn and needs asphalt repair or resurfacing, rather than one discrete pothole.\n- polluted runoff or illegal discharge: Someone letting pollutants reach the storm drains: washing, hosing or pouring paint, oil, grease, concrete, sewage or irrigation water into the street or gutter.\n- pothole repair: A distinct hole or pit in the asphalt of a street or alley that needs patching; broad cracking, sinking or worn surfaces go to pavement repair.\n- shared scooter or bike problem: A rented dockless scooter or e-bike left blocking a sidewalk, parked illegally, dumped or damaged; the operator is told to move it.\n- sidewalk repair: Damaged public sidewalk concrete: cracked, lifted, raised by roots, broken or uneven slabs that create a trip hazard; not things blocking the sidewalk.\n- street light repair: A street light that is out, flickering, on during the day, or whose pole is knocked down or damaged; traffic signals are not street lights.\n- street sweeping: A request for the street sweeper: dirt, leaves, glass or debris along streets and gutters, or a missed or needed sweeping route.\n- traffic sign repair: An existing traffic or street sign that is knocked down, missing, bent, faded, turned or blocked from view and needs repair or replacement.\n- traffic signal malfunction: A traffic or pedestrian signal that is out, dark, flashing, stuck, damaged or has a broken push button, i.e. the equipment itself fails.\n- traffic signal timing: A working signal whose timing is a problem: waits too long, greens too short, turn arrows or sensors not giving enough time, causing backups.\n- tree trimming or fallen tree: A street tree in the public right-of-way that needs trimming, has fallen or hanging limbs or fronds, is dead, or should be evaluated for removal.\n- vegetation blocking the sidewalk: Bushes, hedges or plants from a private property growing over or blocking the public sidewalk; the owner is ordered to cut them back.\n- waste on private property: Trash, junk or debris accumulating on private property (a yard, lot or building grounds) that the owner must clean up, not dumping in the street."
 },
 {
  "qid": "qa82abe0b44",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (OSV – Assistant Engineer), Electrical – Electronics – Control Engineering.\n\nQuestion: If a digital multimeter set up to measure AC volts reads low value, but constantly changing \"ghost voltages\" when its leads are disconnected, what does this indicate?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "The digital multimeter AC voltage range is at its lowest value.",
   "Stray electromagnetic fields from electrical equipment exist in the air.",
   "The digital multimeter test leads are acting as an antenna.",
   "All the above conditions must exist."
  ],
  "definitions": "- The digital multimeter AC voltage range is at its lowest value.: Answer \"The digital multimeter AC voltage range is at its lowest value.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Stray electromagnetic fields from electrical equipment exist in the air.: Answer \"Stray electromagnetic fields from electrical equipment exist in the air.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The digital multimeter test leads are acting as an antenna.: Answer \"The digital multimeter test leads are acting as an antenna.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- All the above conditions must exist.: Answer \"All the above conditions must exist.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q848b240d8b",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  |  | Year ended December 31, |  |\n|  | 2019 | 2018 | 2017 |\n| Number of repurchased shares (1) | 7.8 | 16.8 | 1.6 |\n| Aggregate purchase price | $138.9 | $315.0 | $25.0 |\n| Fees, commissions and other expenses | 0.1 | 0.3 | — |\n| Total cash used for share repurchases | $139.0 | $315.3 | $25.0 |\n| Weighted-average purchase price per share | $17.89 | $18.78 | $15.35 |\n| Available for future purchases at period end | $1,361.1 | $1,500.0 | $603.2 |\nText:\nShare Repurchase Programs\nOn December 1, 2014, the Company announced the \"Capital Allocation Policy\" under which the Company intends to return to stockholders approximately 80 percent of free cash flow, less repayments of long-term debt, subject to a variety of factors, including the strategic plans, market and economic conditions and the discretion of the Company’s board of directors. For the purposes of the Capital Allocation Policy, the Company defines \"free cash flow\" as net cash provided by operating activities less purchases of property, plant and equipment.\nOn December 1, 2014, the Company announced the 2014 Share Repurchase Program (the \"2014 Share Repurchase Program\") pursuant to the Capital Allocation Policy. Under the Company’s 2014 Share Repurchase Program, the Company had the ability to repurchase up to $ 1.0 billion (exclusive of fees, commissions and other expenses) of the Company’s common stock over a period of four years from December 1, 2014, subject to certain contingencies.\nThe 2014 Share Repurchase Program, which did not require the Company to purchase any particular amount of common stock and was subject to the discretion of the board of directors, expired on November 30, 2018 with approximately $288.2 million remaining unutilized.\nThe Company repurchased common stock worth approximately $315.0 million and $25.0 million under the 2014 Share Repurchase Program during the years ended December 31, 2018 and December 31, 2017, respectively.\nOn November 15, 2018, the Company announced the 2018 Share Repurchase Program (the \"2018 Share Repurchase Program\") pursuant to the Capital Allocation Policy. Under the 2018 Share Repurchase Program, the Company is authorized to repurchase up to $ 1.5 billion of its common shares from December 1, 2018 through December 31, 2022, exclusive of any fees, commissions or other expenses.\nThe Company may repurchase its common stock from time to time in privately negotiated transactions or open market transactions, including pursuant to a trading plan in accordance with Rule 10b5-1 and Rule 10b-18 of the Exchange Act, or by any combination of such methods or other methods.\nThe timing of any repurchases and the actual number of shares repurchased will depend on a variety of factors, including the Company’s stock price, corporate and regulatory requirements, restrictions under the Company’s debt obligations and other market and economic conditions. There were $138.9 million in repurchases of the Company's common stock under the 2018 Share Repurchase Program during the year ended December 31, 2019. As of December 31, 2019, the remaining authorized amount under the 2018 Share Repurchase Program was $1,361.1 million.\nInformation relating to the Company's 2018 and 2014 Share Repurchase Programs is as follows (in millions, except per share data):\n(1) None of these shares had been reissued or retired as of December 31, 2019, but may be reissued or retired by the Company at a later date.\n\nQuestion: How is \"free cash flow\" defined for the the purposes of the Capital Allocation Policy?\nProposed answer: December 1, 2014",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "qc0414bf1a3",
  "kind": "choice",
  "text": "Question: Myositis ossificans is most common around the.....joint:\nOptions: (A) Knee (B) Elbow (C) Wrist (D) Hip",
  "question": "Which medical subject does this exam question belong to?",
  "options": [
   "ENT (otorhinolaryngology)",
   "anaesthesia",
   "anatomy",
   "biochemistry",
   "dermatology",
   "forensic medicine and toxicology",
   "internal medicine",
   "microbiology",
   "obstetrics and gynaecology",
   "ophthalmology",
   "orthopaedics",
   "paediatrics",
   "pathology",
   "pharmacology",
   "physiology",
   "psychiatry",
   "radiology",
   "social and preventive medicine",
   "surgery"
  ],
  "definitions": "- ENT (otorhinolaryngology): Diseases and surgery of the ear, nose, paranasal sinuses, pharynx and larynx, hearing and vestibular tests, and head-neck conditions treated by ENT surgeons.\n- anaesthesia: Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, regional blocks and pain or ICU management as practised by anaesthetists.\n- anatomy: Normal structure of the body: gross anatomy, relations, nerve and blood supply, embryology, histology and neuroanatomy; not how organs function (physiology) or disease (pathology).\n- biochemistry: Molecules and metabolism: enzymes, vitamins, metabolic pathways and their inborn errors, molecular biology and genetics techniques, lipids, proteins and nutrition chemistry.\n- dermatology: Skin, hair and nail diseases, their lesions and treatment, and sexually transmitted diseases and leprosy as taught in dermatology (venereology).\n- forensic medicine and toxicology: Medico-legal practice: injuries and wounds, death and post-mortem changes, identification, sexual offences, legal procedures, and poisons with their antidotes (toxicology).\n- internal medicine: Diagnosis and non-surgical management of adult systemic diseases (cardiac, renal, endocrine, infectious, neurological...); drug mechanism questions go to pharmacology, tissue-level mechanisms to pathology.\n- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation.\n- obstetrics and gynaecology: Pregnancy, labour, puerperium and their complications, contraception, and diseases of the female reproductive organs, including gynaecological cancers.\n- ophthalmology: Eye diseases, their signs, investigations and treatment, optics and refraction, and eye surgery.\n- orthopaedics: Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and their orthopaedic management.\n- paediatrics: Child health: growth and development milestones, neonatal care, immunisation schedules, nutrition and diseases of infants and children.\n- pathology: Mechanisms and morphology of disease: cell injury, inflammation, neoplasia, haematology, and the gross/microscopic features and lab findings of diseases.\n- pharmacology: Drugs: mechanisms of action, pharmacokinetics, adverse effects, interactions, drug of choice and classification of drugs.\n- physiology: Normal function of the body's systems (nerve, muscle, blood, heart, lungs, kidney, endocrine, special senses) and their regulation, not their structure or disease.\n- psychiatry: Mental disorders, their symptoms, classification and treatment (including psychotropic therapy choices), psychology and substance-use disorders.\n- radiology: Imaging and radiation: X-ray, CT, MRI, ultrasound and nuclear-medicine signs and choice of investigation, radiation physics, radiotherapy and radiation protection.\n- social and preventive medicine: Community medicine: epidemiology, biostatistics, national health programmes, screening, nutrition and environmental and occupational health at population level.\n- surgery: Surgical diseases and their operative management: trauma, GI and hepatobiliary surgery, breast, thyroid, vascular, urology, neurosurgery and surgical oncology."
 },
 {
  "qid": "qc6c6bf3fcd",
  "kind": "yes/no",
  "text": "Wikipedia page: Eddie Johnson (American soccer)\nTable (first row is the header):\n| # | Date | Venue | Opponent | Score | Result | Competition |\n| 1. | 10 October 2004 | Estadio Cuscatlán, San Salvador, El Salvador | El Salvador | 2–0 | 2–0 | 2006 FIFA World Cup qualification |\n| 2. | 13 October 2004 | RFK Stadium, Washington, D.C., United States | Panama | 3–0 | 6–0 | 2006 FIFA World Cup qualification |\n| 3. | 13 October 2004 | RFK Stadium, Washington, D.C., United States | Panama | 4–0 | 6–0 | 2006 FIFA World Cup qualification |\n| 4. | 13 October 2004 | RFK Stadium, Washington, D.C., United States | Panama | 5–0 | 6–0 | 2006 FIFA World Cup qualification |\n| 5. | 17 November 2004 | Columbus Crew Stadium, Columbus, United States | Jamaica | 1–0 | 1–1 | 2006 FIFA World Cup qualification |\n| 6. | 9 February 2005 | Queen's Park Oval, Port of Spain, Trinidad | Trinidad and Tobago | 1–0 | 2–1 | 2006 FIFA World Cup qualification |\n| 7. | 19 March 2005 | University Stadium, Albuquerque, United States | Honduras | 1–0 | 1–0 | Friendly |\n| 8. | 30 March 2005 | Legion Field, Birmingham, United States | Guatemala | 1–0 | 2–0 | 2006 FIFA World Cup qualification |\n| 9. | 19 February 2006 | Pizza Hut Park, Frisco, United States | Guatemala | 3–0 | 4–0 | Friendly |\n| 10. | 9 June 2007 | The Home Depot Center, Carson, United States | Trinidad and Tobago | 2–0 | 2–0 | 2007 CONCACAF Gold Cup |\n| 11. | 28 June 2007 | Estadio José Pachencho Romero, Maracaibo, Venezuela | Argentina | 1–0 | 1–4 | 2007 Copa América |\n| 12. | 15 June 2008 | The Home Depot Center, Carson, United States | Barbados | 6–0 | 8–0 | 2010 FIFA World Cup qualification |\n| 13. | 12 October 2012 | Sir Vivian Richards Stadium, Antigua, Antigua and Barbuda | Antigua and Barbuda | 1–0 | 2–1 | 2014 FIFA World Cup qualification |\n| 14. | 12 October 2012 | Sir Vivian Richards Stadium, Antigua, Antigua and Barbuda | Antigua and Barbuda | 2–1 | 2–1 | 2014 FIFA World Cup qualification |\n| 15. | 12 June 2013 | CenturyLink Field, Seattle, United States | Panama | 2–0 | 2–0 | 2014 FIFA World Cup qualification |\n| 16. | 21 July 2013 | M&T Bank Stadium, Baltimore, United States | El Salvador | 3–1 | 5–1 | 2013 CONCACAF Gold Cup |\n| 17. | 24 July 2013 | Cowboys Stadium, Arlington, United States | Honduras | 1–0 | 3–1 | 2013 CONCACAF Gold Cup |\n| 18. | 14 August 2013 | Asim Ferhatović Hase Stadium, Sarajevo, Bosnia and Herzegovina | Bosnia and Herzegovina | 1–2 | 4–3 | Friendly |\n| 19. | 10 September 2013 | Columbus Crew Stadium, Columbus, United States | Mexico | 1–0 | 2–0 | 2014 FIFA World Cup qualification |\n\nQuestion: how many times has he played against honduras?\nProposed answer: 2",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 },
 {
  "qid": "q9c3e6eaf26",
  "kind": "choice",
  "text": "Assistant's task: giving patients their doctor's follow-up instructions.\nUser: Hello I'm so confused who did I just call?\nAssistant: Hello, how can I help?\nUser: It's me. Mark. I saw a doctor I think I don't remember what they said to do. Dr. Alexis.\n[Assistant sends a LOOKUP request to the system: Name=Dr. Alexis, PatientName=Mark]\n[System result: Take your medicine before you go to sleep. If you experience nausea, please contact your doctor immediately.]\nAssistant: Your instructions are: Take your medicine before you go to sleep. If you experience nausea, please contact your doctor immediately..\nUser: Oh wait it was Dr. Johnson. I'm at the doctor so often I forget who I saw.\n[Assistant sends a LOOKUP request to the system: Name=Dr. Johnson, PatientName=Mark]\n[System result: You must take your medicine 2 times a day before meals.]\nAssistant: Your instructions are: You must take your medicine 2 times a day before meals..\nUser: Oh well no wonder I took it all at once!",
  "question": "Following its flow chart for giving patients their doctor's follow-up instructions, what should the assistant do next?",
  "options": [
   "ask for the user's name",
   "ask if anything else is needed",
   "ask who the patient's doctor is",
   "greet the user",
   "look it up in the system",
   "say goodbye",
   "say no doctor is available",
   "say the request is out of scope",
   "tell the patient the doctor's instructions"
  ],
  "definitions": "- ask for the user's name: Ask for the user's name: the first step after the greeting; choose it once the user has said what they want, unless they already gave this information.\n- ask if anything else is needed: Ask whether the user needs anything else: right after the task's final result (confirmation, failure or information) has been told to the user.\n- ask who the patient's doctor is: Ask who the patient's doctor is: comes right after 'ask for the user's name' in this flow chart; choose it once earlier steps are settled and the user has not yet given this.\n- greet the user: Open with 'Hello, how can I help?'; only for the assistant's very first turn, before anything else is done.\n- look it up in the system: Submit the lookup to the system: once all details the chart collects (name, who the patient's doctor is) are known; say nothing about the result before it.\n- say goodbye: Say goodbye: when the user indicates they need nothing more, typically answering no to 'is there anything else?'.\n- say no doctor is available: Say no doctor is available: when the most recent system lookup returns no matching record at all.\n- say the request is out of scope: Say the assistant can only help with giving patients their doctor's follow-up instructions: when the user asks for something outside that task.\n- tell the patient the doctor's instructions: Tell the patient the doctor's instructions: when the most recent system lookup returns the requested information."
 },
 {
  "qid": "q8c20edaec5",
  "kind": "yes/no",
  "text": "A 26-year-old medical student comes to the physician for a chest x-ray to rule out active pulmonary tuberculosis. He needs a medical and radiological report before starting a medical internship in South Africa. He has no history of serious illness and does not complain of any symptoms. He has smoked 1 pack of cigarettes daily for the past 6 years. He does not drink alcohol. He is 190 cm (6 ft 3 in) tall and weighs 75 kg (165 lbs); BMI is 20.8 kg/m2. His temperature is 37°C (98.6°F), pulse is 80/min, respirations are 18/min, and blood pressure is 128/89 mm Hg. The lungs are clear to auscultation. Cardiac examination shows no abnormalities. The x-ray of the chest shows a small pneumothorax (rim of < 2 cm) between the upper left lung margin and the chest wall. Which of the following is the most appropriate next step in management of this patient?\n\nAnswer choices:\nA. Emergent needle thoracostomy\nB. Observation and follow-up x-ray\nC. Immediate intubation and assisted ventilation\nD. CT of the chest\nE. Urgent chest tube placement\n\nProposed answer: B. Observation and follow-up x-ray",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q2669fc1f82",
  "kind": "yes/no",
  "text": "Booking database (what the assistant can look up or book without the FAQ pages): hotels - name, area, price range, star rating, hotel or guesthouse, parking and internet (yes/no), address, phone, postcode, room booking; restaurants - name, food type, area, price range, address, phone, postcode, table booking; attractions - name, type, area, entrance fee, opening hours, address, phone, postcode; trains - departure, destination, day, leave and arrive times, duration, ticket price, train ID, seat booking; taxis - pickup, destination, times, car type, contact number.\n\nConversation (the last line is the customer's latest message):\nCustomer: I like the sound of that. Can you tell me the type and entrance fee please?\nAssistant: It is a park and the fee is free\nCustomer: I also need a taxi to between the 2 places. I need to leave milton county park by 12:15.\nAssistant: Where will you be leaving from?\nCustomer: I'll be leaving from the hotel.",
  "question": "Does the customer's latest message need an answer from the business's FAQ and policy pages, rather than from the booking database or a booking action?",
  "definitions": "- yes: The latest customer message asks about something the booking database does not hold (a policy, service or amenity detail such as pets, check-in times, payment, cancellations, discounts, accessibility or menu), so the FAQ pages must answer it.\n- no: The latest customer message can be handled with the listed booking-database fields or a search or booking action, or it asks for no information at all (giving details, confirming, choosing, thanking)."
 },
 {
  "qid": "qfdc57b1a62",
  "kind": "choice",
  "text": "Question: What is the treatment of after cataract?\nOptions: (A) Surgical (B) Laser (C) Medical (D) None of these",
  "question": "Which medical subject does this exam question belong to?",
  "options": [
   "ENT (otorhinolaryngology)",
   "anaesthesia",
   "anatomy",
   "biochemistry",
   "dermatology",
   "forensic medicine and toxicology",
   "internal medicine",
   "microbiology",
   "obstetrics and gynaecology",
   "ophthalmology",
   "orthopaedics",
   "paediatrics",
   "pathology",
   "pharmacology",
   "physiology",
   "psychiatry",
   "radiology",
   "social and preventive medicine",
   "surgery"
  ],
  "definitions": "- ENT (otorhinolaryngology): Diseases and surgery of the ear, nose, paranasal sinuses, pharynx and larynx, hearing and vestibular tests, and head-neck conditions treated by ENT surgeons.\n- anaesthesia: Anaesthetic agents and techniques, airway management, muscle relaxants, perioperative monitoring, regional blocks and pain or ICU management as practised by anaesthetists.\n- anatomy: Normal structure of the body: gross anatomy, relations, nerve and blood supply, embryology, histology and neuroanatomy; not how organs function (physiology) or disease (pathology).\n- biochemistry: Molecules and metabolism: enzymes, vitamins, metabolic pathways and their inborn errors, molecular biology and genetics techniques, lipids, proteins and nutrition chemistry.\n- dermatology: Skin, hair and nail diseases, their lesions and treatment, and sexually transmitted diseases and leprosy as taught in dermatology (venereology).\n- forensic medicine and toxicology: Medico-legal practice: injuries and wounds, death and post-mortem changes, identification, sexual offences, legal procedures, and poisons with their antidotes (toxicology).\n- internal medicine: Diagnosis and non-surgical management of adult systemic diseases (cardiac, renal, endocrine, infectious, neurological...); drug mechanism questions go to pharmacology, tissue-level mechanisms to pathology.\n- microbiology: Bacteria, viruses, fungi and parasites: their properties, culture, lab diagnosis, virulence, immunology and vaccines, and sterilisation.\n- obstetrics and gynaecology: Pregnancy, labour, puerperium and their complications, contraception, and diseases of the female reproductive organs, including gynaecological cancers.\n- ophthalmology: Eye diseases, their signs, investigations and treatment, optics and refraction, and eye surgery.\n- orthopaedics: Fractures, dislocations, bone and joint diseases, bone tumours, nerve injuries of the limbs and their orthopaedic management.\n- paediatrics: Child health: growth and development milestones, neonatal care, immunisation schedules, nutrition and diseases of infants and children.\n- pathology: Mechanisms and morphology of disease: cell injury, inflammation, neoplasia, haematology, and the gross/microscopic features and lab findings of diseases.\n- pharmacology: Drugs: mechanisms of action, pharmacokinetics, adverse effects, interactions, drug of choice and classification of drugs.\n- physiology: Normal function of the body's systems (nerve, muscle, blood, heart, lungs, kidney, endocrine, special senses) and their regulation, not their structure or disease.\n- psychiatry: Mental disorders, their symptoms, classification and treatment (including psychotropic therapy choices), psychology and substance-use disorders.\n- radiology: Imaging and radiation: X-ray, CT, MRI, ultrasound and nuclear-medicine signs and choice of investigation, radiation physics, radiotherapy and radiation protection.\n- social and preventive medicine: Community medicine: epidemiology, biostatistics, national health programmes, screening, nutrition and environmental and occupational health at population level.\n- surgery: Surgical diseases and their operative management: trauma, GI and hepatobiliary surgery, breast, thyroid, vascular, urology, neurosurgery and surgical oncology."
 },
 {
  "qid": "qc6c7c1c289",
  "kind": "choice",
  "text": "Product: Samsung French Door Refrigerator with ice maker (3 Door Refrigerator) fingerprint resistant stainless steel, 22 cu ft capacity. (category: Refrigerators)\nIncident description: Prior to 1/18/24 when my Samsung refrigerator/freezer (purchased 4/3/23 & set up/delivered by Lowes) 3 Door French, model #RF22A4221SR/AA, SN 0BA34BBW301714Wfailed totally, but I didnt know it because digital readings still read 34 degrees F/-2 degrees F, I was experiencing gi upset and diarrhea. I didnt know what it was, my doctor thought I was getting a re-occurring virus. I happened to notice the taste of the mayonnaise was off, so I bought a refrigerator thermometer. It indicated that the refrigerator temperature was 45 degrees, this was October 2023. So I reset the temps on the refrigerator. It seemed to be working. But November 2023 temps were up again. Reset again, thought maybe not enough clearance around fridge, moved across the kitchen. No difference in refrigeration performance. Unplugged fridge, reset temps, seemed to be working. Total unit failure 1/18/24, I went to get frozen bagels from freezer, they were thawed. Freezer display read -4 degrees, I checked fridge thermometer 45 again! I tried texting Samsung chat support and they disconnected on me 11 times over a 3 day period (1/18/24) Went online to Samsung.com, scheduled a repair ticket myself for 1/26/24, they cancelled that and rescheduled for 1/30/24 (they said I cancelled the appt). I wrote a bad review for Lowes & Samsung, Lowes conference called Samsung and was told theres parts on order (sight unseen) & will be addressed on 1/30/24 by technician. This is unacceptable for a refrigerator/freezer which temperatures are too warm to keep food safe, causing illness and doesnt display proper temperatures.",
  "question": "Based on this consumer product incident report, what was the most serious outcome for the primary victim on the SaferProducts.gov severity scale?",
  "options": [
   "no incident, no injury",
   "incident, but no injury",
   "injury, no first aid or medical care",
   "injury, first aid by a non-medical person",
   "injury, seen by a medical professional",
   "injury, emergency department treatment",
   "injury, hospital admission",
   "death"
  ],
  "definitions": "- no incident, no injury: The report describes a hazard or defect that was noticed before anything happened: the product did not actually fail, burn, break or harm anyone during use.\n- incident, but no injury: The product actually failed, overheated, caught fire, broke or malfunctioned during use, but no person was physically hurt (property damage or a near miss only).\n- injury, no first aid or medical care: The primary victim was physically hurt (for example a small burn, cut, bruise or shock), but no first aid was given and no medical care was sought.\n- injury, first aid by a non-medical person: The primary victim was hurt and was treated only by themselves or another lay person (ice, cold water, bandage, ointment, over-the-counter medicine), with no doctor, clinic or hospital.\n- injury, seen by a medical professional: The primary victim's highest level of care was a doctor, urgent-care clinic, dentist, nurse or other medical professional outside an emergency department, with no hospital admission.\n- injury, emergency department treatment: The primary victim was treated in a hospital emergency department (ER), possibly after an ambulance ride, and was released without being admitted.\n- injury, hospital admission: The primary victim was admitted to a hospital as an inpatient (for example overnight stay, intensive care, burn unit or surgery) and survived.\n- death: The primary victim died from the incident, whether at the scene or later in hospital."
 },
 {
  "qid": "q8ed15f1e44",
  "kind": "choice",
  "text": "overseen by traitor obama & killary hitlary with funding from soros",
  "question": "Which type of group does this post's hateful rhetoric mainly target?",
  "options": [
   "race or ethnicity",
   "nationality or region",
   "gender",
   "religion",
   "sexual orientation",
   "ideology",
   "political affiliation",
   "health or disability"
  ],
  "definitions": "- race or ethnicity: The hateful rhetoric mainly targets people for their race or ethnicity, for example anti-Black, anti-Asian, anti-Latino, anti-Arab or antisemitic attacks on Jews as a people (the manual codes antisemitism here).\n- nationality or region: The hateful rhetoric mainly targets people for their nationality, country or region of origin, including general xenophobia, attacks on immigrants as foreigners, or on named countries or regions.\n- gender: The hateful rhetoric mainly targets people for their gender or gender identity, for example anti-woman, anti-man or anti-trans attacks.\n- religion: The hateful rhetoric mainly targets people for their religion or spiritual beliefs, for example anti-Muslim or anti-Christian attacks on believers or the faith.\n- sexual orientation: The hateful rhetoric mainly targets people for their sexual orientation, for example gay, lesbian or bisexual people.\n- ideology: The hateful rhetoric mainly targets people for their ideology or worldview, such as liberals, leftists, conservatives or the right wing as a camp of believers, not as members of a party.\n- political affiliation: The hateful rhetoric mainly targets people for membership of a political organisation or party, such as Democrats or Republicans, or a named party's members or politicians.\n- health or disability: The hateful rhetoric mainly targets people for their mental or physical health status, mental illness or a physical disability."
 },
 {
  "qid": "qfd15dffe19",
  "kind": "yes/no",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), PWR question bank, topic: Thermodynamic Cycles.\n\nQuestion: Initially, a nuclear power plant was operating at steady-state 85 percent reactor power when extraction steam to the feedwater heaters was isolated. With extraction steam still isolated, reactor power was returned to 85 percent and the plant was stabilized. Compared to the conditions just prior to the transient, the current main generator output (MW) is...",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?\nIs the correct answer \"lower, because the steam cycle thermal efficiency has decreased.\"?",
  "definitions": "- lower, because the steam cycle thermal efficiency has decreased.: Answer \"lower, because the steam cycle thermal efficiency has decreased.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- lower, because decreased steam flow through the main turbine caused the main generator to reject load.: Answer \"lower, because decreased steam flow through the main turbine caused the main generator to reject load.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- higher, because increased steam flow through the main turbine caused the main generator to pick up load.: Answer \"higher, because increased steam flow through the main turbine caused the main generator to pick up load.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- higher, because the steam cycle thermal efficiency has increased.: Answer \"higher, because the steam cycle thermal efficiency has increased.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qe1c300b21e",
  "kind": "yes/no",
  "text": "Table caption: Texture of uncoated and coated tomatoes during storage.\n| Treatment | Storage periods | Storage periods | Storage periods | Storage periods | Storage periods |\n| Treatment | 0th day | 7th day | 14th day | 21st day | 28th day |\n| 1% K. alvarezii | Fresh and firm | Firm | Slightly shrinked | Shrinked and dots appeared | Oozing of water |\n| 2% K. alvarezii | Fresh and firm | Firm | Slightly shrinked | Slightly shrinked | Shrinked |\n| 3% K. alvarezii | Fresh and firm | Firm | Firm and bright in colour | Firm | Firm |\n| 1% S. tenerrimum | Fresh and firm | Slightly shrinked | Shrinked | Dots and shrinked | Decayed |\n| 2% S. tenerrimum | Fresh and firm | Firm | Slightly shrinked | Slightly shrinked | Shrink and damaged |\n| 3% S. tenerrimum | Fresh and firm | Firm | Firm | Firm | Slightly shrinked |\n| Control (Uncoated) | Fresh and firm | Slightly shrinked | Shrink and cracked | Oozing of water | Decayed |\n\nStatement: In 28th day all the coated and uncoated tomatoes is oozing of water.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "qc79bb60a01",
  "kind": "choice",
  "text": "Assistant's task: giving patients their doctor's follow-up instructions.\nUser: Hello\nAssistant: Hello, how can I help?\nUser: I need to contact Dr. Morgan. Oops, I mean Dr. Alexis. That's who I had an appointment with, I think.\nAssistant: Could I get your name, please?\nUser: My name is Angela. I don't remember where I left my keys. Do you know? I had them when I went to the grocery store.\nAssistant: I am sorry, I don't quite understand what you mean. I am only able to help schedule a followup appointment with your doctor.\nUser: I just need to know when to take my medicine. Dr. Morgan, I mean, Dr. Alexis told me, but I forgot.\n[Assistant sends a LOOKUP request to the system: Name=Dr. Alexis, PatientName=Angela]\n[System result: Take your medicine before you go to sleep. If you experience nausea, please contact your doctor immediately.]\nAssistant: Your instructions are: Take your medicine before you go to sleep. If you experience nausea, please contact your doctor immediately..\nUser: Oh, alright. Thank you.",
  "question": "Following its flow chart for giving patients their doctor's follow-up instructions, what should the assistant do next?",
  "options": [
   "ask for the user's name",
   "ask if anything else is needed",
   "ask who the patient's doctor is",
   "greet the user",
   "look it up in the system",
   "say goodbye",
   "say no doctor is available",
   "say the request is out of scope",
   "tell the patient the doctor's instructions"
  ],
  "definitions": "- ask for the user's name: Ask for the user's name: the first step after the greeting; choose it once the user has said what they want, unless they already gave this information.\n- ask if anything else is needed: Ask whether the user needs anything else: right after the task's final result (confirmation, failure or information) has been told to the user.\n- ask who the patient's doctor is: Ask who the patient's doctor is: comes right after 'ask for the user's name' in this flow chart; choose it once earlier steps are settled and the user has not yet given this.\n- greet the user: Open with 'Hello, how can I help?'; only for the assistant's very first turn, before anything else is done.\n- look it up in the system: Submit the lookup to the system: once all details the chart collects (name, who the patient's doctor is) are known; say nothing about the result before it.\n- say goodbye: Say goodbye: when the user indicates they need nothing more, typically answering no to 'is there anything else?'.\n- say no doctor is available: Say no doctor is available: when the most recent system lookup returns no matching record at all.\n- say the request is out of scope: Say the assistant can only help with giving patients their doctor's follow-up instructions: when the user asks for something outside that task.\n- tell the patient the doctor's instructions: Tell the patient the doctor's instructions: when the most recent system lookup returns the requested information."
 },
 {
  "qid": "q7a25d03535",
  "kind": "yes/no",
  "text": "Booking database (what the assistant can look up or book without the FAQ pages): hotels - name, area, price range, star rating, hotel or guesthouse, parking and internet (yes/no), address, phone, postcode, room booking; restaurants - name, food type, area, price range, address, phone, postcode, table booking; attractions - name, type, area, entrance fee, opening hours, address, phone, postcode; trains - departure, destination, day, leave and arrive times, duration, ticket price, train ID, seat booking; taxis - pickup, destination, times, car type, contact number.\n\nConversation (the last line is the customer's latest message):\nCustomer: No, I need help finding a cinema located in the east\nAssistant: I have one located in the south and one located in the centre. do you have a location preference?\nCustomer: Either is fine. I just need a phone number so I can call one of them. Thanks.\nAssistant: vue cinema is in the centre & the phone number is 08712240240\nCustomer: I'm sorry, but if their is no cinema in the east, can you find me a swimming pool instead?",
  "question": "Does the customer's latest message need an answer from the business's FAQ and policy pages, rather than from the booking database or a booking action?",
  "definitions": "- yes: The latest customer message asks about something the booking database does not hold (a policy, service or amenity detail such as pets, check-in times, payment, cancellations, discounts, accessibility or menu), so the FAQ pages must answer it.\n- no: The latest customer message can be handled with the listed booking-database fields or a search or booking action, or it asks for no information at all (giving details, confirming, choosing, thanking)."
 },
 {
  "qid": "qd83f453b3f",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  |  | Fiscal Year Ended |  |\n|  | December 28, 2019 | December 29, 2018 | December 30, 2017 |\n| Balance at beginning of year | $185 | $200 | $299 |\n| Charges (reversals) to costs and expenses | 37 | (15) | (99) |\n| Balance at end of year | $222 | $185 | $200 |\nText:\nAccounts Receivable and Allowance for Doubtful Accounts\nThe majority of our accounts receivable are derived from sales to large multinational semiconductor manufacturers throughout the world, are recorded at their invoiced amount and do not bear interest.\nIn order to monitor potential credit losses, we perform ongoing credit evaluations of our customers' financial condition. An allowance for doubtful accounts is maintained based upon our assessment of the expected collectability of all accounts receivable. The allowance for doubtful accounts is reviewed and assessed for adequacy on a quarterly basis.\nWe take into consideration (1) any circumstances of which we are aware of a customer's inability to meet its financial obligations and (2) our judgments as to prevailing economic conditions in the industry and their impact on our customers. If circumstances change, and the financial condition of our customers is adversely affected and they are unable to meet their financial obligations, we may need to take additional allowances, which would result in an increase in our operating expense.\nActivity related to our allowance for doubtful accounts receivable was as follows (in thousands):\n\nQuestion: What is the main source of accounts receivable?\nProposed answer: derived from sales to large multinational semiconductor manufacturers throughout the world",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q20445fbae8",
  "kind": "yes/no",
  "text": "Request:\nCompute: $0.\\overline{7}-0.\\overline{4}+0.\\overline{2}$. Express your answer as a common fraction.\n\nResponse:\nThis problem involves adding and subtracting decimals that have repeating digits.\nA useful trick for dealing with repeating decimals is to multiply them by a power of 10 that matches the length of the repeating part.\nThis way, we can shift the decimal point and get rid of the bar.\nFor example, if we multiply $0.\\overline{7}$ by 10, we get $7.\\overline{7}$.\nThen, if we subtract $0.\\overline{7}$ from this, we get $7.\\overline{7}-0.\\overline{7}=7$, which is a whole number.\nWe can do the same thing for $0.\\overline{4}$ and $0.\\overline{2}$, multiplying them by 10 and subtracting the original decimals.\nWe get $0.\\overline{4}\\times 10-0.\\overline{4}=4-0.4=3.6$ and $0.\\overline{2}\\times 10-0.\\overline{2}=2-0.2=1.8$.\nNow, we can rewrite the original expression using these results.\nWe have $0.\\overline{7}-0.\\overline{4}+0.\\overline{2}=(7-0.\\overline{7})-(3.6-0.\\overline{4})+(1.8-0.\\overline{2})$.\nNext, we can simplify the parentheses by combining the terms with and without bars.\nWe get $7-0.\\overline{7}-3.6+0.\\overline{4}+1.8-0.\\overline{2}=7-3.6+1.8-0.\\overline{7}+0.\\overline{4}-0.\\overline{2}$.\nNow, we can group the terms with bars together and the terms without bars together.\nWe get $7-3.6+1.8-(0.\\overline{7}-0.\\overline{4}+0.\\overline{2})=5.2-(0.\\overline{7}-0.\\overline{4}+0.\\overline{2})$.\nNotice that the expression inside the parentheses is the same as the original expression.\nSo, we have a recursive equation of the form $x=5.2-x$, where $x=0.\\overline{7}-0.\\overline{4}+0.\\overline{2}$.\nTo solve for $x$, we can add $x$ to both sides and divide by 2.\nWe get $2x=5.2$ and $x=\\frac{5.2}{2}=2.6$.\nTherefore, $0.\\overline{7}-0.\\overline{4}+0.\\overline{2}=2.6$.\nTo express this as a common fraction, we can multiply and divide by 10 to get rid of the decimal point.\nWe get $\\frac{2.6}{1}=\\frac{2.6\\times 10}{1\\times 10}=\\frac{26}{10}$.\nTo simplify this fraction, we can divide both the numerator and the denominator by the greatest common factor, which is 2.\nWe get $\\frac{26}{10}=\\frac{26\\div 2}{10\\div 2}=\\frac{13}{5}$.\n# Answer\n\n13/5",
  "question": "Does the response contain at least one substantive error or miss an explicit requirement?"
 },
 {
  "qid": "q6beba24643",
  "kind": "choice",
  "text": "A 33YOM WAS HIT BY CAR AT WORK SHOULDER PAIN",
  "question": "Which OIICS event category describes how this worker's injury happened?",
  "options": [
   "Class M",
   "Class C",
   "Class U",
   "Class F",
   "Class S",
   "Class B",
   "Class K",
   "Class Q",
   "Class G",
   "Class N",
   "Class Z",
   "Class D",
   "Class J",
   "Class T"
  ],
  "definitions": "- Class M: A rail vehicle (train, trolley, streetcar, subway or mine rail car) caused the injury: collision, derailment, or sudden movement while the worker was on, under or beside it.\n- Class C: A change in air or water pressure caused the injury: barotrauma of the ears or sinuses, decompression sickness, or altitude illness.\n- Class U: An uncontrolled fire caused the injury: burns, smoke inhalation, overheating, or being struck or cut while fighting or escaping a fire; it outranks the contact, fall or exertion that happened during it.\n- Class F: The worker's own movement drove a body part into an object: bumping, banging, hitting or jamming against something, stepping on a nail or sharp object, or walking into equipment, with no fall.\n- Class S: Friction, pressure or foreign matter caused the injury: blisters, chafing, rope or rug burns, or dust, dirt, sawdust, metal or other particles getting into the eye without being described as flying into it.\n- Class B: The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a public road (a motor-vehicle crash), including hitting the inside of the vehicle during it.\n- Class K: A moving object hit the worker: something fell, was dropped, flew, swung, rolled or slipped onto or into them, including a tool that slipped in use; the object moved, not the worker (a moving vehicle hitting a worker on foot is a pedestrian incident).\n- Class Q: Another person hurt the worker with no assault or fight described: bumped, collided with, fell or landed on, grabbed or struck the worker accidentally, during a seizure, a game or while being cared for.\n- Class G: Pain or a disorder from repeating small, low-force motions over time (typing, keying, scanning, gripping, cutting, using the hands or wrists all day), with no single heavy exertion.\n- Class N: The worker was on foot, not in or on a vehicle, and was struck, run over or pinned by a moving car, truck, forklift or other vehicle, on or off the road.\n- Class Z: The worker was on or operating a motorized land vehicle or mobile machine away from public traffic (forklift, tractor, ATV, riding mower, golf cart, loader) that tipped, rolled, crashed or threw them off.\n- Class D: The worker deliberately jumped down from a higher place (truck bed, trailer, dock, ladder, scaffold, equipment) and was hurt on landing.\n- Class J: The worker was riding an animal or a non-motorized vehicle (horse, bull, bicycle, scooter, skateboard) and fell, was thrown or crashed.\n- Class T: The worker fell to the floor, ground or other surface they were standing or walking on (slip-and-fall, trip-and-fall, falling against something at that level); used when no height, stairs, ladder or vehicle is mentioned."
 },
 {
  "qid": "q4cf6eb95ef",
  "kind": "yes/no",
  "text": "Wikipedia page: Welsh League Cup\nSection: Past winners\nTable:\n| Season | Winner | Score | Runner-up | Venue |\n| 1992–93 | Afan Lido | 1 – 1 | Caersws | Park Avenue, Aberystwyth |\n| 1992–93 | Afan Lido won 4–3 on penalties | Afan Lido won 4–3 on penalties | Afan Lido won 4–3 on penalties |  |\n| ... |\n| 2003–04 | Rhyl | 4 – 0 | Carmarthen Town | Latham Park, Newtown |\n| 2004–05 | Carmarthen Town | 2 – 0 (a.e.t.) | Rhyl | Latham Park, Newtown |\n| 2005–06 | Total Network Solutions | 4 – 0 | Port Talbot Town | Park Avenue, Aberystwyth |\n| ... |\n| 2008–09 | The New Saints | 2 – 0 | Bangor City | Latham Park, Newtown |\n| 2009–10 | The New Saints | 3 – 1 | Rhyl | The Airfield, Broughton |\n| 2010–11 | The New Saints | 4 – 3 (a.e.t.) | Llanelli | Park Avenue, Aberystwyth |\n| ... |\n| 2014–15 | The New Saints | 3 – 0 | Bala Town | Latham Park, Newtown |\n| 2015–16 | The New Saints | 2 – 0 | Denbigh Town | Maesdu Park, Llandudno |\n| 2016–17 | The New Saints | 4 – 0 | Barry Town United | Cyncoed Stadium, Cardiff |\n| 2017–18 | The New Saints | 1 – 0 | Cardiff MU | Park Avenue, Aberystwyth |\n| ... |\n\nClaim: The first Welsh League Cup was won by Total Network Solutions in 1992/93, who beat Caersws 4–3 on penalties, after drawing in the final 1–1, while the New Saints hold the record for the most League Cup titles overall.",
  "question": "Is the claim contradicted by the table?",
  "definitions": "- yes: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name).\n- no: The claim is supported: every fact matches the table and its page and section titles, with each value paired with the right row and column."
 },
 {
  "qid": "qe6f912a495",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (Tankerman Assistant), Tankship Dangerous Liquids.\n\nQuestion: According to U.S. regulations, which of the following does not qualify as a discharge of oil?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Pumping oil overboard through a fixed piping system",
   "Leakage of oil to the water by an improperly blanked transfer hose",
   "Spilling oil on the main deck and having it flow over the side",
   "Discharging oil into the sea for pollution research"
  ],
  "definitions": "- Pumping oil overboard through a fixed piping system: Answer \"Pumping oil overboard through a fixed piping system\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Leakage of oil to the water by an improperly blanked transfer hose: Answer \"Leakage of oil to the water by an improperly blanked transfer hose\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Spilling oil on the main deck and having it flow over the side: Answer \"Spilling oil on the main deck and having it flow over the side\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Discharging oil into the sea for pollution research: Answer \"Discharging oil into the sea for pollution research\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qc06cf35530",
  "kind": "choice",
  "text": "NWS Storm Data tornado entry (September 2024, Jefferson County, New York). Survey: path length 0.1 miles; maximum path width 50 yards.\n\nThe National Weather Service in Buffalo used Sentinel-2 satellite imagery and found tornadic damage in Jefferson County. A damage scar was found using difference techniques of satellite imagery. The scar was found in a wooded area south of Macklin Road in the Town of Worth. A damage survey could not be conducted due to limited access into the wooded area.",
  "question": "Based on this National Weather Service storm-survey narrative, which Enhanced Fujita (EF) rating was assigned to the tornado?",
  "options": [
   "EFU (unrated)",
   "EF0",
   "EF1",
   "EF2",
   "EF3",
   "EF4",
   "EF5"
  ],
  "definitions": "- EFU (unrated): No rating could be assigned because the tornado struck no rateable damage indicator (for example it stayed over open fields, water or unpopulated land); used for confirmed tornadoes with no surveyable damage.\n- EF0: Estimated 3-second gust 65-85 mph: light damage such as shingles or siding peeled, gutters damaged, branches broken and shallow-rooted trees pushed over; some damage to at least one indicator is required.\n- EF1: Estimated gust 86-110 mph: moderate damage such as roofs badly stripped, mobile homes overturned or badly damaged, exterior doors lost, windows broken and many trees snapped or uprooted.\n- EF2: Estimated gust 111-135 mph: considerable damage such as roofs torn off well-built houses, frame houses shifted on foundations, mobile homes destroyed, large trees snapped or uprooted, cars lifted.\n- EF3: Estimated gust 136-165 mph: severe damage such as entire stories of well-built houses destroyed, major damage to large buildings, trains overturned, trees debarked, heavy cars lifted and thrown.\n- EF4: Estimated gust 166-200 mph: devastating damage such as well-constructed houses and whole frame houses leveled, cars thrown and large debris becoming airborne missiles.\n- EF5: Estimated gust over 200 mph: incredible damage such as strong frame houses leveled and swept clean off their foundations, reinforced-concrete structures critically damaged, car-sized missiles thrown far."
 },
 {
  "qid": "q11dc5a2348",
  "kind": "yes/no",
  "text": "Wikipedia page: Word...Life\nTable (first row is the header):\n| # | Title | Songwriters | Producer(s) | Performer (s) |\n| 1 | \"Creative Control\" | O. Credle, L. Baskerville, T. Jamerson | Organized Konfusion | O.C. |\n| 2 | \"Word...Life\" | O. Credle, A. Best | Buckwild | O.C. |\n| 3 | \"O-Zone\" | O. Credle, A. Best | Buckwild | O.C. |\n| 4 | \"Born 2 Live\" | O. Credle, A. Best | Buckwild | O.C. |\n| 5 | \"Time's Up\" | O. Credle, A. Best | Buckwild | O.C. |\n| 6 | \"Point O' Viewz\" | O. Credle, D. Vanderpool, A. Best | Buckwild, Prestige | O.C. |\n| 7 | \"Constables\" | O. Credle, L. Baskerville, T. Jamerson | Organized Konfusion | O.C. |\n| 8 | \"Ga Head\" | O. Credle, R. Hall | Lord Finesse | O.C. |\n| 9 | \"No Main Topic\" | O. Credle, G. Scott | DJ Ogee/O.Gee | O.C., Prince Po |\n| 10 | \"Let It Slide\" | O. Credle, A. Best | Buckwild | O.C., Pharoahe Monch |\n| 11 | \"Ma Dukes\" | O. Credle, A. Best | Buckwild | O.C. |\n| 12 | \"Story\" | O. Credle, G. Scott | DJ Ogee/O.Gee | O.C. |\n| 13 | \"Outtro (Sabotage)\" | O. Credle, A. Best | Buckwild | O.C. |\n| 14 | \"Born 2 Live (Remix)\" | O. Credle, A. Best | Organized Konfusion | O.C. |\n\nQuestion: how many tracks in word...life were produced by buckwild?\nProposed answer: 7",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 },
 {
  "qid": "qfba0d59164",
  "kind": "choice",
  "text": "Duties:\n- Pull, push, or pry structural steel members into approximate positions for bolting into place.\n- Connect columns, beams, and girders with bolts, following blueprints and instructions from supervisors.\n- Cut, bend, or weld steel pieces, using metal shears, torches, or welding equipment.",
  "question": "Which occupation performs all of the listed duties?",
  "options": [
   "Brickmasons and Blockmasons",
   "Construction Laborers",
   "Drywall and Ceiling Tile Installers",
   "Floor Layers, Except Carpet, Wood, and Hard Tiles",
   "Structural Iron and Steel Workers"
  ],
  "definitions": "- Brickmasons and Blockmasons: Lay and bind building materials, such as brick, structural tile, concrete block, cinder block, glass block, and terra-cotta block, with mortar and other substances, to construct or repair walls, partitions, arches, sewers, and other structures.\n- Construction Laborers: Perform tasks involving physical labor at construction sites. May operate hand and power tools of all types: air hammers, earth tampers, cement mixers, small mechanical hoists, surveying and measuring equipment, and a variety of other equipment and instruments.\n- Drywall and Ceiling Tile Installers: Apply plasterboard or other wallboard to ceilings or interior walls of buildings. Apply or mount acoustical tiles or blocks, strips, or sheets of shock-absorbing materials to ceilings and walls of buildings to reduce or reflect sound. Materials may be of decorative quality.\n- Floor Layers, Except Carpet, Wood, and Hard Tiles: Apply blocks, strips, or sheets of shock-absorbing, sound-deadening, or decorative coverings to floors.\n- Structural Iron and Steel Workers: Raise, place, and unite iron or steel girders, columns, and other structural members to form completed structures or structural frameworks. May erect metal storage tanks and assemble prefabricated metal buildings."
 },
 {
  "qid": "q069adc96c5",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  |  | 2019 |  | 2018 |  |\n|  | NOTE | NUMBER OF SHARES | STATED CAPITAL | NUMBER OF SHARES | STATED CAPITAL |\n| Outstanding, January 1 |  | 898,200,415 | 20,036 | 900,996,640 | 20,091 |\n| Shares issued for the acquisition of AlarmForce | 34 | – | – | 22,531 | 1 |\n| Shares issued under employee stock option plan | 28 | 4,459,559 | 251 | 266,941 | 13 |\n| Repurchase of common shares |  | – | – | (3,085,697) | (69) |\n| Shares issued under ESP |  | 1,231,479 | 75 | – | – |\n| Shares issued under DSP |  | 16,729 | 1 | – | – |\n| Outstanding, December 31 |  | 903,908,182 | 20,363 | 898,200,415 | 20,036 |\nText:\nCOMMON SHARES AND CLASS B SHARES\nBCE’s articles of amalgamation provide for an unlimited number of voting common shares and non-voting Class B shares, all without par value. The common shares and the Class B shares rank equally in the payment of dividends and in the distribution of assets if BCE is liquidated, dissolved or wound up, after payments due to the holders of preferred shares. No Class B shares were outstanding at December 31, 2019 and 2018.\nThe following table provides details about the outstanding common shares of BCE.\nIn Q1 2018, BCE repurchased and canceled 3,085,697 common shares for a total cost of $175 million through a NCIB. Of the total cost, $69 million represents stated capital and $3 million represents the reduction of the contributed surplus attributable to these common shares. The remaining $103 million was charged to the deficit.\nCONTRIBUTED SURPLUS\nContributed surplus in 2019 and 2018 includes premiums in excess of par value upon the issuance of BCE common shares and share-based compensation expense net of settlements.\n\nQuestion: What comprised of the total cost that went into the repurchase of common shares in 2018?\nProposed answer: NUMBER OF SHARES; reduction of the contributed surplus attributable to these common shares; charged to the deficit",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q3a7416851b",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (First Assistant Engineer), Steam Plants.\n\nQuestion: What is the primary operational difference between a nozzle reaction safety valve and a huddling chamber safety valve?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "The difference in valve relieving capacities.",
   "The manner in which steam pressure causes initial valve opening.",
   "The principle by which blowdown is accomplished.",
   "The manner in which lifting pressure is adjusted."
  ],
  "definitions": "- The difference in valve relieving capacities.: Answer \"The difference in valve relieving capacities.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The manner in which steam pressure causes initial valve opening.: Answer \"The manner in which steam pressure causes initial valve opening.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The principle by which blowdown is accomplished.: Answer \"The principle by which blowdown is accomplished.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- The manner in which lifting pressure is adjusted.: Answer \"The manner in which lifting pressure is adjusted.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q856a7f7108",
  "kind": "choice",
  "text": "FCC amateur radio licence exam: Technician class (Element 2) question pool 2026-2030.\nSubelement: Antennas and feed lines.\n\nQuestion: Which of the following describes a type of antenna loading?",
  "question": "Which answer choice is correct for this FCC amateur radio licence exam question?",
  "options": [
   "Electrically lengthening by inserting inductors in radiating elements",
   "Inserting a resistor in the radiating portion of the antenna to make it resonant",
   "Installing a spring in the base of a mobile vertical antenna to make it more flexible",
   "Strengthening the radiating elements of a beam antenna to better resist wind damage"
  ],
  "definitions": "- Electrically lengthening by inserting inductors in radiating elements: Answer \"Electrically lengthening by inserting inductors in radiating elements\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Inserting a resistor in the radiating portion of the antenna to make it resonant: Answer \"Inserting a resistor in the radiating portion of the antenna to make it resonant\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Installing a spring in the base of a mobile vertical antenna to make it more flexible: Answer \"Installing a spring in the base of a mobile vertical antenna to make it more flexible\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Strengthening the radiating elements of a beam antenna to better resist wind damage: Answer \"Strengthening the radiating elements of a beam antenna to better resist wind damage\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q27504950f1",
  "kind": "choice",
  "text": "Product: Pass & Seymour light switches. Both 2 way and 3 way light switches have been faulty. They were manufactured on or before 1995. (category: Electric Wire or Wiring Systems (Excl Panelboards Recept)\nIncident description: My house came with Pass & Seymour light switches, which was built around 1995.\n\nWithin the last 3 or so years, I've had to replace several of my light switches due to safety concerns.\n\nNearly all of the light switches arc and you can see light when you turn them on. They also create a crackle type of sound when you turn them on or off.\n\nThe more severe issue is that a couple of them have smoked and caused a breaker to throw. After taking off the wall plate and removing the switch, the switch fell apart in my hands. It was split in half. This particular switch powered my 40watt light bulb in my closet. So there wasn't a lot of load on it.\n\nSince then, I've been going around and replacing any that make noise.",
  "question": "Based on this consumer product incident report, what was the most serious outcome for the primary victim on the SaferProducts.gov severity scale?",
  "options": [
   "Code 19",
   "Code 24",
   "Code 53",
   "Code 58",
   "Code 49",
   "Code 35",
   "Code 33",
   "Code 39"
  ],
  "definitions": "- Code 19: The report describes a hazard or defect that was noticed before anything happened: the product did not actually fail, burn, break or harm anyone during use.\n- Code 24: The product actually failed, overheated, caught fire, broke or malfunctioned during use, but no person was physically hurt (property damage or a near miss only).\n- Code 53: The primary victim was physically hurt (for example a small burn, cut, bruise or shock), but no first aid was given and no medical care was sought.\n- Code 58: The primary victim was hurt and was treated only by themselves or another lay person (ice, cold water, bandage, ointment, over-the-counter medicine), with no doctor, clinic or hospital.\n- Code 49: The primary victim's highest level of care was a doctor, urgent-care clinic, dentist, nurse or other medical professional outside an emergency department, with no hospital admission.\n- Code 35: The primary victim was treated in a hospital emergency department (ER), possibly after an ambulance ride, and was released without being admitted.\n- Code 33: The primary victim was admitted to a hospital as an inpatient (for example overnight stay, intensive care, burn unit or surgery) and survived.\n- Code 39: The primary victim died from the incident, whether at the scene or later in hospital."
 },
 {
  "qid": "q01c25e0403",
  "kind": "choice",
  "text": "Women drown in an ocean of attention, men struggle in a desert without it.\n\n(Answer key: backhanded gendered compliments)",
  "question": "Which specific type of sexism does this sexist post show?",
  "options": [
   "threats of harm",
   "incitement and encouragement of harm",
   "descriptive attacks",
   "aggressive and emotive attacks",
   "dehumanising attacks and sexual objectification",
   "casual use of gendered slurs, profanities and insults",
   "immutable gender differences and stereotypes",
   "backhanded gendered compliments",
   "condescending explanations or unwelcome advice",
   "supporting mistreatment of individual women",
   "supporting systemic discrimination against women"
  ],
  "definitions": "- threats of harm: The author states an intent, willingness or wish to harm a woman or women, physically, sexually, emotionally or by violating their privacy.\n- incitement and encouragement of harm: The post urges or encourages others to harm women, or argues that harming women is justified, rather than only insulting them.\n- descriptive attacks: The post openly describes women in a derogatory way, such as negative generalisations about their abilities, intellect, character, morals, appearance or sexual behaviour.\n- aggressive and emotive attacks: The post expresses strong negative emotion such as hatred or disgust toward women, through stated feelings, baseless accusations or gendered slurs used to attack women.\n- dehumanising attacks and sexual objectification: The post compares women to animals, objects, vermin or refuse, or reduces them to sexual objects valued only for sex or their bodies.\n- casual use of gendered slurs, profanities and insults: The post uses a slur or insult that traditionally describes women, such as bitch or slut, casually rather than to deliberately attack women, often even aimed at a man.\n- immutable gender differences and stereotypes: The post asserts natural or unchangeable differences between men and women or uses gender stereotypes, including using women's traits to mock men; most sexist jokes fall here.\n- backhanded gendered compliments: The post seems to praise women but actually belittles them, implying they are weak, need protection or matter only for their looks.\n- condescending explanations or unwelcome advice: The post gives women patronising or unsolicited advice or explanations, implying they cannot understand or judge for themselves.\n- supporting mistreatment of individual women: The post denies, understates or justifies mistreatment of a particular woman or women, such as blaming a victim of abuse or harassment.\n- supporting systemic discrimination against women: The post denies, understates or justifies discrimination against women as a group, such as denying sexism exists or opposing women's rights."
 },
 {
  "qid": "q49435fa29c",
  "kind": "yes/no",
  "text": "remember when the HASHTAG_EASTASIA aka influenza was trendy? yeah i got a lot of, don’t get close to me fucken brownie looks, welcome to the racism fueled by this dumb ass... HASHTAG_EASTASIA+VIRUS smh 🤦🏽‍♂️",
  "question": "Under the East Asian prejudice codebook, which category does this tweet fall into?\nIs it wrong to answer \"discussion of East Asian prejudice\"?",
  "definitions": "- discussion of East Asian prejudice: The tweet talks about Sinophobia or anti-Asian racism, or debates names like 'China virus', without itself engaging in or explicitly countering the prejudice.\n- counter-speech against East Asian prejudice: The tweet explicitly challenges or condemns anti-East-Asian prejudice, slurs or stereotypes, or shows solidarity with East Asian people, without itself abusing the same target.\n- criticism of an East Asian entity: The tweet criticises an East Asian institution, affiliation or practice (such as the Chinese government hiding data) in a factual or reasoned way without abuse, stereotypes, conspiracy claims or normative 'they can't be trusted' framing.\n- hostility toward an East Asian entity: The tweet derogates or demeans an East Asian group, country, government or culture: extreme negative portrayal, hatred, conspiracy or bioweapon claims, 'they should leave', celebrating suffering, boycott calls, or mocking virus names; it outranks all other categories.\n- none of these: The tweet is none of the above: unrelated, neutral news, or mentions East Asia or the virus without hostility, criticism, counter-speech or discussion of prejudice, including a neutral geographic 'Wuhan virus'."
 },
 {
  "qid": "qf78dfedd73",
  "kind": "yes/no",
  "text": "Wikipedia page: The Notorious B.I.G. discography\nTable (first row is the header):\n| Title | Year | Peak chart positions US | Peak chart positions US R&B | Peak chart positions US Rap | Peak chart positions UK | Certifications | Album |\n| \"Can't You See\" (Total featuring The Notorious B.I.G.) | 1995 | 13 | 3 | — | 43 | RIAA: Gold | Total |\n| \"Player's Anthem\" (with Junior M.A.F.I.A.) | 1995 | 13 | 7 | 2 | — | RIAA: Gold | Conspiracy |\n| \"This Time Around\" (Michael Jackson featuring The Notorious B.I.G.) | 1995 | — | — | — | — |  | HIStory |\n| \"You Can't Stop the Reign\" (Shaquille O'Neal and The Notorious B.I.G.) | 1996 | — | — | — | 40 |  | You Can't Stop the Reign |\n| \"Only You\" (112 featuring The Notorious B.I.G., Mase and Puff Daddy) | 1996 | 13 | 3 | — | — | RIAA: Gold | 112 |\n| \"Get Money\" (with Junior M.A.F.I.A.) | 1996 | 17 | 4 | 1 | 63 | RIAA: Platinum | Conspiracy |\n| \"Crush on You\" (Lil' Kim featuring The Notorious B.I.G. & Lil Cease) | 1996 | 6 | — | 1 | 36 |  | Hard Core |\n| \"Stop the Gunfight\" (Trapp featuring 2Pac and The Notorious B.I.G.) | 1997 | 77 | 35 | 9 | — |  | Stop the Gunfight |\n| \"Be the Realist\" (Trapp featuring 2Pac and The Notorious B.I.G.) | 1997 | — | 65 | 14 | — |  | Stop the Gunfight |\n| \"Been Around the World\" (Puff Daddy featuring Mase and The Notorious B.I.G.) | 1997 | 2 | 7 | 1 | 4 |  | No Way Out |\n| \"It's All About the Benjamins\" (Puff Daddy featuring Lil' Kim, The LOX and The Notorious B.I.G.) | 1997 | 2 | 7 | 1 | 20 |  | No Way Out |\n| \"Victory\" (Puff Daddy featuring The Notorious B.I.G. and Busta Rhymes) | 1998 | 19 | 13 | 2 | — |  | No Way Out |\n| \"Runnin' (Dying to Live)\" (2Pac featuring The Notorious B.I.G.) | 2004 | 19 | 11 | 5 | 17 |  | Tupac: Resurrection |\n| \"Angels\" (Diddy-Dirty Money featuring The Notorious B.I.G. and Rick Ross) | 2009 | 116 | 71 | — | — |  | Last Train to Paris |\n\nQuestion: what were the only 2 years there were riaa gold certifications?\nProposed answer: 1995; 1996",
  "question": "Based only on the table, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer is exactly what the table gives for this question: the right cell, count or value, and when the question asks for several items, all of them and nothing else.\n- no: The proposed answer is not what the table gives: a different cell or value (for example a neighbouring row's entry), a count or number that is off, the opposite yes/no, or a list that misses or adds an item."
 },
 {
  "qid": "q4ba1d1256e",
  "kind": "yes/no",
  "text": "Evidence:\nWikipedia page: 2007 NLL season\nSection: Final standings\nTable (caption: East Division):\n| P | Team | GP | W | L | PCT | GB | Home | Road | GF | GA | Diff | GF/GP | GA/GP |\n|  |  |  |  |  |  |  |  |  |  |  |  |  |  |\n| 1 | Rochester Knighthawks – xyz | 16 | 14 | 2 | .875 | 0.0 | 8–0 | 6–2 | 249 | 194 | +55 | 15.56 | 12.12 |\n| 2 | Buffalo Bandits – x | 16 | 10 | 6 | .625 | 4.0 | 6–2 | 4–4 | 207 | 188 | +19 | 12.94 | 11.75 |\n| 3 | Minnesota Swarm – x | 16 | 9 | 7 | .562 | 5.0 | 4–4 | 5–3 | 200 | 207 | -7 | 12.50 | 12.94 |\n| 4 | Toronto Rock – x | 16 | 6 | 10 | .375 | 8.0 | 3–5 | 3–5 | 187 | 183 | +4 | 11.69 | 11.44 |\n| 5 | Chicago Shamrox | 16 | 6 | 10 | .375 | 8.0 | 4–4 | 2–6 | 176 | 191 | -15 | 11.00 | 11.94 |\n| 6 | Philadelphia Wings | 16 | 6 | 10 | .375 | 8.0 | 4–4 | 2–6 | 178 | 186 | -8 | 11.12 | 11.62 |\n| 7 | New York Titans | 16 | 4 | 12 | .250 | 10.0 | 3–5 | 1–7 | 195 | 233 | -38 | 12.19 | 14.56 |\n\nClaim: In the 2007 regular season East Division conference standings, the Rochester Knighthawks were in first place, with 14 wins and 2 losses, and the New York Titans were in last, with 4 wins and 12 losses.",
  "question": "Does the evidence support the claim?",
  "definitions": "- yes: The evidence (table cells, sentences and list items, with their page and headers) shows every part of the claim is true, directly or by simple reasoning such as counting, comparing or adding values.\n- no: The evidence does not establish the claim: it contradicts at least one part of it, or leaves some part unconfirmed (not enough information counts as no)."
 },
 {
  "qid": "qd419ee8e8b",
  "kind": "yes/no",
  "text": "Wikipedia page: 2017 Turkish constitutional referendum\nSection: Parliamentary voting\nTable:\n| Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines | Theoretical distribution of votes according to party lines |\n| Party | Party | Party | Leader | Party position | Total MPs | Eligible to vote | Voting yes | Voting no | Graphical representation |\n|  | AKP | Justice and Development Party | Binali Yıldırım | Yes | 317 | 315 | 315 | 0 | - |\n|  | CHP | Republican People's Party | Kemal Kılıçdaroğlu | No | 133 | 133 | 0 | 133 | - |\n|  | MHP | Nationalist Movement Party | Devlet Bahçeli | Yes | 39 | 39 | 33 | 6 | - |\n|  | HDP | Peoples' Democratic Party | Selahattin Demirtaş / Serpil Kemalbay | No | 59 | 48 | Boycotting | Boycotting | - |\n|  |  | Independents |  | No (both) | 2 | 2 | 0 | 2 | MPs ordered by party line. Black denotes MPs ineligible to vote |\n| Total | Total | Total | Total | Total | 550 | 537 | 348 | 141 | Referendum |\n\nClaim: Of the MHP's 39 MPs, 2 had voted against the amendments, the total number of MPs voting 'Yes' were 348.",
  "question": "Is the claim supported by the table?",
  "definitions": "- yes: Every fact in the claim matches the table and its page and section titles: each value is paired with the right row and column (right entity, year, number, place or name).\n- no: The table contradicts the claim: at least one stated value belongs to a different row than the one the claim ties it to (for example another year's number or another entry's name)."
 },
 {
  "qid": "q93ec2160c9",
  "kind": "choice",
  "text": "In the pituitary, haloperidol and <e1>sulpiride</e1> induced similar increases of mRNAs of pro-opiomelanocortin (<e2>POMC</e2>) (+65% and +73%), prolactin (PRL) (+821% and +840%) and growth hormone (GH) (+32% and +47%), but sulpiride induced a greater increase of D2R mRNA (+125%) than haloperidol (+92%).",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"sulpiride\" (marked <e1>) and the gene or protein \"POMC\" (marked <e2>)?",
  "options": [
   "substrate",
   "agonist-activator",
   "indirect downregulator",
   "product of",
   "substrate and product of",
   "activator",
   "antagonist",
   "inhibitor",
   "indirect upregulator",
   "agonist",
   "part of",
   "direct regulator (binder)",
   "agonist-inhibitor"
  ],
  "definitions": "- substrate: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- agonist-activator: The chemical is an agonist stated to increase the receptor's response when it binds, typically called a full or partial agonist that activates the receptor.\n- indirect downregulator: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- product of: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- substrate and product of: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical.\n- activator: The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead.\n- antagonist: The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist.\n- inhibitor: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- indirect upregulator: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- agonist: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- part of: The chemical is a structural part of the gene product, e.g. an amino-acid residue (Ser-15, cysteine residues), a sugar chain or another chemical group within the protein.\n- direct regulator (binder): The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it.\n- agonist-inhibitor: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist."
 },
 {
  "qid": "qe36d0f4b06",
  "kind": "yes/no",
  "text": "Problem:\nThe Happy Valley Kennel has 4 chickens, 2 dogs, and 5 cats. (Some people in Happy Valley like to keep chickens as pets!) In how many ways can the 11 animals be placed in a row of 11 cages, such that all of the animals of each type are in adjacent cages? (Two animals of the same species are considered distinguishable.)\n\nSolution steps so far:\nStep 1: I need to arrange the animals in a row, but I can't just do 11 factorial, because I have to keep the same species together.\nStep 2: That means I need to think of the groups of animals as blocks, rather than individual animals.\nStep 3: How many ways can I arrange the blocks of chickens, dogs, and cats?\nStep 4: Well, there are 3 blocks, so I can arrange them in 3 factorial ways.\nStep 5: For example, one way is CDC, where C stands for the block of cats, D for the block of dogs, and C for the block of chickens.\nStep 6: Another way is DCC, and so on.\nStep 7: Now, within each block, how many ways can I arrange the animals of that species?\nStep 8: For the chickens, there are 4 of them, so I can arrange them in 4 factorial ways.\nStep 9: For the dogs, there are 2 of them, so I can arrange them in 2 factorial ways.\nStep 10: For the cats, there are 5 of them, so I can arrange them in 5 factorial ways.\nStep 11: So, for any given arrangement of the blocks, I can multiply these numbers to get the number of ways to arrange the animals within the blocks.\nStep 12: For example, if I have CDC, then I can arrange the chickens in 4 factorial ways, the dogs in 2 factorial ways, and the cats in 5 factorial ways, for a total of 4! * 2! * 5! ways.\nStep 13: Since this is true for any arrangement of the blocks, I can multiply this by the number of ways to arrange the blocks, which is 3 factorial.\nStep 14: So, the total number of ways to arrange the animals is 3! * 4! * 2! * 5!.\n\nLast step (Step 15):\nThis is the answer, but I can simplify it a bit by canceling out some common factors.",
  "question": "Is the last step of this partial solution correct and acceptable as a next step?",
  "definitions": "- yes: The last step is acceptable: everything it states is correct, quickly verifiable and fits the earlier steps, whether it makes real progress or only restates or stalls; a final answer counts only if it is correct and follows from a complete solution.\n- no: The last step is not acceptable: it states something wrong (even partly), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a wrong, unjustified or incomplete final answer."
 },
 {
  "qid": "q8e0c664857",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | € million 2019 | € million 2018 |\n|  |  | (Restated)(a) |\n| Underlying operating profit before tax(b) | 9,947 | 9,463 |\n| Tax on underlying operating profit(c) | (2,536) | (2,432) |\n| Operating profit after tax | 7,411 | 7,031 |\n| Goodwill | 18,067 | 17,341 |\n| Intangible assets | 12,962 | 12,152 |\n| Property, plant and equipment | 12,062 | 12,088 |\n| Net assets held for sale | 81 | 108 |\n| Inventories | 4,164 | 4,301 |\n| Trade and other current receivables | 6,695 | 6,482 |\n| Trade payables and other current liabilities | (14,768) | (14,457) |\n| Period-end invested capital | 39,263 | 38,015 |\n| Average invested capital for the period | 38,639 | 38,749 |\n| Return on average invested capital | 19.2% | 18.1% |\nText:\nReturn on invested capital\nReturn on invested capital (ROIC) is a measure of the return generated on capital invested by the Group. The measure provides a guide rail for longterm value creation and encourages compounding reinvestment within the business and discipline around acquisitions with low returns and long payback. ROIC is calculated as underlying operating profit after tax divided by the annual average of: goodwill, intangible assets, property, plant and equipment, net assets held for sale, inventories, trade and other current receivables, and trade payables and other current liabilities.\n(a) Restated following adoption of IFRS 16. See note 1 and note 24 for further details.\n(b) See reconciliation of operating profit to underlying operating profit on page 30.\n(c) Tax on underlying operating profit is calculated as underlying operating profit before tax multiplied by underlying effective tax rate of 25.5% (2018: 25.7%) which is shown on page 30.\n\nQuestion: How is ROIC calculated?\nProposed answer: underlying operating profit before tax multiplied by underlying effective tax rate",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "q804a136088",
  "kind": "choice",
  "text": "Democrat women are so butt fucking ugly.",
  "question": "Which specific type of sexism does this sexist post show?",
  "options": [
   "Class W",
   "Class A",
   "Class L",
   "Class F",
   "Class E",
   "Class Z",
   "Class H",
   "Class M",
   "Class S",
   "Class U",
   "Class C"
  ],
  "definitions": "- Class W: The author states an intent, willingness or wish to harm a woman or women, physically, sexually, emotionally or by violating their privacy.\n- Class A: The post urges or encourages others to harm women, or argues that harming women is justified, rather than only insulting them.\n- Class L: The post openly describes women in a derogatory way, such as negative generalisations about their abilities, intellect, character, morals, appearance or sexual behaviour.\n- Class F: The post expresses strong negative emotion such as hatred or disgust toward women, through stated feelings, baseless accusations or gendered slurs used to attack women.\n- Class E: The post compares women to animals, objects, vermin or refuse, or reduces them to sexual objects valued only for sex or their bodies.\n- Class Z: The post uses a slur or insult that traditionally describes women, such as bitch or slut, casually rather than to deliberately attack women, often even aimed at a man.\n- Class H: The post asserts natural or unchangeable differences between men and women or uses gender stereotypes, including using women's traits to mock men; most sexist jokes fall here.\n- Class M: The post seems to praise women but actually belittles them, implying they are weak, need protection or matter only for their looks.\n- Class S: The post gives women patronising or unsolicited advice or explanations, implying they cannot understand or judge for themselves.\n- Class U: The post denies, understates or justifies mistreatment of a particular woman or women, such as blaming a victim of abuse or harassment.\n- Class C: The post denies, understates or justifies discrimination against women as a group, such as denying sexism exists or opposing women's rights."
 },
 {
  "qid": "qfdf771ea13",
  "kind": "choice",
  "text": "I need help.   The AC isn't working in my room.  I need it fixed immediately!",
  "question": "What task does the user want the assistant's help with?",
  "options": [
   "schedule apartment viewing",
   "search for apartment",
   "check bank balance",
   "report bank fraud",
   "doctor follow-up instructions",
   "schedule doctor appointment",
   "book hotel room",
   "search for hotel",
   "hotel room service request",
   "schedule meeting",
   "plan a party",
   "RSVP to a party",
   "book flight",
   "search for flight",
   "book restaurant table",
   "search for restaurant",
   "book a ride",
   "change or cancel ride",
   "check ride status",
   "spaceship access codes",
   "spaceship life support repair",
   "trip directions",
   "play trivia",
   "weather forecast"
  ],
  "definitions": "- schedule apartment viewing: The user wants to book a time to view a specific apartment or building, giving the apartment name, day and time for the viewing.\n- search for apartment: The user wants to find an apartment matching criteria such as number of bedrooms, floor, price budget, elevator or other amenities.\n- check bank balance: The user wants to learn the current balance of their bank account, usually after identifying themselves with account number, PIN or security questions.\n- report bank fraud: The user wants to report suspicious or unauthorised activity on their bank account, such as unknown transfers, withdrawals or a lost card being used.\n- doctor follow-up instructions: The user had a recent appointment and wants to find out or confirm the doctor's orders, such as how often to take their medicine.\n- schedule doctor appointment: The user wants to book a new appointment with a doctor, often mentioning symptoms and the doctor and day they prefer.\n- book hotel room: The user wants to reserve a room at a named hotel for specific dates, possibly with a custom request such as a balcony.\n- search for hotel: The user wants to find a hotel or learn about one, such as its rating, location in town or price, without making a reservation.\n- hotel room service request: The user is already staying at a hotel and wants a service delivered to their room at a given time, such as food or a repair.\n- schedule meeting: The user wants to set up a meeting with a named person at a specific day and time, often stating its duration and reason.\n- plan a party: The user wants to organise and host a party, such as reserving a venue for a day and time, arranging food, drinks or guests.\n- RSVP to a party: The user has been invited to someone else's party and wants to confirm attendance, arrival time, number of guests, parking or dietary needs.\n- book flight: The user wants to reserve or book a flight they have already picked, usually giving its flight id, rather than searching routes and dates.\n- search for flight: The user wants to find flights matching a route, date, airline, seat class or price limit, rather than reserving a flight id they already have.\n- book restaurant table: The user wants to reserve a table at a named restaurant for a number of people at a given time.\n- search for restaurant: The user wants to find or learn about a restaurant by price range, cuisine, rating, location or delivery, without reserving a table.\n- book a ride: The user wants a new taxi, Lyft, Uber or other car to pick them up and take them somewhere, possibly naming a vehicle or driver preference.\n- change or cancel ride: The user already booked a ride and wants to modify it, such as changing departure or arrival location or time, or cancel it.\n- check ride status: The user already booked a ride and wants to know where it is or why it has not arrived yet.\n- spaceship access codes: The user is locked out of a spaceship deck during an attack and needs the onboard computer's help with access or clearance codes to unlock the door.\n- spaceship life support repair: The spaceship's life support is failing and the user directs the repair robot to open the sealed engineering deck by tampering with a lock and swapping cables.\n- trip directions: The user is lost or wants step-by-step directions to a destination by car, on foot or by public transit, rather than a booked ride.\n- play trivia: The user wants to play a trivia game, asking for questions (often starting from a given question number) and giving answers.\n- weather forecast: The user wants to know the current or upcoming weather, such as temperature or rain, for their city or another place and day."
 },
 {
  "qid": "q8174d59a44",
  "kind": "choice",
  "text": "41YM FELL FROM 12 15FTH SCAFFOLDING WORK LANDING ONTO BUSHES ANKLE FX",
  "question": "Which OIICS event category describes how this worker's injury happened?",
  "options": [
   "Code 25",
   "Code 34",
   "Code 52",
   "Code 17",
   "Code 49",
   "Code 36",
   "Code 55",
   "Code 22",
   "Code 16",
   "Code 57",
   "Code 32",
   "Code 58",
   "Code 24",
   "Code 53",
   "Code 46",
   "Code 10",
   "Code 38",
   "Code 40",
   "Code 50",
   "Code 27",
   "Code 12",
   "Code 42",
   "Code 54",
   "Code 39"
  ],
  "definitions": "- Code 25: The worker was riding an animal or a non-motorized vehicle (horse, bull, bicycle, scooter, skateboard) and fell, was thrown or crashed.\n- Code 34: The worker was pricked by a needle described as clean, sterile, unused or otherwise free of blood or other harmful substances (for example a sewing-machine needle).\n- Code 52: A harmful substance was touched, inhaled, swallowed or injected: chemicals, caustics, cleaning agents, fumes, gases, pepper spray, allergens, blood or body fluids, including needlesticks with used or dirty needles.\n- Code 17: The worker was cut, punctured, bruised or fractured by contact with an object or equipment, but the narrative does not say whether they were struck by it, struck against it, caught in it or rubbed by it.\n- Code 49: A collapsing structure or material struck, caught or buried the worker: trench or excavation cave-in, or collapse of a ceiling, wall, floor, scaffold or stacked material not set off by an explosion or fire.\n- Code 36: Extreme heat or cold caused the injury without a fire or explosion: burns or scalds from hot liquids, steam, food, surfaces or equipment, heat exhaustion or stroke, frostbite or hypothermia.\n- Code 55: The worker's own movement drove a body part into an object: bumping, banging, hitting or jamming against something, stepping on a nail or sharp object, or walking into equipment, with no fall.\n- Code 22: The worker deliberately jumped down from a higher place (truck bed, trailer, dock, ladder, scaffold, equipment) and was hurt on landing.\n- Code 16: Radiation or noise caused the injury: welding arc flash burns to the eyes, ultraviolet or laser light, ionizing radiation, or loud noise damaging hearing.\n- Code 57: A person deliberately hurt the worker (assault, punching, kicking, biting, stabbing, shooting, choking, shoving, robbery or a fight, including by patients, inmates or suspects); this outranks any fall, contact or exposure that followed.\n- Code 32: The worker fell from a higher place to a lower one: off a ladder, roof, scaffold, stool, chair, vehicle, dock or platform, down stairs or steps, or into a hole, pit or trench.\n- Code 58: The worker slipped, tripped, stumbled or lost balance but did NOT fall, and was hurt by the slip itself or by catching or twisting to recover.\n- Code 24: The worker was on foot, not in or on a vehicle, and was struck, run over or pinned by a moving car, truck, forklift or other vehicle, on or off the road.\n- Code 53: An explosion, blast or sudden burst (of a container, tank, tire, battery, aerosol can or pressurized vessel) caused the injury, including burns or debris from it.\n- Code 46: An uncontrolled fire caused the injury: burns, smoke inhalation, overheating, or being struck or cut while fighting or escaping a fire; it outranks the contact, fall or exertion that happened during it.\n- Code 10: The worker was on or boarding a boat, barge or ship and was hurt by the vessel's motion, sinking or collision, or by falling on board, overboard or from the vessel.\n- Code 38: Vibration caused the injury: prolonged use of vibrating tools or equipment (jackhammers, grinders), or being jolted and bounced while operating a vehicle or machine.\n- Code 40: Another person hurt the worker with no assault or fight described: bumped, collided with, fell or landed on, grabbed or struck the worker accidentally, during a seizure, a game or while being cared for.\n- Code 50: The worker fell to the floor, ground or other surface they were standing or walking on (slip-and-fall, trip-and-fall, falling against something at that level); used when no height, stairs, ladder or vehicle is mentioned.\n- Code 27: Breathing was blocked or oxygen was lacking: choking on food or an object, drowning, suffocation or an oxygen-deficient space, with no assault or vehicle incident.\n- Code 12: The worker was on or operating a motorized land vehicle or mobile machine away from public traffic (forklift, tractor, ATV, riding mower, golf cart, loader) that tipped, rolled, crashed or threw them off.\n- Code 42: The worker fell or jumped from a height and a personal fall arrest system (harness, lanyard, lifeline) stopped or caught the fall.\n- Code 54: The injury happened aboard or from an aircraft in operation: turbulence, hard landing, crash, or parachuting or rappelling from it.\n- Code 39: Pain or a disorder from repeating small, low-force motions over time (typing, keying, scanning, gripping, cutting, using the hands or wrists all day), with no single heavy exertion."
 }
]
