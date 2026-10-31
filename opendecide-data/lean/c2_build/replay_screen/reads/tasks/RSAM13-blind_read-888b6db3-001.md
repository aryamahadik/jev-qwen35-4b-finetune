# A46 replay label-noise blind read RSAM13-blind_read-888b6db3-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSAM13-blind_read-888b6db3-001.json

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
  "qid": "q60c9613b53",
  "kind": "yes/no",
  "text": "A 26-year-old woman is found wandering in the street at 3 AM in the morning shouting about a new cure for cancer. When interviewed in the psychiatric triage unit, she speaks rapidly without pauses and continues to boast of her upcoming contribution to science. When the physician attempts to interrupt her, she becomes angry and begins to shout about all of her “accomplishments” in the last week. She states that because she anticipates a substantial sum of money from the Nobel Prize she will win, she bought a new car and diamond earrings. In addition, the patient divulges that she is 8 weeks pregnant with a fetus who is going to “change the course of history.” Her chart in the electronic medical record shows an admission 3 months ago for suicidality and depression. She was released on fluoxetine after being stabilized, but the patient now denies ever taking any medications that “could poison my brain.” Urine pregnancy test is positive. Which of the following is a potential adverse outcome of the drug shown to reduce suicide-related mortality in this patient?\n\nAnswer choices:\nA. Tardive dyskinesia\nB. Atrialization of the right ventricle in the patient’s fetus\nC. Weight loss\nD. Stevens-Johnson syndrome\nE. Hyperprolactinemia and galactorrhea\n\nProposed answer: D. Stevens-Johnson syndrome",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q98253b8b39",
  "kind": "yes/no",
  "text": "We performed a study in spontaneous hypertensive rats (SHR) to determine whether <e1>carvedilol</e1>, a nonselective <e2>beta-adrenoceptor</e2> antagonist, activates capsaicin-sensitive sensory neurons (CSSNs), thereby promoting the release of calcitonin gene-related peptide (CGRP), a neuropeptide with an important role in maintenance of cardiovascular homeostasis.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"carvedilol\" (marked <e1>) and the gene or protein \"beta-adrenoceptor\" (marked <e2>)?\nIs it wrong to answer \"antagonist\"?",
  "definitions": "- antagonist: The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist.\n- agonist: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- inhibitor: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- direct regulator (binder): The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it.\n- indirect upregulator: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment."
 },
 {
  "qid": "q4deaa1fd0e",
  "kind": "choice",
  "text": "We have previously demonstrated that, in the presence of the lysine analogue epsilon-aminocaproic acid, <e2>apolipoprotein(a)</e2> [apo(a)] undergoes a conformational change from a closed to an open structure that is characterized by a change in <e1>tryptophan</e1> fluorescence, an increase in the radius of gyration, an alteration of domain stability, and an enhancement in the efficiency of covalent lipoprotein(a) [Lp(a)] formation.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"tryptophan\" (marked <e1>) and the gene or protein \"apolipoprotein(a)\" (marked <e2>)?",
  "options": [
   "Code 15",
   "Code 42",
   "Code 27",
   "Code 50",
   "Code 17",
   "Code 24",
   "Code 57",
   "Code 45",
   "Code 46",
   "Code 43",
   "Code 32",
   "Code 56",
   "Code 18"
  ],
  "definitions": "- Code 15: The chemical binds or physically interacts with the gene product (binder, ligand, affinity, modulator) but the text does not say whether it activates, inhibits, agonises or antagonises it.\n- Code 42: The chemical raises the amount, expression, release or activity of the gene product through other targets: e.g. X induced Y expression, increased Y levels, secretion or phosphorylation after X treatment.\n- Code 27: The chemical is both a substrate and a product of the gene product's reaction, e.g. an enzyme that interconverts or exchanges that chemical.\n- Code 50: The chemical is an antagonist or blocker of the gene product (usually a receptor): it binds and prevents or reduces the receptor's response to an agonist.\n- Code 17: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased.\n- Code 24: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- Code 57: The chemical is produced by the gene product: it is the product of the enzyme's reaction or is released or exported by the transporter.\n- Code 45: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist.\n- Code 46: The chemical is an agonist stated to increase the receptor's response when it binds, typically called a full or partial agonist that activates the receptor.\n- Code 43: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- Code 32: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- Code 56: The chemical is a structural part of the gene product, e.g. an amino-acid residue (Ser-15, cysteine residues), a sugar chain or another chemical group within the protein.\n- Code 18: The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead."
 },
 {
  "qid": "qb17c8eef5f",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nSee Heiser, 466 F.Supp.2d at 270-71 (concluding that there was insufficient evidence to determine that the IRGC is commercial); Blais, 459 F.Supp.2d at 60-61 (same); Prevatt v. Islamic Republic of Iran, 421 F.Supp.2d 152, 162 (D.D.C.2006) (Lam-berth, J.) (finding no evidence that the IRGC’s functions are commercial rather than governmental); Holland v. Islamic Republic of Iran, 496 F.Supp.2d 1, 32-33 (D.D.C.2005) (Kollar-Kotelly, J.) (declining to award punitive damages but acknowledging that the IRGC “appears to be a true ‘instrumentality’ of the dominant party of the state, used by the government and its officials in largely ‘illegal,’ paramilitary, and sub rosa activities”); Salazar v. Islamic Republic of Iran, 370 F.Supp.2d 105, 116 (D.D.C.2005) (Bates, J.) (<HOLDING>); Welch v. Islamic Republic of Iran, Civ. A.\n\nCandidate holding for <HOLDING>: holding that a party waived the right to allege contrary facts on appeal eg that defendant was not an agent or instrumentality of the mexican government for sovereign immunity purposes where the party alleged that the defendant was an agent or instrumentality in its complaint",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "q02464735ff",
  "kind": "choice",
  "text": "Graffiti on palm ridge park utility box",
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
  "qid": "q8c93e35bbb",
  "kind": "yes/no",
  "text": "Court opinion passage (the parenthetical after one citation is replaced by <HOLDING>):\nSee Delmarva Power & Light Co. v. United States, 79 Fed.Cl. 205 (2007). Furthermore, the only claim for which this Court has awarded damages is Meritor’s derivative breach of contract claim, a claim which is currently owned by the FDIC. Consequently, the Government asserts that the Plaintiff-Intervenor’s claims have not been assigned, and the Court agrees that the Act does not bar the current shareholders from lawfully receiving the distribution of the award. Alternatively, the Plaintiff-Intervenor asserts that § 1821(d)(ll) allows only the owner at the time of the seizure to assert a takings claim. See United States v. Dow, 357 U.S. 17, 20-21, 78 S.Ct. 1039, 2 L.Ed.2d 1109 (1958) (<HOLDING>); Maniere v. United States, 31 Fed.Cl. 410,\n\nCandidate holding for <HOLDING>: holding that the owners at the time the land was seized are owed compensation rather than the subsequent purchasers",
  "question": "Does the candidate statement correctly give the holding of the case that this court opinion cites at the <HOLDING> marker?",
  "definitions": "- yes: The candidate is the holding the citing court attributes to the case cited at <HOLDING>: it states the legal rule or outcome of that cited case and supports the exact proposition the passage uses it for.\n- no: The candidate is a holding from a different case: its rule, statute, jurisdiction, party situation or outcome does not match the proposition the passage cites that case for, even if it shares topic words."
 },
 {
  "qid": "qa83c02dc51",
  "kind": "choice",
  "text": "U.S. Coast Guard merchant mariner credential exam (OSV – Assistant Engineer), Engineering Safety & Environmental Protection.\n\nQuestion: If flammable vapors have penetrated a gas free space, which of the following actions would be the most hazardous to perform?",
  "question": "Which answer choice is correct for this U.S. Coast Guard merchant mariner licensing exam question?",
  "options": [
   "Opening switches in the space to de-energize circuits",
   "Closing switches adjacent to the space to operate vent fans",
   "Leaving electrical circuits energized in the space",
   "Securing all power to the space from a remote location"
  ],
  "definitions": "- Opening switches in the space to de-energize circuits: Answer \"Opening switches in the space to de-energize circuits\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Closing switches adjacent to the space to operate vent fans: Answer \"Closing switches adjacent to the space to operate vent fans\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Leaving electrical circuits energized in the space: Answer \"Leaving electrical circuits energized in the space\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- Securing all power to the space from a remote location: Answer \"Securing all power to the space from a remote location\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "qeeb7cba525",
  "kind": "choice",
  "text": "Well I think I speak for all men when I say I hate when professional women use Instagram to get business instead of dates,",
  "question": "This post is sexist. Which specific type of sexism does it show?",
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
  "definitions": "- threats of harm: The author states an intent, willingness or wish to harm a woman or women, whether physically, sexually, emotionally or by violating their privacy.\n- incitement and encouragement of harm: The post urges or encourages others to harm a woman or women, or argues that harming women is justified; it calls for or endorses harm rather than only insulting women.\n- descriptive attacks: The post openly describes women in a derogatory way, for example negative generalisations about their abilities, intellect, character, morals, appearance or sexual behaviour.\n- aggressive and emotive attacks: The post expresses strong negative emotion such as hatred or disgust toward women, for example through the author's stated feelings, baseless accusations, or gendered slurs used to attack women.\n- dehumanising attacks and sexual objectification: The post compares women to animals, objects, vermin or refuse, or reduces them to sexual objects valued only for sex or their bodies.\n- casual use of gendered slurs, profanities and insults: The post uses a slur or insult that traditionally describes women, such as bitch or slut, casually and not to deliberately attack women, often even aimed at a man.\n- immutable gender differences and stereotypes: The post asserts natural, essential or unchangeable differences between men and women or uses gender stereotypes, including using women's traits to mock men; most sexist jokes fall here.\n- backhanded gendered compliments: The post seems to praise women but actually belittles them, for example implying they are weak, need protection or matter only for their looks.\n- condescending explanations or unwelcome advice: The post gives women patronising or unsolicited advice or explanations on matters they know more about ('mansplaining'), implying they cannot understand or judge for themselves.\n- supporting mistreatment of individual women: The post supports mistreatment of a particular woman or women by denying, understating or justifying it, for example blaming a victim of abuse or harassment.\n- supporting systemic discrimination against women: The post supports discrimination against women as a group by denying, understating or justifying it, for example denying that sexism exists or opposing women's rights."
 },
 {
  "qid": "q2790a60e84",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | July 31, 2019 | July 31, 2018 |\n| Exercise of stock options to purchase common stock | 216,727 | 537,064 |\n| Vesting of restricted stock awards | 2,384,673 | 2,932,155 |\n| Shares available for grant under stock plans | 24,776,361 | 21,592,494 |\n| Total common stock reserved for issuance | 27,377,761 | 25,061,713 |\nText:\nCommon Stock Reserved for Issuance\nAs of July 31, 2019 and 2018, the Company was authorized to issue 500,000,000 shares of common stock with a par value of $0.0001 per share and, of these, 82,140,883 and 80,611,698 shares of common stock were issued and outstanding, respectively. Per the terms of the Company’s 2011 Stock Plan, on January first of each year, an additional number of shares equal to up to 5% of the number of shares of common stock issued and outstanding on the preceding December 31st is added to the Company’s 2011 Stock Plan reserve.\nAs of July 31, 2019 and 2018, the Company had reserved shares of common stock for future issuance as follows:\nIn March 2018, the Company completed a public offering of 2,628,571 shares of its common stock. The public offering price of the shares sold in the offering was $87.50 per share. No shares were sold by the Company’s stockholders in this public offering.\n\nQuestion: What was the average Vesting of restricted stock awards for 2018 and 2019?\nProposed answer: 2,658,414",
  "question": "Based only on the report's table and text, is the proposed answer to the question correct?",
  "definitions": "- yes: The proposed answer matches what the table and text give for this exact question: the same value at the precision shown, the same sign or direction, the same unit or scale (%, thousand, million, billion), and for list answers exactly the right items.\n- no: The proposed answer does not match: a different value or item (for example another year's figure or another line item), a wrong sign or wrong base for a change, a wrong unit or scale such as million instead of thousand, or a list that misses or adds an item."
 },
 {
  "qid": "qfbc7b0be3e",
  "kind": "choice",
  "text": "Heading: IP user expressing incivility in almost every post on The Troubles article.\nuser:131.164.141.250 \n [diff] Kind of talk can't possibly be of any benefit to our project across the board, let alone on such a controversial article. The above diff is one of the most serious I could find, but most of this IP editor's posts contain varying degrees of hostility. I can't believe that anyone would come here with a good general understanding of Wikipedia's processes and let themselves go so quickly. I'm therefore also recommending a check user.",
  "question": "Which Wikipedia noticeboard or help page is the right place for this post?",
  "options": [
   "Option H",
   "Option C",
   "Option W",
   "Option J",
   "Option R",
   "Option M",
   "Option A",
   "Option X",
   "Option G"
  ],
  "definitions": "- Option H: Urgent or chronic user-conduct problems that need an administrator to act: harassment, disruption, personal attacks, block evasion or misuse of tools.\n- Option C: Problems with content about a living (or recently dead) person: unsourced or defamatory claims, privacy, undue negative material about them.\n- Option W: Editors who appear to edit about themselves, their employer, clients or products (paid or undisclosed promotional editing).\n- Option J: Articles promoting or giving undue credence to fringe, pseudoscientific or conspiracy ideas that depart from mainstream scholarship.\n- Option R: Questions about how to use or edit Wikipedia itself: creating articles, citing, formatting, uploading images, account and editing problems.\n- Option M: Whether an article's wording, weight or balance is biased or gives undue weight to one viewpoint, when sourcing itself is not the issue.\n- Option A: Whether article content goes beyond what sources say: editors' own analysis, synthesis of several sources into a new conclusion, or unsourced interpretation.\n- Option X: Whether a particular source (outlet, book, website, paper) is reliable enough to cite for a given statement in an article.\n- Option G: Technical problems and questions about the site's software: bugs, templates, gadgets, scripts, rendering, bots, tools and MediaWiki features."
 },
 {
  "qid": "qb569ef786d",
  "kind": "choice",
  "text": "40 YOF ON DUTY AT SUBJECT INJURED SHOULDER WHILE PUSHING ASTRETCHER DX RIGHT SHOULDER STRAIN",
  "question": "Which OIICS event category describes how this worker's injury happened?",
  "options": [
   "pedestrian struck by vehicle",
   "aircraft incident",
   "multiple types of overexertion and bodily reaction",
   "other exertions or bodily reactions",
   "overexertion involving outside sources",
   "fire",
   "exposure to radiation or noise",
   "fall on same level",
   "struck by object or equipment",
   "repetitive motions involving microtasks",
   "jump to lower level",
   "water vehicle incident",
   "overexertion or bodily reaction, type unspecified",
   "exposure to temperature extremes"
  ],
  "definitions": "- pedestrian struck by vehicle: The worker was on foot, not in or on a vehicle, and was struck, run over or pinned by a moving car, truck, forklift or other vehicle, on or off the road.\n- aircraft incident: The injury happened aboard or from an aircraft in operation: turbulence, hard landing, crash, or parachuting or rappelling from it.\n- multiple types of overexertion and bodily reaction: The narrative gives two or more different exertion types together as the cause (for example lifting and bending, or carrying and twisting), with no other event.\n- other exertions or bodily reactions: Injury from the worker's own body motion with no outside load and no fall: bending, reaching, twisting, kneeling, squatting, climbing, standing up, walking, running or stepping wrong.\n- overexertion involving outside sources: Strain or pain from exerting force on an outside object or person: lifting, pushing, pulling, carrying, holding, throwing, moving or transferring loads or patients, with no fall or being struck.\n- fire: An uncontrolled fire caused the injury: burns, smoke inhalation, overheating, or being struck or cut while fighting or escaping a fire; it outranks the contact, fall or exertion that happened during it.\n- exposure to radiation or noise: Radiation or noise caused the injury: welding arc flash burns to the eyes, ultraviolet or laser light, ionizing radiation, or loud noise damaging hearing.\n- fall on same level: The worker fell to the floor, ground or other surface they were standing or walking on (slip-and-fall, trip-and-fall, falling against something at that level); used when no height, stairs, ladder or vehicle is mentioned.\n- struck by object or equipment: A moving object hit the worker: something fell, was dropped, flew, swung, rolled or slipped onto or into them, including a tool that slipped in use; the object moved, not the worker (a moving vehicle hitting a worker on foot is a pedestrian incident).\n- repetitive motions involving microtasks: Pain or a disorder from repeating small, low-force motions over time (typing, keying, scanning, gripping, cutting, using the hands or wrists all day), with no single heavy exertion.\n- jump to lower level: The worker deliberately jumped down from a higher place (truck bed, trailer, dock, ladder, scaffold, equipment) and was hurt on landing.\n- water vehicle incident: The worker was on or boarding a boat, barge or ship and was hurt by the vessel's motion, sinking or collision, or by falling on board, overboard or from the vessel.\n- overexertion or bodily reaction, type unspecified: The worker has a strain, sprain or muscle pain from exertion at work, but the narrative does not say what motion or activity (lifting, pushing, bending, repetitive use) caused it.\n- exposure to temperature extremes: Extreme heat or cold caused the injury without a fire or explosion: burns or scalds from hot liquids, steam, food, surfaces or equipment, heat exhaustion or stroke, frostbite or hypothermia."
 },
 {
  "qid": "qc24f72c37e",
  "kind": "choice",
  "text": "Health topic: Ewing sarcoma\nPassage: This condition is generally not inherited but arises from a mutation in the body's cells that occurs after conception (somatic mutation). Most cases are considered to be sporadic. However, the incidence of neuroectodermal and stomach malignancies is increased among family members of patients with tumors of the Ewing sarcoma family. A search of the medical literature did identify a very small number of cases of Ewing sarcoma among siblings. To access articles on this topic, click here.",
  "question": "Which consumer-health question about the named topic does this passage from an NIH health page answer?",
  "options": [
   "causes",
   "complications",
   "diagnosis and tests",
   "how common it is",
   "inheritance pattern",
   "outlook (prognosis)",
   "prevention",
   "research and clinical trials",
   "signs and symptoms",
   "stages",
   "treatment",
   "what it is (overview)",
   "who is at risk"
  ],
  "definitions": "- causes: Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or environmental agent that produces it (not who is more likely to get it).\n- complications: Describes further problems or conditions the disease can lead to.\n- diagnosis and tests: Explains how the condition is detected or confirmed: exams, lab tests, imaging, genetic testing and diagnostic criteria.\n- how common it is: Gives the prevalence or incidence: how many people or what share of a population have it, or that it is rare or its frequency is unknown.\n- inheritance pattern: States how the condition is passed down in families (autosomal dominant or recessive, X-linked, mitochondrial, de novo) and the chance relatives are affected.\n- outlook (prognosis): Describes the expected course and outcome: survival, recovery, progression or life expectancy.\n- prevention: Describes steps that lower the chance of getting the condition or its spread, such as vaccines, hygiene, lifestyle or avoiding exposures.\n- research and clinical trials: Describes research being done or funded on the condition: studies, trials, and what scientists are investigating.\n- signs and symptoms: Describes what people with the condition experience or show: symptoms, physical signs, features and how they present or vary.\n- stages: Explains how the disease (usually a cancer) is staged: how spread is measured and what each stage means.\n- treatment: Describes how the condition is treated or managed: therapies, drugs, surgery, and standard or trial treatment options.\n- what it is (overview): Defines or describes the condition or topic in general (what it is, which body part it affects, its main features) without being mainly about one aspect below.\n- who is at risk: Names risk factors or groups more likely to get the condition (age, sex, family history, exposures), rather than its mechanism."
 },
 {
  "qid": "q0f91aaa0a9",
  "kind": "choice",
  "text": "Heading: Criticism of Swaminarayan sect\nFour or more editors have been pressuring at the Talk:Criticism of Swaminarayan sect want to include all of the justification from the sect. They tried to give it so by giving more weight to apology and justification. As WP:Criticism states criticism article is for negative viewpoints of the particular philosophy and religion then why justification from the sect can be included in the article? Like, Criticism of Marxism exists and there is no such balancing and inclusion of the arguments regarding justification from marxists. Same with Criticism of Islam, Criticism of Christianity, Criticism of Buddhism and Criticism of Religion. If the article will go for balancing the thoughts and inclusion of justification from apologetic then how it will serve the purpose of the criticism as per heading? I tried to let them understand that this is sub POV of Swaminarayana sect in which negative points are included by keeping NPOV in mind but none of them is agreeing on the issue and most of them are not even extended confirmed and pressurising to include positive viewpoints. I had made the page by looking at the pages stated above and if all the things will be added in this article then how it will be different from original POV article i.e. Swaminarayan sect. I am looking for the comments of more experienced editors and administrators regarding this page.",
  "question": "Which Wikipedia noticeboard or help page is the right place for this post?",
  "options": [
   "Class B",
   "Class T",
   "Class N",
   "Class G",
   "Class F",
   "Class R",
   "Class Q",
   "Class K",
   "Class H"
  ],
  "definitions": "- Class B: Urgent or chronic user-conduct problems that need an administrator to act: harassment, disruption, personal attacks, block evasion or misuse of tools.\n- Class T: Problems with content about a living (or recently dead) person: unsourced or defamatory claims, privacy, undue negative material about them.\n- Class N: Editors who appear to edit about themselves, their employer, clients or products (paid or undisclosed promotional editing).\n- Class G: Articles promoting or giving undue credence to fringe, pseudoscientific or conspiracy ideas that depart from mainstream scholarship.\n- Class F: Questions about how to use or edit Wikipedia itself: creating articles, citing, formatting, uploading images, account and editing problems.\n- Class R: Whether an article's wording, weight or balance is biased or gives undue weight to one viewpoint, when sourcing itself is not the issue.\n- Class Q: Whether article content goes beyond what sources say: editors' own analysis, synthesis of several sources into a new conclusion, or unsourced interpretation.\n- Class K: Whether a particular source (outlet, book, website, paper) is reliable enough to cite for a given statement in an article.\n- Class H: Technical problems and questions about the site's software: bugs, templates, gadgets, scripts, rendering, bots, tools and MediaWiki features."
 },
 {
  "qid": "q818f1c5e6b",
  "kind": "yes/no",
  "text": "To gain a better understanding of this oxime specificity problem for future design of improved reactivators, we conducted a QSAR analysis for <e1>oxime</e1> reactivation of <e2>AChE</e2> inhibited by OP agents and their analogues.",
  "question": "Which chemical-protein relation does the sentence state between the chemical \"oxime\" (marked <e1>) and the gene or protein \"AChE\" (marked <e2>)?\nIs it wrong to answer \"inhibitor\"?",
  "definitions": "- inhibitor: The chemical lowers the activity or function of the gene product, by binding it or with no mechanism stated ('X inhibits Y', 'Y inhibitor X'); lower amounts or expression of Y are indirect downregulation instead.\n- activator: The chemical raises the activity or function of the gene product, by binding it or with no mechanism stated ('X activates Y', 'X enhanced Y activity'); higher amounts or expression of Y are indirect upregulation instead.\n- substrate: The gene product (an enzyme or transporter) acts on the chemical: the chemical is metabolised, converted, modified or transported by it.\n- agonist-inhibitor: The chemical is an agonist that binds the receptor and decreases its response, typically an inverse agonist.\n- indirect downregulator: The chemical lowers the amount, expression, release or activity of the gene product through other targets: e.g. reduced Y mRNA or protein levels, decreased Y secretion or phosphorylation after X treatment.\n- agonist: The chemical is an agonist of the gene product (usually a receptor) that binds and triggers its response, with no statement of whether the response is increased or decreased."
 },
 {
  "qid": "q487ab73ec9",
  "kind": "choice",
  "text": "Health topic: Weill-Marchesani syndrome\nPassage: The diagnosis of Weill-Marchesani syndrome is made on the presence of the characteristic signs and symptoms. Genetic testing can help confirm the diagnosis. The Genetic Testing Registry (GTR) provides information on the genetic tests available for Weill-Marchesani syndrome. The intended audience for the GTR is health care providers and researchers. Patients and consumers with specific questions about a genetic test should contact a health care provider or a genetics professional.",
  "question": "Which consumer-health question about the named topic does this passage from an NIH health page answer?",
  "options": [
   "causes",
   "complications",
   "diagnosis and tests",
   "how common it is",
   "inheritance pattern",
   "outlook (prognosis)",
   "prevention",
   "research and clinical trials",
   "signs and symptoms",
   "stages",
   "treatment",
   "what it is (overview)",
   "who is at risk"
  ],
  "definitions": "- causes: Explains why the condition happens: the biological mechanism, the gene mutations or the infectious or environmental agent that produces it (not who is more likely to get it).\n- complications: Describes further problems or conditions the disease can lead to.\n- diagnosis and tests: Explains how the condition is detected or confirmed: exams, lab tests, imaging, genetic testing and diagnostic criteria.\n- how common it is: Gives the prevalence or incidence: how many people or what share of a population have it, or that it is rare or its frequency is unknown.\n- inheritance pattern: States how the condition is passed down in families (autosomal dominant or recessive, X-linked, mitochondrial, de novo) and the chance relatives are affected.\n- outlook (prognosis): Describes the expected course and outcome: survival, recovery, progression or life expectancy.\n- prevention: Describes steps that lower the chance of getting the condition or its spread, such as vaccines, hygiene, lifestyle or avoiding exposures.\n- research and clinical trials: Describes research being done or funded on the condition: studies, trials, and what scientists are investigating.\n- signs and symptoms: Describes what people with the condition experience or show: symptoms, physical signs, features and how they present or vary.\n- stages: Explains how the disease (usually a cancer) is staged: how spread is measured and what each stage means.\n- treatment: Describes how the condition is treated or managed: therapies, drugs, surgery, and standard or trial treatment options.\n- what it is (overview): Defines or describes the condition or topic in general (what it is, which body part it affects, its main features) without being mainly about one aspect below.\n- who is at risk: Names risk factors or groups more likely to get the condition (age, sex, family history, exposures), rather than its mechanism."
 },
 {
  "qid": "qa032d33a5e",
  "kind": "choice",
  "text": "Heading: Request review of Sal the Stockbroker\nI dislike semi-protecting talk pages, so wanted to request a review of my actions at Sal the Stockbroker. The talk page consensus was to convert to a redirect about a year ago. Since then, IPs have repeated edit-warred over restoring the content, and vandalizing the article talk page. Both have had protections applied for this, the article multiple times.\nI haven't yet blocked any of the IPs - I'm suspecting a range block would be most effective for most of them, but I'm uncertain how wide of a range to address, or how heavily the range is used by legitimate users. Additional eyes and input would be appreciated.",
  "question": "Which Wikipedia noticeboard or help page is the right place for this post?",
  "options": [
   "Class S",
   "Class D",
   "Class M",
   "Class U",
   "Class A",
   "Class N",
   "Class Q",
   "Class F",
   "Class V"
  ],
  "definitions": "- Class S: Urgent or chronic user-conduct problems that need an administrator to act: harassment, disruption, personal attacks, block evasion or misuse of tools.\n- Class D: Problems with content about a living (or recently dead) person: unsourced or defamatory claims, privacy, undue negative material about them.\n- Class M: Editors who appear to edit about themselves, their employer, clients or products (paid or undisclosed promotional editing).\n- Class U: Articles promoting or giving undue credence to fringe, pseudoscientific or conspiracy ideas that depart from mainstream scholarship.\n- Class A: Questions about how to use or edit Wikipedia itself: creating articles, citing, formatting, uploading images, account and editing problems.\n- Class N: Whether an article's wording, weight or balance is biased or gives undue weight to one viewpoint, when sourcing itself is not the issue.\n- Class Q: Whether article content goes beyond what sources say: editors' own analysis, synthesis of several sources into a new conclusion, or unsourced interpretation.\n- Class F: Whether a particular source (outlet, book, website, paper) is reliable enough to cite for a given statement in an article.\n- Class V: Technical problems and questions about the site's software: bugs, templates, gadgets, scripts, rendering, bots, tools and MediaWiki features."
 },
 {
  "qid": "q8cccb8f720",
  "kind": "yes/no",
  "text": "News article:\nHonor a Hero's Legacy - Join Us in Paying Respects to U.S. Army Corporal Mirl Duane Forrest\nFollow me on Newsbreak for the latest developements on this story! https://original.newsbreak.com/@dr-michael-moates-1589310\nIn a heartfelt call to the community, the Central Texas State Veterans Cemetery is extending an open invitation to all members of the public to partake in honoring the service and memory of U.S. Army Corporal Mirl Duane Forrest during his Unaccompanied Veteran Burial.\nCorporal Forrest, born on April 3, 1937, dedicated nearly a decade of his life in service to our nation, actively serving in the U.S. Army from September 1954 to October 1963. His commitment and sacrifices for our country will be commemorated in a burial ceremony, ensuring his memory lives on with the respect and honor it deserves.\nThe ceremony, scheduled for Thursday, Oct. 5 at 11 a.m., is anticipated to proceed without the presence of next-of-kin. The Texas General Land Office has expressed, \"Corporal Forrest is not expected to have any next-of-kin attend his burial. Please help us spread the word and ensure that this U.S. Army Veteran is not buried alone. Members of the Killeen community are encouraged to attend.\"\nIn a solemn tribute to Corporal Forrest's military service, he will be accorded military honors. In the event that no family members are present, a representative from the Veterans Land Board will respectfully accept the United States flag on Corporal Forrest’s behalf.\nThe Central Texas State Veterans Cemetery and the wider community are coming together to ensure that no veteran is laid to rest alone. Your presence can stand as a testament to the enduring respect and gratitude our community holds for those who have served.\nLet us come together to honor Corporal Forrest's memory and service, ensuring that his contributions to our nation are celebrated and remembered with the dignity they warrant.\nFor those who wish to pay their respects, the burial will take place at the Central Texas State Veterans Cemetery. Community members are encouraged to share this message widely and stand united in honoring the memory of a veteran who served our country with honor and distinction.\n\nSummary:\nThe Central Texas State Veterans Cemetery is inviting the public to attend the burial of U.S. Army Corporal Mirl Duane Forrest, who served from 1954 to 1963. As he does not have any known next-of-kin, the community is encouraged to attend the ceremony on October 5th at 11am to show respect and gratitude for his service. The cemetery is located in Killeen, Texas.",
  "question": "Is everything stated in the summary supported by the news article?",
  "definitions": "- yes: Faithful: every claim in the summary is stated in or directly inferable from the article, with names, numbers, dates, attributions and certainty kept as the article gives them; omissions are fine.\n- no: Unfaithful: at least one claim contradicts the article (changed name, number, date, cause, who said what, certainty), or adds information the article does not contain, even if it is true in the real world or only a subtle overstatement."
 },
 {
  "qid": "qa8b623a526",
  "kind": "choice",
  "text": "The effect of surgical and/or medical androgen ablation on the imaging performance of Indium In 111 ProstaScint ® has not been studied. Preliminary data suggest hormone ablation may increase PSMA expression, with concurrent decrease in tumor expression of PSA. 3 The use of ProstaScint ® in this patient population cannot be recommended at this time.",
  "question": "Which section of a US prescription drug label does this passage come from?",
  "options": [
   "contraindications",
   "pregnancy",
   "references",
   "nursing mothers (lactation)",
   "indications and usage",
   "animal pharmacology and/or toxicology",
   "adverse reactions",
   "instructions for use",
   "how supplied",
   "drug interactions",
   "pediatric use",
   "clinical studies",
   "pharmacokinetics",
   "overdosage",
   "microbiology",
   "carcinogenesis, mutagenesis, impairment of fertility",
   "drug/laboratory test interactions",
   "description",
   "laboratory tests",
   "dosage forms and strengths"
  ],
  "definitions": "- contraindications: Lists the situations in which the drug must not be used at all, such as known hypersensitivity or specific conditions or co-medications.\n- pregnancy: Covers use during pregnancy: pregnancy category or risk summary, human and animal embryo-fetal data, and teratogenic or non-teratogenic effects on the fetus or newborn.\n- references: Lists the literature citations referred to in the label.\n- nursing mothers (lactation): Covers breastfeeding: whether the drug passes into human milk, effects on the breastfed infant or on milk production, and advice to nursing mothers.\n- indications and usage: States the diseases, conditions or patient groups the drug is approved to treat, prevent or diagnose, and any limitations of use.\n- animal pharmacology and/or toxicology: Reports other nonclinical animal findings (such as organ toxicity or pharmacology in animals) that are not about cancer, mutagenicity or fertility.\n- adverse reactions: Reports undesirable effects seen with the drug, usually with frequencies from clinical trials or from postmarketing reports, often grouped by body system.\n- instructions for use: Step-by-step instructions for the patient on preparing and using the product or its device (injector, pen, inhaler), usually numbered steps.\n- how supplied: Describes how the product is packaged and supplied: package types and sizes, NDC numbers and the appearance of the units in each package.\n- drug interactions: Describes how other drugs, foods or substances change this drug's effects or blood levels, or vice versa, and what to do about it.\n- pediatric use: Covers use in children: whether safety and effectiveness are established in pediatric patients, pediatric study data and child-specific risks.\n- clinical studies: Describes the clinical trials that support effectiveness: design, patient populations, endpoints and efficacy results.\n- pharmacokinetics: Describes absorption, distribution, metabolism and elimination: blood levels, half-life, bioavailability, protein binding, clearance, and effects of food, age or organ impairment.\n- overdosage: Describes the signs and symptoms of overdose and how to manage it (supportive care, antidotes, dialysis).\n- microbiology: Describes antimicrobial activity: spectrum of susceptible organisms, susceptibility testing and breakpoints, and mechanisms of resistance.\n- carcinogenesis, mutagenesis, impairment of fertility: Reports long-term animal carcinogenicity studies, genotoxicity or mutagenicity tests, and effects on fertility in animal studies.\n- drug/laboratory test interactions: Explains how the drug interferes with laboratory test results (false positives or altered assay values).\n- description: Describes the product itself: chemical name, structure, molecular formula and weight, physical properties, dosage form, and active and inactive ingredients.\n- laboratory tests: Tells which laboratory tests to perform or monitor before or during treatment (for example liver function tests or blood counts).\n- dosage forms and strengths: Lists the available dosage forms and strengths with the units' appearance (shape, color, markings), without package sizes or NDC numbers."
 },
 {
  "qid": "q0900da2ddf",
  "kind": "choice",
  "text": "Product: reebok easy tone shoe (category: Footwear)\nIncident description: Since wearing these shoes I have experienced hip bursitis in BOTH hips...extreme pain radiating across the low pelvis area....I have been seen by numerous doctors...pain, neurologists, orthopedics etc. Gone through pain theraphy sessions.",
  "question": "Based on this consumer product incident report, what was the most serious outcome for the primary victim on the SaferProducts.gov severity scale?",
  "options": [
   "Code 56",
   "Code 22",
   "Code 14",
   "Code 25",
   "Code 54",
   "Code 23",
   "Code 16",
   "Code 26"
  ],
  "definitions": "- Code 56: The report describes a hazard or defect that was noticed before anything happened: the product did not actually fail, burn, break or harm anyone during use.\n- Code 22: The product actually failed, overheated, caught fire, broke or malfunctioned during use, but no person was physically hurt (property damage or a near miss only).\n- Code 14: The primary victim was physically hurt (for example a small burn, cut, bruise or shock), but no first aid was given and no medical care was sought.\n- Code 25: The primary victim was hurt and was treated only by themselves or another lay person (ice, cold water, bandage, ointment, over-the-counter medicine), with no doctor, clinic or hospital.\n- Code 54: The primary victim's highest level of care was a doctor, urgent-care clinic, dentist, nurse or other medical professional outside an emergency department, with no hospital admission.\n- Code 23: The primary victim was treated in a hospital emergency department (ER), possibly after an ambulance ride, and was released without being admitted.\n- Code 16: The primary victim was admitted to a hospital as an inpatient (for example overnight stay, intensive care, burn unit or surgery) and survived.\n- Code 26: The primary victim died from the incident, whether at the scene or later in hospital."
 },
 {
  "qid": "qe7af36d9d7",
  "kind": "choice",
  "text": "employee was sitting on top of the trailer tank and went to pull themselves up when they felt a burning in left hip.",
  "question": "Which part of the body was injured in this mine accident report?",
  "options": [
   "Code 55",
   "Code 19",
   "Code 25",
   "Code 14",
   "Code 28",
   "Code 26",
   "Code 23",
   "Code 45",
   "Code 44",
   "Code 57",
   "Code 29",
   "Code 37",
   "Code 35",
   "Code 42",
   "Code 51",
   "Code 38",
   "Code 50",
   "Code 36",
   "Code 58",
   "Code 40",
   "Code 43",
   "Code 34"
  ],
  "definitions": "- Code 55: The hips, including the pelvis, pelvic organs, kidneys and buttocks.\n- Code 19: The arm when the narrative does not say which part of it (upper arm, elbow or forearm) was hurt.\n- Code 25: Two or more different face parts (for example nose and mouth, or eye and cheek).\n- Code 14: The mouth, lips, teeth, tongue, throat or sense of taste.\n- Code 28: The shoulder, including the collarbone (clavicle), shoulder blade (scapula) and rotator cuff.\n- Code 26: The knee, including the kneecap (patella) and meniscus.\n- Code 23: A whole body system rather than one part (for example poisoning, heat illness or a heart attack).\n- Code 45: Both the inner or middle ear (or hearing) and the outer ear.\n- Code 44: The abdomen, stomach area or internal abdominal organs.\n- Code 57: Two or more different parts of the same leg (for example knee and thigh).\n- Code 29: The foot itself (heel, arch, instep, metatarsals), not the ankle or toes.\n- Code 37: The brain itself, such as a concussion or other brain injury named as such.\n- Code 35: The ankle joint.\n- Code 42: The bones of the skull (cranium), for example a skull fracture.\n- Code 51: One or more toes.\n- Code 38: The thigh, including the femur and hamstring.\n- Code 50: Two or more parts of the trunk (for example back and chest).\n- Code 36: The back, including back muscles, the thoracic and lumbar spine, spinal cord and tailbone; not the neck.\n- Code 58: Parts of both arms or hands, or several different arm and hand parts.\n- Code 40: The outer ear only (auricle or earlobe), for example a cut, bruise or burn on the ear.\n- Code 43: The leg when the narrative does not say which part of it (thigh, knee or lower leg) was hurt.\n- Code 34: The arm between the shoulder and the elbow, including the humerus, biceps and triceps."
 },
 {
  "qid": "q8577693768",
  "kind": "yes/no",
  "text": "NWS Storm Data tornado entry (February 2024, Miami-Dade County, Florida). Survey: path length 0.63 miles; maximum path width 30 yards.\n\nA brief tornado touched down in Miami-Dade County approximately 4 miles north of the intersection of SW 8th street and Highway 997 (Krome Avenue). A driver reported a tornado crossing Krome Ave via social media. Minor vegetation damage was noted. Time, path length, and path width are estimated by radar and video reports from the public. Maximum wind speed and EF rating are unknown.",
  "question": "Based on this National Weather Service storm-survey narrative, which Enhanced Fujita (EF) rating was assigned to the tornado?\nIs it wrong to answer \"EFU (unrated)\"?",
  "definitions": "- EFU (unrated): No rating could be assigned because the tornado struck no rateable damage indicator (for example it stayed over open fields, water or unpopulated land); used for confirmed tornadoes with no surveyable damage.\n- EF5: Estimated gust over 200 mph: incredible damage such as strong frame houses leveled and swept clean off their foundations, reinforced-concrete structures critically damaged, car-sized missiles thrown far.\n- EF4: Estimated gust 166-200 mph: devastating damage such as well-constructed houses and whole frame houses leveled, cars thrown and large debris becoming airborne missiles.\n- EF1: Estimated gust 86-110 mph: moderate damage such as roofs badly stripped, mobile homes overturned or badly damaged, exterior doors lost, windows broken and many trees snapped or uprooted.\n- EF2: Estimated gust 111-135 mph: considerable damage such as roofs torn off well-built houses, frame houses shifted on foundations, mobile homes destroyed, large trees snapped or uprooted, cars lifted."
 },
 {
  "qid": "qe52bdbfcec",
  "kind": "choice",
  "text": "Associate wetting down muck pile with water truck \"cannon\" older model and associate needed to be on outside of vehicle. Truck was approx. 10 feet from pile. While spraying rock 3 to 4 feet in diameter rolled down pile hit corner of platform associate standing on, broke into piece and one piece flew up hitting associate in right shin",
  "question": "Which type of mining equipment was involved in this mine accident?",
  "options": [
   "Option V",
   "Option C",
   "Option G",
   "Option B",
   "Option T",
   "Option K",
   "Option A",
   "Option F",
   "Option M",
   "Option J",
   "Option Q",
   "Option L",
   "Option Z",
   "Option U",
   "Option S",
   "Option P",
   "Option D",
   "Option N",
   "Option E"
  ],
  "definitions": "- Option V: Slushers (scraper or slusher hoists): winch-pulled scraper buckets that drag broken ore along a drift or stope.\n- Option C: Stationary shop machines: bench grinders, drill presses, band and table saws, sandblasters.\n- Option G: Gunite and shotcrete machines that spray concrete or mortar onto rock surfaces.\n- Option B: Vehicles that carry miners: mantrips, mancars, personnel carriers, porta-buses, jeeps, jitneys, ATVs.\n- Option T: Belt conveyors and their parts: belt feeders, stage loaders, hopper shakers, belt structure, pulleys.\n- Option K: Underground shuttle cars, buggies and ram cars that haul from the miner to the belt.\n- Option A: Large off-road haul trucks used inside the mine or pit (rigid-frame or articulated rock trucks).\n- Option F: Raise climbers (for example Alimak): platforms that climb a rail up a raise carrying miners and equipment.\n- Option M: Machines that load blasting agents into drill holes: pneumatic ANFO or prill loaders, powder buggies, driller-loaders.\n- Option J: Longwall roof supports and parts other than the cutter: shields, ram jacks, Dowdy jacks, Duke.\n- Option Q: Flotation cells and filters (filter presses, disc or drum filters) in mineral processing plants.\n- Option L: Airplanes and helicopters used for mine work or travel.\n- Option Z: Pumps: slurry, sump, water and other pumps, including their motors, hoses and piping.\n- Option U: Mucking machines (overshot loaders, Cryderman muckers) that load broken rock in shafts, drifts or tunnels.\n- Option S: Light and support trucks: service, utility, pickup, water, fuel and lube trucks (not ore haulage).\n- Option P: Chutes: inclined troughs or spouts that material slides down between bins, conveyors, crushers or trucks.\n- Option D: Track equipment used to lay or repair rail track or re-rail cars: re-railers, track jacks, track shifters.\n- Option N: Hand-held tools with a motor or air/hydraulic power: impact wrenches, angle grinders, chain saws, power drills.\n- Option E: Ore haulage trucks licensed for public highways (over-the-road dump trucks and tractor-trailers)."
 },
 {
  "qid": "qc93fa1188b",
  "kind": "choice",
  "text": "Hang related graffiti on sidewalk",
  "question": "Which crew or agency should this graffiti report be routed to for removal?",
  "options": [
   "Caltrans",
   "City graffiti crew",
   "Metropolitan Transit System",
   "Park and Recreation Department",
   "Port of San Diego",
   "San Diego Unified School District",
   "US Postal Service",
   "property owner via code enforcement",
   "utility company that owns the box or pole"
  ],
  "definitions": "- Caltrans: Graffiti on state highway property (freeways, on- and off-ramps, freeway signs, sound walls, overpasses on state routes), referred to Caltrans.\n- City graffiti crew: Graffiti on City right-of-way or City street furniture (sidewalks, curbs, street signs, light poles, alleys, bridges, public walls), removed by the City's own crew.\n- Metropolitan Transit System: Graffiti on transit property (trolley stations and tracks, bus stops, benches and shelters), referred to the Metropolitan Transit System.\n- Park and Recreation Department: Graffiti inside a City park, playground, recreation center, trail or open-space canyon, handled by the Parks and Recreation Department.\n- Port of San Diego: Graffiti on Port of San Diego tidelands (Harbor Drive waterfront, Embarcadero, Shelter Island, marinas, bayfront parks), referred to the Port.\n- San Diego Unified School District: Graffiti on a public school's buildings, fences or grounds, referred to the San Diego Unified School District.\n- US Postal Service: Graffiti on a blue mailbox, postal collection box or post office, referred to the US Postal Service.\n- property owner via code enforcement: Graffiti on a private business, building, house, fence or dumpster; code enforcement notifies the owner, who must remove it.\n- utility company that owns the box or pole: Graffiti on a utility box, cabinet, transformer or pole owned by a utility (SDG&E, AT&T or Cox); the report is referred to that company."
 },
 {
  "qid": "q632230da37",
  "kind": "yes/no",
  "text": "Lakuna\nLakuna was an electronic instrumental project begun by drummer David Narcizo after Throwing Muses first split up following their 1996 \"Limbo\" album. Lakuna first released a 12-inch called \"So Happy\" and then a 1999 full-length album called \"Castle of Crime.\" Narcizo provided drums, drum programming, and keyboards on all the tracks. The album's guest musicians included Bernard Georges on bass, Kristin Hersh on guitar loops, Belly's Tom Gorman on bass, Melissa \"Misi\" Narcizo on piano and keyboards, and Frank Gardner on bass and bass synthesizer. Narcizo employed tape loops and samples from obscure, vintage music to achieve the album's ambient-styled instrumental sounds. Lakuna recorded on the 4AD and Throwing Music labels.\n\nThrowing Muses\nThrowing Muses is an alternative rock band formed in 1981 in Newport, Rhode Island, that toured and recorded extensively until 1997, when its members began concentrating more on other projects. The group was originally fronted by two lead singers, Kristin Hersh, and Tanya Donelly, who both wrote the group's songs. Throwing Muses are known for performing music with shifting tempos, creative chord progressions, unorthodox song structures, and surreal lyrics. The group was set apart from other contemporary acts by Hersh's stark, candid writing style; Donelly's pop stylings and vocal harmonies; and David Narcizo's unusual drumming techniques eschewing use of cymbals. Hersh's hallucinatory, febrile songs occasionally touched on the subject of mental illness, more often drawing portraits of characters from daily life or addressing relationships.\n\nGrouplove\nGrouplove (also typeset as GROUPLOVE) is an American band that was formed in 2009 by Hannah Hooper (vocals, keyboards), Christian Zucconi (vocals, guitar), Sean Gadd (bass), Andrew Wessen (guitar, vocals), and Ryan Rabin (drums).\n\nCaulfield Sisters\nThe Caulfield Sisters (2000–present) are a critically praised independent band based in Brooklyn, New York, noted at times for their sonic similarity to Throwing Muses or Galaxie 500. They have appeared at the annual CMJ music festival in New York, were featured in the New York art magazine \"Esopus\" and in an April 2005 live performance on Seattle independent radio station KEXP, and have performed with bands such as Interpol.",
  "question": "Are both Throwing Muses and Grouplove American bands?",
  "definitions": "- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every entity it names (for 'both' questions both have the property, for 'same' questions the two values match, for a comparison the stated order is right).\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the property or is not described as having it, the two values differ, or the stated comparison is the wrong way round. Paragraphs about other topics are distractors and do not decide the answer."
 },
 {
  "qid": "q36d4713b17",
  "kind": "yes/no",
  "text": "Company annual report excerpt\nTable:\n|  | 2019 | 2018 |\n|  | $ million | $ million |\n| Neither impaired nor past due | 115.3 | 99.8 |\n| Past due but not impaired: |  |  |\n| – Less than 30 days overdue | 8.6 | 16.8 |\n| – 30 to 60 days | 3.6 | 3.2 |\n| – Over 60 days | 1.2 | 3.6 |\n| Trade receivables | 128.7 | 123.4 |\nText:\n30. Financial instruments and financial risk management continued\nb) Credit risk continued\nThe composition of trade receivables at 31 December is as follows:\nThe Group closely monitors amounts due from customers and performs activities such as credit checks and reviews of payment history and has put in place appropriate credit approval limits. Based on these procedures, management assessed the quality of those receivables that are past due but not impaired as low risk.\nThe receivables’ provision is based on expected credit losses. The movement on the provision during the year is given in note 20. The value of impaired trade receivables is $1.4 million (2018 $0.9 million). For all other financial assets, the maximum exposure to credit risk is represented by the carrying amount.\n\nHypothetical question: What would the change in trade receivables be if the amount in 2019 was $129.4 million?\nProposed answer: 1 million",
  "question": "Using the report's table and text together with the question's hypothetical assumption, is the proposed answer correct?",
  "definitions": "- yes: The proposed answer is what the figures give after applying the question's hypothetical change (the assumed value replaces the reported one): same value at the precision shown, same sign, same unit or scale, and for lists exactly the right items.\n- no: The proposed answer is not the hypothetical result: it ignores the assumption and uses the reported figure, uses a wrong figure or base, sums instead of averaging, has the wrong sign or scale, or lists the wrong items."
 },
 {
  "qid": "q2bda5206f9",
  "kind": "choice",
  "text": "US NRC reactor operator licensing exam (Generic Fundamentals Examination), BWR question bank, topic: Fission Product Poisons.\n\nQuestion: A reactor has been operating at 50 percent power for 1 week. If a reactor power increase to 100 percent is initiated, the xenon-135 concentration will initially…",
  "question": "Which answer choice is correct for this NRC reactor operator licensing exam question?",
  "options": [
   "decrease, and then build up to a higher equilibrium concentration.",
   "increase, and then build up to a higher equilibrium concentration.",
   "decrease, and then return to the same equilibrium concentration.",
   "increase, and then return to the same equilibrium concentration."
  ],
  "definitions": "- decrease, and then build up to a higher equilibrium concentration.: Answer \"increase, and then return to the same equilibrium concentration.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- increase, and then build up to a higher equilibrium concentration.: Answer \"increase, and then build up to a higher equilibrium concentration.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- decrease, and then return to the same equilibrium concentration.: Answer \"decrease, and then return to the same equilibrium concentration.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong.\n- increase, and then return to the same equilibrium concentration.: Answer \"decrease, and then build up to a higher equilibrium concentration.\": correct only if it is the best answer to the question as asked; a choice that is only partly true, true only in other conditions, or less complete than another is wrong."
 },
 {
  "qid": "q534dbfbeef",
  "kind": "choice",
  "text": "Sentence: Visas and Study Permits are [administered] by Citizenship and Immigration Canada, and any questions regarding applications should be directed to them.\nMarked event or state: [administered]",
  "question": "How long did the event or state marked [ ] in the sentence last? Choose the most likely duration class given the sentence.",
  "options": [
   "Class R",
   "Class K",
   "Class Q",
   "Class U",
   "Class D",
   "Class G",
   "Class B",
   "Class E",
   "Class Y",
   "Class M",
   "Class W"
  ],
  "definitions": "- Class R: Happens at a single moment with essentially no duration (arriving, noticing, winning, a click or a shot).\n- Class K: Lasts from about a second up to under a minute (a sentence spoken, a glance, a quick reply).\n- Class Q: Lasts from about one minute up to under an hour (a phone call, a meal, a short meeting).\n- Class U: Lasts from about one hour up to under a day (a workday, a flight, a party).\n- Class D: Lasts from about one day up to under a week (a trip, an illness, a weekend event).\n- Class G: Lasts from about one week up to under a month (a vacation, a short course, a hospital stay).\n- Class B: Lasts from about one month up to under a year (a season, a project, a pregnancy).\n- Class E: Lasts from about one year up to under a decade (a job, schooling, living somewhere).\n- Class Y: Lasts from about ten years up to under a century (a career, a marriage, a person's adult life).\n- Class M: Lasts a hundred years or more but has a beginning or end (an institution, a tradition, an empire).\n- Class W: Has no bounded duration: permanent, timeless or generic states and truths (being a species, a mathematical fact, a general rule)."
 },
 {
  "qid": "q8db933efe8",
  "kind": "choice",
  "text": "Our cule de sac pavement needs to be repaved!!! Road is in bab shape!!!!",
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
  "qid": "q4d88f816cd",
  "kind": "yes/no",
  "text": "Product: Honda HRC2163HXA commercial power lawnmower (category: Rotary Power Lawn Mowers)\nIncident description: I have had my Honda HRC216HXA commercial lawnmower since July 2008, frame serial number MAKA-1062862. This year I noticed that the transmission drive clutch lever was not returning when released, i.e. the lawnmower would continue on cutting and propelling without any hands on the drive clutch lever.",
  "question": "Based on this consumer product incident report, what was the most serious outcome for the primary victim on the SaferProducts.gov severity scale?\nIs it wrong to answer \"incident, but no injury\"?",
  "definitions": "- incident, but no injury: The product actually failed, overheated, caught fire, broke or malfunctioned during use, but no person was physically hurt (property damage or a near miss only).\n- no incident, no injury: The report describes a hazard or defect that was noticed before anything happened: the product did not actually fail, burn, break or harm anyone during use.\n- death: The primary victim died from the incident, whether at the scene or later in hospital.\n- injury, first aid by a non-medical person: The primary victim was hurt and was treated only by themselves or another lay person (ice, cold water, bandage, ointment, over-the-counter medicine), with no doctor, clinic or hospital.\n- injury, no first aid or medical care: The primary victim was physically hurt (for example a small burn, cut, bruise or shock), but no first aid was given and no medical care was sought.\n- injury, seen by a medical professional: The primary victim's highest level of care was a doctor, urgent-care clinic, dentist, nurse or other medical professional outside an emergency department, with no hospital admission."
 },
 {
  "qid": "qfc0a326553",
  "kind": "yes/no",
  "text": "An 18-year-old woman comes to see her primary care physician for a physical for school. She states she has not had any illnesses last year and is on her school's volleyball team. She exercises daily, does not use any drugs, and has never smoked cigarettes. On physical exam you note bruising around the patients neck, and what seems to be burn marks on her back and thighs. The physician inquires about these marks. The patient explains that these marks are the result of her sexual activities. She states that in order for her to be aroused she has to engage in acts such as hitting, choking, or anything else that she can think of. The physician learns that the patient lives with her boyfriend and that she is in a very committed relationship. She is currently monogamous with this partner. The patient is studying with the hopes of going to law school and is currently working in a coffee shop. The rest of the patient’s history and physical is unremarkable. Which of the following is the most likely diagnosis?\n\nAnswer choices:\nA. Domestic abuse\nB. Dependent personality disorder\nC. Avoidant personality disorder\nD. Sexual masochism\nE. Sexual sadism\n\nProposed answer: D. Sexual masochism",
  "question": "Is the proposed answer the single best answer to this medical exam question?",
  "definitions": "- yes: Among the listed answer choices, the proposed option is the single best answer to the question exactly as asked, given the vignette's findings and standard medical knowledge (for an EXCEPT / NOT / LEAST question, it is the one option that is the exception).\n- no: The proposed option is one of the other listed choices: it may be plausible, partly true or appropriate in a different situation, but it is not the best answer to the question as asked."
 },
 {
  "qid": "q14c049dee7",
  "kind": "choice",
  "text": "Runway maintenance services",
  "question": "Which NAICS 2022 subsector does a business whose primary activity is described here belong to?",
  "options": [
   "551 Management of Companies and Enterprises",
   "493 Warehousing and Storage",
   "532 Rental and Leasing Services",
   "928 National Security and International Affairs",
   "487 Scenic and Sightseeing Transportation",
   "561 Administrative and Support Services",
   "485 Transit and Ground Passenger Transportation",
   "713 Amusement, Gambling, and Recreation Industries",
   "212 Mining (except Oil and Gas)",
   "483 Water Transportation",
   "484 Truck Transportation",
   "114 Fishing, Hunting and Trapping",
   "481 Air Transportation",
   "486 Pipeline Transportation",
   "492 Couriers and Messengers",
   "459 Sporting Goods, Hobby, Musical Instrument, Book, and Miscellaneous Retailers",
   "482 Rail Transportation",
   "521 Monetary Authorities-Central Bank",
   "491 Postal Service",
   "488 Support Activities for Transportation",
   "445 Food and Beverage Retailers"
  ],
  "definitions": "- 551 Management of Companies and Enterprises: Holding the securities of companies in order to own a controlling interest, or overseeing and managing other units of the same company.\n- 493 Warehousing and Storage: Operating warehousing and storage facilities for general merchandise, refrigerated goods, farm products and other goods.\n- 532 Rental and Leasing Services: Renting or leasing tangible goods such as cars, equipment, consumer goods and machinery to customers.\n- 928 National Security and International Affairs: Government national security (armed forces) and international affairs.\n- 487 Scenic and Sightseeing Transportation: Transportation mainly for sightseeing or recreation, such as scenic railroads, harbor cruises, hot-air balloon and sightseeing flights.\n- 561 Administrative and Support Services: Routine support services for other organizations: office administration, employment agencies, business support, travel arrangement, security, cleaning and landscaping services.\n- 485 Transit and Ground Passenger Transportation: Ground passenger transportation: urban transit, interurban buses, taxis and limousines, school and charter buses.\n- 713 Amusement, Gambling, and Recreation Industries: Amusement parks and arcades, gambling establishments, and other recreation facilities such as golf courses, marinas, fitness centers and bowling centers.\n- 212 Mining (except Oil and Gas): Mining and quarrying of coal, metal ores and nonmetallic minerals (stone, sand, gravel, clay) and beneficiating them at the mine.\n- 483 Water Transportation: Transporting passengers and cargo by ship or barge on oceans, coasts, the Great Lakes and inland waterways.\n- 484 Truck Transportation: Transporting cargo by truck, general freight or specialized freight, local or long-distance.\n- 114 Fishing, Hunting and Trapping: Catching or taking fish, shellfish and other wild animals from their natural habitat: commercial fishing, hunting and trapping.\n- 481 Air Transportation: Transporting passengers and cargo by aircraft, scheduled or nonscheduled.\n- 486 Pipeline Transportation: Transporting products such as crude oil, natural gas and refined products through pipelines.\n- 492 Couriers and Messengers: Couriers and messengers delivering parcels and documents, including local delivery services, without operating under a universal service obligation.\n- 459 Sporting Goods, Hobby, Musical Instrument, Book, and Miscellaneous Retailers: Retailing sporting goods, hobby items, musical instruments, books, florist items, office supplies, gifts, used merchandise, pets and other goods not elsewhere classified.\n- 482 Rail Transportation: Operating railroads for passengers or freight over long distances (line-haul and short-line railroads).\n- 521 Monetary Authorities-Central Bank: The central bank: monetary authorities managing the money supply and banking system.\n- 491 Postal Service: The national postal service delivering mail and small parcels.\n- 488 Support Activities for Transportation: Services supporting transportation, such as airport and port operations, navigational services to shipping, motor vehicle towing, freight arrangement and packing for shipping.\n- 445 Food and Beverage Retailers: Retailing food and beverages for home consumption, such as supermarkets, convenience stores, specialty food stores and beer, wine and liquor stores."
 },
 {
  "qid": "q49cb06afeb",
  "kind": "choice",
  "text": "Heading: Normalizing Associated Legendre Polynomials to get Spherical Harmonics\nHi all. I've been working on this problem for like weeks, and I can't seem to figure it out. I'm trying to normalize Associated Legendre polynomials to turn them into Spherical harmonics. The integral comes out to:\n \\int_{-1}^1 P_{\\ell_1}^m(x) P_{\\ell_2}^m(x) dx = \\frac{1}{A^2} \nwhere A is the normalization constant.\n A can be found in Spherical harmonics#Orthogonality and normalization. I know that it involves integrating by parts \\ell+m times, and that the boundary terms vanish in each case, but I'm not sure why they vanish. Can anyone point me to a (very detailed) discussion of how to actually do the integral, or maybe a better way than by parts? Thanks!",
  "question": "Which Wikipedia Reference Desk should this question be posted to?",
  "options": [
   "Computing reference desk",
   "Entertainment reference desk",
   "Humanities reference desk",
   "Language reference desk",
   "Mathematics reference desk",
   "Science reference desk"
  ],
  "definitions": "- Computing reference desk: Questions about computers, software, programming, the internet, electronics as used in computing, and IT or device problems.\n- Entertainment reference desk: Questions about popular culture: films, television, music, video games, sports, comics, celebrities and other entertainment.\n- Humanities reference desk: Questions about history, politics, law, religion, philosophy, economics and finance, society, the arts, literature and geography of human affairs.\n- Language reference desk: Questions about words and languages: meaning, grammar, spelling, pronunciation, etymology, translation and usage.\n- Mathematics reference desk: Questions about mathematics, statistics, probability, logic and puzzles that need mathematical reasoning.\n- Science reference desk: Questions about the natural and applied sciences: physics, chemistry, biology, medicine and health, astronomy, earth science, engineering and technology (not software)."
 },
 {
  "qid": "q5b2d166a88",
  "kind": "choice",
  "text": "30 YOM DRILLING HOLE IN METAL TRAILER AT WORK GOT SOMETHING IN EYE DXCORNEAL ABRASION",
  "question": "Which OIICS event category describes how this worker's injury happened?",
  "options": [
   "exposure to radiation or noise",
   "struck by object or equipment",
   "rubbed, abraded or jarred by vibration",
   "pedestrian struck by vehicle",
   "roadway motor vehicle incident",
   "rubbed or abraded by friction, pressure or foreign matter",
   "struck against object or equipment",
   "overexertion involving outside sources",
   "rail vehicle incident",
   "non-roadway motorized land vehicle incident",
   "slip or trip without a fall",
   "contact with object or equipment, mechanism unspecified",
   "exposure to other harmful substances"
  ],
  "definitions": "- exposure to radiation or noise: Radiation or noise caused the injury: welding arc flash burns to the eyes, ultraviolet or laser light, ionizing radiation, or loud noise damaging hearing.\n- struck by object or equipment: A moving object hit the worker: something fell, was dropped, flew, swung, rolled or slipped onto or into them, including a tool that slipped in use; the object moved, not the worker (a moving vehicle hitting a worker on foot is a pedestrian incident).\n- rubbed, abraded or jarred by vibration: Vibration caused the injury: prolonged use of vibrating tools or equipment (jackhammers, grinders), or being jolted and bounced while operating a vehicle or machine.\n- pedestrian struck by vehicle: The worker was on foot, not in or on a vehicle, and was struck, run over or pinned by a moving car, truck, forklift or other vehicle, on or off the road.\n- roadway motor vehicle incident: The worker was a driver or passenger of a motorized vehicle in a crash, collision or rollover on a public road (a motor-vehicle crash), including hitting the inside of the vehicle during it.\n- rubbed or abraded by friction, pressure or foreign matter: Friction, pressure or foreign matter caused the injury: blisters, chafing, rope or rug burns, or dust, dirt, sawdust, metal or other particles getting into the eye without being described as flying into it.\n- struck against object or equipment: The worker's own movement drove a body part into an object: bumping, banging, hitting or jamming against something, stepping on a nail or sharp object, or walking into equipment, with no fall.\n- overexertion involving outside sources: Strain or pain from exerting force on an outside object or person: lifting, pushing, pulling, carrying, holding, throwing, moving or transferring loads or patients, with no fall or being struck.\n- rail vehicle incident: A rail vehicle (train, trolley, streetcar, subway or mine rail car) caused the injury: collision, derailment, or sudden movement while the worker was on, under or beside it.\n- non-roadway motorized land vehicle incident: The worker was on or operating a motorized land vehicle or mobile machine away from public traffic (forklift, tractor, ATV, riding mower, golf cart, loader) that tipped, rolled, crashed or threw them off.\n- slip or trip without a fall: The worker slipped, tripped, stumbled or lost balance but did NOT fall, and was hurt by the slip itself or by catching or twisting to recover.\n- contact with object or equipment, mechanism unspecified: The worker was cut, punctured, bruised or fractured by contact with an object or equipment, but the narrative does not say whether they were struck by it, struck against it, caught in it or rubbed by it.\n- exposure to other harmful substances: A harmful substance was touched, inhaled, swallowed or injected: chemicals, caustics, cleaning agents, fumes, gases, pepper spray, allergens, blood or body fluids, including needlesticks with used or dirty needles."
 },
 {
  "qid": "qefe83dab97",
  "kind": "choice",
  "text": "Eurisko made many interesting discoveries and enjoyed significant acclaim, with his paper Heuretics: Theoretical and Study of Heuristic Rules winning the Best Paper award at the <e>1982 Association for the Advancement of Artificial Intelligence</e>.",
  "question": "In this artificial-intelligence text, what type of entity is \"1982 Association for the Advancement of Artificial Intelligence\" (marked <e>)?",
  "options": [
   "researcher",
   "organisation",
   "task",
   "location",
   "algorithm",
   "university",
   "person",
   "programming language",
   "country",
   "field",
   "metric",
   "conference",
   "miscellaneous",
   "product"
  ],
  "definitions": "- researcher: A named person known as a researcher or scientist in computing or artificial intelligence.\n- organisation: A named organisation, company, agency or institution that is not one of the more specific organisation types listed (university or conference).\n- task: A named problem or task that methods are built to solve (e.g. 'speech recognition', 'image segmentation').\n- location: A named place that is not a country: city, region, state, building, venue, river or other geographic feature.\n- algorithm: A named algorithm, model, method or technique (e.g. 'backpropagation', 'support vector machine').\n- university: A named university, college or research institute.\n- person: A named person who is not in one of the more specific person types listed (e.g. not a researcher).\n- programming language: A named programming language (e.g. 'Python', 'MATLAB', 'Lisp').\n- country: A named sovereign country or nation state (e.g. 'France', 'United States'), including historical countries.\n- field: A named research field or sub-field (e.g. 'machine learning', 'computer vision').\n- metric: A named evaluation metric or measure (e.g. 'F1 score', 'BLEU', 'mean squared error').\n- conference: A named academic conference or workshop (e.g. 'NeurIPS', 'AAAI').\n- miscellaneous: A named entity that fits none of the other listed types (e.g. a nationality, language, law or other named thing).\n- product: A named software product, system, device or tool (e.g. 'Octave', 'TensorFlow', 'Siri')."
 },
 {
  "qid": "qd29ccaeb3c",
  "kind": "yes/no",
  "text": "Problem:\nCompute $\\dbinom{10}{5}$.\n\nSolution steps so far:\nStep 1: This problem asks me to find the number of ways to choose 5 elements out of 10, without regard to order.\nStep 2: I recall that the binomial coefficient $\\dbinom{n}{k}$ can be calculated using the formula $\\dbinom{n}{k} = \\frac{n!}{k!(n-k)!}$, where $n!$ denotes the factorial of $n$, which is the product of all positive integers up to $n$.\nStep 3: In this case, I can plug in $n=10$ and $k=5$ into the formula and simplify.\nStep 4: I get $\\dbinom{10}{5} = \\frac{10!}{5!(10-5)!} = \\frac{10!}{5!5!}$.\nStep 5: To evaluate the factorials, I start with the largest one and work my way down, canceling out common factors as I go.\nStep 6: I see that $10! = 10 \\times 9 \\times 8 \\times 7 \\times 6 \\times 5!$.\nStep 7: So I can cancel out the $5!$ in the numerator and the denominator, leaving me with $\\frac{10 \\times 9 \\times 8 \\times 7 \\times 6}{5 \\times 4 \\times 3 \\times 2 \\times 1}$.\nStep 8: Now I can simplify the fractions by dividing each pair of factors by their greatest common divisor.\nStep 9: I see that $10$ and $5$ are both divisible by $5$, so I can divide them both by $5$ and get $2$ and $1$ respectively.\nStep 10: Similarly, $9$ and $3$ are both divisible by $3$, so I can divide them both by $3$ and get $3$ and $1$ respectively.\nStep 11: And $8$ and $4$ are both divisible by $4$, so I can divide them both by $4$ and get $2$ and $1$ respectively.\nStep 12: This leaves me with $\\frac{2 \\times 3 \\times 2 \\times 7 \\times 6}{1 \\times 1 \\times 1 \\times 2 \\times 1}$.\nStep 13: I can multiply the remaining factors in the numerator and the denominator to get the final answer.\nStep 14: I get $\\dbinom{10}{5} = \\frac{2 \\times 3 \\times 2 \\times 7 \\times 6}{1 \\times 1 \\times 1 \\times 2 \\times 1} = \\frac{504}{2} = 252$.\n\nLast step (Step 15):\n# Answer\n\n252",
  "question": "Is the last step of this partial solution correct and acceptable as a next step?",
  "definitions": "- yes: The last step is acceptable: everything it states is correct, quickly verifiable and fits the earlier steps, whether it makes real progress or only restates or stalls; a final answer counts only if it is correct and follows from a complete solution.\n- no: The last step is not acceptable: it states something wrong (even partly), cannot be checked in about 30 seconds, is off-topic or gibberish, leads into an obvious dead end or loop, or gives a wrong, unjustified or incomplete final answer."
 },
 {
  "qid": "qf5c9aa0c40",
  "kind": "choice",
  "text": "rt @cfchack coronavirus videos everyday makes you numb tbh.  wuhan china coronavirus: this chinese billionare says china is lying. 1,200 bodies are burned every day in wuhan alone. #HASHTAG HASHTAG_VIRUS HASHTAG_VIRUS HASHTAG_EASTASIA HASHTAG_EASTASIA+VIRUS HASHTAG_EASTASIA #HASHTAG https://t.co/t79rxi5fyt",
  "question": "Under the East Asian prejudice codebook, which category does this tweet fall into?",
  "options": [
   "hostility toward an East Asian entity",
   "criticism of an East Asian entity",
   "counter-speech against East Asian prejudice",
   "discussion of East Asian prejudice",
   "none of these"
  ],
  "definitions": "- hostility toward an East Asian entity: The tweet derogates or demeans an East Asian group, country, government or culture: extreme negative portrayal, hatred, conspiracy or bioweapon claims, 'they should leave', celebrating suffering, boycott calls, or mocking virus names; it outranks all other categories.\n- criticism of an East Asian entity: The tweet criticises an East Asian institution, affiliation or practice (such as the Chinese government hiding data) in a factual or reasoned way without abuse, stereotypes, conspiracy claims or normative 'they can't be trusted' framing.\n- counter-speech against East Asian prejudice: The tweet explicitly challenges or condemns anti-East-Asian prejudice, slurs or stereotypes, or shows solidarity with East Asian people, without itself abusing the same target.\n- discussion of East Asian prejudice: The tweet talks about Sinophobia or anti-Asian racism, or debates names like 'China virus', without itself engaging in or explicitly countering the prejudice.\n- none of these: The tweet is none of the above: unrelated, neutral news, or mentions East Asia or the virus without hostility, criticism, counter-speech or discussion of prejudice, including a neutral geographic 'Wuhan virus'."
 },
 {
  "qid": "qc47b562c68",
  "kind": "yes/no",
  "text": "Table caption: Methodology to study the integrity of LC-NE system in humans.\n| Method | Relation to LC-NE system | Advantages | Limitations |\n| Pharmacological challenge (e.g. atomoxetine) | Changes in synaptic concentrations of NE mimic the effects of elevated/ reduced NE release by LC. | Allows within-subject comparison of behavior and physiology (i.e. normal vs. elevated NE levels). | Pharmacological agents are rarely specific of one neuromodulatory system and likely interact with other systems; each individual may have different responsivity; invasive. |\n| PET | NE transporter availability reflects functionality of LC projections. | Allows for direct molecular quantification. | Very low temporal resolution; invasive. |\n| Pupillometry | Non-reflexive pupil dilation accompanies LC phasic activation and tracks changes in tonic LC firing. | Relatively high temporal resolution to study task-evoked LC activity with low budget; non-invasive. | Constitutes an indirect measurement of LC activity; other neuromodulators may contribute to changes in pupil size. |\n| Neuromelanin-sensitive MRI | LC is rich in neuromelanin, a molecule that is paramagnetic and can be detected through MRI. | Allows the highest precision in LC localization in humans in vivo; non-invasive. | Does not provide information about LC function; intensity in LC may vary with age. |\n| fMRI | Blood oxygen level dependent (BOLD) changes in LC reflect the level of neuronal activation in the nuclei. | Allows measuring task-related and resting state changes of activity with relatively high spatial resolution; non-invasive. | Many sources of artifacts affect the quality of the measurements, i.e. head movement and confounds from cerebro-spinal fluid vicinity; the small size of LC may also provide a low signal-to-noise ratio; requires specific brainstem co-registration steps. |\n| ERP (P300) | P3 indexes phasic LC response. | Allows high temporal resolution of a relatively well characterized component; non-invasive. | LC contributes only in part to the component. |\n\nStatement: Molecular quantification is an advantage of PET method.",
  "question": "Is the statement supported by the table?",
  "definitions": "- yes: Everything the statement says is true according to the table's cells, caption and notes, including any counting, summing, comparison, ranking (highest, lowest) or 'all/every' check it requires; minor typos or paraphrased row and column names do not matter.\n- no: The table shows the statement is false: a value, unit, count, comparison or ranking is wrong, an 'all' or 'every' claim fails for at least one row, or the statement attributes a value to the wrong row, column or group."
 },
 {
  "qid": "q2687698eb0",
  "kind": "choice",
  "text": "While performing maintenance during hot weather the employee did not realize he had become dehydrated and at the end of the job showed heat related symptoms and was later diagnosed with heat exhaustion.",
  "question": "What is the nature of the injury described in this mine accident report?",
  "options": [
   "chemical burn (chemicals, fumes, compounds)",
   "hearing loss or impairment",
   "contagious or infectious disease",
   "electric arc or flash burn (no contact)",
   "freezing, frostbite or low-temperature effects",
   "burn or scald from heat",
   "suffocation, smoke inhalation or drowning",
   "silicosis",
   "joint, tendon or muscle inflammation",
   "systemic poisoning",
   "heat stroke, sunstroke or heat exhaustion",
   "cut, laceration or puncture (open wound)",
   "amputation or enucleation",
   "other injury (not elsewhere classified)",
   "dust or particles in the eye",
   "cerebral hemorrhage (not from an impact)",
   "fracture or chipped bone",
   "dislocation",
   "electric shock or electrocution",
   "asbestosis"
  ],
  "definitions": "- chemical burn (chemicals, fumes, compounds): A burn or irritation of the skin or eyes caused by chemicals, caustic material (lime, wet cement, acid, lye), fumes or compounds.\n- hearing loss or impairment: Loss or impairment of hearing, including a standard threshold shift found on a hearing test.\n- contagious or infectious disease: A contagious or infectious disease contracted at work.\n- electric arc or flash burn (no contact): A burn from an electric arc or flash without touching the conductor, including welding arc flash burns to the eyes.\n- freezing, frostbite or low-temperature effects: Frostbite, freezing or other effects of cold.\n- burn or scald from heat: A burn from heat: flames, hot surfaces, molten metal, hot slag, steam or hot liquids; not a chemical, electrical or arc-flash burn.\n- suffocation, smoke inhalation or drowning: Suffocation, asphyxiation, smoke inhalation or drowning.\n- silicosis: Lung disease from breathing crystalline silica dust.\n- joint, tendon or muscle inflammation: Inflammation or irritation of joints, tendons or muscles: tendonitis, bursitis, epicondylitis, synovitis, trigger finger or carpal tunnel syndrome.\n- systemic poisoning: Poisoning of the body as a whole by a toxic substance (for example carbon monoxide or lead), not a local chemical burn.\n- heat stroke, sunstroke or heat exhaustion: Heat stroke, sunstroke, heat exhaustion or heat cramps.\n- cut, laceration or puncture (open wound): An open wound: a cut, laceration, gash or puncture, including wounds closed with stitches or staples.\n- amputation or enucleation: Loss of all or part of a body part (finger, toe, limb) by cutting off, tearing off or surgical removal after the injury, or removal of an eye.\n- other injury (not elsewhere classified): An injury of a kind with no more specific code here.\n- dust or particles in the eye: Dust, grit or small particles in the eye, with no cut, burn, scratch or other eye wound named.\n- cerebral hemorrhage (not from an impact): Bleeding in the brain or a stroke not caused by a blow.\n- fracture or chipped bone: A broken, fractured or chipped bone.\n- dislocation: A joint forced out of its normal position (dislocated or subluxed).\n- electric shock or electrocution: An electric shock or electrocution without a named electrical burn.\n- asbestosis: Lung disease from asbestos dust."
 },
 {
  "qid": "q6681cbb561",
  "kind": "choice",
  "text": "Cheese on the bottom, sauce on top - not too thick or doughy.",
  "question": "Apart from the food, which other aspect category of the restaurant does this review sentence discuss?",
  "options": [
   "menu",
   "staff",
   "service",
   "ambience",
   "place",
   "price",
   "miscellaneous"
  ],
  "definitions": "- menu: What the restaurant offers rather than how it tasted: the menu or wine list, the range, selection or variety of dishes and drinks, specials, prix-fixe or tasting options, and whether items are available.\n- staff: The people who work there, such as waiters, waitresses, servers, hosts, bartenders, managers, chefs, owners or a DJ, and anything a staff member does: how they behave (friendly, rude, knowledgeable, helpful) and how they serve you (attentive, checking on the table, forgetting an order, being slow). When a person who works there is the one acting, choose staff rather than service.\n- service: The service in general, not tied to a particular person: the word service itself, how fast or slowly food, drinks or the check arrived, waits for food, dishes coming out in the wrong order, and delivery or takeout. If a waiter, server or other staff member is the one being described, that is staff, not service. Reservations and waiting for a table usually count as miscellaneous.\n- ambience: The atmosphere and feel of the room: decor, art, lighting, music, live entertainment, noise, mood, vibe, and how romantic, cozy, trendy or comfortable it feels.\n- place: The restaurant as a physical venue: the place or restaurant as such, its location, neighbourhood or view, and its spaces (dining rooms, the bar, the counter, the kitchen, tables and seating, the terrace, bathrooms), including their size and how crowded or packed they are.\n- price: Money: prices, the cost of dishes or the meal, the bill or check, the tip, dollar amounts, and whether it was cheap, expensive, overpriced or worth the money.\n- miscellaneous: Any other aspect not covered by the concrete categories: portion sizes, reservations and getting a table, the time or occasion of the visit, lines, who the other diners are, restaurant policies, general value or deals, and the overall experience."
 },
 {
  "qid": "q63ab879c25",
  "kind": "choice",
  "text": "Identification of the nuclear localization motif in the <e2>ETV6</e2> (<e2>TEL</e2>) protein.\n<e2>ETV6</e2>, or <e2>Translocation-Ets-Leukemia</e2> (<e2>TEL</e2>), is an ETS family transcriptional repressor that is essential for establishing hematopoiesis in neonatal bone marrow, and is frequently a target of chromosomal translocations in human <e1>cancer</e1>. <e2>ETV6</e2> is predominantly a nuclear phosphoprotein that represses transcription by binding directly to the promoters of target genes. The nuclear localization mechanism of <e2>ETV6</e2>, however, is not well understood. In this report, we provide evidence that a nuclear localization signal (NLS) exists in the C-terminal region of <e2>ETV6</e2>. <e2>ETV6</e2> proteins with mutations outside of amino acids 332-452 localize to the nucleus, whereas proteins with mutations within amino acids 332-452 remain in the cytoplasm. Furthermore, when a fragment of <e2>ETV6</e2> comprised of amino acids 332-452 was fused to cytoplasmic beta-galactosidase protein, the fusion protein was able to enter the nucleus. These results strongly indicate that residues 332-452 mediate nuclear localization of <e2>ETV6</e2>.",
  "question": "Which relation does the abstract state between the disease \"cancer\" (marked <e1>) and the gene/protein \"ETV6\" (marked <e2>)?",
  "options": [
   "Option Z",
   "Option F",
   "Option J",
   "Option D",
   "Option E",
   "Option W",
   "Option M",
   "Option Q"
  ],
  "definitions": "- Option Z: The two drugs interact: taking them together changes their effect or toxicity (a pharmacodynamic or pharmacokinetic drug-drug interaction).\n- Option F: One chemical is converted into the other (a metabolic or chemical transformation).\n- Option J: The abstract links the two concepts without a stated direction: a genetic association, a regulation or modification whose effect is not called increasing or decreasing, or any link fitting no other type.\n- Option D: The two chemicals are given together as a combined treatment.\n- Option E: One concept raises the other or its risk, level or activity: a chemical induces a disease, a gene or variant increases disease risk, upregulation, or drug response/sensitivity.\n- Option W: The two concepts physically bind: protein-protein binding, or a chemical binding a protein as its ligand or receptor.\n- Option M: One concept lowers the other or its risk, level or activity: a drug treats or prevents a disease, a protective gene or variant, downregulation, inhibition, or drug resistance.\n- Option Q: The two chemicals are compared with each other, e.g. their efficacy, potency or side effects are evaluated side by side."
 }
]
