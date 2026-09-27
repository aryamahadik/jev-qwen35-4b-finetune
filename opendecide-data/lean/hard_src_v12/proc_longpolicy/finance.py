"""proc_longpolicy / loans, grants, bursaries, pensions, payments and financial terms."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ fn01
# why: variation (from 1 Jan 2025) lets 10% of the balance at the start of the loan year be
# overpaid free: 10% x 60,000 = 6,000. Repayment £8,000 in loan year 2 -> 2,000 x 2% = £40.
# Twin: repayment £5,000 -> within allowance -> £0.
C("fn01", "What early repayment charge applies to the lump sum?",
"""
HAVERSTOCK BUILDING SOCIETY — PERSONAL LOAN AGREEMENT (fixed rate)
Borrower: Imelda Varga. Loan amount: £75,000. Term: 7 years. Drawdown: 1 March 2024.

1. DEFINITIONS
1.1 "Loan Year" means each 12-month period starting on the drawdown date or its anniversary.
1.2 "Opening Balance" means the amount outstanding on the first day of a Loan Year.
1.3 "Overpayment" means any payment above the scheduled monthly repayment.
1.4 "Early Repayment Charge" (ERC) means the charge payable on an Overpayment.

2. INTEREST
2.1 Interest is charged at a fixed 6.9% a year on the daily balance.

5. REPAYMENTS
5.1 Monthly repayments are collected by direct debit on the 1st of each month.
5.2 Overpayments reduce the balance on the day they are received.

6. EARLY REPAYMENT
6.1 The ERC is 2% of the amount of any Overpayment made in Loan Years 1 and 2, and 1% in Loan Years 3 to 5. No ERC is payable after Loan Year 5.
6.2 The ERC is added to the balance unless paid separately.

7. MISSED PAYMENTS
7.1 A missed payment incurs a £12 fee.

8. PAYMENT HOLIDAYS
8.1 Payment holidays are not available on fixed-rate loans.

9. CHANGES
9.1 Haverstock may change fees by giving 30 days' notice; changes that benefit the Borrower may take effect immediately.

10. ARREARS AND DEFAULT
10.1 If two monthly repayments are missed, Haverstock may issue a default notice giving 14 days to pay.
10.2 After a default notice expires unpaid, the whole balance may become payable.

11. STATEMENTS
11.1 An annual statement is sent on each anniversary of the drawdown date, showing the Opening Balance for the new Loan Year.

12. COMPLAINTS
12.1 Complaints are acknowledged within 5 working days and answered within 8 weeks.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

VARIATION LETTER — dated 5 December 2024, effective 1 January 2025
"We are improving your loan terms. From 1 January 2025, in each Loan Year you may make Overpayments totalling up to 10% of the Opening Balance without any ERC. The ERC in clause 6.1 applies only to Overpayments above that allowance."

ACCOUNT RECORD
• Loan Year 2 runs from 1 March 2025 to 28 February 2026. Opening Balance on 1 March 2025: £60,000.
• Overpayments earlier in Loan Year 2: none.
• 14 August 2025: lump sum Overpayment of £8,000 received from the Borrower.
• Borrower's email: "I understood the improved terms mean no charge at all."
""",
[("erc_40", "The first £6,000 (10% of the Opening Balance) is free under the variation, and 2% of the remaining £2,000 is £40."),
 ("erc_160", "The variation only changes the rate for Overpayments made after Loan Year 2, so this Overpayment carries the 2% ERC on the whole £8,000, which is £160."),
 ("erc_80", "The Overpayment falls in the 1% band, so the ERC on £8,000 is £80."),
 ("erc_0", "The whole Overpayment is within the annual allowance, so no ERC applies.")],
"erc_40", 2,
twin=T([("lump sum Overpayment of £8,000 received", "lump sum Overpayment of £5,000 received")], "erc_0")),

# ------------------------------------------------------------------ fn02
# why: the 2025 revision (cumulative GPA >= 2.8) applies only to scholars entering from Sep
# 2025. Scholar entered Sep 2024 -> original rule: annual GPA must be >= 3.0; 2.9 -> withdraw.
# Twin: revision applies to all scholars at reviews from June 2025 -> cumulative 3.1 -> continue.
C("fn02", "What should the scholarship committee decide at the June 2025 review?",
"""
CARRADALE FOUNDATION — MERIT SCHOLARSHIP TERMS

1. DEFINITIONS
1.1 "Scholar" means a student holding a Carradale Merit Scholarship.
1.2 "Annual GPA" means the grade point average for the academic year just completed, on a 4.0 scale.
1.3 "Cumulative GPA" means the grade point average across all years completed.
1.4 "Review" means the committee's annual review of each Scholar, held in June.
1.5 "Entry Cohort" means the September in which the Scholar began their degree.

2. AWARD
2.1 The scholarship pays £6,000 a year towards tuition for up to four years.
2.2 Payments are made to the university in two instalments, in October and February.

3. CONTINUATION
3.1 To keep the scholarship, a Scholar must achieve an Annual GPA of at least 3.0 at each Review.
3.2 A Scholar who falls below that standard loses the scholarship from the next academic year. There is no probation period.
3.3 A Scholar who takes an approved leave of absence is reviewed on return.

4. CONDUCT
4.1 A Scholar found responsible for serious academic misconduct loses the scholarship immediately.

5. SERVICE
5.1 Scholars attend one Foundation mentoring event each year.

6. APPEALS
6.1 A Scholar may appeal a Review outcome on the ground of documented extenuating circumstances within 14 days.

7. LEAVE OF ABSENCE
7.1 A Scholar may take up to one year's approved leave; the scholarship is suspended, not lost, during leave.

8. TRANSFERS
8.1 A Scholar who changes degree programme within the same university keeps the scholarship if the committee approves.

9. CHANGES TO THESE TERMS
9.1 The trustees may amend these terms. An amendment applies to the Scholars it names, from the date it states.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

REVISED CONTINUATION RULE — adopted by the trustees, 10 March 2025
"This revision applies to Scholars in the September 2025 Entry Cohort and later. For them, clause 3.1 reads: 'To keep the scholarship, a Scholar must maintain a Cumulative GPA of at least 2.8.' Clause 3.2 is unchanged."

REVIEW FILE — June 2025
Scholar: Tobiah Ncube, BSc Chemical Engineering, Entry Cohort September 2024.
Annual GPA 2024/25: 2.9. Cumulative GPA: 2.9 for year one; including a credit-bearing summer bridging course taken before entry, the university reports an overall GPA of 3.1.
Extenuating circumstances: none claimed.
Mentoring event attended: yes.
Committee member's note: "He's close — let's give him a probation semester."
""",
[("withdraw_scholarship", "The revision covers only the September 2025 Entry Cohort onwards, so the original rule applies and an Annual GPA of 2.9 is below 3.0."),
 ("continue_scholarship", "The continuation standard that applies to this Scholar at this Review is met, so the scholarship continues."),
 ("probation_semester", "Under clause 3.2 a Scholar just below the standard is first placed on probation for one semester, so withdrawal cannot happen at this Review."),
 ("reduce_award_by_half", "A shortfall of less than 0.2 in GPA reduces the award by half for the next year.")],
"withdraw_scholarship", 2,
twin=T([("\"This revision applies to Scholars in the September 2025 Entry Cohort and later. For them, clause 3.1 reads:",
         "\"This revision applies to all Scholars at Reviews held from June 2025 onwards. For them, clause 3.1 reads:"),
        ("Cumulative GPA: 2.9 for year one; including a credit-bearing summer bridging course taken before entry, the university reports an overall GPA of 3.1.",
         "Cumulative GPA: 3.1, including a credit-bearing summer bridging course that the university counts in the Cumulative GPA.")],
       "continue_scholarship")),

# ------------------------------------------------------------------ fn03
# why: from 1 Mar 2025: £5 per Late Instalment (paid more than 3 days after due), max £15 per
# order. Instalments 2 and 3 late (8 and 5 days); instalment 4 paid 2 days late (within grace)
# -> 2 x £5 = £10. Twin: instalment 4 paid 5 days late -> 3 x £5 = £15 (cap reached, not exceeded).
C("fn03", "What late fees should be applied to the order?",
"""
PAYLETTE — PAY IN FOUR: CUSTOMER TERMS

1. DEFINITIONS
1.1 "Order" means a purchase split into four equal Instalments.
1.2 "Instalment" means each of the four payments, due every two weeks from the date of purchase.
1.3 "Grace Period" means 3 days after an Instalment's due date.
1.4 "Late Instalment" means an Instalment not paid in full by the end of its Grace Period.

2. PAYMENTS
2.1 The first Instalment is taken at checkout; the rest are collected automatically from the card on file.
2.2 If a collection fails we retry the next day and at the end of the Grace Period.

3. LATE FEES
3.1 A late fee of £6 is charged for each Late Instalment.
3.2 Total late fees on an Order may not exceed 25% of the Order value.

4. ACCOUNT RESTRICTIONS
4.1 Customers with a Late Instalment cannot place new Orders until all overdue amounts are paid.

5. REFUNDS AND RETURNS
5.1 Refunds from the retailer are applied to the remaining Instalments first.

6. CREDIT REPORTING
6.1 Instalments more than 30 days overdue may be reported to credit reference agencies.

7. COMPLAINTS
7.1 Complaints are answered within 8 weeks.

8. MISSED PAYMENT HELP
8.1 Customers can move an Instalment date once per Order by up to 7 days in the app, before the Instalment is due. A moved Instalment is not late if paid by its new date.

9. CHANGES TO THESE TERMS
9.1 We may change these terms. Changes apply to Orders placed on or after the date stated in the change.

10. GOVERNING LAW
10.1 These terms are governed by the law of the country in which the customer lives.

TERMS UPDATE — effective for Orders placed on or after 1 March 2025
U1. Clause 3.1 is replaced: "A late fee of £5 is charged for each Late Instalment."
U2. Clause 3.2 is replaced: "Total late fees on an Order may not exceed £15."
U3. Definitions 1.3 and 1.4 are unchanged.

ORDER PL-5521908 — placed 2 June 2025, value £48 (4 × £12)
• Instalment 1: taken at checkout, 2 June.
• Instalment 2: due 16 June; paid 24 June (8 days after due date).
• Instalment 3: due 30 June; paid 5 July (5 days after due date).
• Instalment 4: due 14 July; paid 16 July (2 days after due date).
Customer's message: "I know I was late a couple of times. What do I owe?"
""",
[("fees_10", "Instalments 2 and 3 were paid after the Grace Period and Instalment 4 within it, so 2 × £5 = £10 under the updated terms."),
 ("fees_12", "The old £6 fee still applies to this Order, and two Late Instalments at £6 each make £12, which is exactly the 25% cap on a £48 Order."),
 ("fees_15", "Three Instalments were paid after the Grace Period, so 3 × £5 = £15, which is within the cap."),
 ("fees_18", "Three Instalments were paid after their due dates, so 3 × £6 = £18.")],
"fees_10", 2,
twin=T([("Instalment 4: due 14 July; paid 16 July (2 days after due date).", "Instalment 4: due 14 July; paid 19 July (5 days after due date).")], "fees_15")),

# ------------------------------------------------------------------ fn04
# why: grant awarded 20 Feb 2025, after the 1 Jan 2025 terms revision -> virements up to 20% of
# the source line need no approval. £9,000 / £60,000 staff line = 15% -> travel line -> proceed.
# Equipment can never be increased without approval (unchanged). Twin: move into equipment ->
# approval needed.
C("fn04", "Can the research team move the funds without the funder's approval?",
"""
NORTHCOTE RESEARCH TRUST — STANDARD GRANT CONDITIONS

1. DEFINITIONS
1.1 "Budget Line" means a heading in the approved budget: Staff, Travel, Consumables, Equipment, Dissemination.
1.2 "Virement" means moving funds from one Budget Line to another.
1.3 "Source Line" means the Budget Line from which funds are moved.
1.4 "Award Date" means the date on the grant offer letter.

2. PAYMENT
2.1 Grants are paid quarterly in advance against the approved budget.

5. BUDGET CHANGES
5.1 The grant holder may make a Virement of up to 10% of the Source Line's approved amount without the Trust's approval.
5.2 Larger Virements need the Trust's prior written approval.
5.3 The Equipment line may never be increased without the Trust's prior written approval, whatever the amount.
5.4 The total grant may not be increased.

6. REPORTING
6.1 Annual financial reports are due within 3 months of each anniversary of the start date.

7. PUBLICATIONS
7.1 Outputs must acknowledge the Trust and be published open access.

8. UNDERSPEND
8.1 Unspent funds are returned at the end of the grant.

9. STAFF COSTS
9.1 Staff costs must relate to named posts in the approved budget. Delays in recruitment should be reported in the annual report.

10. TRAVEL
10.1 Travel must be by the most economical means; first-class travel is not allowed.

11. EXTENSIONS
11.1 No-cost extensions of up to 12 months may be requested at least 3 months before the end date.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

12. VARIATION OF CONDITIONS
12.1 The Trust may revise these conditions; revisions apply to grants as stated in the revision.

REVISED CONDITIONS — for grants with an Award Date on or after 1 January 2025
R1. In clause 5.1, "10%" is replaced by "20%".
R2. Clauses 5.3 and 5.4 are unchanged.

GRANT NRT-25-031 — "Microplastic transport in upland rivers"
Award Date: 20 February 2025.
Approved budget: Staff £60,000; Travel £15,000; Consumables £12,000; Equipment £8,000; Dissemination £5,000.
Proposed change (July 2025): move £9,000 from Staff (post started three months late) to Travel, to fund extra field campaigns in the Tarn valley.
No earlier Virements.
University grants office's first reply: "Anything over 10% goes to the funder — we'll draft the request."
""",
[("proceed_without_approval", "The revised conditions apply, and £9,000 is 15% of the Staff line, within 20%, moving into Travel, so no approval is needed."),
 ("request_approval_over_threshold", "£9,000 is 15% of the Staff line, more than the 10% that clause 5.1 allows without approval, so the Trust's prior written approval is required."),
 ("request_approval_equipment", "The funds would go into the Equipment line, which can never be increased without the Trust's approval."),
 ("refuse_virement_total_grant", "Moving money between lines increases the grant total, which clause 5.4 forbids.")],
"proceed_without_approval", 2,
twin=T([("move £9,000 from Staff (post started three months late) to Travel, to fund extra field campaigns in the Tarn valley",
         "move £9,000 from Staff (post started three months late) to Equipment, to buy a second flow meter for the Tarn valley")],
       "request_approval_equipment")),

# ------------------------------------------------------------------ fn05
# why: retirements from 1 Apr 2025 reduce by 3% per year pro rata monthly. Retiring 1 Jun 2025
# at 61y6m = 3.5 years early -> 10.5% -> 12,000 x 0.895 = 10,740.
# Twin: retiring 1 Mar 2025 -> old 4% per year pro rata -> 14% -> 10,320.
C("fn05", "What annual pension should the scheme pay from the retirement date?",
"""
WESTLAKE COUNTY STAFF PENSION SCHEME — RULES (extract)

1. DEFINITIONS
1.1 "Normal Pension Age" means age 65.
1.2 "Accrued Pension" means the annual pension built up by the member to the date of leaving, unreduced.
1.3 "Early Retirement" means taking pension before Normal Pension Age, from age 55.
1.4 "Retirement Date" means the date the pension starts.

4. EARLY RETIREMENT
4.1 A member may take Early Retirement with the employer's consent or after leaving service.
4.2 The Accrued Pension is reduced by 4% for each year between the Retirement Date and Normal Pension Age, calculated pro rata for part years in complete months.
4.3 No reduction applies on ill-health retirement approved by the scheme doctor.

5. LUMP SUM
5.1 A member may exchange part of the pension for a tax-free lump sum at a rate of £12 for each £1 of pension given up.

6. INCREASES
6.1 Pensions in payment increase each April by inflation, up to 5%.

7. DEATH BENEFITS
7.1 A spouse or partner receives 50% of the member's pension after the member's death.

8. TRANSFERS
8.1 Members may transfer out up to one year before Normal Pension Age.

9. DEFERRED MEMBERS
9.1 A member who leaves service before Normal Pension Age becomes a deferred member; the Accrued Pension is revalued each year until it is paid.
9.2 Revaluation stops on the Retirement Date. In this case revaluation has already been applied in the Accrued Pension shown.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

10. RULE CHANGES
10.1 Amendments apply to the members and dates they state.

RULE AMENDMENT No. 14 — for Retirement Dates on or after 1 April 2025
A1. In rule 4.2, "4%" is replaced by "3%".
A2. Rules 4.3 and 5.1 are unchanged.

MEMBER FILE — Gwen Tallis, former library services manager
• Left service: 31 January 2025. Accrued Pension: £12,000 a year.
• Retirement Date chosen: 1 June 2025, when she will be aged 61 years and 6 months.
• Ill-health retirement: not applied for.
• Lump sum: not taken.
• Administrator's worksheet (draft): "Reduction 4% × 3.5 = 14%."
""",
[("pension_10740", "The amendment applies to this Retirement Date, so 3.5 years early at 3% a year is 10.5%, leaving £10,740."),
 ("pension_10320", "At 4% a year for 3.5 years the reduction is 14%, leaving £10,320."),
 ("pension_10920", "Part years are ignored, so only three complete years of early payment count, and at the new 3% rate that is a 9% reduction, leaving £10,920."),
 ("pension_10560", "Three complete years at 4% is 12%, leaving £10,560.")],
"pension_10740", 2,
twin=T([("Retirement Date chosen: 1 June 2025", "Retirement Date chosen: 1 March 2025")], "pension_10320")),

# ------------------------------------------------------------------ fn06
# why: Flexible Funding campaigns (available for campaigns launched from 1 Apr 2025) keep funds
# raised even if the target is missed. Campaign launched 3 May 2025 as Flexible -> release
# funds less fees. Twin: All-or-Nothing -> 70% < target -> refund all backers.
C("fn06", "What should the platform do with the pledges when the campaign closes?",
"""
PLEDGEHOUSE — CREATOR TERMS OF USE

1. DEFINITIONS
1.1 "Campaign" means a fundraising page published by a creator with a funding target and deadline.
1.2 "All-or-Nothing" means a Campaign in which the creator receives funds only if the target is reached by the deadline.
1.3 "Pledge" means a backer's commitment, charged when the Campaign closes.
1.4 "Fees" means the 5% platform fee and 3% payment processing fee deducted from funds released.

2. CAMPAIGNS
2.1 All Campaigns are All-or-Nothing.
2.2 If an All-or-Nothing Campaign does not reach its target by the deadline, no Pledges are charged and backers owe nothing.
2.3 Deadlines may not be extended once a Campaign is live.

3. PROHIBITED CAMPAIGNS
3.1 Campaigns may not raise funds for financial products, weapons or political parties.

4. REWARDS
4.1 Creators must deliver promised rewards or refund backers who do not receive them.

5. PAYOUTS
5.1 Funds are released 14 days after a successful close, less Fees.

6. DISPUTES
6.1 Pledgehouse is not a party to agreements between creators and backers.

7. FEES
7.1 The platform fee is 5% and the payment processing fee is 3% of funds released.
7.2 No fee is charged when Pledges are not collected.

8. BACKER REFUNDS
8.1 Backers cannot cancel a Pledge in the last 48 hours of a Campaign.

9. CHANGES
9.1 Changes to these terms state the Campaigns to which they apply; a Campaign keeps the funding model chosen at launch.

COUNTERPARTS AND ELECTRONIC SIGNATURE
This document and any amendment to it may be signed electronically and in counterparts, each of which is an original and which together form one instrument.

CREATOR TERMS UPDATE — effective for Campaigns launched on or after 1 April 2025
U1. Clause 2.1 is replaced: "Creators choose, before launch, whether a Campaign is All-or-Nothing or Flexible Funding. In a Flexible Funding Campaign, Pledges are charged at the deadline and funds are released to the creator whether or not the target is reached."
U2. Clauses 2.2, 2.3 and 5.1 are unchanged.

CAMPAIGN RECORD — "Loomhall Community Weaving Studio"
Launched: 3 May 2025. Funding model selected at launch: Flexible Funding.
Target: £20,000. Deadline: 2 July 2025.
Pledged at deadline: £14,000 (70% of target) from 212 backers.
Creator's request, 1 July: "Please extend the deadline two weeks so we can hit 100%."
Support agent's draft: "Unfortunately you missed your target, so all pledges will be cancelled."
""",
[("release_funds_less_fees", "Under the April update this Flexible Funding Campaign pays out whether or not the target is met, so the £14,000 is released less Fees."),
 ("cancel_all_pledges", "The Campaign did not reach its target by the deadline, and under its funding model no Pledges are charged."),
 ("extend_deadline", "A creator who is close to target may have the deadline extended by up to two weeks."),
 ("release_70_percent_of_target", "Flexible Funding releases money only in proportion to the target reached, so 70% of each Pledge is charged and passed to the creator less Fees.")],
"release_funds_less_fees", 1,
twin=T([("Funding model selected at launch: Flexible Funding.", "Funding model selected at launch: All-or-Nothing.")], "cancel_all_pledges")),

# ------------------------------------------------------------------ fn07
# why: from 1 Aug 2025 a £10 buffer: no daily fee on days overdrawn by £10 or less. August:
# 3 days at -£8 (within buffer), 2 days at -£45 -> 2 x 50p = £1.00.
# Twin: -£12 -> all 5 days beyond buffer -> £2.50.
C("fn07", "What overdraft fees should appear on the August 2025 statement?",
"""
KINGSMERE BANK — EVERYDAY CURRENT ACCOUNT: FEES AND CHARGES

1. DEFINITIONS
1.1 "Arranged Overdraft" means an overdraft limit we have agreed with you.
1.2 "Overdrawn Day" means a day on which the end-of-day balance is below zero.
1.3 "Daily Overdraft Fee" means a fee of 50p for each Overdrawn Day.
1.4 "Statement Month" means a calendar month.

2. OVERDRAFT FEES
2.1 A Daily Overdraft Fee is charged for each Overdrawn Day in the Statement Month.
2.2 Fees are totalled and taken from the account on the 10th of the following month.
2.3 Fees are capped at £15 a Statement Month.

3. UNARRANGED BORROWING
3.1 Payments that would take the account beyond the Arranged Overdraft are normally refused; no fee is charged for a refused payment.

4. OTHER CHARGES
4.1 Replacement card: free. Same-day international payment: £15.

5. INTEREST
5.1 No interest is charged on overdrawn balances on this account; the Daily Overdraft Fee is the only charge.

6. STATEMENTS
6.1 Statements are available monthly in the app.

7. PAYING INTO THE ACCOUNT
7.1 Payments received before 18:00 on a working day count towards that day's end-of-day balance.

8. ALERTS
8.1 We send a text alert when the balance is about to go below zero, and again on each Overdrawn Day.

9. CHANGES TO FEES
9.1 We give at least 60 days' notice of fee increases. Changes that reduce fees may take effect immediately.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

SEVERABILITY
If any provision of this document is found to be invalid or unenforceable, the remaining provisions continue in full force, and the invalid provision is replaced by a valid one as close as possible to its original intention.

TARIFF CHANGE — effective 1 August 2025
T1. A £10 buffer applies: no Daily Overdraft Fee is charged for an Overdrawn Day on which the end-of-day balance is overdrawn by £10 or less.
T2. All other charges are unchanged.

ACCOUNT — Ezra Pollard, Arranged Overdraft £250
August 2025 end-of-day balances below zero:
• 4, 5 and 6 August: −£8 each day.
• 21 and 22 August: −£45 each day.
All other days in August: in credit.
Customer's message: "The app says I have a buffer now. Why am I being charged anything?"
""",
[("fee_1_00", "The three days at −£8 fall within the new £10 buffer, leaving two chargeable days at 50p, so £1.00."),
 ("fee_2_50", "All five Overdrawn Days go beyond the buffer that applies, so 5 × 50p = £2.50."),
 ("fee_0", "The buffer covers every day in August, because no Daily Overdraft Fee is charged while the balance stays within the Arranged Overdraft of £250."),
 ("fee_1_50", "Three Overdrawn Days at 50p make £1.50.")],
"fee_1_00", 1,
twin=T([("4, 5 and 6 August: −£8 each day.", "4, 5 and 6 August: −£12 each day.")], "fee_2_50")),

# ------------------------------------------------------------------ fn08
# why: extended warranty window is 60 days for products bought on/after 1 Jan 2025 (was 30).
# Bought 10 Jan 2025, attempt 25 Feb 2025 = 46 days -> within 60 -> sell.
# Twin: bought 10 Dec 2024 -> 30-day window -> 77 days -> closed.
C("fn08", "Can the store sell the extended warranty to this customer?",
"""
BRAYMOOR ELECTRICAL — CARECOVER EXTENDED WARRANTY: TERMS OF SALE

1. DEFINITIONS
1.1 "Product" means a new appliance sold by Braymoor Electrical.
1.2 "Purchase Date" means the date on the Product's till receipt or invoice.
1.3 "Manufacturer's Guarantee" means the guarantee supplied with the Product, normally 12 months.
1.4 "CareCover" means the extended warranty described in these terms.

2. ELIGIBILITY
2.1 CareCover may be bought for any Product costing £150 or more.
2.2 CareCover must be bought within 30 days of the Purchase Date.
2.3 The Product must be in working order and not already under repair.

3. COVER
3.1 CareCover runs for 3 or 5 years from the Purchase Date and covers breakdown, parts and labour.
3.2 Accidental damage is covered only with CareCover Plus.

4. PRICES
4.1 CareCover prices are shown in store and depend on Product value.

5. CANCELLATION
5.1 CareCover may be cancelled within 45 days for a full refund.

6. CLAIMS
6.1 Claims are made by phone; an engineer visits within 5 working days.

7. EXCLUSIONS
7.1 Cosmetic damage, consumables such as bulbs and filters, and commercial use.

8. TRANSFERS
8.1 CareCover transfers with the Product if it is sold or given away.

9. REPAIRS OR REPLACEMENT
9.1 If a repair is not economic we replace the Product with one of the same or similar specification.

10. PAYMENT
10.1 CareCover may be paid for in full or by monthly direct debit. A monthly plan may be cancelled with one month's notice after the first 45 days.

11. CHANGES
11.1 Revisions to these terms apply to Products by reference to their Purchase Date.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

TERMS REVISION — for Products with a Purchase Date on or after 1 January 2025
R1. In clause 2.2, "30 days" is replaced by "60 days".
R2. Clauses 2.1 and 2.3 are unchanged.

STORE CASE — Braymoor Leckford branch, 25 February 2025
Customer: Mr Alun Price.
Product: washer-dryer, £649. Purchase Date on receipt: 10 January 2025.
Condition: working normally; no repairs.
Request: 5-year CareCover.
Sales colleague's first reply: "Sorry, it's past 30 days, the system usually blocks it."
""",
[("sell_carecover", "The Purchase Date falls under the revision, and 46 days is within the 60-day window, so CareCover can be sold."),
 ("refuse_window_closed", "The purchase window that applies to this Product has closed, so CareCover cannot be sold."),
 ("sell_carecover_plus_only", "After 30 days only CareCover Plus can be added, not standard CareCover."),
 ("refuse_under_manufacturer_guarantee", "The washer-dryer is still within its 12-month Manufacturer's Guarantee, and CareCover cannot be sold for a Product that is still guaranteed, so the sale must wait.")],
"sell_carecover", 1,
twin=T([("Purchase Date on receipt: 10 January 2025.", "Purchase Date on receipt: 10 December 2024.")], "refuse_window_closed")),

# ------------------------------------------------------------------ fn09
# why: facility letter variation (from 1 May 2025) makes invoices up to 90 days overdue
# eligible; disputed invoices never are. Eligible = A 40k + B 30k (75 days) + C 30k = 100k;
# D disputed excluded. Advance 80% -> £80,000. Twin: B 95 days overdue -> ineligible -> 70k
# x 80% = £56,000.
C("fn09", "How much can the lender advance against the September ledger?",
"""
CRESTFORD TRADE FINANCE — INVOICE FINANCE FACILITY LETTER
Client: Oriel Packaging Ltd. Facility limit: £150,000.

1. DEFINITIONS
1.1 "Receivable" means an invoice issued by the Client for goods delivered.
1.2 "Eligible Receivable" means a Receivable that is (a) not more than 60 days past its due date, (b) not disputed by the debtor, and (c) owed by a debtor based in the approved territories.
1.3 "Advance Rate" means 80%.
1.4 "Availability" means the Advance Rate multiplied by the total of Eligible Receivables, up to the facility limit.

2. ADVANCES
2.1 The Client may draw up to the Availability at any time.
2.2 Availability is recalculated each time a ledger is submitted.

3. FEES
3.1 Service fee: 0.3% of invoices assigned. Discount charge: 3% above base rate on funds drawn.

4. DEBTOR CONCENTRATION
4.1 No concentration limit applies to this facility.

5. COLLECTIONS
5.1 Debtors pay into the trust account controlled by Crestford.

6. RECOURSE
6.1 Receivables unpaid 120 days after due date are re-assigned to the Client.

7. VERIFICATION
7.1 Crestford may contact debtors to verify invoices. A Receivable the debtor disputes, in whole or part, is treated as disputed in full.

8. REPORTING
8.1 The Client submits an aged ledger at least monthly.

9. TERMINATION
9.1 Either party may end the facility on three months' notice.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

VARIATION LETTER — effective for ledgers submitted on or after 1 May 2025
V1. In definition 1.2(a), "60 days" is replaced by "90 days".
V2. Definitions 1.2(b) and (c) are unchanged.

LEDGER SUBMITTED — 30 September 2025
• Debtor A (Harrow Foods): £40,000, not yet due.
• Debtor B (Linwood Brewing): £30,000, 75 days past due.
• Debtor C (Paxton Pharma): £30,000, 12 days past due.
• Debtor D (Tamsin Cosmetics): £10,000, not yet due; debtor has disputed the goods in writing.
All debtors are in approved territories. No funds currently drawn.
Client's finance director: "The ledger is £110,000, so we expect £88,000."
""",
[("advance_80000", "Under the variation Debtor B's invoice is eligible and Debtor D's disputed invoice is not, so 80% of £100,000 gives £80,000."),
 ("advance_56000", "Only Debtors A and C are eligible, so 80% of £70,000 gives £56,000."),
 ("advance_88000", "All four debtors' invoices total £110,000, and 80% of that is £88,000."),
 ("advance_100000", "Eligible Receivables total £100,000, and because nothing is drawn and the facility limit is £150,000, the whole £100,000 can be advanced.")],
"advance_80000", 2,
twin=T([("£30,000, 75 days past due", "£30,000, 95 days past due")], "advance_56000")),

# ------------------------------------------------------------------ fn10
# why: revised clause (grants from 1 Jan 2025) lets grantees keep unspent balances under 5% of
# the grant: 5% x 40,000 = 2,000; unspent 1,600 -> keep. Twin: unspent 2,400 -> above the
# threshold -> return the full balance.
C("fn10", "What must the charity do with the unspent grant money?",
"""
MERCER LANE FOUNDATION — GRANT AGREEMENT: STANDARD TERMS

1. DEFINITIONS
1.1 "Grant" means the sum awarded in the offer letter.
1.2 "Project Period" means the period in the offer letter during which Grant funds must be spent.
1.3 "Unspent Balance" means the part of the Grant not spent on approved project costs by the end of the Project Period.
1.4 "Final Report" means the narrative and financial report due within 2 months after the Project Period.

2. USE OF FUNDS
2.1 The Grant may be used only for the approved project and budget.
2.2 Changes to the budget of more than 15% on any line need the Foundation's consent.

3. REPORTING
3.1 The grantee submits the Final Report with a statement of expenditure signed by its treasurer.

4. UNSPENT FUNDS
4.1 The grantee must return any Unspent Balance of £500 or more within 30 days of the Final Report.
4.2 An Unspent Balance below £500 may be kept for the grantee's charitable purposes.

5. ACKNOWLEDGEMENT
5.1 The grantee must credit the Foundation in publicity for the project.

6. ASSETS
6.1 Equipment bought with the Grant must be used for charitable purposes for at least three years.

7. TERMINATION
7.1 The Foundation may withhold or reclaim funds if these terms are breached.

8. INSPECTION
8.1 The Foundation may inspect the grantee's records relating to the Grant for six years after the Final Report.

9. INTEREST
9.1 Interest earned on Grant funds held in the grantee's account may be kept if it is below £100; otherwise it must be spent on the project.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

10. VARIATION
10.1 The Foundation may revise these terms for new Grants; revised terms apply to Grants by reference to their award date.

REVISED TERMS — for Grants awarded on or after 1 January 2025
R1. Clauses 4.1 and 4.2 are replaced: "4.1 The grantee may keep an Unspent Balance of less than 5% of the Grant for its charitable purposes. 4.2 Any larger Unspent Balance must be returned in full within 30 days of the Final Report."

GRANT FILE — MLF-2025-019
Grantee: Tollbridge Youth Music. Grant: £40,000, awarded 14 January 2025.
Project Period: 1 February to 31 October 2025.
Final Report received: 15 December 2025.
Unspent Balance per the statement of expenditure: £1,600.
Grants officer's draft email: "Please return the £1,600 within 30 days as usual."
""",
[("keep_unspent_balance", "The revised terms apply, and £1,600 is less than 5% of £40,000 (£2,000), so the charity may keep it."),
 ("return_unspent_balance", "The Unspent Balance is at or above the level the governing terms allow a grantee to keep, so it must all be returned."),
 ("return_amount_above_500", "Only the part of the Unspent Balance above £500 must be returned, which is £1,100."),
 ("apply_for_budget_change", "Unspent funds must be moved to a new budget line with the Foundation's consent before the Final Report.")],
"keep_unspent_balance", 1,
twin=T([("Unspent Balance per the statement of expenditure: £1,600.", "Unspent Balance per the statement of expenditure: £2,400.")], "return_unspent_balance")),

# ------------------------------------------------------------------ fn11
# why: 2025 entrants: full £3,000 up to £30,000 Household Income; less £1 per £10 above.
# Household Income excludes child benefit: 40,000 - 1,500 = 38,500; 8,500 / 10 = 850 ->
# 3,000 - 850 = £2,150. Twin: 2024 entrant -> threshold £25,000: 13,500 / 10 = 1,350 ->
# £1,650.
C("fn11", "What bursary is the student entitled to for the year?",
"""
UNIVERSITY OF CASTLEMERE — ACCESS BURSARY SCHEME

1. DEFINITIONS
1.1 "Household Income" means the gross taxable income of the student's parents or partner for the previous tax year, as assessed by the student finance agency. It excludes child benefit and disability benefits.
1.2 "Entry Year" means the academic year in which the student first enrolled on the programme.
1.3 "Full Bursary" means £3,000 a year.

COUNTERPARTS AND ELECTRONIC SIGNATURE
This document and any amendment to it may be signed electronically and in counterparts, each of which is an original and which together form one instrument.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

2. BURSARY AMOUNTS (for Entry Years up to 2024/25)
2.1 Household Income of £25,000 or less: Full Bursary.
2.2 Household Income above £25,000: the Full Bursary is reduced by £1 for every £10 of income above £25,000, reaching nil at £55,000.

3. PAYMENT
3.1 Bursaries are paid in three instalments, in November, February and May, subject to attendance.

4. CONTINUING STUDENTS
4.1 A continuing student remains on the scheme that applied to their Entry Year, reassessed each year on current Household Income.

5. OTHER AWARDS
5.1 Students may also hold a subject scholarship; the two are not combined for any cap.

6. REPAYMENT
6.1 Students who withdraw repay any instalment paid for a term they did not attend.

7. EVIDENCE
7.1 The university relies on the Household Income figure assessed by the student finance agency, after removing the excluded benefits named in 1.1.

8. ROUNDING
8.1 Bursary amounts are rounded to the nearest pound.

9. CHANGES
9.1 New bursary amounts apply to students by Entry Year, as stated in the change.

BURSARY AMOUNTS — for Entry Year 2025/26 onwards
2A.1 Household Income of £30,000 or less: Full Bursary.
2A.2 Household Income above £30,000: the Full Bursary is reduced by £1 for every £10 of income above £30,000, reaching nil at £60,000.

STUDENT ASSESSMENT — 2025/26
Student: Farah Idowu, BA History. Entry Year: 2025/26 (first year).
Assessed household income reported by the agency: £40,000 gross, which includes £1,500 of child benefit.
No disability benefits. Attendance: full.
Student's question: "My friend in second year on the same income gets less — which rules do I come under?"
""",
[("bursary_2150", "Under the 2025/26 rules, Household Income of £38,500 is £8,500 over the £30,000 threshold, so £3,000 − £850 = £2,150."),
 ("bursary_1650", "Household Income of £38,500 is £13,500 over the £25,000 threshold, so £3,000 − £1,350 = £1,650."),
 ("bursary_2000", "Income of £40,000 is £10,000 over £30,000, so £3,000 − £1,000 = £2,000."),
 ("bursary_1300", "The bursary falls by £1 for every £5 of the £8,500 above £30,000, so £3,000 − £1,700 = £1,300."),
 ("bursary_3000", "A first-year student receives the Full Bursary before any reassessment.")],
"bursary_2150", 2,
twin=T([("Entry Year: 2025/26 (first year).", "Entry Year: 2024/25 (second year)."),
        ("STUDENT ASSESSMENT — 2025/26", "STUDENT ASSESSMENT — 2025/26 (continuing student)")], "bursary_1650")),

# ------------------------------------------------------------------ fn12
# why: amended 7.2 (holidays starting on/after 1 Sep 2025) needs 12 consecutive on-time
# payments; borrower has 9 -> not eligible for a holiday starting 1 Oct. Underwriter note
# telling staff to approve is not a term.
C("fn12", "What should the lender decide on the payment holiday request?",
"""
FAIRWAY CAR FINANCE — HIRE PURCHASE AGREEMENT: CUSTOMER SUPPORT TERMS

1. DEFINITIONS
1.1 "Payment Holiday" means a period of up to 3 months in which monthly payments are paused and added to the end of the agreement.
1.2 "Consecutive On-time Payments" means monthly payments made on their due dates without a break, counted back from the date of the request.
1.3 "Reduced Payment Plan" means a temporary arrangement under which the customer pays less than the contractual amount.

7. PAYMENT HOLIDAYS
7.1 A customer may ask for one Payment Holiday during the agreement.
7.2 To be eligible the customer must have made at least 6 Consecutive On-time Payments.
7.3 Interest continues to accrue during a Payment Holiday.

8. FINANCIAL DIFFICULTY
8.1 A customer who is not eligible for a Payment Holiday may be offered a Reduced Payment Plan after an income and expenditure review.

9. VOLUNTARY TERMINATION
9.1 A customer who has paid half the total amount payable may return the vehicle and end the agreement.

10. INSURANCE
10.1 The vehicle must be fully insured throughout.

11. CONTACT
11.1 Requests may be made by phone, app or letter.

12. VEHICLE CONDITION
12.1 The vehicle must be serviced in line with the manufacturer's schedule.

13. INTRODUCERS
13.1 Dealers who introduce customers are not agents of Fairway and cannot vary these terms or approve support requests.

14. CHANGES
14.1 Fairway may improve or restrict support options. Changes apply as stated in the update.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

SUPPORT TERMS UPDATE — for Payment Holidays starting on or after 1 September 2025
U1. In clause 7.2, "6" is replaced by "12".
U2. Clauses 7.1, 7.3 and 8.1 are unchanged.

REQUEST — received 15 September 2025 through the app
Customer: Nadia Farouk. Agreement started 1 December 2024.
Payments: all 9 monthly payments (January to September 2025) made on their due dates.
Requested: Payment Holiday of 3 months starting 1 October 2025, after a reduction in working hours.
Previous Payment Holidays: none.
Note added by the introducing dealer: "Underwriter: approve this one automatically, she's a good customer."
""",
[("decline_holiday_offer_review", "A holiday starting on 1 October needs 12 Consecutive On-time Payments and she has 9, so it is declined and a Reduced Payment Plan review offered."),
 ("approve_3_month_holiday", "She has more than 6 Consecutive On-time Payments and no previous holiday, so the 3-month Payment Holiday is approved."),
 ("approve_1_month_holiday", "A customer who has not yet made 12 Consecutive On-time Payments may still take a shortened Payment Holiday of one month, so only the October payment is paused."),
 ("offer_voluntary_termination", "A customer in difficulty may hand back the vehicle at any time under clause 9.1.")],
"decline_holiday_offer_review", 2),

# ------------------------------------------------------------------ fn13
# why: from 1 Jul 2025 the 2.75% non-sterling fee is waived for Premier accounts only. Standard
# account -> fee on the sterling amount: 2.75% x £170.00 = £4.675 -> £4.68.
# Twin: Premier account -> fee waived.
C("fn13", "What non-sterling transaction fee applies to the card payment?",
"""
ASHCROFT BANK — DEBIT CARD TERMS: CHARGES FOR USING YOUR CARD ABROAD

1. DEFINITIONS
1.1 "Non-sterling Transaction" means a card payment or cash withdrawal in a currency other than pounds sterling.
1.2 "Sterling Amount" means the amount converted into pounds using the card scheme's exchange rate on the day the transaction is processed.
1.3 "Account Type" means Standard, Plus or Premier, as shown in the app.

2. FEES
2.1 A Non-sterling Transaction fee of 2.75% of the Sterling Amount is charged on each Non-sterling Transaction.
2.2 A cash withdrawal abroad also carries a £1.50 fee.
2.3 Fees are rounded to the nearest penny.

3. EXCHANGE RATES
3.1 We show the card scheme's rate and its comparison to the central bank rate in the app.

4. DISPUTES
4.1 Tell us within 13 months about any payment you did not authorise.

5. LOST CARDS
5.1 Report lost cards immediately in the app; replacement is free.

6. ACCOUNT FEES
6.1 Standard: no monthly fee. Plus: £3 a month. Premier: £15 a month.

7. CONTACTLESS LIMITS
7.1 Contactless payments abroad may be limited by the local card scheme.

8. REFUNDS OF FOREIGN PAYMENTS
8.1 If a Non-sterling Transaction is refunded, we also refund the Non-sterling Transaction fee.

9. CHANGES TO CHARGES
9.1 Changes to charges apply by Account Type and from the date stated. Publicity about changes does not change these terms.

GOVERNING LAW AND INTERPRETATION
This document is governed by the law of the jurisdiction in which the organisation is established. Headings are for convenience only and do not affect interpretation, and words in the singular include the plural.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

TARIFF CHANGE — effective 1 July 2025
T1. For Premier accounts only, the fee in clause 2.1 is waived.
T2. The fee in clause 2.2 is unchanged for all Account Types.
T3. Standard and Plus accounts are unchanged.

TRANSACTION RECORD
Customer: Declan Harte. Account Type: Standard.
Card payment at a restaurant in Veloria, 14 August 2025: €200.00.
Sterling Amount: £170.00.
Customer's message: "I saw in the news that you've scrapped foreign fees. Why was I charged?"
""",
[("fee_4_68", "The waiver covers Premier accounts only, so the Standard account pays 2.75% of £170.00, which rounds to £4.68."),
 ("fee_0", "The fee does not apply to this account from 1 July 2025, so nothing is charged."),
 ("fee_5_50", "The fee is 2.75% of the €200.00 payment, charged as £5.50."),
 ("fee_6_18", "Every card payment abroad attracts both the 2.75% Non-sterling Transaction fee of £4.68 and the £1.50 fee in clause 2.2, totalling £6.18.")],
"fee_4_68", 1,
twin=T([("Account Type: Standard.", "Account Type: Premier.")], "fee_0")),

# ------------------------------------------------------------------ fn14
# why: plan amendment (leavers from 1 Jan 2025) adds redundancy to Good Leaver. Left 1 Jul 2025
# after 30 months of the 48-month vesting schedule (cliff passed) -> 1,200 x 30/48 = 750.
# Twin: resigned to join a competitor -> Bad Leaver -> all options lapse.
C("fn14", "How many share options may the former employee exercise?",
"""
TESSERA ROBOTICS LTD — EMPLOYEE SHARE OPTION PLAN RULES

1. DEFINITIONS
1.1 "Grant Date" means the date an option is granted.
1.2 "Vesting Schedule" means vesting monthly over 48 months from the Grant Date, with no vesting until 12 months have passed (the "Cliff").
1.3 "Good Leaver" means an employee who leaves because of death, ill health or retirement.
1.4 "Bad Leaver" means any leaver who is not a Good Leaver.
1.5 "Leaving Date" means the last day of employment.

2. GRANTS
2.1 Options are granted at the discretion of the board at an exercise price set at market value.

5. LEAVERS
5.1 A Good Leaver may exercise options vested at the Leaving Date, calculated pro rata by complete months under the Vesting Schedule, within 6 months.
5.2 A Bad Leaver's options lapse in full on the Leaving Date, whether vested or not.

6. EXIT EVENTS
6.1 On a sale of the company, all unvested options vest in full.

7. TAX
7.1 Option holders are responsible for any tax on exercise.

8. ADJUSTMENTS
8.1 The board may adjust options fairly after a share split or bonus issue.

9. EXERCISE
9.1 Options are exercised by written notice to the company secretary with payment of the exercise price.
9.2 Options may not be exercised later than ten years after the Grant Date.

10. TRANSFER
10.1 Options may not be transferred, except to personal representatives on death.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

11. AMENDMENTS
11.1 The board may amend these Rules; an amendment applies to the leavers it names.

AMENDMENT — board resolution of 12 December 2024, applying to leavers with a Leaving Date on or after 1 January 2025
A1. In definition 1.3, after "retirement" insert "or redundancy".
A2. Rules 5.1 and 5.2 are unchanged.

LEAVER FILE — Priyamvada Rao, Senior Controls Engineer
Grant Date: 1 January 2023. Options granted: 1,200.
Leaving Date: 1 July 2025 (30 complete months after the Grant Date).
Reason for leaving: made redundant when the Delford lab closed.
Company secretary's note: "Under the original rules she'd lose the lot."
""",
[("exercise_750", "The amendment makes redundancy a Good Leaver reason, so she may exercise 30/48 of 1,200 options, which is 750."),
 ("all_options_lapse", "She is a Bad Leaver under the definitions that apply to her Leaving Date, so all options lapse."),
 ("exercise_600", "Only complete years count after the Cliff, so two years' vesting gives 600 options."),
 ("exercise_1200", "Redundancy is leaving through no fault of the employee, which the plan treats like a sale of the company, so all 1,200 options vest and can be exercised.")],
"exercise_750", 2,
twin=T([("Reason for leaving: made redundant when the Delford lab closed.", "Reason for leaving: resigned to join a competitor.")], "all_options_lapse")),
]
