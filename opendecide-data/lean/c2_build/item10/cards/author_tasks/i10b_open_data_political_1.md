# Item 10 card authoring i10b_open_data_political_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10b_open_data_political_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of datasets published on government open-data portals.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: public affairs. The cards are about what kind of public or political matter a text is about, or how the text presents a decision or measure. Invent your own labels. Do not use left / right / centre or party scales, do not ask about any person's party, beliefs or character, and do not ask whether a named person or group is good or bad. The cards are about the text, not about people. A card must be answerable without knowing who any person or party is.
Card 1 angle: kind of public matter: what sort of public or political matter the text is about.
Card 2 angle: framing: how the text presents a decision, measure or event (for example as a cost, a benefit, a dispute, a routine step).
Card 3 angle: part of public life: which part of public life or which level of decision-making the matter touches.
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

{"task_id": "i10b_open_data_political_1",
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
  "text": "Appropriation Numbers and Titles by Agency and Appropriation Year\nAll 5-digit Appropriation numbers are listed in this file by 3-digit agency number and 2-digit appropriation year. These represent specific authority, granted by legislation in a given biennium or appropriation year, to expend or collect money. Regular appropriations are generally in the 13000 series"
 },
 {
  "sid": "s02",
  "text": "Educational Attaiment For The Population Ages 18-24 Years- ZIP Code Tabulation Areas 2010-2014\nThis dataset includes annual estimates of educational attainment for the population ages 18-24. Through its American Community Survey, the U.S. Census Bureau produces 5-year estimates for most geographies in the U.S, and its territories. The educational attainment estimates reports a percentage of the population who have completed increasing levels of education from less than high school completion to a bachelor’s degree or higher. Estimates are for the highest level of education completed.\n\nThis dataset is for the Census bureau defined ZIP Code Tabulation Areas (ZCTA). Though roughly formed with the U.S. Postal Service’s ZIP Code areas as a guide, across the nation the ZCTAs do not always conform to the exact boundaries of ZIP Code areas. However, in St. Louis County the boundaries rarely differ."
 },
 {
  "sid": "s03",
  "text": "Connecticut Population Projections - State, County, and Regional Councils of Governments Level, 2015-2040\nThe 2015 to 2040 population projections for the state of Connecticut were developed by the Connecticut State Data Center for planning, analysis, and to inform decision making. The projections are individual population projections for the resident population of Connecticut and were developed on July 31, 2017 and revised and republished on September 19, 2017 to address an error in the original dataset that was published on July 31, 2017. The County and Regional Council of Government Projections were published on June 29, 2018 and are based on the projections developed on September 19, 2017. These projections supersede the 2012 edition of the population projections developed by the Connecticut State Data Center."
 },
 {
  "sid": "s04",
  "text": "Annual Crime Incidents in Atlanta by Type\nThis dataset contains an annual count of crime incidents reported by the Atlanta Police Department (APD). It is based on incident-level data compiled from files released publicly by the ATP at The numbers in this dataset may vary from other published statistics because the numbers here represent crime incidents and data from other sources often represent crime victims."
 },
 {
  "sid": "s05",
  "text": "EWDD - Business Source Center Program Performance Objectives\nThe BSC Program, funded through the CDBG, provides entrepreneurial training, technical assistance and access to capital for micro-enterprise and start-up businesses. The program promotes job creation for Angelenos by providing entrepreneurs and small businesses the support they need to start and/or expand their businesses. Goals are established through HUD guidelines and local measures."
 },
 {
  "sid": "s06",
  "text": "Births to Teen Girls Ages 10-19\nThis dataset includes annual counts and rates of live births to girls ages 10-19 who are residents of St. Louis County. Data is collected, maintained and published by the Missouri Department of Health & Senior Services (HSS). Information on each birth and the mothers is gathered from birth certificates. HSS only reports the number of live births along with other health, social and demographic variables through the Missouri Information for Community Assessment (MICA) system. Rates of live births is calculated using both MICA and U.S. Census data.\nLive Births Per 1,000 Teen Girls for a specified time period is calculated as:\n(# Live Births to Girls Ages 10-19/Total Population of Girls Ages 10-19) x 1,000."
 },
 {
  "sid": "s07",
  "text": "PDI (Police Data Initiative) Traffic Stops (All Subjects)\nData Description: This dataset captures all subjects of traffic stops involving motor vehicles. Time of incident, officer assignment, race/sex of stop subject, and outcome of the stop (\"Action taken\") are also included in this data. Individual traffic stops may populate multiple data rows to account for multiple subjects and multiple outcomes: \"interview number\" is the unique identifier for every one (1) traffic stop.\n\nData Creation: Cincinnati Police Department (CPD) officers record all traffic stops involving motor vehicles via Contact Cards. Contact Cards are completed every time a CPD officer stops vehicles or pedestrians. The use of Contact Cards came out of the Collaborative Agreement.\n\nData Created By: The source of this data is the Cincinnati Police Department.\n\nRefresh Frequency: This data is updated daily.\n\nCincyInsights: The City of Cincinnati maintains an interactive dashboard portal, CincyInsights in addition to our Open Data in an effort to increase access and usage of city data. This data set has an associated dashboard available here:\n\nData Dictionary: A data dictionary providing definitions of columns and attributes is available as an attachment to this dataset.\n\nProcessing: The City of Cincinnati is committed to providing the most granular and accurate data possible. In that pursuit the Office of Performance and Data Analytics facilitates standard processing to most raw data prior to publication. Processing includes but is not limited: address verification, geocoding, decoding attributes, and addition of administrative areas (i.e. Census, neighborhoods, police districts, etc.).\n\nData Usage: For directions on downloading and using open data please visit our How-to Guide:\n\nDisclaimer: In compliance with privacy laws, all Public Safety datasets are anonymized and appropriately redacted prior to publication on the City of Cincinnati’s Open Data Portal. This means that for all public safety datasets: (1) the last two digits of all addresses have been replaced with “XX,” and in cases where there is a single digit street address, the entire address number is replaced with \"X\"; and (2) Latitude and Longitude have been randomly skewed to represent values within the same block area (but not the exact location) of the incident."
 },
 {
  "sid": "s08",
  "text": "CT State Library Cross-Index Search\nThis index is a handy way to search for a name or topic across a number of Connecticut State Library indexes. There may be more information contained in the original index than is included here.\n\nEach entry in this list has a location of either a record or a file. Records are a brief summary of the case and the court's verdict that can be found in court record books. Files may have more information, such as the original divorce petition, statements from the litigants and witnesses, costs, and other material.\n\nThere may be a small fee, depending on the size of the order and whether you would like a digital or physical copy. When requesting a copy of a record or file, please include the information from the relevant entry in the index. You are also more than welcome to visit the Connecticut State Library to see these materials for yourself!\n\nThe following indexes are included:\nPersons of Color Troop Enlistments from Connecticut in the Civil War 1863-65\nConnecticut Courant Index 1764–1799\nConservators & Guardians, 1699-1900\nConnecticut Divorce Index, 1655-1953\nFitch's Home for Soldiers, 1882-1936\nInquests into Deaths 1711-1892\nLoyalist Connecticut court records index, 1776-84\nMilitary Service Personnel Photograph Collection Index, c.1938-1953\nNoble Pension Records, 1861-1912\nConnecticut Nurses Census 1917\nConnecticut Paupers 1844 – 1907\nGov. Jonathan Trumbull Papers 1631-1784\nWethersfield Prison Records 1800-1903\nWW1 Veterans' Questionnaires"
 },
 {
  "sid": "s09",
  "text": "Monthly Building Permit Counts\nThis dataset contains counts of permits for privately-owned residential construction issued by local jurisdictions in the U.S. summarized by county. Permits are categorized by number of units within the building: 1 unit (single-family), 2 units (duplex), 3-4 units (tri-/quadra-plex), and 5+ units (apartment). Permit counts are given as both reported and imputed."
 },
 {
  "sid": "s10",
  "text": "COVID-19 Assistance\nGrants provided in Fiscal Year 2021 to businesses, hospitals, tenants/landlords, public municipalities, and community organizations to deliver various forms of relief to impacts of the COVID-19 pandemic. Funding for these programs comes from federal and state allocations.\n\nBusiness Oregon continues to update pandemic related materials on its site. Most information can generally be found at"
 },
 {
  "sid": "s11",
  "text": "City of Denver Pending Short Term Rentals\nThis dataset represents Short Term Rental business licenses (issued in the City of Denver) with a pending renewal record associated with it. 11/6/2025 Update: Deprecated due to short term rental licenses and pending rentals being combined into one dataset by Denver. See this dataset for up to date info:"
 },
 {
  "sid": "s12",
  "text": "Traffic Route Stats\nThis dataset contains historic Route Definitions and Statistics with Geometry of traffic flow. The detailed documentation is included at\n\nDisclaimer : Even though the real-time API updates the info every 30 seconds, we only sample at every 5 minutes for historical archiving"
 }
]
