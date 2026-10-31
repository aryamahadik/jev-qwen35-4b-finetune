# Item 10 card authoring i10a_open_data_4

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_open_data_4.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of datasets published on government open-data portals.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: detail level: what one record in the dataset stands for, where neighbouring answers are easy to confuse.
Card 2 angle: first look: which kind of team should look at the dataset first, where neighbouring answers are easy to confuse.
Card 3 angle: subject area: which area of public life the dataset is about, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_open_data_4",
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
  "text": "Pole Attachments\nThis dataset contains information about pole attachments in Austin, TX.\n\nThe data is maintained by the Arterial Management Division of Austin Transportation and Public Works.\n\nThis dataset is currently being developed and may change at any time. As a result, this may contain incomplete or inaccurate information."
 },
 {
  "sid": "s02",
  "text": "Prince George's County Full and Part Time Jobs By Industry: Historic 2001 to 2018 and Projected 2020 to 2040\nTotal Jobs by Industry, Historic 2001 to 2018 and Projected 2020 to 2040 in Prince George's County by Industry and by Place of Work"
 },
 {
  "sid": "s03",
  "text": "High Cost Disbursements\nThis dataset provides information about total dollar amounts disbursed by month and year to Eligible Telecommunication Carriers (ETCs) participating in the High Cost Program. The tool displays data for the current year and the previous 10 years."
 },
 {
  "sid": "s04",
  "text": "Safe Drinking Water Facilities Information System for Pennsylvania 2018 - Current Environmental Protection\nSafe Drinking Water Information System (SDWIS) is EPA’s national database that manages and collects public water system information from states, including reports of drinking water standard violations, reporting and monitoring violations, and other basic information. The data derived in the State of Pennsylvania is published and searchable online on the website. This set contains the Water System Facility data, which will be updated annually for the prior calendar year in the first Quarter of the following year."
 },
 {
  "sid": "s05",
  "text": "Fort Collins Shelter Service Data\nThis dataset shows data on the numbers served by Catholic Charities and Fort Collins Rescue Mission shelters in Fort Collins. It is updated monthly with the previous-month\"s data. These data are recorded by the shelters and compiled by the City of Fort Collins.\n\nTo note when using this data: the Rescue Mission does not have family rooms or accept children, and Catholic Charities does not report turnaways by gender."
 },
 {
  "sid": "s06",
  "text": "Nutrition, Physical Activity, and Obesity - National Survey of Children's Health (NSCH)\nThis dataset includes select data from the National Survey of Children’s Health (NSCH) sponsored by the Maternal and Child Health Bureau of the Health Resources and Services Administration, an Agency in the U.S. Department of Health and Human Services. The dataset includes the percent of children who eat fruits and vegetables less than once a day, 1–5-year-olds who drink sugar sweetened beverages, and infants who are fed anything other than breastmilk of formula before they are 4 months old. This data is used for DNPAO's Data, Trends, and Maps database, which provides national and state specific data on obesity, nutrition, physical activity, and breastfeeding. For more information about NSCH visit"
 },
 {
  "sid": "s07",
  "text": "2014 ITS World Congress Connected Vehicle Test Bed Demonstration Vehicle Situation Data\nDuring the 2014 ITS World Congress a demonstration of the connected vehicle infrastructure in the City of Detroit was conducted. The test site included approximately 14 intersections around Detroit’s COBO convention center and involved 9 equipped vehicles. The Vehicle Situation Data (VSD) data set includes a series of data files that recorded vehicle situational data that were generated by an equipped vehicle. During the ITS World Congress, VSDs were encoded with one of two schemas. The dataset contains decoded data using both 2.0 and 2.1 ASN.1 schemas."
 },
 {
  "sid": "s08",
  "text": "COVID-19 in Correctional Facilities\nJune 8, 2023: Daily transmission is no longer available.\n\nSummary of COVID-19 statistics for Connecticut correctional facilities including:\n\nTotal # of Staff Positive for COVID-19\nTotal # of Inmates Pos. for COVID-19\nCOVID-19 Pos. Inmates Housed at Northern CI Medical Isolation Unit\nCOVID-19 Pos. Inmates Housed at MacDougall-Walker Medical Isolation Unit\nCOVID-19 Pos. Staff Returned to Work\nTotal # of Inmates Medically Cleared\nTotal # of COVID-19 Pos. Inmate Deaths\n\nMore information can be found on the DOC website:\n\nData will be updated every weekday.\n\nAdditional notes:\nThe data on 7/15 reflects a decrease in the number of inmates testing positive for COVID-19 and those who have recovered; this decrease was due to an internal data audit that led to the removal of some duplicate information.\n\nThe data on 6/2/2020 reflects an increase in the number of inmates who had been medically cleared; this increase was the result of 146 asymptomatic positive inmates who had completed a 14-day isolation period."
 },
 {
  "sid": "s09",
  "text": "DQS NHANES Select Mean Dietary Intake Estimates\nThese data represent mean intake, on a given day, estimates of nutrients from foods and beverages from the National Health and Nutrition Examination Survey (NHANES).\nSearch, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from:"
 },
 {
  "sid": "s10",
  "text": "Housing Data by Type and Census Data [Archived]\nThis dataset has been archived and is no longer being updated by Ramsey County. This was originally for a point-in-time request and was not intended for indefinite updates.\n\nSummary data on housing by type (apartments, duplex/triplex, condo, single family, etc) and census block for 2016."
 },
 {
  "sid": "s11",
  "text": "Community Survey: 2017 Survey Data (Opt-in Non-representative)\nThe City of Bloomington contracted with National Research Center, Inc. to conduct the 2017 Bloomington Community Survey. This was the first time a scientific citywide survey had been completed covering resident opinions on service delivery satisfaction by the City of Bloomington and quality of life issues. This is the opt-in companion to that scientific survey. The statistically valid and representative survey results are available at\n\nAn additional 1,435 residents completed an opt-in survey online. The data in this collection is opt-in data and is provided in the interest of transparency. It is not recommended for analysis. The statistically valid and representative survey results are available at"
 },
 {
  "sid": "s12",
  "text": "2025-2026 Vaccine Exemption Rates by School (All Grades)\nThe annual pre-kindergarten (pre-K) through 12th grade school immunization survey collects school-level, grade-specific data on vaccine coverage and exemptions. The survey collects vaccination and exemption status data on children who entered the school system on or before a specified date during the fall semester. Individual vaccine information on each student is not collected.\n\nThis table shows the total percentage of vaccination exemptions (medical or religious) for each school. Data includes all schools who reported data students in any grade level Pre-K through twelve.\n\nAbbreviations\n\n• DS = Data Suppressed\n• DNC = Did Not Complete\n\nData Limitations and Considerations:\n• The school level data shown here are as tabulated and reported by schools and discrepancies may exist.\n• The Immunization Program identifies outliers and internally inconsistent data points and works with schools to resolve any data quality issues, when possible.\n• CT DPH cannot verify the accuracy of vaccine data for individual children or whether the documentation necessary to claim an exemption has been submitted.\n• Data are collected at the beginning of the school year, by which time vaccines are due. As the year progresses, immunization rates may increase as additional children receive required immunizations. Additionally, the student body is dynamic and as students arrive and leave school, the immunization rates are impacted.\n• Vaccine status is assessed on the level of the child and not on each vaccine. Once a child is listed as exempt, vaccination data is no longer collected in the survey for that child. Therefore, children with exemptions are not counted as vaccinated in the vaccine level assessments although they may have received some vaccines."
 }
]
