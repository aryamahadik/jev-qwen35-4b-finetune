# Item 10 card authoring i10a_volunteer_posts_1

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/item10/cards/author_answers/i10a_volunteer_posts_1.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands, do not use the web, and use only the Read and Write tools.

Items: 12. Answers expected: 3.

## Instructions

You are helping design decision tasks for a small text classifier.
The 12 example texts below are volunteer opportunity postings from a county volunteer centre.
Write exactly 3 task cards. Every card is a CHOICE question with 4 to 8 options (5 or 6 is best).
SLICE: boundary pairs. The cards are about intent or topic where neighbouring answers are easy to confuse, like the hard choices in a help-desk or routing system. Build every card so that its options are near neighbours.
Card 1 angle: kind of work: what sort of work the volunteer would do, where neighbouring answers are easy to confuse.
Card 2 angle: commitment: how much time and regularity the posting asks for, where neighbouring answers are easy to confuse.
Card 3 angle: who benefits: whom the volunteer work helps directly, where neighbouring answers are easy to confuse.
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

{"task_id": "i10a_volunteer_posts_1",
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
  "text": "Deliver Meals with Parent/Adult in Montgomery County\nDeliver meals out of our distribution site at Leisure World! Meal delivery takes place Monday-Friday, 11am-12:30pm. Routes take about an hour to complete. Volunteers use their own vehicles and typically help once a week on a consistent weekday. Substitute positions available! Volunteer orientation required. Parent/guardian must accompany teen volunteers and consent to a background check. Great for days off of school and summer/winter break!\nNot approved for MCPS SSL hours. See guidelines for agencies on how virtual opportunities may be considered for SSL.\nHours: 11am-12:30pm\nAge requirement: 0-0"
 },
 {
  "sid": "s02",
  "text": "Volunteer Opportunity for 50+ & retirees - teach English!\nThe Latino Student Fund is inviting the 50+ and retirees to volunteer in assisting non-English speakers learn or master the English language. If you always had a passion for teaching this is the opportunity you have been searching for - come join us!\nSkills Needed:\n\nHigh School Diploma / GED (Minimum)\nPass a criminal background check\nAttend Volunteer Training\nCommit to 1-3 hours weekly/1-3 hours biweekly (at your convenience)\nInternet Connection\nOwn Smart Device (laptop, computer, iPad, android, etc.)\n\nThank you and we look forward to having you on board.\n\nHours: Flexible\nAge requirement: 50-120"
 },
 {
  "sid": "s03",
  "text": "Group Volunteering\nAre you a part of a youth/adult group, 4H club, church group, Scout troop, class, team, or any group of people that want to work together and do good? Sign up together to volunteer as a team and have some fun on the farm!\nVolunteer groups make a difference in the lives of our horses while promoting community and team spirit.\nScheduled group volunteer days are flexible and can be catered towards the need(s) of your team. Volunteers will help with an assigned project that could include, but is not limited to:\n\nWorking on landscaping\nWorking on building/maintenance projects\nVolunteer in the barn and help with daily chores\nOther team interests!\n\nGroups are welcome to have full use of our outdoor pavilion or indoor classroom for lunch or to use as a place to meet and follow up about the day.\nStudent participation in this service project is at the discretion of the student’s parent/guardian and must be completed outside of school hours. The nonprofit organization is responsible for maintaining student safety.\nHours: 9am-4pm\nAge requirement: 5-120"
 },
 {
  "sid": "s04",
  "text": "Description\nThis opportunity takes place in-person at our Silver Spring location.\nVolunteers support our referral program which enables our participants to receive food from us and so much more!\nVolunteers will use our Salesforce database for scheduling our participants and entering agency referrals.\n\nSkills and Qualifications\n\nInterested candidates should friendly and possess strong customer service skills and be able to problem solve and multi-task in a fast-paced office environment.\nVolunteers will assist people from a diverse background.\nWe are looking for volunteers that can make a regular weekly commitment for at least 6 months to a year.\nVolunteers must be 18 or older.\nBi-lingual skills are a plus but not required.\nThis opportunity is not open to people needing to complete service hours.\n\nAvailable Shifts\n\nWednesdays: 9am-12:30pm\nWednesdays: 12:30pm-4pm\nThursdays: 9am-12:30pm\nThursdays: 12:30-4pm\nFridays: 9am-12:30pm\nFridays: 12:30-4pm\n\nTraining and Materials\nVolunteers will complete an in-person training over 5 consecutive days.\nAge requirement: 18-120"
 },
 {
  "sid": "s05",
  "text": "Battle Buddy\nBATTLE BUDDY to help VETERANSWe have many patients who are veterans and we would like to have volunteers who are veterans visit them. You would be assigned a veteran to visit. Weekly visits of about 1 -2 hour is typically what is needed to establish a connection and provide support to your battle buddy. Veterans will often not open up to civilians (even family members) but they will to other veterans. Battle Buddies provide our veterans with a much needed friend, someone who understands. In addition, we provide specialized Ceremonies to our veterans as a way of honoring the service they gave to our country. Battle Buddies will gather information on the veterans service so we can read it at the ceremony. We also have special lapel pins and certificates for the veteran which the volunteer can present. We are currently providing ceremonies in person. This is a great way to honor veterans. Veterans often need other Veterans to talk with, they understand the language and provide a \"safe place\" to discuss issues. Please consider sharing your time with our veterans. They served us, let's serve them.MUST BE COVID VACCINATED WITH BOOSTERMUST BE ABLE TO PROVIDE 4-8 HOURS PER MONTHMUST BE ABLE TO COMMIT TO 1 YEAR SERVICETwo set TB test required, Flu Shot required, and background checkHospice Training providedMATURE AND COMMITTED INDIVIDUALS NEEDED\nHours: Weekdays, weekends (4-8 hours a month)\nAge requirement: 18-120"
 },
 {
  "sid": "s06",
  "text": "OFFICE WORKER VOLUNTEERS - KIDS IN SHOWBIZ / Z SUPER CHANNEL\nKids In Showbiz is seeking Volunteer Office Workers to help with Office, Administrative, Clerical and Data Entry work. Kids in Showbiz/Rise Training School/Z Super Channel provides professional training and a world class education to Youth and Young Adults in the Multimedia field. We welcome you to join us!\nHours: 1pm to 5pm; 2pm to 6pm; 3pm to 7pm.\nAge requirement: 18-65"
 },
 {
  "sid": "s07",
  "text": "Supply Drive Coordinators\nReach is seeking supply drive coordinators to inventory supplies at our main office and our Mansfield Kaseman Health Clinic and coordinate the collection, delivery, and organization of new supplies on an as-needed basis. The types of supplies most needed are housewares, cleaning supplies, toiletries, and gift cards that will benefit our Clinic and Housing Program clients.\nNot approved for MCPS SSL hours. See guidelines for agencies on how virtual opportunities may be considered for SSL.\n\nHours: Hours may vary\nAge requirement: 18-120"
 },
 {
  "sid": "s08",
  "text": "Package and Distribute Food for COVID-19 Relief\nDescription:\nWe are currently looking for volunteers 18+ to assist with food recovery operations at Nourish Now. During this pandemic we are currently feeding family students and seniors in the DC metropolitan area. We need volunteers at our warehouses in Rockville and distribution sites in the Gaithersburg and Rockville area. Warehouse volunteers shifts are from 9:30am-12:30pm and from 12:30pm-3:30pm.\n\nWarehouse Volunteers will:\n\nAssist with warehouse tasks such as creating and preparing boxes given at distribution sites.\nMay be asked to deliver food to local families in the area.\n\nDistribution Site Volunteers will:\n\nAssist with handling and putting boxes in the cars of people picking up food.\nGather and record information from event. (If bilingual, that would help tremendously)\n\nBackground of Nourish Now:\nNourish Now is a 501c3 nonprofit food bank, specializing in food recovery and providing donations from grocers, caterers, restaurants, bakeries, and other food donors for the benefit of children, families, and the elderly, as well as shelters, food pantries, and other organizations working to end hunger. Through our programs, viable food partners are identified, and donations of food are recovered and redistributed through our network.\nHours: 9:30am-12:30pm, 12:30pm-3:30pm\nAge requirement: 18-120"
 },
 {
  "sid": "s09",
  "text": "Emergency Response - Donate Now - Friendship Place\nFriendship Place has an urgent appeal to help us meet new and unexpected needs during the Covid-19 health crisis and for the period after this crisis subsides through $100,000 in new support.\nYour support enables us to do this life-saving work for the over 3,300 people Friendship Place serves each year.\nPlease donate today to help us provide food to families in need, conduct critical street outreach to at-risk people, and prepare for an influx of people for whom this crisis will last for years.\nThank you for all you do to make Friendship Place’s work possible.\nDonate By Clicking Here\nFriendship Place is the premier provider of housing services for people experiencing homelessness in the Washington DC region. Our innovative, customized, person-focused programs produce demonstrative and lasting results. We empower our participants to rebuild their lives, find homes, get jobs and reconnect with friends, family and the community, permanently.\nOur goal is to end homelessness in Washington, DC, and to establish a sustainable model which can be replicated across the nation.\nIn 2019, our programs ended or prevented homelessness for 1,437 people through creative, customized housing solutions. Across all of our programs, Friendship Place served more than 3,305 individuals in 2019.\nAge requirement: 0-0"
 },
 {
  "sid": "s10",
  "text": "Marketing and Social Media Manager (Internship)\nDevelopIT Inc. is a 501(c)(3) nonprofit with the goal of creating future leaders in technology by offering a free program that includes hands-on applications and student-led learning environments. We are looking for student volunteers to serve as Marketing & Social Media Managers to help develop social media marketing content and campaigns to increase visibility, engagement, and community involvement.\nIf you are interested in earning SSL hours for this activity, please let us know. We will review your marketing material or campaign plans (template for content creation will be provided) and approve them for execution within the organization by our core team. Once we have reviewed your submissions, we will award SSL hours according to the following equivalency:\n\n1 marketing collateral created (e.g., flyer, brochure, etc.) = 2 SSL hours\n1 marketing video created = 4 SSL hours\n\nVolunteers will also attend check-in meetings with our core team through a virtual platform (Google Meet) using their personal/private accounts and SSL hours will also be granted for meetings (1 meeting hour = 1 SSL hour).\nIf you are interested in the position, please submit an application on our website:\nAdditional Information Regarding Opportunity:\n\nStudent participation in this service project is at the discretion of the student's parent/guardian.\nThe nonprofit organization is responsible for maintaining student safety and privacy.\nThe nonprofit organization will determine the number of SSL hours awarded based on the evidence submitted.\nA student's parent / guardian must provide the nonprofit with written approval of the student's participation in the virtual platform prior to the student serving/volunteering.\nStudents must use personal/private accounts (not MCPS student accounts) to engage in the virtual platform.\nStudents will only engage with others under the direct supervision of a nonprofit supervisor. The nonprofit supervisor will be directly present in the virtual space (including any breakout sessions) at all times.\nThe nonprofit supervisor will initial and host all virtual sessions. If the nonprofit supervisor is not available to initiate and host the virtual session, the session will not occur.\nVirtual sessions will not be recorded.\n\nStudent participation in this service project is at the discretion of the student’s parent/guardian. The nonprofit organization is responsible for maintaining student safety and privacy at any time the student is interacting with the nonprofit and its clients. The nonprofit organization will determine the number of SSL hours awarded based on the evidence submitted."
 },
 {
  "sid": "s11",
  "text": "Program Volunteers\nGreat and Small is looking for volunteers to support our therapeutic riding program working with participants and horses. All volunteers must attend an orientation and then additional training as needed. We offer program spots on a weekly per session basis and during summer camp. All volunteers will agree to abide by all County and State COVID-19 regulations and health safety practices. Join us today!\nApply to volunteer at\nStudent participation in this service project is at the discretion of the student’s parent/guardian and must be completed outside of school hours. The nonprofit organization is responsible for maintaining student safety.\n\nHours: Monday to Saturday 12-6\nAge requirement: 14-85"
 },
 {
  "sid": "s12",
  "text": "Online Sales -- Non-Profit Bridal Boutique\nJoin a fantastic Volunteer Staff at Fairytale Brides on a Shoestring Boutique. Volunteer to be an Online Sales/Marketing Coordinator who can commit some of your time to postings of online sales of bridal, bridal accessories on retail sites. Online Experience important, willing to learn, enthusiastic and reliable. Fairytale Brides on a Shoestring Boutique is a non-profit 501(c)3 Bridal Boutique in the DC-VA-MD area, with prices up to 75% off retail wedding dresses. Our primary mission is to offer reduced-price designer bridal gowns and accessories for women, and donate our net proceeds to Johns Hopkins Breast Cancer Center at Suburban Hosp, Alzheimer Foundation, Cystic Fibrosis Foundation and other charities in Montgomery County.\nHours: during week and weekends\nAge requirement: 18-75"
 }
]
