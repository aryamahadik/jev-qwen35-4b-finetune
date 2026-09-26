"""codebook_c / political statements coded by policy area and direction (Civic Signal
Lab statement codebook, invented; speakers, places and races invented)."""
from _lib import C, Y, T

ST = {
    "Taxation (lower)": "Wants taxes on income, property, sales, fuel or business cut, new tax credits or exemptions, or a proposed tax increase blocked. Carbon pricing is coded under environmental rules.",
    "Taxation (raise)": "Wants new or higher taxes on income, property, sales, fuel or business, or existing tax credits or exemptions removed.",
    "School funding (expand)": "Wants more public money for K-12 schools, or opposes cuts to it.",
    "School funding (cut)": "Wants less public money for K-12 schools, including closures or layoffs to save money, or opposes increases.",
    "Policing and sentencing (expand)": "Wants more police funding, officers or powers, or longer or mandatory sentences, or opposes shortening them.",
    "Policing and sentencing (restrain)": "Wants less police funding, limits on police powers, shorter sentences or alternatives to incarceration.",
    "Immigration (more open)": "Wants more visas, admissions or legal pathways, or fewer enforcement measures, including limits on local cooperation with federal immigration enforcement.",
    "Immigration (more restrictive)": "Wants fewer visas or admissions, or more enforcement, including penalties on employers of workers without legal status.",
    "Environmental rules (tighten)": "Wants stricter emissions or pollution limits, carbon pricing, or tougher enforcement and penalties for polluters.",
    "Environmental rules (loosen)": "Wants environmental limits, permits or carbon pricing relaxed, repealed or blocked, including exemptions from environmental permits for any industry.",
    "Social assistance (expand)": "Wants broader eligibility, higher benefits or fewer hurdles in cash aid, food aid, housing vouchers or public health coverage for low-income people.",
    "Social assistance (restrict)": "Wants stricter eligibility, work requirements, more verification or lower benefits in those programs.",
    "Housing construction (promote)": "Wants zoning, density or height rules changed so more homes can be built, or opposes limits on new housing.",
    "Housing construction (restrict)": "Wants limits on new housing density, height or permits, or opposes loosening them.",
    "Firearms rules (tighten)": "Wants stricter rules on buying, carrying or owning guns.",
    "Firearms rules (loosen)": "Wants fewer restrictions on buying, carrying or owning guns, including more places where guns may be carried.",
    "none of these": "The statement takes no position on any listed policy area (procedural remarks, thanks, attacks on character without a policy, or neutral descriptions).",
}


def st(*names):
    return [(n, ST[n]) for n in names]


RULES = """Coder instructions (Civic Signal Lab, statement codebook v3):
1. Code the single policy change the speaker advocates. The topic used as an illustration, the group that benefits and the way a proposal is paid for do not decide the area.
2. If the speaker proposes moving money from one area to another, code the area that receives the money.
3. If the speaker attacks an opponent's proposal, code the speaker's own position: the opposite direction in the same area."""

ITEMS = [
# ------------------------------------------------------------------ st01
# why: school costs are the illustration; the change is a bigger tax credit -> Taxation (lower).
#      twin: doubles a school lunch/supply grant -> School funding (expand).
C("st01", "Under the statement codebook, which area-and-direction code fits this statement?",
f"""
{RULES}

Statement ID: TW-2027-0412
Speaker: Adaeze Morrow, candidate for state senate, District 9 (Tamsworth)
Setting: back-to-school town hall, Tamsworth Middle School gym

Transcript excerpt:
"Every family in this gym knows what August costs. New shoes, a backpack, the calculator the math teacher says you need, the field-trip money, the lunch account that's always somehow empty. I've been there with three kids. So here's my plan: I will double the state child tax credit, from $500 to $1,000 per child, so that parents keep more of what they earn and decide for themselves what their kids need. No new program, no new office. Just your money, back in your pocket, every April."
""",
st("Taxation (lower)", "School funding (expand)", "Social assistance (expand)", "Taxation (raise)", "School funding (cut)",
   "Housing construction (promote)", "Policing and sentencing (expand)", "none of these"),
"Taxation (lower)", 2,
twin=T([("I will double the state child tax credit, from $500 to $1,000 per child, so that parents keep more of what they earn and decide for themselves what their kids need",
         "I will double the state grant that pays for school lunches and classroom supplies, so that no parent in a public school gets a bill for lunch or a calculator again")],
       "School funding (expand)")),

# ------------------------------------------------------------------ st02
# why: rule 2 -> code the receiving area: school counselors -> School funding (expand).
#      twin: money moves into police overtime -> Policing and sentencing (expand).
C("st02", "Code this statement by policy area and direction.",
f"""
{RULES}

Statement ID: BH-2027-0088
Speaker: Councilmember Rafael Iturbe, Brookhaven City Council
Setting: council budget hearing, public comment closed

Transcript excerpt:
"People keep telling me Brookhaven needs more officers after the Delmont Avenue break-ins. I've read every one of those emails. But I've also sat with the principals at Brookhaven High and Fenwick Middle, and they have one counselor for 700 kids. My amendment is simple. It moves $2.4 million from the police overtime line to the school counselor program, enough to hire 24 counselors this fall. That is where this money does the most good."
""",
st("School funding (expand)", "Policing and sentencing (restrain)", "Policing and sentencing (expand)", "School funding (cut)",
   "Taxation (lower)", "Social assistance (expand)", "none of these"),
"School funding (expand)", 3,
twin=T([("It moves $2.4 million from the police overtime line to the school counselor program, enough to hire 24 counselors this fall.",
         "It moves $2.4 million from the school counselor program to the police overtime line, enough to put 24 more officers on night patrols this fall.")],
       "Policing and sentencing (expand)")),

# ------------------------------------------------------------------ st03
# why: attacks a carbon fee; codebook puts carbon pricing under environmental rules -> Environmental rules (loosen) (not Taxation).
#      twin: attacks a plain fuel-tax increase -> Taxation (lower).
C("st03", "Which code from the statement codebook applies?",
f"""
{RULES}

Statement ID: RV-2027-1130
Speaker: Gwendolyn Aske, incumbent representative, House District 44
Setting: televised debate, Riverbend public television

Transcript excerpt:
"My opponent's carbon fee would add about thirty cents to every gallon at the pump. Thirty cents. For a nurse driving forty miles each way from Carrow to the county hospital, that's real money every single week. He calls it a climate plan. I call it a commute penalty. I've voted against it twice and I will vote against it every time it comes to the floor."
""",
st("Environmental rules (loosen)", "Taxation (lower)", "Environmental rules (tighten)", "Taxation (raise)",
   "Social assistance (expand)", "Housing construction (promote)", "none of these"),
"Environmental rules (loosen)", 3,
twin=T([("My opponent's carbon fee would add about thirty cents to every gallon at the pump.",
         "My opponent's plan to raise the state gasoline tax would add about thirty cents to every gallon at the pump.")],
       "Taxation (lower)")),

# ------------------------------------------------------------------ st04
# why: removing the annual paperwork re-check for Medicaid = fewer hurdles in public health coverage -> Social assistance (expand).
C("st04", "Assign the statement codebook label for this remark.",
f"""
{RULES}

Statement ID: HM-2027-0203
Speaker: Governor candidate Lionel Achterberg-Moss
Setting: interview, Hollowmere Public Radio "Morning Line"

Transcript excerpt:
"Last year eleven thousand people in this state lost their Medicaid, and not because their income changed. They lost it because a letter went to an old address, or the form came back with one box blank. That's not fraud prevention; that's a paperwork trap. On my first day I will end the annual re-verification packet for anyone whose income the state can already confirm from tax and wage records. If the state has the data, it shouldn't make a sick person fill out a form."
""",
list(ST.items()),
"Social assistance (expand)", 2),

# ------------------------------------------------------------------ st05
# why: the change asked for is more seasonal worker visas -> Immigration (more open); farms are the setting.
#      twin: halve the visas -> Immigration (more restrictive).
C("st05", "Which area and direction does this statement take under the codebook?",
f"""
{RULES}

Statement ID: OV-2027-0561
Speaker: Congressional candidate Maren Oduya, 3rd District
Setting: county fair forum, Orland Valley Growers' tent

Transcript excerpt:
"Walk the Heston orchards in September and you'll see apples on the ground. Not because the market's bad. Because there aren't enough hands to pick them. I have talked to forty growers this summer and every one of them said the same thing. So in Congress I'll push to triple the number of seasonal farmworker visas and to cut the paperwork so a grower can get a crew approved in weeks, not months. Our growers are ready to pay fair wages. They just need the workers."
""",
st("Immigration (more open)", "Immigration (more restrictive)", "Taxation (lower)", "Environmental rules (loosen)",
   "Social assistance (expand)", "Housing construction (promote)", "none of these"),
"Immigration (more open)", 2,
twin=T([("So in Congress I'll push to triple the number of seasonal farmworker visas and to cut the paperwork so a grower can get a crew approved in weeks, not months. Our growers are ready to pay fair wages. They just need the workers.",
         "So in Congress I'll push to cut the number of seasonal farmworker visas in half over five years, so growers compete for local workers instead. Our growers can pay fair wages. They just need to hire here.")],
       "Immigration (more restrictive)")),

# ------------------------------------------------------------------ st06
# why: keeps the height limit to stop a six-story building -> Housing construction (restrict).
#      twin: raise the limit to allow it -> Housing construction (promote).
C("st06", "Under the codebook, what is the correct code for this statement?",
f"""
{RULES}

Statement ID: FV-2027-0317
Speaker: Planning commissioner and council candidate Beatrix Lindqvist
Setting: neighbourhood association meeting, Fairview Community Hall

Transcript excerpt:
"I've heard you. The developer's drawing for the Kessler lot shows a six-story building with 140 apartments right up against people's back fences on Linden and Ash. The traffic study was done in August, when half the street was on vacation. I will vote to keep the height limit on that corridor at three stories, and I will oppose any rezoning that lifts it. Fairview can welcome new neighbours without losing what makes it Fairview."
""",
st("Housing construction (restrict)", "Housing construction (promote)", "Environmental rules (tighten)", "Taxation (lower)",
   "Social assistance (restrict)", "Policing and sentencing (expand)", "none of these"),
"Housing construction (restrict)", 2,
twin=T([("I will vote to keep the height limit on that corridor at three stories, and I will oppose any rezoning that lifts it.",
         "I will vote to raise the height limit on that corridor to six stories so these homes can be built, and I will oppose any effort to block it.")],
       "Housing construction (promote)")),

# ------------------------------------------------------------------ st07
# why: letting trained teachers carry concealed handguns in classrooms = more places guns may be carried -> Firearms rules (loosen).
#      twin: ban guns near schools including for permit holders -> Firearms rules (tighten).
C("st07", "Which statement-codebook category best fits?",
f"""
{RULES}

Statement ID: LW-2027-0744
Speaker: State Rep. Colton Braddock, candidate for re-election
Setting: press conference outside Linwood Elementary

Transcript excerpt:
"Three weeks ago, parents at this school waited ninety minutes to learn whether their children were safe. Thank God it was a false alarm. But the nearest deputy was eleven miles away. I'm here to announce that I'm filing a bill to let teachers who complete 40 hours of training and a background check carry a concealed handgun in their classroom. The parents I've talked to want every school in this county to be safer, and this is the fastest way to get there."
""",
st("Firearms rules (loosen)", "Firearms rules (tighten)", "Policing and sentencing (expand)", "School funding (expand)",
   "School funding (cut)", "Policing and sentencing (restrain)", "Social assistance (expand)", "none of these"),
"Firearms rules (loosen)", 2,
twin=T([("I'm filing a bill to let teachers who complete 40 hours of training and a background check carry a concealed handgun in their classroom.",
         "I'm filing a bill to ban firearms within 1,000 feet of any school, including for people who hold a concealed carry permit.")],
       "Firearms rules (tighten)")),

# ------------------------------------------------------------------ st08
# why: a procedural remark about debate scheduling; no policy position -> none of these (childcare/taxes are mentioned only as reasons).
C("st08", "What code does the statement codebook assign to this statement?",
f"""
{RULES}

Statement ID: MB-2027-0915
Speaker: Ines Valcourt, candidate for mayor of Marrow Bay
Setting: letter to the League of Neighbourhood Voters, read aloud at a press availability

Transcript excerpt:
"I am asking the League to move the October debate from 2 p.m. on a Tuesday to 7 p.m. on a Thursday, and to stream it with captions in English and Spanish. The people who pay the taxes in this city and who will be hit by every budget decision we make are at work at 2 p.m. on a Tuesday, or picking up their children from school. My opponent has agreed to the change. I hope the League will too."
""",
st("Taxation (lower)", "School funding (expand)", "Social assistance (expand)", "Immigration (more open)",
   "Policing and sentencing (restrain)", "Housing construction (promote)", "none of these"),
"none of these", 2),

# ------------------------------------------------------------------ st09
# why: opposing school closures/teacher layoffs = opposes cuts -> School funding (expand) (property tax is only mentioned).
#      twin: voting yes on the closure plan -> School funding (cut).
C("st09", "Code the policy position in this statement.",
f"""
{RULES}

Statement ID: PC-2027-0149
Speaker: School board trustee Harriet Ngata, Pinecrest Unified
Setting: school board meeting, budget vote

Transcript excerpt:
"The district says the numbers force our hand: a $6 million gap, enrolment down four percent, and property tax receipts flat. I understand the arithmetic. But I will not balance this budget by closing Pinecrest Elementary and laying off 60 teachers. I am voting no on the superintendent's reduction plan tonight, and I'll keep voting no until we find the money elsewhere."
""",
st("School funding (expand)", "School funding (cut)", "Taxation (raise)", "Taxation (lower)",
   "Social assistance (expand)", "Policing and sentencing (restrain)", "none of these"),
"School funding (expand)", 2,
twin=T([("But I will not balance this budget by closing Pinecrest Elementary and laying off 60 teachers. I am voting no on the superintendent's reduction plan tonight, and I'll keep voting no until we find the money elsewhere.",
         "So I will support balancing this budget by closing Pinecrest Elementary and laying off 60 teachers. I am voting yes on the superintendent's reduction plan tonight, because there is no other honest way to close the gap.")],
       "School funding (cut)")),

# ------------------------------------------------------------------ st10
# why: limiting jail cooperation with federal immigration agents is an enforcement limit named in Immigration (more open),
#      not a policing restraint.
C("st10", "Under the codebook, which area-direction label applies to this statement?",
f"""
{RULES}

Statement ID: DC-2027-0602
Speaker: County commissioner Esperanza Villalobos, Dunmore County
Setting: commission meeting, discussion of the sheriff's proposed agreement

Transcript excerpt:
"Sheriff Holloway wants to sign an agreement that would let federal immigration agents work out of our county jail and would have our deputies hold people for them after their release date. I respect the sheriff. But our deputies were hired to keep Dunmore County safe, not to do federal immigration work. I'm voting against this agreement, and I'll introduce a policy that bars county staff from holding anyone past release on an immigration request alone."
""",
list(ST.items()),
"Immigration (more open)", 3),

# ------------------------------------------------------------------ st11
# why: per-day fines on a polluter for permit violations = tougher enforcement/penalties -> Environmental rules (tighten) (not Taxation).
C("st11", "Pick the statement code.",
f"""
{RULES}

Statement ID: HW-2027-0376
Speaker: Attorney general candidate Oskar Lindahl
Setting: press conference, Harwell riverfront trail

Transcript excerpt:
"The Harwell refinery has broken its air permit six times in two years. Every time, the state sent a letter. Every time, the flaring came back. Families on Dock Street keep their windows shut in July. As attorney general I will seek the maximum penalty the law allows, fifty thousand dollars for every day a permit is violated, and I will ask the legislature to double that maximum. The money should cost them more than the violation saves them."
""",
st("Environmental rules (tighten)", "Environmental rules (loosen)", "Taxation (raise)", "Policing and sentencing (expand)",
   "Housing construction (restrict)", "Social assistance (expand)", "none of these"),
"Environmental rules (tighten)", 2),

# ------------------------------------------------------------------ st12
# why: work requirement to keep food assistance -> Social assistance (restrict).
#      twin: repeal the work rule -> Social assistance (expand).
C("st12", "Which codebook label captures the speaker's position?",
f"""
{RULES}

Statement ID: GL-2027-0288
Speaker: State Sen. Thaddeus Grieve
Setting: floor speech on SB 311

Transcript excerpt:
"We have 14,000 open jobs in the Glenmore region, and employers who will train anyone who shows up. At the same time, 9,000 adults with no children and no disability are receiving food assistance with no expectation that they work or train at all. SB 311 says those adults should work, volunteer or be in job training for 20 hours a week to keep receiving food assistance after three months. Work pays. I urge a yes vote."
""",
st("Social assistance (restrict)", "Social assistance (expand)", "Taxation (lower)", "Immigration (more restrictive)",
   "School funding (expand)", "Policing and sentencing (expand)", "none of these"),
"Social assistance (restrict)", 2,
twin=T([("SB 311 says those adults should work, volunteer or be in job training for 20 hours a week to keep receiving food assistance after three months. Work pays. I urge a yes vote.",
         "SB 311 repeals the rule that cuts those adults off food assistance after three months if they cannot log 20 hours a week of work. Hunger doesn't help anyone find a job. I urge a yes vote.")],
       "Social assistance (expand)")),

# ------------------------------------------------------------------ st13
# why: rule 3: attacks an opponent's plan to end mandatory minimums -> own position is keeping them -> Policing and sentencing (expand).
C("st13", "According to the statement codebook, how should this statement be coded?",
f"""
{RULES}

Statement ID: SH-2027-0521
Speaker: District attorney candidate Rowena Sallis
Setting: candidate forum, Shelby Heights Rotary

Transcript excerpt:
"My opponent has said she would ask the legislature to end mandatory minimum sentences for armed robbery. She says it would save the state $30 million a year in prison costs. I've prosecuted these cases for fifteen years. I've sat with the store clerks. Ending those minimums would be a mistake, and I will testify against that bill if it is ever filed."
""",
list(ST.items()),
"Policing and sentencing (expand)", 3),

# ------------------------------------------------------------------ st14
# why: removing a property tax exemption = tax raise; vacant housing is the setting -> Taxation (raise).
C("st14", "Assign one code from the statement codebook.",
f"""
{RULES}

Statement ID: CQ-2027-0457
Speaker: Council candidate Mateo Arrowsmith, Crescent Quay Ward 2
Setting: tenant union candidate night

Transcript excerpt:
"There are 1,300 luxury condos on the Crescent Quay waterfront that sit empty eleven months a year. Right now their owners qualify for the same property tax exemption as a family that lives in its home year-round, because the exemption was written before anyone imagined buying a condo just to park money. I will end that exemption for any unit that is empty more than six months a year. The owners can afford it."
""",
st("Taxation (raise)", "Taxation (lower)", "Housing construction (promote)", "Housing construction (restrict)",
   "Social assistance (expand)", "Environmental rules (tighten)", "none of these"),
"Taxation (raise)", 3),

# ------------------------------------------------------------------ st15
# why: pulling business licences from employers of workers without legal status = employer penalties -> restrictive (yes).
#      twin: repeal the employer verification mandate -> fewer enforcement measures -> not restrictive (no).
Y("st15", "Does this statement take the more-restrictive side on immigration under the codebook?",
f"""
{RULES}

Statement ID: KT-2027-0633
Speaker: Gubernatorial candidate Everett Kowalczyk
Setting: speech to the Kestrel Township Builders' Exchange

Transcript excerpt:
"Honest contractors in this room bid jobs at honest wages, and they lose those bids to outfits that pay cash under the table to people with no papers and no protections. That's not fair to you, and it's not fair to the workers. When I'm governor, any employer found knowingly hiring workers without legal status will lose its state business licence for a year. Play by the rules or don't play."
""",
[("Immigration (more restrictive)", ST["Immigration (more restrictive)"]),
 ("Immigration (more open)", ST["Immigration (more open)"])],
1, 2,
twin=T([("When I'm governor, any employer found knowingly hiring workers without legal status will lose its state business licence for a year. Play by the rules or don't play.",
         "When I'm governor, I'll repeal the state rule that makes contractors verify every worker's immigration status through the federal database, and no one will lose a business licence over a worker's paperwork. Enforce the wage laws instead.")],
       0)),

# ------------------------------------------------------------------ st16
# why: pure character attack on attendance; no policy -> none of these (yes).
#      twin: attacks a vote to cut officers and promises to restore them -> Policing expand -> codable (no).
Y("st16", "Does this statement fail to take any codable policy position?",
f"""
{RULES}

Statement ID: AW-2027-0810
Speaker: Council candidate Bernadette Achebe-Ruiz, Ashworth Ward 5
Setting: campaign mailer, text transcribed by coder

Transcript excerpt:
"Councilman Deverell says he fights for Ward 5. The record says otherwise. He missed 41% of council votes last year, including the vote on the Fenner Street bridge and the vote on the library hours. He skipped the budget workshop entirely. You deserve a councilmember who shows up. On November 4th, vote Achebe-Ruiz."
""",
[("none of these", ST["none of these"]),
 ("Codable position", "the statement advocates a change in one of the listed policy areas, in either direction.")],
1, 2, role="neg",
twin=T([("He missed 41% of council votes last year, including the vote on the Fenner Street bridge and the vote on the library hours. He skipped the budget workshop entirely.",
         "He voted last year to eliminate 90 police officer positions to close the budget gap. I will restore all 90 positions in my first budget.")],
       0)),

# ------------------------------------------------------------------ st17
# why: rule 1: the tax is how the school bond is paid for; the advocated change is school money -> NOT Taxation (no).
Y("st17", "Should this statement be coded in the Taxation area (either direction)?",
f"""
{RULES}

Statement ID: EF-2027-0977
Speaker: Superintendent Lorraine Okafor, Eastfield School District (speaking as a private citizen)
Setting: yes-on-Measure-K rally

Transcript excerpt:
"Eastfield High was built in 1958. The boilers fail every winter and the science labs still have gas taps we can't use. Measure K raises $180 million to rebuild it, and yes, it's paid for with a property tax increase, about $38 a year for every $100,000 of assessed value. I'm asking you to vote yes on K for our kids."
""",
[("Taxation (raise)", ST["Taxation (raise)"]),
 ("Taxation (lower)", ST["Taxation (lower)"]),
 ("School funding (expand)", ST["School funding (expand)"]),
 ("Rule 1", "the way a proposal is paid for does not decide the area.")],
0, 2),

# ------------------------------------------------------------------ st18
# why: exempting small builders from stormwater permit rules = relaxing an environmental permit -> Environmental rules (loosen) (yes);
#      builders/housing are the beneficiaries (rule 1).
Y("st18", "Is Environmental rules (loosen) the correct code for this statement?",
f"""
{RULES}

Statement ID: NB-2027-0164
Speaker: State Rep. Delia Farnsworth
Setting: Northbank Homebuilders Association breakfast

Transcript excerpt:
"A family builder in Northbank putting up four houses now needs the same stormwater permit, the same engineered runoff plan and the same quarterly inspections as a regional mall. That adds five months and about $22,000 to each home. My bill exempts any project of ten homes or fewer from the state stormwater permit. Let's get people into houses."
""",
[("Environmental rules (loosen)", ST["Environmental rules (loosen)"]),
 ("Housing construction (promote)", ST["Housing construction (promote)"]),
 ("Rule 1", "the group that benefits does not decide the area; code the policy that changes.")],
1, 3),
]
