# Item 10 card authoring i10a_open_data_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_open_data_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are descriptions of datasets published on government open-data portals.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: subject area: which area of public life the dataset is about, where neighbouring answers are easy to confuse.
Card 2 angle: detail level: what one record in the dataset stands for, where neighbouring answers are easy to confuse.
Card 3 angle: first look: which kind of team should look at the dataset first, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_open_data_2",
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
  "text": "ACT Nature Conservation Act - Protected Native Species List\nIn the ACT, native wildlife are protected under the Nature Conservation Act 2014 (the NC Act). Greater protection for both native plants and animals is provided through listing processes. Native species may receive additional protection through two mechanisms: special protection status (SPS) and inclusion on the Protected Native Species List.\n\nSpecial protection status applies automatically to any native species that is:\n\na threatened native species under the Act,\na listed threatened species, or\na listed migratory species under the Environment Protection and Biodiversity Conservation Act 1999 (Cth).\nSpecies with special protection status may have conservation plans or action plans prepared for them.\n\nSeparately, the Minister must establish a Protected Native Species List (this list), which identifies non‐threatened native species requiring additional protection within the ACT (for example, species that may be at risk in other jurisdictions, naturally rare in the ACT, data‐deficient, or facing pressure from trade or collection). The list must be divided into categories, including:\n\nRestricted trade – species for which unrestricted trade could negatively impact wild populations. This may include taxa listed under legislation in another jurisdiction.\nRare – species that are rare in the ACT but are not threatened and do not have special protection status.\nData deficient – species for which there is insufficient information to assess eligibility for threatened status or other categories.\nAny other category prescribed by regulation.\n\nThe Minister is responsible for developing the criteria and decision‐making processes for determining whether a species is to be included in a category. The criteria must focus solely on scientific matters and be prepared in consultation with the Scientific Committee. The Nature Conservation (Protected Native Species List) Criteria and Processes 2025) criteria is a disallowable instrument.\n\nThe criteria may be reviewed if the conservator or Scientific Committee considers them inadequate or inconsistent with changing national or international standards. If a review is requested, the Minister must consider the recommendation and either undertake a review or issue a notifiable refusal with reasons.\n\nNgunnawal names have been provided in consultation with the Winanggaay Ngunnawal Language Aboriginal Corporation © Winanggaay Ngunnawal Language Aboriginal Corporation."
 },
 {
  "sid": "s02",
  "text": "PRESENCE OF A COMPUTER AND TYPE OF INTERNET SUBSCRIPTION IN HOUSEHOLD\nPRESENCE OF A COMPUTER AND TYPE OF INTERNET SUBSCRIPTION IN HOUSEHOLD\nUniverse: Households\nAmerican Community Survey 1-Year Estimates\nACS Table: B28003\n\nThis dataset can be updated via the Census API using this workspace:\ndata.countyofriverside.us - Count of device... - pns3-pyie - FMEv2016.fmw"
 },
 {
  "sid": "s03",
  "text": "Illinois Criminal Justice Information Authority Active Grants Beginning SFY16\nThis is a list of all grants issued by the Illinois Criminal Justice Information Authority that were active at any point beginning with State Fiscal Year 2016 (7/1/2015) through the most recent quarter. Some of our grantees are agencies such as domestic violence shelters and drug task forces. Their Zip Codes are considered sensitive information and are not disclosed in this dataset."
 },
 {
  "sid": "s04",
  "text": "Docked Bikeshare Ridership\nHistoric data updated on 07/14/2023. Q4 of 2023 and data for all years on systems allowing parking outside of a docking station updated on 06/04/2024.\n\nBikeshare ridership by system for bikeshare systems with docking stations. Data summarized for each system by: (1) month, (2) day, and (3) hour. Data starting in January 2019. In monthly summary, months are rearranged to include the same number of days of the week across years (see below).\n\nRidership data not available for all docked bikeshare systems. Only docked bikeshare systems with ridership data shown. Some systems included in the data permit users to leave a bicycle outside of a docking station; these trips are indicated by the trip type. Trips defined as rides from point A to B. If user makes trip from B to A on same day, counted as a second trip. Trips labeled as round trips in Metro Bike Share and Indego trip files counted as 2 trips. Trips with no trip time are not counted. For trips starting and ending at a docking station or on systems where only docked trips are permitted, trips with no start station identifier and/or end station id are not counted in totals. Trips shorter than 1 minute or greater than 2 hours excluded. In monthly summary, days aligned to include the same days of weeks across years.\n\nDays included in each month can be found in the attachments (\n\nData visualizations available at:"
 },
 {
  "sid": "s05",
  "text": "Department of Recreation and Parks' Facility and Park Information\nThe Department of Recreation and Parks' Facility and Park Information dataset provide information such as facilities and parks' addresses, contact phone numbers, websites, and mapping info by categories: beaches, camps, dog parks, equestrian centers, gardens, golf courses, lakes, museums, public computer centers, recreation centers, rental facilities, senior centers, skate parks, swimming pools, tennis courts, and theatres; and amenities: baseball/softball fields, basketball courts, hiking trails, outdoor fitness equipment, swimming pools with diving boards and universally accessible playgrounds."
 },
 {
  "sid": "s06",
  "text": "Historical Agency Expenditures – Multi-Year Report (2014 - 2018)\nThis is a historical listing of state agencies expenditure data covering fiscal years (2014 - 2018). The data and information provided in this dataset is for educational and informational purposes. The format of data and information being reported was for years 2014 - 2018. Visit the Oregon Transparency website for more current expenditure data, information, and reporting formats."
 },
 {
  "sid": "s07",
  "text": "$10M Demolition List\nThis dataset contains a list of the dangerous buildings that are scheduled to be demolished through the $10,000,000 demolition program.\n\nHow is this different than the dangerous buildings list? - This is a list of the structures that are being demolished through the $10M program. Additional cases will only be added to the $10M Demolition list for emergency reasons, however as the city discovers new dangerous buildings they will be added to the Dangerous Buildings List."
 },
 {
  "sid": "s08",
  "text": "Calls for Service 2018\nThis dataset reflects incidents that have been reported to the New Orleans Police Department in 2018. Data is provided by Orleans Parish Communication District (OPCD), the administrative office of 9-1-1 for the City of New Orleans. In the OPCD system, NOPD may reclassify or change the signal type for up to 36 hours after the incident is marked up. For information about an incident after this time period, citizens may request police reports from the NOPD Public Records Division. In order to protect the privacy of victims, addresses are shown at the block level and the call types cruelty to juveniles, juvenile attachment and missing juvenile have been removed in accordance with the Louisiana Public Records Act, L.R.S. 44:1. Map coordinates (X,Y) have been removed for the following call types: Aggravated Rape, Aggravated Rape - MA, Crime Against Nature, Mental Patient, Oral Sexual Battery, Prostitution, Sexual Battery, Simple Rape, Simple Rape - Male V, and Soliciting for Prost.\n\nPlease request 911 audio via our public records request system here:\n\nDisclaimer: These incidents may be based upon preliminary information supplied to the Police Department by the reporting parties that have not been verified. The preliminary crime classifications may be changed at a later date based upon additional investigation and there is always the possibility of mechanical or human error. Therefore, the New Orleans Police Department does not guarantee (either expressed or implied) the accuracy, completeness, timeliness, or correct sequencing of the information and the information should not be used for comparison purposes over time. The New Orleans Police Department will not be responsible for any error or omission, or for the use of, or the results obtained from the use of this information. All data visualizations on maps should be considered approximate and attempts to derive specific addresses are strictly prohibited. The New Orleans Police Department is not responsible for the content of any off-site pages that are referenced by or that reference this web page other than an official City of New Orleans or New Orleans Police Department web page. The user specifically acknowledges that the New Orleans Police Department is not responsible for any defamatory, offensive, misleading, or illegal conduct of other users, links, or third parties and that the risk of injury from the foregoing rests entirely with the user. Any use of the information for commercial purposes is strictly prohibited."
 },
 {
  "sid": "s09",
  "text": "Bloomington Enterprise Zone\nThis map data layer represents the boundary for the Bloomington Urban Enterprise Zone. The data is divided into sections which separate expansion areas from the original enterprise zone area. These sections have no meaning relevance to the eligibility of properties within the zone."
 },
 {
  "sid": "s10",
  "text": "Tampa CV Pilot Basic Safety Message (BSM) Sample\nThe Tampa CV Pilot generates data from the interaction between vehicles and between vehicles and infrastructure. This dataset consists of Basic Safety Messages (BSMs) generated by participant and public transportation vehicles onboard units (OBU) and transmitted to road-side units (RSU) located throughout the Tampa CV Pilot Study area. The full set of raw, BSM data from Tampa CV Pilot can be requested from the ITS DataHub Sandbox . The data fields follow SAE J2735 and J2945/1 standards and adopted units of measure.\n\nThis dataset holds a flattened sample of the BSM data from Tampa CV Pilot. An extra geo column (coreData_position) was added to this dataset to allow for mapping of the geocoded BSM data within Socrata, and a column of random numbers (randomNum) was added to allow for random sampling of data points within Socrata."
 },
 {
  "sid": "s11",
  "text": "Intake\nThis dataset is no longer actively maintained as of 12/30/2024. Please visit the site below to explore data dashboards published by the State’s Attorney’s Office beginning 2025.\nData Dashboards | Cook County State's Attorney\n\nThe intake data presented in this data reflects the cases brought in for review. Each row represents a potential defendant in a case."
 },
 {
  "sid": "s12",
  "text": "Neighborhood Conservation Districts\nSec. 26-3. - Neighborhood Conservation District (NCD). (a) The NCD shall encompass the area generally bounded, on the east bank of the Mississippi River, by the Orleans/Jefferson Parish line, Metairie Road, Interstate 10, Norfolk-Southern Railroad track, Orleans Avenue, City Park Avenue, Wisner Boulevard, Interstate 610, Florida Boulevard, the Orleans/St. Bernard Parish line, and the Mississippi River; on the west bank, the NCD shall encompass the area generally bounded by Atlantic Avenue, Bodenger Boulevard, the Orleans/Jefferson Parish line, and the Mississippi River, as well as all National Register Historic Districts that are on the National Register of Historic Places, pursuant to 16 U.S.C. 470 et seq., section 26-11, and other applicable laws. Any National Register Historic Districts created after the adoption of this ordinance shall be included within the boundaries as well. In addition to the Gentilly Terrace National Register District, the area bounded by the following streets, and those properties fronting on the bounding streets, shall be deemed to be part of the NCD: beginning at Elysian Fields Avenue at Gentilly Boulevard, north along Elysian Fields Avenue to Filmore Avenue, east along Filmore Avenue to Peoples Avenue, south along Peoples Avenues to Gentilly Boulevard, and along Gentilly Boulevard back to Elysian Fields. (b) The purpose of the NCD shall be:(1) To attempt to preserve those buildings within the NCD having a historical or architectural value or buildings that contribute to the overall character of the neighborhood. (2) To preserve and stabilize neighborhoods through the protection of those structures that represent the character and quality of the neighborhood or the architectural history of New Orleans. (3) To promote redevelopment that contributes to the historic character of the neighborhood.(Ord. No. 19,791, § 1, 8-3-00; M.C.S., Ord. No. 22882, § 1, 11-1-07; M.C.S., Ord. No. 23005, § 1, 2-21-08; M.C.S., Ord. No. 23764, § 1, 11-5-09; M.C.S., Ord. No. 23820, § 1, 12-1-09; M.C.S., Ord. No. 26037, § 1, 9-18-14)"
 }
]
