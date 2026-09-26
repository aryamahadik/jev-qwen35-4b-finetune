"""codebook_c / HR case types (Aldercrest Health employee relations) and insurance claim
types (Carrow Mutual auto and home). Companies, employees and policyholders are invented."""
from _lib import C, Y, T

HR = {
    "Harassment": "Unwelcome conduct directed at an employee because of a protected characteristic (race, national origin, sex, age, religion, disability, pregnancy), or sexual harassment.",
    "Discrimination": "An employment decision (hiring, pay, promotion, scheduling, discipline, termination) alleged to be based on a protected characteristic.",
    "Retaliation": "An adverse action alleged to follow a protected activity: a complaint, a report to a regulator, taking part in an investigation, or requesting leave or an accommodation. If a case alleges both discrimination and retaliation, code Retaliation.",
    "Bullying and conduct": "Abusive, hostile or unprofessional behaviour not linked to a protected characteristic or a protected activity.",
    "Wage and hour": "Unpaid work time, overtime, missed meal breaks or misclassification caused by a practice, instruction or policy.",
    "Payroll error": "A one-time processing mistake in a paycheque that the employee wants corrected, with no claim that anyone denied the pay on purpose.",
    "Leave and accommodation": "Requests for, and the handling of, medical, family or bereavement leave and disability or religious accommodations.",
    "Workplace safety": "Hazards, injuries, and threats of violence at work.",
    "Conflict of interest": "Personal relationships or financial interests that could affect an employee's duties, such as supervising a partner or relative.",
    "Benefits administration": "Enrolment, deductions and eligibility problems with health, dental and retirement plans.",
    "Performance management": "Disputes about reviews, ratings or improvement plans with no protected-characteristic or retaliation claim.",
    "Policy question": "The employee asks how a policy applies, without alleging that anything went wrong.",
    "none of these": "The case fits none of the other listed types.",
}

IN = {
    "Collision": "Damage to the insured vehicle from impact with another vehicle or an object (including potholes, curbs and guardrails), or from rollover, whoever was at fault.",
    "Comprehensive": "Damage to the insured vehicle from causes other than collision: theft, vandalism, fire, hail, flood, falling objects and striking an animal.",
    "Glass only": "Damage limited to the windshield or windows, with no other damage to the vehicle, from any cause.",
    "Liability, property damage": "Another party claims the insured driver damaged their vehicle or property.",
    "Liability, bodily injury": "Another party claims the insured driver injured them.",
    "Uninsured motorist": "Injury to the insured or passengers caused by an at-fault driver who has no insurance or cannot be identified.",
    "Home, sudden water discharge": "Sudden and accidental discharge of water from plumbing, heating or appliances inside the home.",
    "Home, gradual leakage (excluded)": "Water damage from a leak or seepage that continued for 14 days or more before discovery.",
    "Home, flood (refer to flood policy)": "Water entering the home from outside at ground level: rising rivers, surface runoff or storm surge.",
    "Home, wind and hail": "Damage to the dwelling or its contents from wind, hail or objects blown by wind.",
    "Home, theft": "Property stolen from the home or from household members.",
    "Home, personal liability": "Someone outside the household claims injury or damage caused on the property or by a household member or pet.",
    "none of these": "The claim fits none of the other listed types.",
}


def hr(*names):
    return [(n, HR[n]) for n in names]


def ins(*names):
    return [(n, IN[n]) for n in names]


HRULE = ("Aldercrest Employee Relations intake guide: assign one case type by the employee's core allegation; "
         "the department, the job and the words the employee uses do not decide the type.")
IRULE = "Carrow Mutual first-notice-of-loss coding: assign one claim type by the cause of the loss, not the property damaged or the words the caller uses."

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: shifts cut after she reported a hazard to the state safety agency -> adverse action after protected activity -> Retaliation.
#      twin: cut after telling her manager she is pregnant (no complaint, no leave request) -> Discrimination.
C("hr01", "Which employee-relations case type should intake assign?",
f"""
{HRULE}

Case intake ER-27-0412   Channel: hotline   Site: Aldercrest Northfield Hospital
Employee: Ramona Delacourt, sterile processing technician, 6 years

Intake notes:
Employee states that in March she reported to the state occupational safety agency that the department's steam sterilizer door seal was leaking and burning staff. The agency inspected on 2 April. Since mid-April her weekly schedule has dropped from 40 hours to 24, while two technicians hired after her still get 40. Her manager told her "the schedule is what it is." She has had no discipline and her last review was "exceeds expectations." She wants her hours restored.
""",
list(HR.items()),
"Retaliation", 2,
twin=T([("Employee states that in March she reported to the state occupational safety agency that the department's steam sterilizer door seal was leaking and burning staff. The agency inspected on 2 April.",
         "Employee states that in March she told her manager she is pregnant and due in October. She has not requested leave or any change to her duties.")],
       "Discrimination")),

# ------------------------------------------------------------------ hr02
# why: a supervisor who insults everyone, with no link to a protected characteristic -> Bullying and conduct (not Harassment).
#      twin: mocks two nurses' national origin and accents -> Harassment.
C("hr02", "Code this HR case using the intake guide.",
f"""
{HRULE}

Case intake ER-27-0455   Channel: email to HR   Site: Aldercrest Lakeside Clinic
Employee: Tobias Wren, registered nurse

"I'm writing about our charge nurse, Glenda Moss. On nights she screams at whoever is nearest, calls us 'idiots' and 'useless' in front of patients, and slams charts on the desk. Last week she threw a clipboard across the station. She does this to everyone on the unit, men and women, new grads and 20-year veterans alike; nobody is singled out. Three nurses have transferred out since January. I want HR to do something before someone quits mid-shift."
""",
hr("Bullying and conduct", "Harassment", "Workplace safety", "Discrimination", "Performance management",
   "Retaliation", "none of these"),
"Bullying and conduct", 2,
twin=T([("She does this to everyone on the unit, men and women, new grads and 20-year veterans alike; nobody is singled out.",
         "She saves most of it for the two nurses who trained in the Philippines, calling them 'the imports' and mimicking their accents over the intercom.")],
       "Harassment")),

# ------------------------------------------------------------------ hr03
# why: required pre-shift huddle is unpaid because of the manager's instruction = unpaid work time by practice -> Wage and hour.
#      twin: one paycheque missing an approved night differential -> Payroll error.
C("hr03", "Which case type applies to this HR intake?",
f"""
{HRULE}

Case intake ER-27-0490   Channel: HR portal   Site: Aldercrest Central Lab
Employee: Kwame Addo-Brennan, lab assistant (hourly)

Intake notes:
Employee states that his supervisor requires all lab assistants to attend a 20-minute handoff huddle before every shift, but has told them not to clock in until the huddle ends because "the budget doesn't cover it." He estimates he has worked about 60 unpaid hours this year. He says every assistant on his shift is treated the same way. He has not been disciplined and is not alleging bias; he wants the time paid and the practice stopped.
""",
hr("Wage and hour", "Payroll error", "Policy question", "Discrimination", "Benefits administration",
   "Performance management", "Retaliation", "none of these"),
"Wage and hour", 2,
twin=T([("Employee states that his supervisor requires all lab assistants to attend a 20-minute handoff huddle before every shift, but has told them not to clock in until the huddle ends because \"the budget doesn't cover it.\" He estimates he has worked about 60 unpaid hours this year. He says every assistant on his shift is treated the same way.",
         "Employee states that his 14 June paycheque left out the night differential for six shifts, even though his timesheet shows those shifts approved by his supervisor with the differential code. Every earlier paycheque this year was correct and his supervisor agrees it looks like a processing slip.")],
       "Payroll error")),

# ------------------------------------------------------------------ hr04
# why: a request for a sit-stand desk because of a diagnosed back condition -> disability accommodation -> Leave and accommodation.
C("hr04", "Assign the case type for this intake.",
f"""
{HRULE}

Case intake ER-27-0521   Channel: HR portal   Site: Aldercrest Billing Center
Employee: Marisela Quintanilla, claims analyst

"I have a herniated disc in my lower back and my physician has recommended that I alternate between sitting and standing every 30 minutes (note attached). I'm asking for a sit-stand desk at my workstation. I haven't been injured at work and my chair is fine for most people; this is about my condition. My supervisor told me to submit it here. Thank you."
""",
hr("Leave and accommodation", "Workplace safety", "Benefits administration", "Policy question", "Discrimination",
   "none of these"),
"Leave and accommodation", 2),

# ------------------------------------------------------------------ hr05
# why: a manager in a consensual relationship with his direct report -> Conflict of interest (no unwelcome conduct).
#      twin: he keeps asking her out after she said no and comments on her body -> Harassment (sexual harassment).
C("hr05", "Which case type from the intake guide fits?",
f"""
{HRULE}

Case intake ER-27-0544   Channel: anonymous hotline   Site: Aldercrest Northfield Hospital

Report text:
"The pharmacy operations manager, Declan Rourke, has been in a relationship with one of his own direct reports, a pharmacy buyer, since last autumn. They are open about it and both seem happy. But he still approves her schedule, her overtime and her annual rating, and last month he gave her the only 'outstanding' rating on the team. Other buyers feel this isn't fair. I am not accusing anyone of anything else."
""",
hr("Conflict of interest", "Harassment", "Discrimination", "Performance management", "Bullying and conduct",
   "Retaliation", "none of these"),
"Conflict of interest", 2,
twin=T([("has been in a relationship with one of his own direct reports, a pharmacy buyer, since last autumn. They are open about it and both seem happy. But he still approves her schedule, her overtime and her annual rating, and last month he gave her the only 'outstanding' rating on the team. Other buyers feel this isn't fair.",
         "keeps asking one of his own direct reports, a pharmacy buyer, out for drinks even though she has told him no in front of us several times. He comments on her body and her clothes most days, and she has started eating lunch in her car to avoid him. Other buyers feel this isn't right.")],
       "Harassment")),

# ------------------------------------------------------------------ hr06
# why: improvement plan issued two weeks after she filed a harassment complaint, and she links them -> Retaliation (not Performance management).
#      twin: no complaint; she disputes the metrics change -> Performance management.
C("hr06", "Code this case with the employee-relations case types.",
f"""
{HRULE}

Case intake ER-27-0588   Channel: meeting with HR business partner   Site: Aldercrest Patient Access
Employee: Yolanda Brisbane, scheduling coordinator, 4 years

Notes:
Employee filed a formal harassment complaint against a team lead on 3 May. On 17 May her manager placed her on a 60-day performance improvement plan citing call handling times. Her handling times have been the same for two years and were rated "meets" in January. She believes the plan is payback for her complaint. She is asking for the plan to be withdrawn.
""",
hr("Retaliation", "Performance management", "Harassment", "Discrimination", "Bullying and conduct",
   "Policy question", "none of these"),
"Retaliation", 3,
twin=T([("Employee filed a formal harassment complaint against a team lead on 3 May. On 17 May her manager placed her on a 60-day performance improvement plan citing call handling times. Her handling times have been the same for two years and were rated \"meets\" in January. She believes the plan is payback for her complaint.",
         "On 17 May her manager placed her on a 60-day performance improvement plan citing call handling times, after the department cut the target from 6 minutes to 4 minutes in April. Her handling times have been the same for two years. She has never filed a complaint and does not allege bias; she believes the new target is unrealistic for complex calls.")],
       "Performance management")),

# ------------------------------------------------------------------ hr07
# why: asks how many bereavement days apply for a grandparent, nothing has gone wrong -> Policy question.
#      twin: the manager refused leave the policy grants -> Leave and accommodation.
C("hr07", "Which HR case type applies?",
f"""
{HRULE}

Case intake ER-27-0602   Channel: HR chat   Site: Aldercrest Westbrook Hospital
Employee: Anatoly Petrenko, respiratory therapist

"Hi, my grandmother passed away yesterday in Lviv and the funeral is next week. How many bereavement days do I get for a grandparent under our policy, and can I add vacation days to them because of the travel? I haven't asked my manager yet; I want to know the rules first. Thank you."
""",
hr("Policy question", "Leave and accommodation", "Benefits administration", "Payroll error", "Discrimination",
   "Wage and hour", "none of these"),
"Policy question", 2,
twin=T([("How many bereavement days do I get for a grandparent under our policy, and can I add vacation days to them because of the travel? I haven't asked my manager yet; I want to know the rules first.",
         "The policy gives three bereavement days for a grandparent, but my manager has refused to approve them because we're short-staffed and told me to swap shifts instead. I need this sorted out today so I can book my flight.")],
       "Leave and accommodation")),

# ------------------------------------------------------------------ hr08
# why: enrolled in dental, but premiums not deducted and claims denied as not covered -> Benefits administration (not Payroll error).
C("hr08", "Pick the case type for this intake.",
f"""
{HRULE}

Case intake ER-27-0630   Channel: HR portal   Site: Aldercrest Home Health
Employee: Beatrix Nakamura-Holt, home health aide

"I signed up for the family dental plan during open enrolment in November (confirmation #OE-55821 attached). My paycheques since January don't show any dental deduction, and last week my son's cleaning was denied by the dental company because 'no active coverage.' My pay is otherwise correct. I need the coverage fixed back to 1 January so the claim can be paid."
""",
hr("Benefits administration", "Payroll error", "Wage and hour", "Policy question", "Leave and accommodation",
   "none of these"),
"Benefits administration", 2),

# ------------------------------------------------------------------ in01
# why: striking a deer -> Comprehensive (animal strike), not Collision.
#      twin: swerved, missed the deer, hit a guardrail -> impact with an object -> Collision.
C("in01", "Which claim type should the adjuster code for this loss?",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10442
Policyholder: Eleanor Fairweather   Vehicle: 2023 Tarrant Ridgeline SUV
Date/time: 14 November, about 18:20   Location: County Road 12 near Birch Hollow

Caller statement:
"It was just getting dark. A deer jumped out of the ditch on the right and I hit it square with the front of the car before I could brake. The headlight is smashed, the bumper is pushed in and the hood is buckled. The deer ran off into the field. No other cars were around, and I didn't hit anything else. I'm fine, just shaken. The car is drivable but one headlight is out."
""",
ins("Comprehensive", "Collision", "Glass only", "Liability, property damage", "Uninsured motorist",
    "Home, personal liability", "none of these"),
"Comprehensive", 2,
twin=T([("A deer jumped out of the ditch on the right and I hit it square with the front of the car before I could brake. The headlight is smashed, the bumper is pushed in and the hood is buckled. The deer ran off into the field. No other cars were around, and I didn't hit anything else.",
         "A deer jumped out of the ditch on the right, I swerved left and missed it completely, and the car slid into the metal guardrail. The headlight is smashed, the bumper is pushed in and the hood is buckled. The deer ran off into the field. No other cars were around.")],
       "Collision")),

# ------------------------------------------------------------------ in02
# why: hail cracked the windshield AND dented the hood/roof -> not limited to glass -> Comprehensive.
#      twin: only the windshield is cracked, body undamaged -> Glass only.
C("in02", "Code this first notice of loss.",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10518
Policyholder: Rashid Montgomery-Ile   Vehicle: 2021 Corvan Lark sedan
Date: 2 June   Location: parked in the open lot at Ferrisburg Station

Caller statement:
"That hailstorm on Tuesday afternoon caught my car in the station lot. When I got off the train the windshield had a long crack across the driver's side, and the hood and roof are covered in dents the size of golf balls. Nothing hit it except the hail. The windows on the sides are fine."
""",
ins("Comprehensive", "Glass only", "Collision", "Home, wind and hail", "Liability, property damage",
    "none of these"),
"Comprehensive", 2,
twin=T([("the windshield had a long crack across the driver's side, and the hood and roof are covered in dents the size of golf balls.",
         "the windshield had a long crack across the driver's side. I went over the hood, roof and doors with a flashlight and there isn't a single dent or scratch.")],
       "Glass only")),

# ------------------------------------------------------------------ in03
# why: a supply line burst and was found within hours -> Home, sudden water discharge.
#      twin: the plumber finds a slow leak running about five weeks -> 14+ days -> Home, gradual leakage (excluded).
C("in03", "Which Carrow Mutual claim type fits this home loss?",
f"""
{IRULE}

First notice of loss — Claim CM-H-27-20331
Policyholder: Isadora Vukovic   Property: 118 Orrin Lane (single-family)
Date reported: 9 February

Caller statement:
"I came downstairs at 7 this morning and there was water all over the kitchen floor and into the dining room. The plumber came at 9 and found that the braided supply line to the kitchen sink had split open. He says a split like that lets go all at once, and the floor was dry when I went to bed at 11 last night. The hardwood is cupping and the bottom cabinets are soaked."
""",
ins("Home, sudden water discharge", "Home, gradual leakage (excluded)", "Home, flood (refer to flood policy)", "Home, wind and hail",
    "Home, personal liability", "Home, theft", "none of these"),
"Home, sudden water discharge", 2,
twin=T([("He says a split like that lets go all at once, and the floor was dry when I went to bed at 11 last night.",
         "He says it had been dripping slowly behind the cabinet for about five weeks before the water finally showed on the floor.")],
       "Home, gradual leakage (excluded)")),

# ------------------------------------------------------------------ in04
# why: river overflow entering at ground level -> Home, flood (refer to flood policy); rain and pipes are not the cause.
#      twin: the washing-machine hose split during a cycle -> Home, sudden water discharge.
C("in04", "Assign the claim type for this loss.",
f"""
{IRULE}

First notice of loss — Claim CM-H-27-20417
Policyholder: Bartholomew Achterberg   Property: 7 Millrace Road (single-family, finished basement)
Date reported: 18 April

Caller statement:
"After three days of heavy rain the Millrace River came over its bank on Saturday night. By morning there was a foot of muddy water in the basement; it came in under the basement door on the river side and through the window wells. The plumbing is all fine; the plumber checked every pipe and the water heater. The furnace, washer and a sofa are ruined."
""",
ins("Home, flood (refer to flood policy)", "Home, sudden water discharge", "Home, gradual leakage (excluded)", "Home, wind and hail",
    "Comprehensive", "none of these"),
"Home, flood (refer to flood policy)", 2,
twin=T([("After three days of heavy rain the Millrace River came over its bank on Saturday night. By morning there was a foot of muddy water in the basement; it came in under the basement door on the river side and through the window wells. The plumbing is all fine; the plumber checked every pipe and the water heater.",
         "After three days of heavy rain I ran a load of towels on Saturday night, and the hose on the back of the washing machine split during the cycle. By morning there was a foot of water in the basement. The river stayed in its banks; the plumber confirmed the split hose was the only source.")],
       "Home, sudden water discharge")),

# ------------------------------------------------------------------ in05
# why: the insured was injured by a hit-and-run driver who cannot be identified -> Uninsured motorist (the claim is for her injuries).
C("in05", "Which claim type should this first notice be coded as?",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10690
Policyholder: Priscilla Oyenuga   Vehicle: 2019 Corvan Lark sedan
Date: 23 August   Location: Halsted Ave at 9th St

Caller statement:
"I was stopped at the red light when a pickup came up fast behind me and slammed into the back of my car, then drove around me and ran the light. Nobody got the plate; the police report says the driver is unknown. I have whiplash and a concussion and was in the emergency room for six hours. I'm calling about my medical bills and lost wages. I'll call separately about the car."
""",
ins("Uninsured motorist", "Collision", "Liability, bodily injury", "Liability, property damage", "Comprehensive",
    "none of these"),
"Uninsured motorist", 3),

# ------------------------------------------------------------------ in06
# why: the other driver claims the insured damaged her car -> Liability, property damage.
#      twin: the other driver claims medical costs for her neck injury -> Liability, bodily injury.
C("in06", "Code this claim using the Carrow Mutual claim types.",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10733
Policyholder: Silas Brandvold   Vehicle: 2022 Tarrant Pioneer pickup
Date: 5 September   Location: Wexford Mall parking lot

Notes:
Our policyholder admits that while backing out of a parking space he struck the rear quarter panel of a parked hatchback owned by Mireille Dupont. His own truck has only a scuff on the tow hitch and he is not claiming for it. Ms. Dupont was not in her car. She has contacted Carrow Mutual with a body-shop estimate of $3,850 for her quarter panel and tail light.
""",
ins("Liability, property damage", "Liability, bodily injury", "Collision", "Uninsured motorist", "Comprehensive",
    "Home, personal liability", "none of these"),
"Liability, property damage", 2,
twin=T([("Ms. Dupont was not in her car. She has contacted Carrow Mutual with a body-shop estimate of $3,850 for her quarter panel and tail light.",
         "Ms. Dupont was sitting in the driver's seat and was taken to urgent care with neck pain. She has contacted Carrow Mutual about her $3,850 in medical bills and has already had her car repaired at her own expense.")],
       "Liability, bodily injury")),

# ------------------------------------------------------------------ in07
# why: a tree limb blown onto the insured's parked car -> falling object -> Comprehensive (auto), not Home, wind and hail (the house is undamaged).
C("in07", "Which claim type applies to this loss?",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10801
Policyholder: Winona Castellanos   Vehicle: 2020 Harlan Scout SUV (insured under her Carrow auto policy; the house is also insured with Carrow)
Date: 30 October   Location: her own driveway, 22 Elm Street

Caller statement:
"During the windstorm last night a big limb broke off the maple in my front yard and came down on the SUV parked in the driveway. The roof is caved in and the rear window shattered. The house wasn't touched: no shingles, no gutters, nothing. Nobody was hurt."
""",
list(IN.items()),
"Comprehensive", 3),

# ------------------------------------------------------------------ in08
# why: the insured's dog bit the mail carrier on the insured's porch -> injury to someone outside the household caused by a household pet
#      -> Home, personal liability.
C("in08", "Assign the correct claim type.",
f"""
{IRULE}

First notice of loss — Claim CM-H-27-20560
Policyholder: Gregor Lindqvist   Property: 403 Sable Court (homeowners policy)
Date: 12 July

Caller statement:
"Our dog, Juno, slipped past my wife when she opened the front door to take in a package, and she bit the mail carrier on the forearm on our porch. He needed eight stitches. His union rep called today to say he is making a claim for his medical costs and missed work. Nothing of ours was damaged."
""",
ins("Home, personal liability", "Liability, bodily injury", "Home, theft", "Uninsured motorist", "Comprehensive",
    "none of these"),
"Home, personal liability", 2),

# ------------------------------------------------------------------ hr09
# why: passed over for promotion, alleging it was because of her age (a protected characteristic) -> Discrimination (yes).
#      twin: attributes it to not being in the director's social circle -> no protected characteristic -> not Discrimination (no).
Y("hr09", "Should this case be coded Discrimination?",
f"""
{HRULE}

Case intake ER-27-0677   Channel: HR portal   Site: Aldercrest Finance
Employee: Georgina Abernathy, senior accountant, 14 years

"The controller role went to a colleague with six years' experience and weaker reviews than mine. When I asked the director why, he said the team needs 'fresh energy' and someone who will 'be around for the long haul,' and that at 57 I should be thinking about slowing down. I have never filed a complaint or asked for leave. I believe I was passed over because of my age."
""",
[("Discrimination", HR["Discrimination"]),
 ("Protected characteristic", "race, national origin, sex, age, religion, disability or pregnancy.")],
1, 2,
twin=T([("When I asked the director why, he said the team needs 'fresh energy' and someone who will 'be around for the long haul,' and that at 57 I should be thinking about slowing down. I have never filed a complaint or asked for leave. I believe I was passed over because of my age.",
         "When I asked the director why, he said the colleague 'fits the culture' better. She plays golf with him every Saturday and I don't. I have never filed a complaint or asked for leave, and I don't think age, sex or anything like that played a part; it's favouritism.")],
       0)),

# ------------------------------------------------------------------ hr10
# why: clerical duties classified as exempt, 50 h/week with no overtime -> misclassification by practice -> within Wage and hour,
#      so "outside Wage and hour?" -> no.
Y("hr10", "Is this case outside the Wage and hour case type?",
f"""
{HRULE}

Case intake ER-27-0701   Channel: HR portal   Site: Aldercrest Central Administration
Employee: Florian Achebe, office assistant

"I was hired as salaried and exempt. My duties are answering phones, filing, scanning records and ordering supplies; I don't supervise anyone and I don't make any decisions. Since the reorganisation I work about 50 hours a week and I've been told salaried staff don't get overtime. A friend in payroll said my job title is normally hourly. I'd like my classification reviewed and back pay for the overtime."
""",
[("Wage and hour", HR["Wage and hour"]),
 ("Payroll error", HR["Payroll error"])],
0, 2, role="neg"),

# ------------------------------------------------------------------ in09
# why: leak started about 20 Feb, discovered 3 Mar = 11 days (<14) -> not gradual leakage (no).
#      twin: started about 10 Feb -> 21 days (Feb has 28 days in 2027) -> gradual leakage (yes).
Y("in09", "Is this water damage claim excluded as gradual leakage?",
f"""
{IRULE}

First notice of loss — Claim CM-H-27-20298
Policyholder: Cornelius Mbatha   Property: 56 Gantry Street (single-family)
Date of discovery: 3 March 2027

Caller statement and plumber's report:
The policyholder noticed a soft spot and dark staining in the bathroom floor on 3 March 2027. His plumber opened the floor and found a pinhole leak in the copper line to the toilet. Based on the corrosion and the spread of the staining, the plumber's written report dates the start of the leak to about 20 February 2027. The subfloor and the ceiling of the room below are damaged.
""",
[("Home, gradual leakage (excluded)", IN["Home, gradual leakage (excluded)"]),
 ("Leak duration", "days from the start of the leak to its discovery.")],
0, 3,
twin=T([("dates the start of the leak to about 20 February 2027", "dates the start of the leak to about 10 February 2027")], 1)),

# ------------------------------------------------------------------ in10
# why: a stone chip that cracked only the windshield, body undamaged -> Glass only (yes).
Y("in10", "Should this loss be coded Glass only?",
f"""
{IRULE}

First notice of loss — Claim CM-A-27-10912
Policyholder: Henrietta Osei-Lund   Vehicle: 2024 Harlan Scout SUV
Date: 19 March   Location: Interstate 7 near Cobb's Crossing

Caller statement:
"A gravel truck in front of me kicked up a stone that hit my windshield. There's a chip that has now grown into a crack about eight inches long. I checked the hood and the paint around the windshield and there's no other damage anywhere on the car. I didn't get the truck's number."
""",
[("Glass only", IN["Glass only"]),
 ("Comprehensive", IN["Comprehensive"])],
1, 2),
]
