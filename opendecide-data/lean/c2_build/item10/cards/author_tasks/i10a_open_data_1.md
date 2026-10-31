# Item 10 card authoring i10a_open_data_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_open_data_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of datasets published on government open-data portals.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: kind of dataset: what sort of records the dataset holds, where neighbouring answers are easy to confuse.
Card 2 angle: intended use: what a person would use the dataset for, where neighbouring answers are easy to confuse.
Card 3 angle: freshness: how current, complete or final the data are said to be, where neighbouring answers are easy to confuse.
The three cards must ask three different decisions, not three wordings of one decision.

Rules for all three cards:
1. A careful reader must be able to decide the answer from the text alone, with no outside knowledge.
2. The question must apply to most texts of this kind, not only to these 12 examples.
3. Use plain everyday words. No jargon and no academic terms.
4. Options must not overlap: for any text exactly one option fits best. The last option may be a catch-all (for example
   "something else"), and its definition must say exactly when to pick it.
5. Give every option a one-sentence definition that says exactly when to pick it.
6. Boundary rule, the heart of this task: build the options as near neighbours. At least two pairs of options must be easy to
   confuse for a hurried reader. For every such pair, the two definitions must state the dividing line: what the text must say
   or do to belong to the first option and not to the second.
7. Balance: choose questions where each option is the right answer for a fair share of texts of this kind. No option should
   fit more than half of the texts.
8. Do not copy label names or label sets from public datasets or benchmarks (for example positive/negative/neutral sentiment
   scales, entailment/contradiction, star ratings, standard emotion lists, standard news or topic category lists, or intent
   lists from chatbot or banking datasets). Invent labels that fit the real decision.
9. Do not ask about anyone's identity, health or other personal traits, and do not ask for an opinion about a named person.
10. Do not label, summarise or quote the example texts. Your output holds only the 3 cards.

Labels are short (1 to 5 words), lower case unless a proper noun, and unique within a card. expected_share is your rough guess
for texts of this kind in general, not a count over the examples; the shares of a card sum to 1.

## Answer contract

Write ONE JSON object, and nothing else (no text before or after it), to the answer file named at the top.

{"task_id": "i10a_open_data_1",
  "cards": [
    {"kind": "choice",
      "who_decides": "one sentence: who makes this decision and why",
      "question": "the question, ending with a question mark",
      "options": [{"label": "short label", "definition": "one sentence"}, "... 4 to 8 options in total"],
      "expected_share": {"<each label>": 0.2}},
    "... exactly 3 cards in total"
  ]}

The items below are read-only context (the example texts). Your answer holds exactly 3 cards.

## Example texts (JSON; read-only context, not items to answer)

[
 {
  "sid": "s01",
  "text": "GDP for U.S. Counties\nThis dataset contains the GDP for each county in the U.S. GDP is given as Real GDP (thousands of chained 2012 dollars), Current-dollar GDP (thousands of current dollars) and Chain-type quantity indexes for real GDP for each year from 2001 to the most recent year for which GDP is available. The dataset was retrieved from the Bureau of Labor Statistics website."
 },
 {
  "sid": "s02",
  "text": "VEHSS Modeled Estimates\nVEHSS Composite Prevalence Estimates\n2019, 2021, 2022, 2024. This dataset contains estimates of the prevalence of visual acuity loss and major eye diseases generated using a Bayesian meta-analytic modeling approach that combines information from multiple data sources to produce comprehensive estimates of prevalence by age, race, and sex at the national, state and county levels. These composite prevalence estimates are the primary surveillance measures developed by the Centers for Disease Control and Prevention’s Vision & Eye Health Surveillance System (VEHSS).\n\nFor more information about these estimates including summary tables and maps, methods, and links to related publications visit\nTo view this data in the VEHSS interactive data visualization application, visit and search for “VEHSS Composite Prevalence Estimate”.\n\nVisual Acuity Loss:\nVisual acuity loss prevalence estimates represent best-corrected visual acuity in the better-seeing eye and are included in rows where Category=’Measured Visual Acuity’. Rows with Subgroup = ‘Any vision loss' represents any impairment or blindness of 20/40 or worse; rows with Subgroup = 'US-defined blindness' refers to the subset of vision loss that is 20/200 or worse.\n\nAge Related Macular Degeneration:\nThe age-related macular degeneration (AMD) estimates represent AMD as measured with retinal imaging examination, and are included in rows where Category = ‘Age Related Macular Degeneration’. The Subgroup ‘Vision threatening AMD’ includes patients with geographic atrophy, wet-form AMD, or choroidal neovascularization in either eye. The Subgroup ‘Non-vision threatening AMD’ includes patients with early or intermediate dry-form AMD defined as retinal pigment epithelium abnormalities or drusen ≥125 μm in the worse-affected eye, and do not have vision threatening AMD.\n\nDiabetic Retinopathy:\nThe diabetic retinopathy (DR) estimates represent DR as measured with retinal imaging examination, and are included in rows where Category=’Diabetic Eye Diseases’. The Subgroup ‘Vision threatening DR’ includes patients with severe non-proliferative DR, proliferative DR, and diabetic macular edema. The Subgroup ‘Non-vision threatening DR’ is defined as patients with mild-moderate non-proliferative DR or unspecified DR, and do not have vision threatening DR.\n\nGlaucoma:\nThe glaucoma estimates represent glaucoma as measured with retinal imaging examination and are included in rows where Category=’Glaucoma’. The Subgroup ‘Vision affecting glaucoma’ includes people with glaucoma and abnormal visual field. The Subgroup ‘Non-vision affecting glaucoma’ is defined as people with glaucoma without an abnormal visual field.\n\nAge Groups:"
 },
 {
  "sid": "s03",
  "text": "Campaign Finance - FPPC Form 460 - Schedule C - Non-Monetary Contributions\nThis dataset includes all itemized non-monetary contributions ($100 or more) e-filed on Fair Political Practices Commission (FPPC) Form 460 Schedule \"C\" Non-Monetary Contributions from 2011 to the present.\n\nThe data is current as of the last modified date on this dataset.\n\nSee the data key for column definitions:"
 },
 {
  "sid": "s04",
  "text": "Multifamily Housing FY 2011-2025\nThe Maryland Department of Housing and Community Development offers multifamily finance programs for the construction and rehabilitation of affordable rental housing units for low to moderate income families, senior citizens and individuals with disabilities.\n\nOur multifamily bond programs issues tax-exempt and taxable revenue mortgage bonds to finance the acquisition, preservation and creation of affordable multifamily rental housing units in priority funding areas.\n\nBy advocating for increased production of rental housing units, we help create much-needed jobs and leverage opportunities to live, work and prosper for hardworking Maryland families, senior citizens, and individuals with disabilities throughout the state.\n\nDISCLAIMER: Some of the information may be tied to the Department’s bond funded loan programs and should not be relied upon in making an investment decision. The Department provides comprehensive quarterly and annual financial information and operating data regarding its bonds and bond funded loan programs, all of which is posted on the publicly-accessible Electronic Municipal Market Access system website (commonly known as EMMA) that is maintained by the Municipal Securities Rulemaking Board, and on the Department’s website under Investor Information.\n\nMore information accessible here:"
 },
 {
  "sid": "s05",
  "text": "Jobs Created By County with Six County Average Data\nDataset showing employment change resulting from new business establishments and from existing firm expansion. Includes both the total for the 7 County Metro and the average of six counties, excluding Ramsey County for comparison."
 },
 {
  "sid": "s06",
  "text": "Special Primary Statistics 2019\nA special primary election for Ramsey County Commissioner District 1 was held Aug. 13, 2019. Below is a snapshot of ballots cast. For complete statistics, view the election abstract or MN Secretary of State's results website. Learn more about the special election timeline and process at ramseycounty.us/specialelection."
 },
 {
  "sid": "s07",
  "text": "Cambridge Public School Locations\nView full metadata\n\nDescription\nThis layer contains point features of all Cambridge public schools. Created for general use by City staff. Used for both mapping and specific identification of buildings with a similar use. Also used by emergency responders for evacuation and if the school is a designated shelter.\n\nAbout Edit Dates\nThis data is automatically updated on a set schedule. The Socrata edit date may not reflect the actual edit dates in the data. For more details please see the update date on the full metadata page or view the edit date within the data rows."
 },
 {
  "sid": "s08",
  "text": "Housing Infrastructure Programs\nThis report contains FY25 - FY26 data covering Business Oregon's Housing Infrastructure Programs. These include the Housing Infrastructure Support Fund (HISF) and other housing infrastructure related funding legislatively appropriated to Business Oregon.\n\nFor more information on the Housing Infrastructure Support Fund (HISF) please visit:\n\nIn FY27, Business Oregon also began awarding recipients as part of its Housing Infrastructure Financing Program (HIFP). Programmatic data will be added to this report in September 2027. For more information on the HIFP, please visit:"
 },
 {
  "sid": "s09",
  "text": "Department of Human Services(DHS) Family Investment Administration Program Caseloads\nFood Supplement Program (FSP) active cases are the number of total cases that are active at the end of the FSP benefit receiving month and for the following month. These cases are active because they are compliant with all FSP eligibility requirements.\n\nExpedited Food Supplement Program approved cases are FSP cases that meet the expedited requirements and FSP eligibility requirements.\n\nNote: If expedited FSP cases remain active at the end of the application month, they will be included in the overall active FSP cases"
 },
 {
  "sid": "s10",
  "text": "Education & Library Name, Address & GIS (EdNA) Current Statewide Education\nEdNA (Education Names and Addresses) can be used to find name, address, administrator, and related information about the educational entities that PDE serves. These entities include school districts and their schools, intermediate units, career and technical centers, charter schools, nonpublic and private schools, higher education institutions, and many more.\nState Public Libraries are also part of this file and most of them start with a 9 as the first digit of the AUN column. There is one entry for Free Library of Philadelphia AUN 300513650 that does not start with a 9."
 },
 {
  "sid": "s11",
  "text": "Farm Labor Housing\nTo facilitate the rehabilitation and replacement of existing farm worker housing and dilapidated mobile home units, with intent of building partnerships and providing resources to enable farmers and agricultural landowners to improve housing for the County’s low-income agricultural workers who live in these rehabilitated units. HOSFL Measure K Performance"
 },
 {
  "sid": "s12",
  "text": "Paid Parking Occupancy (Last 30 Days)\nNotice: This dataset will soon be deprecated. Please transition to the replacement dataset available at\n\nThe City of Seattle has created an on-street paid parking occupancy data set and is providing access to this data set for public use for research and entrepreneurial purposes under the City’s Open Data Program. This data set contains the last 30 days of paid occupancy records (after the seven day data delay)."
 }
]
