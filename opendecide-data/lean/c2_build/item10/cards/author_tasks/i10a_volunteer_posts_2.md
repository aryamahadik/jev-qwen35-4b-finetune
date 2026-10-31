# Item 10 card authoring i10a_volunteer_posts_2

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_volunteer_posts_2.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are volunteer opportunity postings from a county volunteer centre.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: skills: what the volunteer needs to bring, where neighbouring answers are easy to confuse.
Card 2 angle: setting: where and in what conditions the work happens, where neighbouring answers are easy to confuse.
Card 3 angle: match: which kind of person the posting suits best, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_volunteer_posts_2",
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
  "text": "Patient Care Volunteers\nUnder the supervision of the clinical staff, provide fresh water, ice & & juice to patients; refill gloves containers; restock nurse servers and thermometer probes; fill out menus for patients; help patients with TV and lighting controls; assist staff with other duties as directed.\nHours: 8am-12 pm; 12 pm - 4pm; 4pm - 8pm or, 2 hour shifts\nAge requirement: 15-120"
 },
 {
  "sid": "s02",
  "text": "Treasurer- Urgently needed\nThe Treasurer of UMAN has the broad responsibility of ensuring that UMAN operates in a fiscally sound and responsible manner.\n\nMAJOR DUTIES AND RESPONSIBILITIES\nAttending monthly Board meetings\nOversee and assist in maintaining UMAN’s financial records\nAssists /reviews Federal, State and Local filings such as Form 990, quarterly payroll report, etc.\nPrepares and distributes monthly financial statements\nPrepares annual budget\nArranges for annual financial review\nKnowledge of Quickbooks necessary\nHours: varies from 1-3 hours/month\nAge requirement: 18-120"
 },
 {
  "sid": "s03",
  "text": "Food packing and distribution\nVolunteers needed for food packing and distribution on Saturdays from 9am to 11am at the College Park Community Food Bank. We are a Community Food Bank in two important ways: we serve the broader College Park community and the broader community supports us with vital donations of money and food items.\nFor more information, please see our website:\nStudent participation in this service project is at the discretion of the student’s parent/guardian and must be completed outside of school hours. The nonprofit organization is responsible for maintaining student safety.\nHours: 9am - 11am\nAge requirement: 14-120"
 },
 {
  "sid": "s04",
  "text": "Kitchens helpers needed\nKitchen helpers assist in making the food we deliver to homebound neighbors. The work includes packing a cold and/or a hot lunch. Volunteers also help, as needed, with cleaning the kitchen after the meals are completed. Volunteers are needed for two shifts, Monday - Friday at 9:00 a.m. - 11:30 a.m. and 12:15 p.m. - 2:15 p.m.\nTraining will be provided on the first day. Volunteers under the age of 16 will need to volunteer with a parent or guardian.\nWhat we need from each person is:\n1. Name:\n2. Address:\n3.\n4.\n5.\n6. Which days of week are best\n\nHours: Monday-Friday 9:00 to 12:00 or 12:15-2:15\nAge requirement: 0-0"
 },
 {
  "sid": "s05",
  "text": "Grown@Pope Volunteer Workdays | Pope Farm Nursery | Gaithersburg\nMontgomery Park's Grown@Pope program strengthens food security in the county and provides families with fresh produce grown on parkland. Grown@Pope Workdays are for individuals or groups that would like to come in for 1 to 3 days this season to help with daily tasks. Workday dates and times will be arranged with the program manager, after you apply. If you're interested in committing more time to this program, please consider signing up for the Crop Production Aide position instead!Workdays are scheduled for 2-to-4-hour shift during the week, between the hours of 7am and 3pm (but usually in the morning). Volunteers will assist with planting summer crops and maintaining the garden. They will work alongside staff to harvest, collect, and weigh produce to be donated to food assistance providers across Montgomery County. The work includes: hand planting seeds as needed, monitoring crops upon emergence, pruning and thinning crop plants as needed, rotation (turning) of larger crops and harvesting crops when they are ready to go! Instruction and tools will be provided. For Individuals, the program manager will send you a list of dates and times to choose from. Families are welcome, but children 15 and under must be supervised by their 18 years+ guardian on a one-to-one ratio. You must be 16 or older to volunteer on your own. SSL Approved!For Groups, this is a great opportunity for team building and learning new skills with your friends, co-workers or any other type of group. After applying the program manager will be in touch to discuss all of the details. Be sure to register as a GROUP on the volunteer application, as the group leader.\nStudent participation in this service project is at the discretion of the student’s parent/guardian and must be completed outside of school hours. The nonprofit organization is responsible for maintaining student safety.\nHours: between 7 am and 3 pm\nAge requirement: 12-120"
 },
 {
  "sid": "s06",
  "text": "High School and College Volunteers to help with after school sports for elementary school kids.\nHigh School and College volunteers needed to assist Lead Coaches in after-school sports programs at elementary schools in Montgomery County. Volunteers will assist Coaches with instruction and lead small groups as necessary. Sports include basketball, soccer, dance & cheer, flag football, and martial arts. Experience in a specific sport is not necessarily required.\nVolunteers must have transportation to and from sites and be available between 3-5 pm on weekdays. Specific times will vary according to the particular school site.\nHours: 3 pm - 5 pm\nAge requirement: 14-120"
 },
 {
  "sid": "s07",
  "text": "Help Homeless Neighbors in Montgomery County! (for individuals, groups, kids, and teens)\nThank you for your interest at Bethesda Cares and wanting to serve those in need. With the spread of COVID-19, we want to preserve the safety and health of our clients, volunteers, and staff, and have determined it is best to suspend all-volunteer services as we seek to minimize community spread. Additionally, we are not accepting any walk-in/drop off donations at this time.\nIn the meantime, we appreciate any support you can give Bethesda Cares in one of the multiple ways:\n1) Please consider making a financial contribution to Bethesda Cares. Our priorities are shifting every day as the news develops, and our clients’ needs change. Monetary donations allow us to be flexible in obtaining items and supplies that we need to meet this constantly evolving situation. You can donate to Bethesda Cares at this link:\n2) We greatly appreciate $5-$10 gift cards to Giant Foods, Safeway, or Target (or a similar grocery store) to assist clients with purchasing needed household/ grocery items. Gift cards of any amount to McDonalds, Subway, Dunkin Donuts, or Starbucks are also accepted for our street outreach team to buy a warm meal or drink for clients sleeping on the streets. These can be mailed to: 7728 Woodmont Ave., Bethesda, MD 20814. Please include your name (we keep a record of each gift card donated and distributed).\n3) If you would prefer to donate items (such as canned goods and nonperishable items), let us know, and we will add you to a rapid response list, and reach out to you when specific needs come up.\nPlease be safe, take care of your health, and know we truly appreciate your commitment to serving those less fortunate in our community.\nNot approved for MCPS SSL hours. While we welcome all donations, students may not earn SSL hours for individual donations or for hosting book drives virtually or from home. See guidelines for agencies on how virtual opportunities may be considered for SSL.\nAge requirement: 0-0"
 },
 {
  "sid": "s08",
  "text": "Looking for host families for high school exchange students!\nDo you want to make a difference in a young person's life while you learn about another culture, create and build friendships and make ever-lasting memories? Do you have a caring heart and extra space in your home? AnB Education is looking for you! Make a difference today and host an international student!\nAll our students need is:\n-A bedroom (can be shared with same gender host sibling)-3 meals a day-Transportation to and from school if there are no school buses provided\nStudents will have their own spending money for personal items, activity fees, and any other costs.\nExchange students are between the ages of 15 and 18, and coming mostly from China, South Korea, and Vietnam.\nAnB Education will get the students enrolled at your local public high school and provide support throughout the program year. We have a Local Coordinator in the area who is excited to work with you!\nCompany website: Application:\n\nAvailable Students to be placed in Montgomery County:\nZhihao (Justin), 15-year-old boy from China\nZhihao is very smart and his teachers speak highly of him. They say that he is able to communicate with native English speakers very well, takes on new challenges, and has many talents, particularly in Math and even performing arts! His hobbies include playing the piano, badminton, and making art. Grade: 9\n\nThuy (Jenny), 16-year-old girl from Vietnam\nJenny speaks English almost fluently after a year of studying in Australia! She enjoys drawing, painting, playing the piano, and dancing. Her favorite subjects are Math and Science. She hopes to become a pilot one day! Grade: 10\n\nAge requirement: 0-0"
 },
 {
  "sid": "s09",
  "text": "A writer and a graphics person for a Quarterly Newsletter\nChevy Chase At Home is a small nonprofit in Chevy Chase, MD. We help older residents age-in-place by providing volunteer services and social programming.\nWe are seeking another writer and a graphics volunteer to assist our Communications Committee to package our quarterly newsletters.\nThis collegial Communications Committee meets/Zooms monthly to create content based upon happenings at the agency.\nWe need a volunteer to package the 4-6 page content into a simple standardized format. We have a template and can teach the volunteer how to insert the articles.\nThe volunteer(s) are not required to attend meetings live - unless they wish to.\nThe newsletter goes out in print March, June, September, December/January.\nHours: flexible\nAge requirement: 18-120"
 },
 {
  "sid": "s10",
  "text": "Food Packers and Distributors Needed To Help Feed the Hungry -- Saturdays in DT Silver Spring\nVolunteer Food Packers/Distributors Needed on Saturdays\nHarvest Intercontinental Church in Downtown Silver Spring needs volunteers to help them with their regular food drives:\nPacking food : Every Saturday from 9:00AM - 12:00PM\nFood Distribution (drive-thru): Every Saturday from 12:00PM - 2:00PM\nIt would be great if volunteers could sign up for regular shifts on Saturday for either packing food, distributing food, or both!\nSpecific instructions will be given when you arrive at the distribution site. Volunteers should wear comfortable attire, be able to stand for 2-3 hours and be able to lift and move minimum of 10-15 pounds repeatedly.\nCOVID-19 Protocol: All volunteers are required to have their masks on before entering the building and will have their temperature check upon arrival. Gloves will be provided to wear at all times while serving.\nAge requirement: 0-120"
 },
 {
  "sid": "s11",
  "text": "Wednesday Adult Volunteer Needed in White Oak area for Early-Stage Dementia Social Club Program\nThe JCA Samuel J. Gorlitz Kensington Clubs are 4-HOUR social clubs designed for older adults in the early stage of memory loss between 9:30-1:30pm on Wednesdays. Experienced staff and volunteers help provide social activities to Club members. Club members are independent with walking and all personal cares. They participate in group games, exercise, art therapy, music therapy, and discussion and then return home again after four hours. A weekly volunteer to assist the manager and activity leader is needed for the club location at the Kensington Club at White Oak Senior Center in Silver Spring.\nHours: Wednesdays 9:15-1:45pm\nAge requirement: 18-120"
 },
 {
  "sid": "s12",
  "text": "Board Leadership Opportunities Developing Youth and Supporting Families\nWe are GROWING and expanding our Leadership Team by conducting a search for candidates to fill vacancies on our Board of Directors and our Board of Trustees.\nIf you have time, energy, and skills to contribute to help us develop youth, build community, fundraise, expand our nonprofit, and promote character, development, and fun, please consider joining our Leadership Team.\nWe are have a variety of leadership, strategy, and operational support opportunities. Skills in highest demand include: General Board Experience, Operations, Franchising, Grant Writing, Events Coordination, Business Development, Child Development, Financial Management, Coaching Curriculum Development, Sponsorship Development, Marketing and Communications, Donor Care and Communications, and Volunteer Management.\nThank you for your consideration.\n<img style=\"float: left;\" src=\" alt=\"\" width=\"100\" height=\"100\" />\n\nAll volunteers working directly with youth must pass a background investigation and complete basic safety training in youth protection.\n\nHours: weekly\nAge requirement: 25-120"
 }
]
