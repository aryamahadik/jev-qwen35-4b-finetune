# Item 10 card authoring i10a_open_data_3

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_open_data_3.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of datasets published on government open-data portals.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: intended use: what a person would use the dataset for, where neighbouring answers are easy to confuse.
Card 2 angle: freshness: how current, complete or final the data are said to be, where neighbouring answers are easy to confuse.
Card 3 angle: kind of dataset: what sort of records the dataset holds, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_open_data_3",
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
  "text": "Counts and Rates of New HIV Diagnoses Among Individuals Using Injection Drugs January 2016 - Current Monthly County & Statewide Health\nThis indicator includes the count and rate of new HIV diagnoses among individuals using injection drugs per 100,000 individuals estimated to have Drug Use Disorder."
 },
 {
  "sid": "s02",
  "text": "Initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury: United States\nOn December 20 2021, all estimates and standard errors for 2017–2018 were revised in this table to correct programming errors.\n\nData on initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder ( for critical information about measures, definitions, and changes over time. Due to a change in national medical data coding standards in 2015, from the International Classification of Diseases, 9th Revision, Clinical Modification (ICD-9-CM) to the ICD-10-CM, the definition for injuries and injury subcategories changed for the 2017 reporting period and beyond. Results from 2017 and subsequent years should not be compared with previous reporting periods. Any observed changes in trends across this transition period should not be considered. Data for 2016 are not included. Additional information regarding injury definitions and categorization of injuries by mechanism and intent of injury is available at: Note that the data file available here has more recent years of data than what is shown in the PDF or Excel version.\n\nSOURCE: NCHS, National Hospital Ambulatory Medical Care Survey. For more information on the National Hospital Ambulatory Medical Care Survey, see the corresponding Appendix entry at"
 },
 {
  "sid": "s03",
  "text": "TxRC 2016 Daily Purses Paid\n2016 Daily purses paid by Texas pari-mutuel racetracks as reported to TxRC. All figures are based on information available to TxRC at the time the data was compiled and are subject to being audited and revised."
 },
 {
  "sid": "s04",
  "text": "Individuals with Medical Assistance (MA) receiving Medication-Assisted Treatment (MAT) CY 2015-Current Annual County Human Services\nThis dataset contains the count of individuals with Medical Assistance coverage (MA) receiving any form of MAT (Medication-Assisted treatment) by case county. The counts cover calendar years 2015 - 2018. If a count field is null, then the count is suppressed due to low numbers. If the county is null, then the county is unknown."
 },
 {
  "sid": "s05",
  "text": "Retail Reports by Industry and County in Colorado\nColorado Retail and Sales Tax information are summarized monthly at the county level by industry. Retail Sales for the monthly filing period are summarized by county and industry in this report including retail trade totals. Contains fields like agriculture, clothing, food & beverage, etc from the Colorado Department of Revenue (CDOR)."
 },
 {
  "sid": "s06",
  "text": "Special Taxing Districts\nA list of special taxing districts in Connecticut. CGS Sec. 7-324 defines special taxing districts as follows: Continuation of former districts. For the purposes of sections 7-324 to 7-329, inclusive, “district” means any fire district, sewer district, fire and sewer district, lighting district, village, beach or improvement association and any other district or association, except a school district, wholly within a town and having the power to make appropriations or to levy taxes. All districts established prior to May 29, 1957, under the provisions of the general statutes or by special act shall be continued; provided any such district may be dissolved or consolidated with the government of any town, city or borough of which it is a part in accordance with the provisions of the general statutes or may, by a two-thirds vote of those voters present at a district meeting, elect to be governed by the provisions of sections 7-324 to 7-329, inclusive, in lieu of the provisions of any general or special act under which such district was established or operated. Notwithstanding any of the provisions of sections 7-324 to 7-329, inclusive, a district established prior to May 29, 1957, and electing to be governed by said sections shall not be required to adopt the form of organization provided for in said sections but may continue its existing form of organization and nevertheless have and exercise the powers and duties granted to districts in said sections and in such event the officers of such district shall have and may exercise the powers and duties granted to district officers in said sections."
 },
 {
  "sid": "s07",
  "text": "Licensed Home Care Services Agency Registration Status: 2019\nThis dataset contains the registration status of each Licensed Home Care Services Agency (LHCSA) in New York State for calendar year 2019. Each LHCSA must register with the New York State Department of Health annually, in order to provide services, bill, and avoid paying a fine. For more information, visit:"
 },
 {
  "sid": "s08",
  "text": "Rate of Women on Medical Assistance (MA) Diagnosed with Opioid Use Disorder (OUD) during Pregnancy CY 2016-Current Statewide Department of Human Services (DHS)\nThis dataset summarizes the number of women on Medical Assistance (MA) ages 12 to 55 years old with a delivery and indicates how many of those women were diagnosed with Opioid Use Disorder (OUD) during their pregnancy. Delivery includes live birth or stillbirth. Data collection started in 2016 and will be updated quarterly as data becomes available."
 },
 {
  "sid": "s09",
  "text": "Energy Storage Solutions (ESS) Event Calendar\nThe Energy Storage Solutions program is an incentive program designed to help Eversource and United Illuminating customers install battery energy storage systems for their home or business. The program helps lower the cost of buying a battery by providing upfront and performance incentives. This incentive program is overseen by the Public Utilities Regulatory Authority (PURA), is paid for by electric ratepayers, and is administered by the Connecticut Green Bank, Eversource, and UI.\n\nThis dataset is a comprehensive listing of all grid dispatch events associated with the ESS program. For more information regarding dispatch events and how they are scheduled/called, consult the Energy Storage Solutions Program Manual, located at\n\nMore information and an interactive dashboard of this and other program data can be found at"
 },
 {
  "sid": "s10",
  "text": "HPMS Sample Mid-America 2018\nThis data represents HPMS Sample limits that correspond to the HPMS Section Data. This dataset contains expansion factors that are used to expand the attributes to State wide aggregation. More information regarding the Sample dataset is contained in the HPMS Field Manual.\nThe Mid-America contains data for the following States: Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Oklahoma, South Dakota, Texas, and Wisconsin"
 },
 {
  "sid": "s11",
  "text": "Michigan Per Capita Personal Income\nMichigan per capita personal income compared to the national average. The annual growth rate of per capita personal income for Michigan and the U.S. is included. For both measures Michigan's rank among the states is included for each year from 1990-2015."
 },
 {
  "sid": "s12",
  "text": "What do I do with...? Recycling options in King County\nThe \"What do I do with...?\" site ( provides King County citizens with recycling and proper disposal options for over 100 products and materials. The site lists over 400 businesses (mostly local) that accept products and materials for recycling or proper disposal. Business details include location (with mapping), contact information, hours of operation, restrictions, fees and more. The goal of \"What do I do with...?\" is to reduce the volume of reusable or recyclable items being added to the waste-stream, thereby reducing the environmental impact of those items while extending the lifespan of our landfills."
 }
]
