"""codebook_c / legislative committee referral (Veloria General Assembly, invented state)."""
from _lib import C, Y, T

LG = {
    "Revenue and Taxation": "Bills whose main instrument is a tax: rates, bases, credits, deductions, exemptions or collection, whatever sector or group the tax change targets.",
    "Appropriations": "Bills whose main purpose is to appropriate or transfer money or to change the budget process; a bill that creates a program and funds it goes to the program's subject committee instead.",
    "K-12 Education": "Public and charter schools from kindergarten to grade 12: curriculum, teachers, the school funding formula, school governance and testing.",
    "Higher Education": "Public universities and community colleges, tuition, student financial aid and academic research institutions.",
    "Health": "Health care delivery, public health, hospitals, licensing of health professions, and the Medicaid benefit package and provider rates.",
    "Human Services": "Cash assistance, food assistance, child care subsidies, child welfare, foster care and non-medical disability services.",
    "Judiciary": "Civil law, courts and judges, family law, probate, civil procedure and civil liability.",
    "Public Safety": "Criminal offences and criminal penalties, policing, corrections, parole and emergency management.",
    "Transportation": "Roads, bridges, transit, vehicle registration, driver licensing, and traffic rules enforced by civil fines.",
    "Natural Resources": "Water rights, state forests, parks, fish and wildlife (including hunting and fishing licences), mining and public lands.",
    "Environmental Quality": "Air, water and soil pollution, waste, recycling and toxic substances.",
    "Agriculture": "Farming, livestock, crop production, farmland and agricultural marketing.",
    "Housing": "Housing supply, landlord-tenant law (including eviction notice periods), homelessness programs and the state housing finance agency.",
    "Labor and Workforce": "Wages, hours, workplace safety, private-sector collective bargaining, unemployment insurance and job training.",
    "Commerce and Consumer Protection": "Business regulation, consumer protection, licensing of occupations other than health professions, and non-tax economic development incentives.",
    "Insurance and Financial Services": "Insurance markets, including coverage mandates on private insurers, and banks, credit unions, lending and securities.",
    "Energy and Utilities": "Electricity, natural gas, utility rates and utility operations, telecommunications and broadband infrastructure.",
    "Elections and State Government": "Elections, including the timing and administration of state and local elections, campaign finance, lobbying, ethics, state agency structure, public records and state employees.",
    "Local Government": "Powers, structure, debt and finances of counties, cities and special districts, including approval rules for local borrowing and the distribution of shared state revenue to localities.",
    "Veterans and Military Affairs": "Programs administered by the Department of Veterans Services, the state national guard and military installations; benefits for veterans delivered through another sector's institutions go to that sector's committee.",
    "none of these": "The bill's primary subject falls under none of the other listed committees.",
}


def lg(*names):
    return [(n, LG[n]) for n in names]


GUIDE = ("Referral guide, rule 1: each bill receives one primary committee, chosen by the bill's main "
         "policy instrument and goal, not by the setting in which it operates or the group it names.")

ITEMS = [
# ------------------------------------------------------------------ lg01
# why: the instrument is a credit against income tax -> Revenue and Taxation; teachers/schools are the setting.
#      twin: same money delivered through the school funding formula -> K-12 Education (program + funding -> subject committee).
C("lg01", "Which standing committee should receive primary referral of this bill?",
f"""
VELORIA GENERAL ASSEMBLY — Office of the Clerk
Referral worksheet, 2027 Regular Session

Bill: HB 1184   Sponsor: Rep. Imogen Farrow (D-12)
Short title: Classroom Supplies Relief Act

Legislative Counsel digest:
Teachers in Veloria's public and charter schools report spending an average of $640 of their own money each year on paper, books, art materials and classroom software. This bill gives each full-time classroom teacher employed by a public or charter school up to $300 a year for classroom supplies the teacher bought with personal funds, delivered as a nonrefundable credit against the state personal income tax. Teachers must keep receipts for three years. The bill applies to supplies bought on or after 1 January 2028.

Estimated fiscal impact: $9.8 million per year.
Supporters listed on the digest: Veloria Education Association, Parent-Teacher Council of Arden County.

{GUIDE}
""",
lg("Revenue and Taxation", "K-12 Education", "Appropriations", "Labor and Workforce", "Higher Education",
   "Human Services", "Commerce and Consumer Protection", "Local Government", "none of these"),
"Revenue and Taxation", 2,
twin=T([("delivered as a nonrefundable credit against the state personal income tax",
         "delivered as a reimbursement paid by the teacher's school district from a new per-teacher supply allotment added to the state school funding formula")],
       "K-12 Education")),

# ------------------------------------------------------------------ lg02
# why: camera enforcement with a civil fine on the owner = traffic rule enforced by civil fine -> Transportation.
#      twin: makes it a misdemeanor with jail -> criminal penalty -> Public Safety.
C("lg02", "Under the referral guide, which committee gets this bill?",
f"""
Referral worksheet — SB 402 (Sen. Tobias Kellan, R-7)
Short title: Stop-Arm Safety Act

Digest: School bus drivers in Veloria logged 3,112 incidents last school year in which a vehicle passed a stopped school bus with its red lights flashing and stop arm extended. SB 402 authorizes school districts to mount cameras on the stop arms of their buses. Under the bill, passing a stopped school bus with its stop arm extended is punishable by a civil fine of $300 mailed to the registered owner of the vehicle, processed in the same way as a red-light camera ticket, with no points added to any driving record. Districts may contract with a camera vendor and keep up to 20% of fine revenue to cover program costs; the rest goes to the state highway safety account.

Supporting organisations: Veloria School Bus Drivers Association, Safe Routes Coalition.
Opposed: none on file.

{GUIDE}
""",
lg("Transportation", "Public Safety", "K-12 Education", "Local Government", "Judiciary", "Commerce and Consumer Protection",
   "Revenue and Taxation", "Elections and State Government", "none of these"),
"Transportation", 2,
twin=T([("is punishable by a civil fine of $300 mailed to the registered owner of the vehicle, processed in the same way as a red-light camera ticket, with no points added to any driving record",
         "becomes a class 1 misdemeanor punishable by up to six months in county jail, and camera images may be used as evidence in the criminal prosecution of the driver")],
       "Public Safety")),

# ------------------------------------------------------------------ lg03
# why: tax rate and base unchanged; the bill only changes how the cities' share is distributed -> Local Government.
#      twin: rate cut -> Revenue and Taxation.
C("lg03", "Which committee should this bill be referred to?",
f"""
Veloria General Assembly — Bill Referral Memo
To: Speaker's Office   From: Referral Clerk   Re: HB 1560

HB 1560 (Rep. Dario Mendes, D-30) concerns the state sales tax. Background: under current law, 1.2 percentage points of the state sales tax collected in each city are returned to that city, based entirely on where the sale took place. Cities with regional shopping centres receive several times more per resident than residential suburbs.

Operative section: the bill changes the formula for the cities' share so that 60% is distributed by population and 40% by point of sale, phased in over four years. The state sales tax rate and the list of taxable goods are unchanged.

Affected parties: 142 cities. The Veloria League of Cities is neutral; the Suburban Mayors Caucus supports the bill; the Retail Merchants Association has not taken a position.

{GUIDE}
""",
list(LG.items()),
"Local Government", 3,
twin=T([("the bill changes the formula for the cities' share so that 60% is distributed by population and 40% by point of sale, phased in over four years. The state sales tax rate and the list of taxable goods are unchanged.",
         "the bill lowers the state sales tax rate from 5.5% to 5.2% for sales made on or after 1 July 2028. The formula for the cities' share is unchanged.")],
       "Revenue and Taxation")),

# ------------------------------------------------------------------ lg04
# why: veterans rule: a veterans' benefit delivered through community colleges goes to the colleges' committee -> Higher Education.
#      twin: cash stipend paid by the Department of Veterans Services -> Veterans and Military Affairs.
C("lg04", "Identify the committee of primary referral for this bill.",
f"""
Referral worksheet — HB 1377 (Rep. Wendell Oyelaran, R-44)
Short title: Service to Scholars Act

Digest: Roughly 61,000 veterans live in Veloria, and fewer than one in five have used any education benefit since discharge. HB 1377 provides that any honourably discharged veteran who has lived in Veloria for at least one year shall have tuition and mandatory fees waived by the public community college in which the veteran enrolls, for up to 60 credit hours. Each community college must designate a veterans' success coordinator and report enrolment and completion figures annually.

Endorsements: Veloria Veterans Council, Community College Presidents' Association (with amendments).
Fiscal note: waived tuition estimated at $14.2 million per year.

{GUIDE}
Rule 6: benefits for veterans delivered through another sector's institutions are referred to that sector's committee.
""",
lg("Higher Education", "Veterans and Military Affairs", "K-12 Education", "Appropriations", "Labor and Workforce",
   "Human Services", "Revenue and Taxation", "none of these"),
"Higher Education", 2,
twin=T([("shall have tuition and mandatory fees waived by the public community college in which the veteran enrolls, for up to 60 credit hours. Each community college must designate a veterans' success coordinator",
         "shall receive a cash education stipend of up to $4,000 per year paid directly by the Department of Veterans Services, usable at any accredited institution. The Department must designate a veterans' education coordinator")],
       "Veterans and Military Affairs")),

# ------------------------------------------------------------------ lg05
# why: the duties fall on electric utilities (shutoffs, mitigation plans filed with the utilities commission) -> Energy and Utilities.
#      twin: duty on the state forestry division to thin state forest land -> Natural Resources.
C("lg05", "Which standing committee should this wildfire bill go to?",
f"""
Office of the Clerk — Referral request
Bill: SB 588, Wildfire Readiness Act (Sen. Priya Halvorsen, D-19)

Summary prepared by Legislative Counsel:
Last summer's Sawtooth Ridge fire burned 41,000 acres of state forest and destroyed 212 homes; investigators traced its ignition to a downed line. SB 588 requires every electric utility operating in Veloria to de-energise distribution lines in areas under a red-flag fire warning, and to file an annual wildfire mitigation plan with the Public Utilities Commission describing vegetation clearance, line inspections and customer notification. The Commission may fine a utility up to $50,000 per day for failing to file.

Stakeholders: Veloria Forestry Association (support), Rural Electric Cooperatives (oppose), Fire Chiefs Association (support).

{GUIDE}
""",
lg("Energy and Utilities", "Natural Resources", "Public Safety", "Environmental Quality", "Housing",
   "Insurance and Financial Services", "Agriculture", "Local Government", "Commerce and Consumer Protection", "none of these"),
"Energy and Utilities", 2,
twin=T([("requires every electric utility operating in Veloria to de-energise distribution lines in areas under a red-flag fire warning, and to file an annual wildfire mitigation plan with the Public Utilities Commission describing vegetation clearance, line inspections and customer notification. The Commission may fine a utility up to $50,000 per day for failing to file.",
         "requires the state forestry division to thin dead timber and brush on at least 30,000 acres of state forest land each year, and to publish an annual fuel-reduction plan describing prescribed burns, thinning contracts and trail closures. The division may hire up to 60 seasonal crews to do the work.")],
       "Natural Resources")),

# ------------------------------------------------------------------ lg06
# why: the instrument is a wage floor for employees -> Labor and Workforce, despite the health-care setting.
#      twin: raises the Medicaid rate paid to facilities -> Health (Medicaid provider rates).
C("lg06", "Which committee should hear this bill first?",
f"""
Referral worksheet — HB 1902 (Rep. Soledad Quiroga, D-8)
Short title: Care Workforce Stability Act

Digest: Veloria's nursing homes and home-care agencies report turnover above 60% a year among aides, and several rural facilities have closed wings for lack of staff. HB 1902 sets a minimum hourly wage of $22 for every employee of a licensed nursing home or home-care agency who provides direct care, rising with inflation each January, and requires employers to post the rate in each facility. The Department of Labor may assess back pay and penalties against employers who pay less.

Fiscal note: indirect costs to the state are uncertain.
Support: Care Workers United, Senior Voices Veloria. Oppose: Veloria Health Care Association.

{GUIDE}
""",
lg("Labor and Workforce", "Health", "Human Services", "Appropriations", "Commerce and Consumer Protection",
   "Insurance and Financial Services", "none of these"),
"Labor and Workforce", 2,
twin=T([("sets a minimum hourly wage of $22 for every employee of a licensed nursing home or home-care agency who provides direct care, rising with inflation each January, and requires employers to post the rate in each facility. The Department of Labor may assess back pay and penalties against employers who pay less.",
         "raises the Medicaid daily reimbursement rate paid to licensed nursing homes and home-care agencies by 14%, rising with inflation each January, and requires facilities to report how the added payments were spent. The Medicaid agency may recover payments from facilities that do not report.")],
       "Health")),

# ------------------------------------------------------------------ lg07
# why: moving school board election dates = timing of local elections, which the Elections definition names expressly.
C("lg07", "Assign HB 1411 to a standing committee using the referral guide.",
f"""
From: Referral Clerk
To: Rules Committee staff
Subject: HB 1411 — referral question

HB 1411 (Rep. Gunnar Achebe, R-51) would move the election of school board members in all 176 school districts from the third Tuesday in May of odd-numbered years to the general election date in November of even-numbered years. Board members elected in May 2027 would serve an extra eighteen months. The bill also requires county election offices, rather than school district clerks, to print and count school board ballots.

Background: turnout in last spring's school board elections averaged 9%. The School Boards Association opposes the bill, arguing that board races will be lost at the bottom of a long ballot; the Association of County Clerks supports it.

The sponsor's office has asked that the bill be sent to K-12 Education, where he sits.

{GUIDE}
""",
list(LG.items()),
"Elections and State Government", 2),

# ------------------------------------------------------------------ lg08
# why: coverage mandate on private insurers -> Insurance and Financial Services (named in its definition).
#      twin: adds the item to the Medicaid benefit package -> Health.
C("lg08", "To which committee should the clerk refer this bill?",
f"""
Referral worksheet — SB 219 (Sen. Rosalind Achterberg, D-3)
Short title: Hear Every Child Act

Digest: About 1,900 Veloria children under 18 have a diagnosed hearing loss that a hearing aid could correct; a pair of paediatric hearing aids costs $3,000 to $6,000 and must be replaced as the child grows. SB 219 requires every health benefit plan issued or renewed in Veloria by a private insurer on or after 1 January 2028 to cover hearing aids and fittings for enrollees under 18, up to one pair every three years. Deductibles may apply.

Testimony requested from: Veloria Audiology Society, Children's Hospital of Marrow Bay, Veloria Association of Health Plans.

{GUIDE}
""",
lg("Insurance and Financial Services", "Health", "Human Services", "Commerce and Consumer Protection", "K-12 Education",
   "Labor and Workforce", "Appropriations", "Judiciary", "none of these"),
"Insurance and Financial Services", 2,
twin=T([("requires every health benefit plan issued or renewed in Veloria by a private insurer on or after 1 January 2028 to cover hearing aids and fittings for enrollees under 18",
         "adds hearing aids and fittings to the Medicaid benefit package from 1 January 2028 for Medicaid enrollees under 18")],
       "Health")),

# ------------------------------------------------------------------ lg09
# why: a sales tax exemption is a tax instrument -> Revenue and Taxation (families/health are the beneficiaries).
#      twin: vouchers through the cash assistance program -> Human Services.
C("lg09", "Which committee has primary jurisdiction over this bill?",
f"""
Referral worksheet — HB 1033 (Rep. Marisol Delacroix, D-22, and Rep. Evan Thorsby, R-40)
Short title: Family Essentials Act

Digest: A family with an infant spends roughly $80 a month on diapers, and public health nurses report parents stretching changes to save money, leading to rashes and infections. Under HB 1033, beginning 1 October 2027, diapers for children and adults and menstrual products are removed from the list of goods subject to the state sales and use tax. Retailers must update point-of-sale systems within 90 days.

Fiscal note: $21 million per year.
Support: Veloria Diaper Bank Network, Pediatric Nurses Association.

{GUIDE}
""",
lg("Revenue and Taxation", "Human Services", "Health", "Commerce and Consumer Protection", "Appropriations",
   "Local Government", "Insurance and Financial Services", "none of these"),
"Revenue and Taxation", 2,
twin=T([("diapers for children and adults and menstrual products are removed from the list of goods subject to the state sales and use tax. Retailers must update point-of-sale systems within 90 days.",
         "households receiving state cash assistance with a child under three receive a monthly diaper voucher worth $60 through the cash assistance program. Participating retailers must accept the voucher within 90 days.")],
       "Human Services")),

# ------------------------------------------------------------------ lg10
# why: home inspectors are a non-health occupation -> Commerce and Consumer Protection (Housing is only the setting).
#      twin: home health aides are a health profession -> Health.
C("lg10", "Which standing committee should receive this licensing bill?",
f"""
Referral worksheet — SB 731 (Sen. Hollis Varga, R-12)
Short title: Occupational Standards Act

Digest: Anyone in Veloria may currently advertise and work as a home inspector, a person paid to examine the roof, wiring, plumbing and foundation of a house for a buyer before closing. SB 731 creates a state licence for this occupation. Applicants must complete 80 hours of approved training, pass a written exam, carry $250,000 in liability coverage and renew every two years with 12 hours of continuing education. The Board of Occupational Licensing will issue licences and may suspend them after a hearing. Working without a licence carries an administrative penalty of up to $1,000.

Complaints to the Attorney General about unlicensed practitioners in this field: 184 in 2026.

{GUIDE}
""",
lg("Commerce and Consumer Protection", "Health", "Housing", "Insurance and Financial Services", "Labor and Workforce",
   "Judiciary", "Local Government", "none of these"),
"Commerce and Consumer Protection", 2,
twin=T([("work as a home inspector, a person paid to examine the roof, wiring, plumbing and foundation of a house for a buyer before closing",
         "work as a home health aide, a person paid to help patients at home with medications, wound dressings, bathing and mobility after a hospital stay")],
       "Health")),

# ------------------------------------------------------------------ lg11
# why: grants for broadband lines = broadband infrastructure -> Energy and Utilities; farms and the Commerce department are the setting.
C("lg11", "Using the referral guide, choose the committee for HB 1650.",
f"""
Referral worksheet — HB 1650 (Rep. Cordelia Nakashima, R-58)
Short title: Connected Fields Act

Digest: Precision irrigation, remote livestock monitoring and online commodity sales all need a reliable internet connection, yet 38% of Veloria farm households lack wired service faster than 25 megabits. HB 1650 creates a grant program within the Department of Commerce that pays up to 70% of the cost for internet service providers to build fibre or fixed-wireless lines to farm properties in unserved census blocks. Providers must offer service at no less than 100 megabits for ten years and accept the state's affordable-rate plan.

Fiscal note: $45 million over three years, paid from the program fund the bill creates.
Support: Veloria Farm Bureau, Rural Telecom Cooperative Alliance.

{GUIDE}
""",
list(LG.items()),
"Energy and Utilities", 3),

# ------------------------------------------------------------------ lg12
# why: approval requirement before county borrowing = local debt -> Local Government (the referendum is the mechanism, not an election-administration change).
C("lg12", "Which committee should the Speaker refer this bill to?",
f"""
Referral request — SB 614 (Sen. Augustin Pellegrini, R-26)
Short title: County Debt Accountability Act

Digest: Counties in Veloria may currently issue general obligation bonds by a two-thirds vote of the county commission. After Harrow County issued $88 million in bonds for a jail and event centre, residents complained that they had no say. SB 614 provides that a county may not issue general obligation bonds above $10 million in a single fiscal year unless a majority of county voters first approves the issue. The ballot question must state the principal amount, the estimated interest cost and the purpose. Revenue bonds repaid from user fees are exempt.

The Association of Counties opposes; Taxpayers for Veloria supports.

{GUIDE}
""",
lg("Local Government", "Elections and State Government", "Revenue and Taxation", "Appropriations", "Public Safety",
   "Insurance and Financial Services", "Judiciary", "none of these"),
"Local Government", 3),

# ------------------------------------------------------------------ lg13
# why: hunting season and tag lottery = fish and wildlife -> Natural Resources, which is NOT offered; ranchers/livestock are
#      the setting (Agriculture is wrong), so the only correct option is none of these.
C("lg13", "Pick the committee of referral for this bill; choose none of these if the correct committee is not offered.",
f"""
Referral worksheet — HB 1718 (Rep. Bartholomew Seng, R-61)
Short title: High Plains Elk Management Act

Digest: The elk herd in the Tallow Creek unit has grown to about 9,400 animals, well above the target of 6,000, and ranchers report elk breaking fences and eating stored hay meant for cattle. HB 1718 extends the general elk hunting season in the Tallow Creek unit by fourteen days and creates a lottery for 300 additional antlerless elk tags each year, with half of the tags reserved for applicants who own or lease land within the unit. The Division of Wildlife must survey the herd annually and report whether the extra tags should continue.

Support: Veloria Cattlemen's Association, Tallow Creek Sportsmen's Club.

{GUIDE}
""",
[(n, d) for n, d in LG.items() if n != "Natural Resources"],
"none of these", 3),

# ------------------------------------------------------------------ lg14
# why: shortening/lengthening an eviction notice period is landlord-tenant law -> Housing, not Judiciary.
#      twin: small-claims court limit -> courts/civil procedure -> Judiciary (yes).
Y("lg14", "Should this bill be referred to the Judiciary Committee?",
f"""
Referral worksheet — HB 1245 (Rep. Leontyne Brathwaite, D-15)

Digest: Tenant advocates report that a large share of tenants who receive a notice to pay or quit cannot gather rent owed within the current window, even when rental assistance has been approved but not yet paid. HB 1245 changes the notice a landlord must give a residential tenant before filing an eviction action for unpaid rent from 3 days to 14 days, and requires the notice to list the phone number of the state rental assistance hotline. Proceedings after filing are unchanged.

Supporters: Veloria Tenants Union. Opponents: Apartment Owners of Veloria.

{GUIDE}
""",
[("Judiciary", LG["Judiciary"]),
 ("Housing", LG["Housing"]),
 ("Primary referral", "one committee, chosen by the bill's main policy instrument and goal, not its setting.")],
0, 2,
twin=T([("HB 1245 changes the notice a landlord must give a residential tenant before filing an eviction action for unpaid rent from 3 days to 14 days, and requires the notice to list the phone number of the state rental assistance hotline. Proceedings after filing are unchanged.",
         "HB 1245 raises the maximum amount that may be claimed in small-claims court from $7,500 to $12,500, so that landlords and tenants can resolve rent and deposit disputes without hiring lawyers, and lets small-claims judges hold hearings by video.")],
       1)),

# ------------------------------------------------------------------ lg15
# why: moving money from the rainy-day fund to the general fund, nothing else = transfer of funds -> Appropriations (yes).
#      twin: creates a clinic loan-repayment program and funds it -> subject committee (Health), not Appropriations.
Y("lg15", "Does this bill belong in the Appropriations Committee under the referral guide?",
f"""
Referral worksheet — SB 90 (Sen. Majority Leader Ottilie Brandt, D-1)

Digest: The Economic Forecast Council projects that general fund revenue for fiscal year 2028 will fall $118 million short of the enacted budget because of lower capital gains receipts. SB 90 transfers $120 million from the Budget Stabilization Fund to the general fund on 1 July 2027. It creates no new program, changes no tax and makes no other change to agency spending.

The Treasurer's office supports the bill; the Senate minority leader has announced opposition, preferring agency cuts.

{GUIDE}
Rule 3: a bill that creates a program and funds it is referred to the program's subject committee.
""",
[("Appropriations", LG["Appropriations"]),
 ("Subject committee", "the committee whose definition covers the program a bill creates, even when the bill also funds it.")],
1, 2,
twin=T([("SB 90 transfers $120 million from the Budget Stabilization Fund to the general fund on 1 July 2027. It creates no new program, changes no tax and makes no other change to agency spending.",
         "SB 90 creates the Rural Clinic Loan Repayment Program in the Department of Health, which repays up to $60,000 of student loans for doctors and nurses who work five years in a rural clinic, and appropriates $12 million to fund it.")],
       0)),

# ------------------------------------------------------------------ lg16
# why: hunting and fishing licences are Natural Resources; veterans are only the beneficiaries -> outside Veterans (yes).
Y("lg16", "Is this bill outside the jurisdiction of the Veterans and Military Affairs Committee?",
f"""
Referral worksheet — HB 1299 (Rep. Delphine Okonkwo-Hart, R-37)
Short title: Honor Outdoors Act

Digest: Outdoor recreation groups that serve veterans report that licence costs are a barrier for disabled veterans on fixed incomes. HB 1299 directs the Division of Wildlife to issue annual fishing and small-game hunting licences free of charge to any Veloria resident with a service-connected disability rating of 50% or more, on proof of the rating. The Division may not charge the habitat stamp fee to these licensees. Lost revenue is estimated at $610,000 a year.

Support: Veloria Veterans Council, Disabled Anglers of Veloria.

{GUIDE}
""",
[("Veterans and Military Affairs", LG["Veterans and Military Affairs"]),
 ("Natural Resources", LG["Natural Resources"])],
1, 2, role="neg"),

# ------------------------------------------------------------------ lg17
# why: card says registration fees are not taxes; vehicle registration -> Transportation, so NOT Revenue and Taxation (no).
Y("lg17", "Is Revenue and Taxation the correct primary committee for SB 842?",
f"""
Referral worksheet — SB 842 (Sen. Cyrus Wainwright, R-33)
Short title: Road Fairness Act

Digest: Electric vehicle owners pay no state fuel tax, which funds 70% of road maintenance. SB 842 adds a $150 annual surcharge to the registration of every battery-electric passenger vehicle and $75 for plug-in hybrids, collected by the Division of Motor Vehicles with the regular registration renewal and deposited in the highway maintenance account. The fuel tax itself is unchanged.

Testimony: Drive Electric Veloria (oppose), Veloria Road Builders (support).

{GUIDE}
Rule 4: fees charged for a state licence or registration are not taxes; a bill changing such a fee goes to the committee for that licence or registration.
""",
[("Revenue and Taxation", LG["Revenue and Taxation"]),
 ("Transportation", LG["Transportation"]),
 ("Registration fee", "a charge for a state licence or registration; under rule 4 it is not a tax.")],
0, 2),
]
