# A46 replay label-noise blind read RSBL05-blind_read-1eccef37-015

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/replay_screen/reads/answers/RSBL05-blind_read-1eccef37-015.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 4. Answers expected: 4 (one per item, each with that item's qid).

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
  "qid": "qe3ef9314ed",
  "kind": "choice",
  "text": "Metformin Hydrochloride Tablets, USP vs Placebo Summary of Mean Changes from Baseline * in Fasting Plasma Glucose HbA 1c and Body Weight, at Final Visit (29-week study) Metformin hydrochloride tablets, USP (n = 141) Placebo (n = 145) P-value FPG (mg/dL) Baseline 241.5 237.7 NS * * Change at FINAL VISIT -53.0 6.3 0.001 Hemoglobin A 1c (%) Baseline 8.4 8.2 NS * * Change at FINAL VISIT -1.4 0.4 0.001 Body Weight (lbs) Baseline 201.0 206.0 NS * * Change at FINAL VISIT -1.4 -2.4 NS * * A 29-week, double-blind, placebo-controlled study of metformin and glyburide, alone and in combination, was conducted in obese patients with type 2 diabetes patients who had failed to achieve adequate glycemic control while on maximum doses of glyburide (baseline FPG of approximately 250 mg/dL). Patients randomized to the combination arm started therapy with metformin hydrochloride 500 mg and glyburide 20 mg.",
  "question": "Which section of a US prescription drug label does this passage come from?",
  "options": [
   "Code 53",
   "Code 29",
   "Code 30",
   "Code 18",
   "Code 35",
   "Code 27",
   "Code 57",
   "Code 28",
   "Code 34",
   "Code 38",
   "Code 51",
   "Code 42",
   "Code 52",
   "Code 25",
   "Code 49",
   "Code 58",
   "Code 16",
   "Code 56",
   "Code 47",
   "Code 33",
   "Code 17",
   "Code 13",
   "Code 39",
   "Code 21",
   "Code 55",
   "Code 23",
   "Code 50",
   "Code 43"
  ],
  "definitions": "- Code 53: Describes the signs and symptoms of overdose and how to manage it (supportive care, antidotes, dialysis).\n- Code 29: Describes the clinical trials that support effectiveness: design, patient populations, endpoints and efficacy results.\n- Code 30: Tells how to dose and give the drug: doses, schedules, titration, dose changes for patient groups, preparation, dilution and administration technique.\n- Code 18: Covers use during pregnancy: pregnancy category or risk summary, human and animal embryo-fetal data, and teratogenic or non-teratogenic effects on the fetus or newborn.\n- Code 35: Covers the drug's effects during labor and delivery (on contractions, the course of delivery or the newborn at birth).\n- Code 27: Explains how the drug produces its therapeutic effect at the molecular, cellular or physiological level.\n- Code 57: Describes how the product is packaged and supplied: package types and sizes, NDC numbers and the appearance of the units in each package.\n- Code 28: Describes how other drugs, foods or substances change this drug's effects or blood levels, or vice versa, and what to do about it.\n- Code 34: Describes the drug's measured effects on the body (for example on heart rhythm, QT interval, hormone levels or receptors) and their time course or dose-response.\n- Code 38: Describes clinically significant risks and precautions in use and how to monitor, prevent or manage them; not the boxed summary and not incidence tables of side effects.\n- Code 51: Describes the drug's potential for abuse and misuse (non-therapeutic use for its psychological effects), abuse-deterrent properties and signs of abuse.\n- Code 42: Step-by-step instructions for the patient on preparing and using the product or its device (injector, pen, inhaler), usually numbered steps.\n- Code 52: The boxed ('black box') warning: a short, emphatic summary of the drug's most serious risks, such as death, suicidality, addiction or fetal harm, and the key action to take.\n- Code 25: Describes absorption, distribution, metabolism and elimination: blood levels, half-life, bioavailability, protein binding, clearance, and effects of food, age or organ impairment.\n- Code 49: States that the drug contains a controlled substance and its DEA schedule (for example Schedule II).\n- Code 58: Tells the prescriber what to advise or counsel patients about; written to the healthcare provider ('Advise patients...', 'Patients should be informed...').\n- Code 16: Describes physical dependence, tolerance and withdrawal symptoms with continued use or abrupt discontinuation.\n- Code 56: Covers use in children: whether safety and effectiveness are established in pediatric patients, pediatric study data and child-specific risks.\n- Code 47: States the diseases, conditions or patient groups the drug is approved to treat, prevent or diagnose, and any limitations of use.\n- Code 33: Reports other nonclinical animal findings (such as organ toxicity or pharmacology in animals) that are not about cancer, mutagenicity or fertility.\n- Code 17: Lists the situations in which the drug must not be used at all, such as known hypersensitivity or specific conditions or co-medications.\n- Code 13: Tells which laboratory tests to perform or monitor before or during treatment (for example liver function tests or blood counts).\n- Code 39: Describes antimicrobial activity: spectrum of susceptible organisms, susceptibility testing and breakpoints, and mechanisms of resistance.\n- Code 21: Lists the literature citations referred to in the label.\n- Code 55: Explains how the drug interferes with laboratory test results (false positives or altered assay values).\n- Code 23: Reports undesirable effects seen with the drug, usually with frequencies from clinical trials or from postmarketing reports, often grouped by body system.\n- Code 50: Covers breastfeeding: whether the drug passes into human milk, effects on the breastfed infant or on milk production, and advice to nursing mothers.\n- Code 43: Reports long-term animal carcinogenicity studies, genotoxicity or mutagenicity tests, and effects on fertility in animal studies."
 },
 {
  "qid": "qd38dd55d72",
  "kind": "choice",
  "text": "Guidance document: Set up and run a motorcycle approved training body (ATB)\n# Overview\nYou must be an approved training body (ATB) with the Driver and Vehicle Standards Agency (DVSA) to provide:\n- compulsory basic training (CBT) for learner motorcyclists\n- direct access scheme (DAS) training to riders learning to ride a large motorcycle\nCBT and DAS training must be given by instructors certified by DVSA working for your approved training body.\nThe sites you use to provide training from must also be approved by DVSA.\nThe process is different Northern Ireland.\n\n# Rules for being an ATB\nYou must meet certain rules to be an approved training body (ATB).\n\n## ‘Fit and proper’\nYou must be a ‘fit and proper’ person to run the ATB.\nWhen deciding if you’re a ‘fit and proper’ person, DVSA will look at if you have:\n- had any convictions in the last 4 years\n- any motoring convictions\n- been disqualified from driving\n- any penalty points on your licence\n- any court proceedings pending against you\n\n## Training\nYou must provide compulsory basic training (CBT) as an ATB. Any CBT and direct access scheme (DAS) courses you provide must meet the legal requirements.\nThe CBT syllabus and guidance notes gives full details on what must be provided.\nAn instructor is only allowed to supervise up to 2 trainees during on-road tuition.\nYour instructors must be in radio contact with all trainees at all times during on-road tuition.\n\n## Training sites\nYou must have the use of a suitable site or sites for training in the off-road parts of the CBT course.\nThese sites must be authorised by DVSA before they’re used.\n\n## Instructors\nYou must make sure that all your instructors have a valid instructor certificate for the type of training they give. This must show the name of your ATB.\nAt least 1 of your instructors must have successfully completed DVSA’s assessment course for motorcycle training.\nDVSA-assessed instructors are allowed to train other people that you want to appoint as instructors - this is known as ‘down-training’.\nYou should have at least 1 DVSA-assessed instructor for every 10 instructors that have been down-trained.\n\n## Monitoring\nYou should send all required information about the courses you provide to DVSA including:\n- reporting any incidents\n- dates when you’re providing CBT courses\n- the CBT certificates of completion you issue\nThe ATB manual gives more details about what you have to send.\n\n# Apply to become an ATB\nTo apply to register an approved training body (ATB), download these 3 application forms, and send them to DVSA:\n- ‘Application to provide compulsory basic training (CBT) courses’\n- ‘Compulsory basic training (CBT) site application form’\n- ‘Application to be authorised as a certified motorcycle instructor’\nIt takes up to 8 weeks to process an application. This includes the time to inspect the site to be used for the off-road elements of compulsory basic training.\n\n# Apply for CBT site authorisation\nAll the sites you intend to use for the practical training and riding elements of the compulsory basic training (CBT) course must be authorised by DVSA.\nYou can’t use a site until you’ve got authorisation from DVSA.\nDownload the compulsory basic training site application form to apply for authorisation.\nSend the completed form to DVSA. You’ll also need to include a draft plan of the intended site, eg an annotated satellite image.\n\n## Site inspection\nDVSA will:\n- inspect the site\n- send a site report to you\n- send a unique site code to you if the site is suitable\nThe site report will explain any rules set by DVSA. This will include how many trainees are allowed on the site.\nYou should make sure all your instructors are aware of these details.\n\n## Changes to authorised sites\nYou must tell DVSA straight away if a site is altered or added to.\nDownload the compulsory basic training site application form and send it to DVSA.\nYou’ll also need to include:\n- a draft plan showing any changes to the original authorised site\n- a permission letter signed by the site owner\nThe site’s authorisation can be removed if it has become unsuitable.\n\n## Stopping using a site\nYou must tell DVSA straight away if you stop using a site for CBT.\nYou can email DVSA - you’ll need to include your approved training body number and the site’s unique code.\n\n# Providing the CBT course\nThe compulsory basic training (CBT) course is made up of 5 parts.\nThe course syllabus and the order in which the parts must be delivered is set out in law.\n\n## CBT certificate of completion\nYou must give trainees a CBT certificate of completion (DL196) when they reach the required standard.\nThe certificate must be completed and signed by the instructor, usually the one who conducted part E of the CBT course.\nThe name and address of your approved training body (ATB) should be included on the certificate.\n\n### Ordering DL196 certificates\nYou can buy books of DL196 certificates online from DVSA.\nEach book contains 25 certificates and costs £200.\n\n# How your ATB is monitored\nDVSA monitors the standard of instruction given by:\n- approved training bodies (ATBs)\n- instructors delivering compulsory basic training (CBT) courses\nYou must make your instructors available for regular standards checks.\nYou should tell your local DVSA CBT manager the dates and times when your ATB will be running CBT courses.\n\n## After an assessment\nYou’ll get a letter of confirmation and report from DVSA after an assessment visit if the training delivered meets the required standard.\nDVSA can conduct more assessments if:\n- the training falls short of the required standard\n- there are breaches of regulations\n- there are reports of failure to follow the conditions of appointment\nDVSA will consider withdrawing an instructor’s authority to deliver courses if they fail to achieve the required standard during the subsequent assessments.\nDVSA can withdraw your ATB’s authorisation to deliver training courses if assessments show that it doesn’t consistently provide full and proper CBT courses.\n\n## Disagreeing with DVSA’s decision\nYou can appeal to DVSA if you or an instructor disagrees with DVSA’s decision to withdraw their authority.\n\n# Documents for ATBs\nDVSA produces the following documents for approved training bodies (ATBs).\n\n## ATB manual\nThe ATB manual gives more details about the rules and processes you should follow when you’re running an ATB.\n\n## Safe and Responsible Riding\nThe ‘National standard for riding mopeds and motorcycles’ sets out the skills, knowledge and understanding that learners need to prove they’re safe and responsible riders.\n\n## Compulsory basic training (CBT) syllabus and guidance notes\nThe CBT syllabus and guidance notes sets out what trainers need to do and what learners need to understand when taking the course.\n\n## Direct access scheme (DAS) motorcycle training guidance\nThe DAS motorcycle training guidance sets out what trainers need to do and what learners need to understand when taking the course.\nChanges to the CBT syllabus and guidance notes\nYou can keep up to date with new versions if you sign up for DVSA email alerts.\n\nUser's scenario: I have a DVSA approved site for practical training and riding elements of the compulsory basic training (CBT) course. Recently we have shut down the site for some financial reasons.\nUser's question: Do we have to inform DVSA about the decision to stop using the CBT site ?",
  "question": "Applying the guidance document to the user's scenario, what is the answer to the user's question?",
  "options": [
   "yes",
   "no",
   "depends on unstated conditions",
   "not answerable"
  ],
  "definitions": "- yes: The document, applied to the facts in the scenario, answers yes with no requirement left open: every condition that matters is met or settled by the scenario.\n- no: The document, applied to the facts in the scenario, answers no with no requirement left open.\n- depends on unstated conditions: The document answers yes or no only if further requirements it names are met (or gives yes in one case and no in another), and the scenario does not say which case applies.\n- not answerable: The document does not contain the information needed to answer this question for this scenario, so neither yes nor no is supported."
 },
 {
  "qid": "q60d79b4c5a",
  "kind": "choice",
  "text": "Customer: I am still waiting for a charge reversal from my return.\nCustomer: Joyce Wu\nCustomer: Username: joycew19",
  "question": "Which specific customer-service request does the customer have?",
  "options": [
   "account credit missing",
   "account international shipping question",
   "add item to existing order",
   "add item to existing refund",
   "billed for item never bought",
   "billed for returned item",
   "boots product question",
   "cart not updating",
   "change account address",
   "change account name",
   "change account payment method",
   "change account phone number",
   "change delivery time",
   "change shipment details",
   "competitor price lower",
   "credit card rejected",
   "dispute subscription bill",
   "downgrade shipping speed",
   "is subscription active",
   "item never arrived",
   "items generally out of stock",
   "jacket product question",
   "jeans product question",
   "membership question",
   "one item out of stock",
   "pay subscription bill",
   "price was lower yesterday",
   "promo code expired",
   "promo code invalid",
   "recover password",
   "recover username",
   "refund status",
   "remove duplicate item from order",
   "reset two-factor authentication",
   "return due to color",
   "return due to size",
   "return due to stain",
   "search not working",
   "service wrongly removed",
   "shipment status question",
   "shipping cost too high",
   "shirt product question",
   "start a refund",
   "store policy question",
   "store pricing question",
   "store timing question",
   "subscription amount due",
   "subscription due date",
   "subscription payment extension",
   "unexpected fee on order",
   "unknown service added",
   "upgrade to overnight shipping",
   "website too slow",
   "wrong order payment method",
   "wrong order quantity"
  ],
  "definitions": "- account credit missing: The customer says some credit that should be on their account is missing.\n- account international shipping question: The customer asks whether their account entitles them to free shipping to or from other countries, i.e. international shipping.\n- add item to existing order: The customer wants to add another item to an order they have already placed.\n- add item to existing refund: The customer already has a refund in progress and wants to add another item to that same refund.\n- billed for item never bought: The customer sees a charge on their bill for something they never bought in the first place.\n- billed for returned item: The customer was billed for an item they already returned and has not received the credit for it; a billing complaint, not a new refund.\n- boots product question: The customer asks a general question about boots, such as stain or gum removal, width, break-in time, waterproofing, laces, sizes in stock or warranty.\n- cart not updating: The customer is trying to put an item in their online shopping cart, but the cart does not update.\n- change account address: The customer wants to update or correct the address saved on their account profile, not the delivery address of a shipment in progress.\n- change account name: The customer wants to update or correct the name saved on their account profile.\n- change account payment method: The customer wants to update, add or replace the payment method saved on their account.\n- change account phone number: The customer wants to update or correct the phone number saved on their account profile.\n- change delivery time: The customer believes the delivery time of their order is wrong and wants to change it, for example from morning to evening, rather than just confirming a date.\n- change shipment details: The customer wants to change something about a shipment in progress, such as the delivery address or the item because they ordered the wrong one.\n- competitor price lower: The customer complains that a competitor sells the same item for a lower price than they paid.\n- credit card rejected: The customer's credit card keeps being rejected as invalid when they try to pay on the website.\n- dispute subscription bill: The customer thinks their subscription bill is wrong, for example that they were charged twice.\n- downgrade shipping speed: The customer wants to switch an order to slower delivery, such as next week, to save on shipping fees, not to get a refund.\n- is subscription active: The customer wants to know whether their payment went through and whether their premium subscription is still active.\n- item never arrived: The customer did not receive an item they ordered and wants to know what happened to it.\n- items generally out of stock: The customer complains that many items or products in general are out of stock, not one specific item.\n- jacket product question: The customer asks a general question about jackets, such as stain removal, washing or dry cleaning, arm length, detaching the hood, shrinking, stock, material or warmth.\n- jeans product question: The customer asks a general question about jeans, such as stain removal, washing, leg length, tailoring cost, shrinking, colors, sizes or ripped designs.\n- membership question: The customer asks a general question about membership: the levels, how to qualify for premium membership, its benefits, or how long it lasts.\n- one item out of stock: The customer complains that one particular item they want is out of stock.\n- pay subscription bill: The customer wants to pay or renew their premium subscription bill.\n- price was lower yesterday: The customer complains that the item was cheaper yesterday than the price they paid or now see.\n- promo code expired: The customer's promo code is rejected because it is considered out of date or expired.\n- promo code invalid: The customer's promo code is rejected as invalid when they try to use it.\n- recover password: The customer cannot log in because they forgot their password and needs a new one generated.\n- recover username: The customer has forgotten or cannot find their username and needs it recovered after verifying their identity.\n- refund status: The customer wants to know the status of a refund they already requested, or which payment method it will go to.\n- remove duplicate item from order: The customer accidentally ordered an extra item, such as two instead of one, and wants the unwanted item removed or cancelled.\n- reset two-factor authentication: The customer is locked out by two-factor authentication and needs it reset, with a reset code sent to their email.\n- return due to color: The customer wants to return an item because its color is wrong or not what they expected.\n- return due to size: The customer wants to return an item because it is the wrong size or does not fit.\n- return due to stain: The customer wants to return an item because it arrived stained or dirty.\n- search not working: The website search keeps showing no results, no matter what the customer searches for.\n- service wrongly removed: The customer believes an important service was mistakenly removed from their account or plan and wants it back.\n- shipment status question: After a confusing email notification, the customer asks a yes/no question to check that their shipment is on track.\n- shipping cost too high: The customer finds the shipping fee too high and wants it waived or refunded, rather than delaying delivery to save on fees.\n- shirt product question: The customer asks a general question about shirts, such as stain removal, washing, arm length, collar width, shrinking, sizes in stock, buttons or material.\n- start a refund: The customer wants to begin a new refund for an item they purchased and chooses how the money is returned.\n- store policy question: The customer asks a general question about store policies, such as cancelling a subscription, late subscription payments, refunds or returns, not about their own bill or order.\n- store pricing question: The customer asks a general question about store prices, such as gift wrapping, name stitching, overnight shipping cost, or whether a cart qualifies for free shipping, without changing an order.\n- store timing question: The customer asks when something happens at the store, such as a new collection drop, store opening hours, the annual sale, or promo code expiry.\n- subscription amount due: The customer wants to know how much they owe on their premium subscription.\n- subscription due date: The customer wants to know when their premium subscription payment or monthly renewal is due.\n- subscription payment extension: The customer cannot pay for their premium subscription right now and asks for more time to pay.\n- unexpected fee on order: The customer believes an extra or unexplained charge was added to their order and wants it explained or removed.\n- unknown service added: The customer believes an unknown or unwanted service was added to their account or plan without their consent.\n- upgrade to overnight shipping: The customer wants to upgrade an existing order to faster, overnight shipping so it arrives sooner.\n- website too slow: The website has become so slow to load that the customer can barely use it to shop.\n- wrong order payment method: The customer believes the wrong payment method was used for an order and may want to change it.\n- wrong order quantity: The customer's order confirmation shows a different quantity than the customer wanted to order."
 },
 {
  "qid": "qaac0f1aee8",
  "kind": "choice",
  "text": "Customer: The $69 Guess Jacket, can I machine wash it?\nCustomer: yes, thank you.\nCustomer: Wonderful, thank you.  Goodbye.",
  "question": "Which specific customer-service request does the customer have?",
  "options": [
   "account credit missing",
   "account international shipping question",
   "add item to existing order",
   "add item to existing refund",
   "billed for item never bought",
   "billed for returned item",
   "boots product question",
   "cart not updating",
   "change account address",
   "change account name",
   "change account payment method",
   "change account phone number",
   "change delivery time",
   "change shipment details",
   "competitor price lower",
   "credit card rejected",
   "dispute subscription bill",
   "downgrade shipping speed",
   "is subscription active",
   "item never arrived",
   "items generally out of stock",
   "jacket product question",
   "jeans product question",
   "membership question",
   "one item out of stock",
   "pay subscription bill",
   "price was lower yesterday",
   "promo code expired",
   "promo code invalid",
   "recover password",
   "recover username",
   "refund status",
   "remove duplicate item from order",
   "reset two-factor authentication",
   "return due to color",
   "return due to size",
   "return due to stain",
   "search not working",
   "service wrongly removed",
   "shipment status question",
   "shipping cost too high",
   "shirt product question",
   "start a refund",
   "store policy question",
   "store pricing question",
   "store timing question",
   "subscription amount due",
   "subscription due date",
   "subscription payment extension",
   "unexpected fee on order",
   "unknown service added",
   "upgrade to overnight shipping",
   "website too slow",
   "wrong order payment method",
   "wrong order quantity"
  ],
  "definitions": "- account credit missing: The customer says some credit that should be on their account is missing.\n- account international shipping question: The customer asks whether their account entitles them to free shipping to or from other countries, i.e. international shipping.\n- add item to existing order: The customer wants to add another item to an order they have already placed.\n- add item to existing refund: The customer already has a refund in progress and wants to add another item to that same refund.\n- billed for item never bought: The customer sees a charge on their bill for something they never bought in the first place.\n- billed for returned item: The customer was billed for an item they already returned and has not received the credit for it; a billing complaint, not a new refund.\n- boots product question: The customer asks a general question about boots, such as stain or gum removal, width, break-in time, waterproofing, laces, sizes in stock or warranty.\n- cart not updating: The customer is trying to put an item in their online shopping cart, but the cart does not update.\n- change account address: The customer wants to update or correct the address saved on their account profile, not the delivery address of a shipment in progress.\n- change account name: The customer wants to update or correct the name saved on their account profile.\n- change account payment method: The customer wants to update, add or replace the payment method saved on their account.\n- change account phone number: The customer wants to update or correct the phone number saved on their account profile.\n- change delivery time: The customer believes the delivery time of their order is wrong and wants to change it, for example from morning to evening, rather than just confirming a date.\n- change shipment details: The customer wants to change something about a shipment in progress, such as the delivery address or the item because they ordered the wrong one.\n- competitor price lower: The customer complains that a competitor sells the same item for a lower price than they paid.\n- credit card rejected: The customer's credit card keeps being rejected as invalid when they try to pay on the website.\n- dispute subscription bill: The customer thinks their subscription bill is wrong, for example that they were charged twice.\n- downgrade shipping speed: The customer wants to switch an order to slower delivery, such as next week, to save on shipping fees, not to get a refund.\n- is subscription active: The customer wants to know whether their payment went through and whether their premium subscription is still active.\n- item never arrived: The customer did not receive an item they ordered and wants to know what happened to it.\n- items generally out of stock: The customer complains that many items or products in general are out of stock, not one specific item.\n- jacket product question: The customer asks a general question about jackets, such as stain removal, washing or dry cleaning, arm length, detaching the hood, shrinking, stock, material or warmth.\n- jeans product question: The customer asks a general question about jeans, such as stain removal, washing, leg length, tailoring cost, shrinking, colors, sizes or ripped designs.\n- membership question: The customer asks a general question about membership: the levels, how to qualify for premium membership, its benefits, or how long it lasts.\n- one item out of stock: The customer complains that one particular item they want is out of stock.\n- pay subscription bill: The customer wants to pay or renew their premium subscription bill.\n- price was lower yesterday: The customer complains that the item was cheaper yesterday than the price they paid or now see.\n- promo code expired: The customer's promo code is rejected because it is considered out of date or expired.\n- promo code invalid: The customer's promo code is rejected as invalid when they try to use it.\n- recover password: The customer cannot log in because they forgot their password and needs a new one generated.\n- recover username: The customer has forgotten or cannot find their username and needs it recovered after verifying their identity.\n- refund status: The customer wants to know the status of a refund they already requested, or which payment method it will go to.\n- remove duplicate item from order: The customer accidentally ordered an extra item, such as two instead of one, and wants the unwanted item removed or cancelled.\n- reset two-factor authentication: The customer is locked out by two-factor authentication and needs it reset, with a reset code sent to their email.\n- return due to color: The customer wants to return an item because its color is wrong or not what they expected.\n- return due to size: The customer wants to return an item because it is the wrong size or does not fit.\n- return due to stain: The customer wants to return an item because it arrived stained or dirty.\n- search not working: The website search keeps showing no results, no matter what the customer searches for.\n- service wrongly removed: The customer believes an important service was mistakenly removed from their account or plan and wants it back.\n- shipment status question: After a confusing email notification, the customer asks a yes/no question to check that their shipment is on track.\n- shipping cost too high: The customer finds the shipping fee too high and wants it waived or refunded, rather than delaying delivery to save on fees.\n- shirt product question: The customer asks a general question about shirts, such as stain removal, washing, arm length, collar width, shrinking, sizes in stock, buttons or material.\n- start a refund: The customer wants to begin a new refund for an item they purchased and chooses how the money is returned.\n- store policy question: The customer asks a general question about store policies, such as cancelling a subscription, late subscription payments, refunds or returns, not about their own bill or order.\n- store pricing question: The customer asks a general question about store prices, such as gift wrapping, name stitching, overnight shipping cost, or whether a cart qualifies for free shipping, without changing an order.\n- store timing question: The customer asks when something happens at the store, such as a new collection drop, store opening hours, the annual sale, or promo code expiry.\n- subscription amount due: The customer wants to know how much they owe on their premium subscription.\n- subscription due date: The customer wants to know when their premium subscription payment or monthly renewal is due.\n- subscription payment extension: The customer cannot pay for their premium subscription right now and asks for more time to pay.\n- unexpected fee on order: The customer believes an extra or unexplained charge was added to their order and wants it explained or removed.\n- unknown service added: The customer believes an unknown or unwanted service was added to their account or plan without their consent.\n- upgrade to overnight shipping: The customer wants to upgrade an existing order to faster, overnight shipping so it arrives sooner.\n- website too slow: The website has become so slow to load that the customer can barely use it to shop.\n- wrong order payment method: The customer believes the wrong payment method was used for an order and may want to change it.\n- wrong order quantity: The customer's order confirmation shows a different quantity than the customer wanted to order."
 }
]
