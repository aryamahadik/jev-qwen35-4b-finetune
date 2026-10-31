"""Domain D: employment classification and wage rules (invented statutes)."""
from _h import it

NONE = "none of these"

ITEMS = [

it("D1", "noul",
   "Can Sunbeam Bakery lawfully classify Lionel as an independent contractor under §2?",
   """Email - HR advisor to owner, Sunbeam Bakery (State of Corvale)
Re: Can we keep Lionel as a contractor?

Lionel Mbeki runs his own one-person web studio. He's building our new online ordering site under a fixed-price contract. He decides his own methods, uses his own laptop and software, advertises his studio online, and has about a dozen other clients. He comes to the bakery on Tuesdays to meet with you, but otherwise works wherever and whenever he likes. You mentioned that because he's here every week he "feels like staff".

Corvale Wage Act §2 (ABC test): A person providing labour or services for remuneration is an employee unless the hiring entity shows all of the following:
(A) the person is free from the hiring entity's control and direction in performing the work, both under the contract and in fact;
(B) the person performs work that is outside the usual course of the hiring entity's business; and
(C) the person is customarily engaged in an independently established trade, occupation, or business of the same nature as the work performed.""",
   1,
   card="- independent contractor under the ABC test: free from the hiring entity's control, doing work outside the usual course of its business, and customarily engaged in an independent business of the same nature; failing any prong makes the worker an employee",
   diff=1),

it("D2", "choice",
   "What is the correct result of applying Regulation 7 to Grace?",
   """Wage audit notes - Tarrin Department of Labour
Employee: Grace Opoku, "Store Manager", Pinewood Hardware (Lakeside branch)
Pay: salary of $1,150 per week, paid regardless of hours worked.
Duties: her primary duty is managing the branch. She directs the work of one full-time clerk (40 hrs/week) and two part-time clerks (20 hrs/week each). She interviews candidates, and her hiring recommendations are almost always followed by the district office.

Tarrin Wage Regulation 7 (Executive exemption from overtime): An employee is exempt only if all of the following are met:
(1) Salary test: paid on a salary basis at least $1,120 per week.
(2) Duties test: primary duty is management of the enterprise or of a recognised department or subdivision.
(3) Supervision test: customarily and regularly directs the work of two or more other full-time employees or their equivalent (for example, one full-time and two half-time employees).
(4) Authority test: has authority to hire or fire, or her recommendations on hiring, firing, or promotion are given particular weight.""",
   "exempt under the executive exemption",
   opts=["exempt under the executive exemption", "not exempt: fails the salary test", "not exempt: fails the supervision test", "not exempt: fails the authority test"],
   card="- exempt under the executive exemption: all four tests are met, so no overtime is owed\n- not exempt: fails the salary test: the salary is below $1,120 per week or not paid on a salary basis\n- not exempt: fails the supervision test: she does not direct two or more full-time employees or their equivalent\n- not exempt: fails the authority test: she cannot hire or fire and her recommendations get no particular weight",
   diff=2, twin=[("and two part-time clerks (20 hrs/week each)", "and one part-time clerk (20 hrs/week)")],
   twin_gold="not exempt: fails the supervision test"),

it("D3", "noul",
   "Can the startup lawfully leave Beatriz unpaid?",
   """Forum: Startups & Small Business - Ravel Province
Posted by founder_kim

We have a design student, Beatriz, doing a 10-week internship. Her university gives academic credit for it and it's part of her degree requirements. Our receptionist is on 3 months' leave, and instead of hiring a temp we've had Beatriz covering the front desk most days; she also sits in on design reviews on Fridays. Do we need to pay her?

Reply quoting the Ravel Employment Standards Code §4A:
An intern at a for-profit employer is not an employee, and need not be paid, only if all of the following apply:
(a) the internship is tied to the intern's accredited educational programme and the intern receives academic credit;
(b) the internship lasts no longer than 12 weeks; and
(c) the intern does not displace paid employees or perform work that the employer would otherwise pay someone to do.""",
   0,
   card="- unpaid internship conditions: tied to an accredited programme with academic credit, no longer than 12 weeks, and the intern neither displaces paid staff nor does work the employer would otherwise pay for",
   diff=1),

it("D4", "choice",
   "What is Dev's correct total gross pay for Week 32?",
   """Payroll query - Harlan Logistics, Week 32
Employee: Dev Raman, warehouse associate, hourly rate $20.00, non-exempt.
Hours worked this week: 50.
Additional pay: a $100 attendance bonus. Under the company handbook, every associate with no absences or late arrivals in the week receives this bonus automatically.

Mallory Wage and Hour Act §9:
(1) Hours worked over 40 in a workweek must be paid at 1.5 times the employee's regular rate.
(2) The regular rate is total remuneration for the workweek (excluding amounts in (3)) divided by total hours worked.
(3) Excluded from the regular rate: gifts on special occasions whose payment and amount are at the employer's sole discretion and not promised in advance; payments for time not worked; reimbursed expenses.
Payroll's draft shows $20 x 40 + $30 x 10 + $100.""",
   "$1,210",
   opts=["$1,100", "$1,200", "$1,210", "$1,310", "$1,350"],
   tpl="Dev's correct gross pay for the week is {}",
   diff=3, twin=[("Additional pay: a $100 attendance bonus. Under the company handbook, every associate with no absences or late arrivals in the week receives this bonus automatically.",
                  "Additional pay: a $100 birthday gift that his manager decided on her own to give him this week; it was never promised or announced.")],
   twin_gold="$1,200"),

it("D5", "noul",
   "Is Tobias entitled to at least the minimum wage for his cafe work?",
   """Letter to the Esker Labour Standards Office
My 17-year-old son Tobias works 20 hours a week at Lindgren's Cafe, which is a limited liability company owned 50/50 by me and my brother. We pay Tobias $8 an hour, below the $15 minimum, because I understood family members are exempt. I run the cafe day to day and I am the one who hired him. Is that right?

Esker Minimum Wage Act §3:
(1) Every employer must pay each employee at least the minimum wage.
(2) Subsection (1) does not apply to a child, spouse, or parent of an employer who is a sole proprietor, when employed in that sole proprietor's business.
(3) An employer that is a corporation, limited liability company, or partnership is not a sole proprietor, regardless of who owns it.""",
   1,
   card="- family exemption: a child, spouse or parent of a sole-proprietor employer, working in that sole proprietor's business, may be paid below the minimum wage; a corporation, LLC or partnership is never a sole proprietor",
   diff=1),

it("D6", "choice",
   "By when must Quarry Hill pay Aoife's final wages?",
   """Employee query - Quarry Hill Garden Centre
From: Aoife Brennan, seasonal sales associate
"I told my manager on Monday morning that Wednesday morning would be my last shift - so about two days' notice - and I'm quitting to start a new job. When do I have to be paid my final wages? The office says I'll get them on the next regular payday, which is 12 days away."

Maraton Final Pay Act §2:
(1) An employee who is discharged must be paid all final wages at the time of discharge.
(2) An employee who quits after giving at least 72 hours' notice must be paid all final wages on the last day of work.
(3) An employee who quits without giving at least 72 hours' notice must be paid all final wages within 72 hours after quitting.
(4) The employer may mail final wages if the employee requests it in writing.""",
   "within 72 hours after she quits",
   opts=["within 72 hours after she quits", "at the time of discharge", "on her last day of work", "on the next regular payday", "within 7 days after she quits"],
   card="- at the time of discharge: immediately, as for an employee who is fired\n- on her last day of work: payment due on the final shift itself\n- within 72 hours after she quits: payment due no later than 72 hours after she leaves\n- on the next regular payday: payment due with the normal payroll cycle\n- within 7 days after she quits: payment due within a week of leaving",
   diff=1),

it("D7", "noul",
   "Is Rohan an employee under §3?",
   """Email - Rohan Pillai to Driver Advocates of Selwyn
The app I drive for, ZipRide, lets me log on whenever I want - no shifts, no minimum hours. I can drive for other apps at the same time, and lots of us do. But ZipRide deactivates any driver whose ride-acceptance rate drops below 80% over a 30-day period; I got a warning last month. Am I an employee or a contractor under the new law?

Selwyn Platform Work Act §3:
An app-based driver is an independent contractor if the network company does not:
(a) unilaterally prescribe the dates, times of day, or minimum number of hours the driver must be logged on;
(b) require the driver to accept any specific ride request, or penalise the driver for declining requests; or
(c) restrict the driver from working for other network companies.
If the company does any of (a) to (c), the driver is an employee.""",
   1,
   card="- employee under the Platform Work Act: a driver whose network company prescribes log-on times or hours, requires acceptance of rides or penalises declining them, or restricts work for other companies",
   diff=2),

it("D8", "choice",
   "What does the Rule require for Kaveh's 14 March shift?",
   """Timesheet dispute - Ostrow Labour Standards, Claim 11-208
Employee: Kaveh Rahimi (non-exempt line cook). Shift on 14 March: 9:00 a.m. to 4:00 p.m. (7 hours). Meal break: 30 minutes, uninterrupted, starting at 2:30 p.m. No waiver was signed. The employer says he "got his full half hour".

Ostrow Meal Break Rule:
(1) An employer may not employ a non-exempt employee for a work period of more than 5 hours without a meal break of at least 30 minutes that begins no later than the end of the employee's fifth hour of work.
(2) If the total work period is no more than 6 hours, the meal break may be waived by mutual written consent.
(3) For each workday on which a meal break is not provided as required, the employer must pay one additional hour of pay at the employee's regular rate.""",
   "one additional hour of pay",
   opts=["no violation: nothing further owed", "no violation because the break could be waived", "two additional hours of pay", "one additional hour of pay"],
   card="- no violation: nothing further owed: the break met the Rule\n- one additional hour of pay: the break was not provided as required, triggering one premium hour\n- two additional hours of pay: two premium hours are owed for the day\n- no violation because the break could be waived: the shift was short enough to waive the break",
   diff=2),

it("D9", "noul",
   "Was payroll's deduction permissible under §5?",
   """HR helpdesk ticket - Calloway Analytics
Employee: Mirela Dascalu, salaried analyst (exempt), $1,500 per week.
She left at noon on Tuesday to attend her brother's graduation, and payroll deducted half a day's salary ($150) from her weekly pay. She has no remaining paid time off. She says the deduction is illegal.

Norrland Salary Basis Rule §5:
(1) An exempt employee must receive the full predetermined salary for any week in which the employee performs any work, subject to (2) and (3).
(2) Deductions may be made for absences of one or more full days for personal reasons other than sickness or disability.
(3) Deductions for full-day absences due to sickness or disability may be made only under a bona fide sick-leave plan.
(4) Deductions for absences of less than a full day are not permitted.""",
   0,
   card="- permitted salary deduction: only for absences of one or more full days for personal reasons (or full-day sickness absences under a bona fide sick-leave plan); never for partial-day absences",
   diff=2, twin=[("She left at noon on Tuesday to attend her brother's graduation, and payroll deducted half a day's salary ($150) from her weekly pay.",
                  "She took all of Tuesday off to attend her brother's graduation, and payroll deducted one day's salary ($300) from her weekly pay.")],
   twin_gold=1),

it("D10", "choice",
   "How does §1 classify Amara in relation to Swiftbox?",
   """Tribunal intake - Lyle Province Employment Tribunal
Worker: Amara Diallo, courier. Engager: Swiftbox Parcels Ltd.
Amara uses her own van, chooses her own routes and delivery order, and decides which days and hours she works; Swiftbox only specifies the pickup depot and the delivery addresses. Over the past 12 months, 85% of her courier income came from Swiftbox; the rest came from two florists.

Lyle Employment Standards Act §1:
(a) "Employee" means a worker whose engager controls both when the work is done and how it is done.
(b) "Dependent contractor" means a worker who is not an employee but who, over the preceding 12 months, received at least 80% of their income from the work from a single engager.
(c) "Independent contractor" means any other worker who is not an employee.""",
   "dependent contractor",
   opts=["employee", "independent contractor", "dependent contractor"],
   card="- employee: the engager controls both when and how the work is done\n- dependent contractor: not an employee, but at least 80% of the worker's income from the work over 12 months came from one engager\n- independent contractor: any other worker who is not an employee",
   diff=2),

it("D11", "noul",
   "Must Morrow Retail Group offer Chidi health coverage?",
   """Benefits eligibility review - Morrow Retail Group
Employee: Chidi Okafor, part-time cashier.
Look-back period: the 52 weeks ending September 30.
Hours actually worked in the look-back period: 1,456. Paid vacation hours taken: 120. Unpaid personal leave: 40 hours.
Store manager's note: "He's scheduled 28 hours a week, so he's under 30 - no coverage."

Morrow State Health Coverage Act §4:
(1) An employer with 50 or more employees must offer health coverage to every employee who averaged at least 30 hours of service per week during the 52-week look-back period.
(2) "Hours of service" means hours for which the employee is paid or entitled to payment, including hours of paid vacation, holiday, and sick leave. Unpaid leave is not counted.
Morrow Retail Group has 340 employees.""",
   1,
   card="- hours of service: hours for which the employee is paid or entitled to payment, including paid vacation, holiday and sick leave, but not unpaid leave\n- coverage duty: an employer with 50 or more employees must offer coverage to anyone averaging at least 30 hours of service per week over the 52-week look-back",
   diff=2, twin=[("Paid vacation hours taken: 120.", "Paid vacation hours taken: 80.")], twin_gold=0),

it("D12", "choice",
   "Whose inclusion in the tip pool is unlawful?",
   """Compliance review - Harrow & Hearth restaurant tip pool
The restaurant pays tipped staff a cash wage of $11.00 an hour and claims a tip credit toward the $15.00 minimum wage. The mandatory nightly tip pool is shared among: servers; bussers; dishwashers; and the shift lead. The shift lead also serves tables, assigns sections and can write staff up, but cannot hire, fire, or set pay.

Vale County Tip Pooling Rule:
(1) An employer may require employees to participate in a tip pool with other employees who customarily and regularly receive tips.
(2) No manager or supervisor with authority to hire, fire, or set pay may receive any share of a tip pool.
(3) Employees who do not customarily and regularly receive tips (such as dishwashers and cooks) may share in a tip pool only if the employer pays all participants at least the full minimum wage and claims no tip credit.
Servers, bussers and the shift lead customarily and regularly receive tips at Harrow & Hearth.""",
   "dishwashers",
   opts=["servers", "bussers", "dishwashers", "the shift lead", NONE],
   card="- servers: front-of-house staff who take orders and serve tables\n- bussers: staff who clear and reset tables\n- dishwashers: back-of-house staff who wash dishes\n- the shift lead: the senior server who assigns sections and can write staff up\n- none of these: every group's inclusion is lawful",
   diff=2),

it("D13", "noul",
   "Is Whitecrest exempt from overtime under §7(c)?",
   """Wage claim response - Whitecrest Mountain Resort (State of Harrowgate)
Lift operator Ewan Duffy claims overtime. The resort says it is exempt as a seasonal recreational establishment.
Operations: ski season from November 15 to April 10; lift-served mountain biking on weekends in June, July, and August. The resort therefore operates in 9 calendar months of the year.
Prior calendar year receipts: November-April months $4.2 million in total; May-October months $1.3 million in total.

Harrowgate Wage Act §7(c): The overtime requirement does not apply to any employee of an amusement or recreational establishment if (i) it does not operate for more than 7 months in any calendar year, or (ii) during the preceding calendar year, its average receipts for any 6 months of that year were not more than 33 1/3% of its average receipts for the other 6 months of that year.""",
   1,
   card="- seasonal recreational exemption: the establishment operates no more than 7 months a year, or in the preceding calendar year its average receipts for some 6 months were no more than one third of its average receipts for the other 6 months",
   diff=3),

it("D14", "choice",
   "How much must the diner add to Lena's pay for the week of 9 June?",
   """Payroll question - Juniper Street Diner
Server: Lena Kowalczyk. Week of 9 June: 30 hours worked. Cash wage paid: $12.00 an hour. Tips reported for the week: $80. She usually receives well over $300 a month in tips, but this was a slow week.

Quillon Minimum Wage Order §6:
(1) The minimum wage is $16.00 per hour.
(2) An employer may pay a tipped employee a cash wage as low as $12.00 per hour if the employee customarily receives more than $30 a month in tips, and the employee's cash wages plus tips for the workweek equal at least the minimum wage for all hours worked.
(3) If cash wages plus tips for the workweek fall short, the employer must pay the difference.""",
   "$40",
   opts=["$0", "$40", "$80", "$120", "$160"],
   tpl="the diner must add {} for the week",
   extra={"$0": "the diner owes nothing extra for the week"},
   diff=2),

it("D15", "noul",
   "As far as §2 is concerned, can Brightline enforce the non-compete against Tamsin?",
   """Email from employment lawyer to client Tamsin Rhee
You earned $72,000 at Brightline Software last year (W-2, box 1). When you joined, you also bought a 15% stake in Brightline. When you resigned last month, you sold that stake back to the company, and the stake buy-back agreement you signed included a 12-month non-compete. You asked whether it can be enforced, since you've heard non-competes are void for anyone under $75,000.

Oakhurst Restrictive Covenants Act:
§2 A covenant not to compete is void and unenforceable against an employee whose earnings from the employer for the prior calendar year, as reported in box 1 of the W-2, were $75,000 or less.
§3 Section 2 does not apply to a covenant entered into in connection with the sale of the covenantor's ownership interest in a business, if the covenantor held at least 10% of that business.""",
   1,
   card="- low-earner voidness rule: a non-compete is void against an employee earning $75,000 or less, except a covenant given in connection with selling an ownership stake of at least 10% in the business",
   diff=2),

it("D16", "choice",
   "How much of Thursday's driving counts as working time?",
   """Payroll question from a site supervisor - Ashdown Surveying
Technician Mika Laine normally drives 30 minutes each way between home and our office. On Thursday we sent her on a one-day job in Carrow: she drove 2 hours from home directly to the Carrow site, then 40 minutes from the Carrow site to a second client site, and 2 hours from the second site straight home. How much of that driving is paid working time?

Halsted Hours of Work Rule:
(1) Ordinary travel between home and the employee's regular workplace is not working time.
(2) When an employee travels from home to a one-day assignment in another city, the travel time (in each direction) is working time except for the time the employee would normally spend commuting.
(3) Travel between work sites during the workday is working time.""",
   "3 h 40 min",
   opts=["0 h", "3 h", "3 h 40 min", "4 h", "4 h 40 min"],
   tpl="{} of Thursday's driving is working time",
   extra={"0 h": "none of Thursday's driving is working time"},
   diff=3),

it("D17", "noul",
   "Can Greenhollow treat Mei's Saturday hours as unpaid volunteer time?",
   """Email thread - Greenhollow Food Bank (registered nonprofit)
From: Director

Mei Tanaka works for us part-time as our paid receptionist, Monday to Wednesday, greeting visitors and answering phones. She's offered to "volunteer" on Saturday to staff the reception desk at our fundraising gala - greeting guests and answering the phones. She says she believes in the cause and doesn't want to be paid. Can we accept without paying her?

Norwood Wage Act §8:
(1) An individual who performs services for a nonprofit organisation for civic, charitable, or humanitarian reasons, without promise or expectation of compensation, is a volunteer and not an employee.
(2) An individual may not be a volunteer for a nonprofit organisation that employs the individual if the services to be performed are the same type of services the individual is employed to perform for that organisation.""",
   0,
   card="- volunteer: someone serving a nonprofit for civic, charitable or humanitarian reasons without expecting pay, but never an employee of that nonprofit doing the same type of services she is employed to perform",
   diff=1),

it("D18", "choice",
   "Whose on-call hours count as working time under §12?",
   """Hospital HR memo - St. Aurel Hospital: on-call pay review
Rule (Ilford Hours of Work Code §12): On-call time is working time if the employee (a) is required to remain on the employer's premises; or (b) is required to be able to arrive at the workplace within 15 minutes of being called; or (c) is, on average, called out more than 3 times per on-call shift. Otherwise on-call time is not working time (actual call-out time is always paid).

Staff under review (all on call from home unless noted):
- Ansel (radiology tech): must arrive within 20 minutes; called out 2 times per shift on average.
- Bettina (surgical nurse): must arrive within 15 minutes; called out once per shift on average.
- Cyrus (lab tech): must arrive within 30 minutes; called out 3 times per shift on average.
- Delphine (resident physician): may arrive within 45 minutes; she chooses to sleep in the hospital's call room because she lives far away; called out twice per shift on average.""",
   "Bettina",
   opts=["Ansel", "Bettina", "Cyrus", "Delphine", NONE],
   card="- Ansel: the radiology tech\n- Bettina: the surgical nurse\n- Cyrus: the lab tech\n- Delphine: the resident physician\n- none of these: nobody's on-call hours count as working time",
   diff=2, twin=[("must arrive within 15 minutes; called out once", "must arrive within 25 minutes; called out once")], twin_gold=NONE),

it("D19", "noul",
   "Was Fenwick & Salt required to include a pay range in the posting?",
   """Job-posting compliance question - Fenwick & Salt LLC
We posted a remote-eligible designer role without a pay range. Our headcount: 9 full-time employees in the State of Delane; 4 part-time employees who live and work in neighbouring states; and 3 independent contractors in Delane. That's 16 people in total. Are we covered?

Delane Pay Transparency Act §2:
(1) An employer with 15 or more employees must include the pay range in every job posting.
(2) In counting employees, include full-time and part-time employees wherever located, provided at least one employee works in Delane. Do not count independent contractors.""",
   0,
   card="- employee count: full-time and part-time employees wherever located (if at least one works in Delane), excluding independent contractors; 15 or more triggers the pay-range duty",
   diff=2, twin=[("4 part-time employees", "6 part-time employees"), ("That's 16 people in total.", "That's 18 people in total.")], twin_gold=1),

it("D20", "choice",
   "What is Hana's eligibility status under §2?",
   """Leave request review - Corby Manufacturing
Employee: Hana Sato, machinist at the Westfield plant (40 employees). Corby's only other site, the Eastmoor plant (25 employees), is 60 miles from Westfield.
Hana has worked for Corby for 14 months and worked 1,300 hours in the past 12 months. She requests 8 weeks of family-care leave. The plant manager believes Westfield is "too small to be covered".

Tallis Family Care Leave Act §2:
An employee is eligible for leave if the employee (a) has been employed by the employer for at least 12 months, (b) worked at least 1,250 hours during the 12 months before the leave, and (c) works at a worksite where the employer has at least 50 employees within 75 miles of that worksite.""",
   "eligible",
   opts=["eligible", "ineligible: length of employment", "ineligible: hours worked", "ineligible: employer size within 75 miles"],
   card="- eligible: all three conditions in §2 are met\n- ineligible: length of employment: employed for less than 12 months\n- ineligible: hours worked: fewer than 1,250 hours in the prior 12 months\n- ineligible: employer size within 75 miles: fewer than 50 employees within 75 miles of her worksite",
   diff=2),

it("D21", "noul",
   "Is Kwame exempt from overtime under §13(i)?",
   """Overtime claim - Kwame Asante v. Vista Home Furnishings (retail)
Representative period (one month): Kwame worked 200 hours and earned $5,200 in total, of which $2,500 was commission on sales and the rest hourly pay. The minimum wage is $16.00 an hour. Vista classifies all its floor salespeople as "commission employees" and pays no overtime.

Branford Wage Act §13(i): An employee of a retail or service establishment is exempt from overtime in any workweek if (1) the employee's regular rate of pay exceeds one and one-half times the minimum wage, and (2) more than half of the employee's total earnings in a representative period of not less than one month consists of commissions.""",
   0,
   card="- retail commission exemption: regular rate above 1.5 times the minimum wage, and more than half of total earnings over a representative period of at least one month consists of commissions",
   diff=2, twin=[("of which $2,500 was commission", "of which $2,700 was commission")], twin_gold=1),

it("D22", "choice",
   "What is Nuno's total required pay for 4 May?",
   """Payroll dispute - Cresthaven Warehouse
Employee: Nuno Almeida, $18 an hour. He was scheduled for a 10-hour shift on 4 May, reported on time, and was sent home after 1 hour because a delivery truck broke down. He was paid for 1 hour ($18).

Lorwen Reporting Time Pay Order:
(1) Each workday an employee is required to report for work and does report, but is furnished less than half the usual or scheduled day's work, the employee must be paid for half the scheduled day's work, but in no event less than 2 hours nor more than 4 hours, at the regular rate.
(2) Pay under (1) includes pay for time actually worked.""",
   "$72",
   opts=["$18", "$36", "$54", "$72", "$90", "$180"],
   tpl="Nuno's total required pay for the day is {}",
   diff=2, twin=[("scheduled for a 10-hour shift", "scheduled for a 6-hour shift")], twin_gold="$54"),

it("D23", "noul",
   "Was Jonah's 8:30 p.m. finish on September 4 lawful under §5?",
   """Inspection note - Delmar Youth Employment Unit
Employer: Popcorn Palace Cinema. Minor: Jonah Reyes, age 15.
On Friday, September 4, 2026, Jonah worked a shift ending at 8:30 p.m. His school year began on Monday, August 31. Labor Day in 2026 fell on Monday, September 7. The manager says the late shift was scheduled because a summer blockbuster was still drawing crowds. The trainee inspector wrote "school in session - 7 p.m. limit" in the margin of the file.

Delmar Child Labour Act §5: A minor aged 14 or 15 may not be employed after 7:00 p.m. on any day, except that from June 1 through Labor Day the limit is 9:00 p.m.""",
   1,
   card="- evening limit for ages 14-15: no work after 7:00 p.m., except no work after 9:00 p.m. from June 1 through Labor Day",
   diff=2),

it("D24", "choice",
   "Which state's Act applies to Farah?",
   """Memo - Payroll compliance, Helix Data Co.
Employee: Farah Idris, account manager. Last year she performed 40% of her work in the State of Norland, 35% in the State of Vesper, and 25% while travelling in other states. Her base of operations - the office she reports to, where her manager sits - is in Vesper. Payroll has been applying Norland law because "that's where she works most".

Both Norland and Vesper have enacted the Uniform Wage Coverage Act, whose §3 reads:
(1) This Act applies to an employee who performs more than 50% of the employee's work in this State.
(2) If the employee does not perform more than 50% of the employee's work in any single State, this Act applies if the employee's base of operations is in this State.""",
   "Vesper's Act only",
   opts=["both states' Acts", "neither state's Act", "Norland's Act only", "Vesper's Act only"],
   card="- Norland's Act only: only Norland's version of the Act covers her\n- Vesper's Act only: only Vesper's version of the Act covers her\n- both states' Acts: both versions cover her\n- neither state's Act: neither version covers her",
   diff=3),

it("D25", "noul",
   "Does the teacher exception in §4(2) apply to Oona?",
   """Wage complaint - Oona Brightwater v. Splash Academy
Oona teaches children's swimming lessons full-time at Splash Academy, a private swim school offering lessons to children aged 4 to 12, earning $620 a week. She regularly works 48 hours a week without overtime pay. The school says she is exempt because her job title is "Swim Teacher" and teaching is her primary duty.

Ferrant Overtime Exemptions §4:
(1) The learned-professional exemption requires a salary of at least $1,000 per week, except as provided in (2).
(2) The salary requirement does not apply to a teacher whose primary duty is teaching in an educational establishment.
(3) "Educational establishment" means an elementary or secondary school, or an institution of higher education, that is accredited by the Ferrant Education Board.""",
   0,
   card="- educational establishment: an accredited elementary or secondary school, or an accredited institution of higher education\n- teacher exception: a teacher whose primary duty is teaching in an educational establishment is exempt from the salary requirement",
   diff=1),

it("D26", "choice",
   "How much must Westmere pay Joan for unused leave?",
   """Final pay calculation - Westmere Credit Union
Departing employee: Joan Adebayo, hourly equivalent $30.
Written leave policy: vacation accrues at 80 hours per year, capped at 120 hours; accrual stops while the balance is at the cap. The policy states in writing that floating holidays are a separate benefit that is not paid out at separation.
Joan's balances at separation: vacation 120 hours; floating holiday 8 hours.

Kester Wage Payment Act §10:
(1) All earned, unused vacation must be paid at the final rate of pay upon separation.
(2) A policy may cap further accrual at a reasonable level, but may not cause earned vacation to be forfeited.
(3) An employer need not pay out floating holidays if its written policy distinguishes them from vacation.""",
   "$3,600",
   opts=["$3,600", "$3,840", "$3,900", "$4,140"],
   tpl="Westmere must pay {} for unused leave",
   diff=2),
]
