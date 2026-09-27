"""proc_temporal / fees: tiered tariffs, pro-rated refunds and charges, statutory
interest, parking and hire tariffs, commissions, cancellation schedules, duties
and filing fees (Ashcombe Water, Pellham Leisure Trust, Garrow & Finch, Tyneside
Quay car parks, Lumen Desk, Oriel Hall, Corvane Freight and others)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ fe01
# why: block tariff, marginal. Usage 31 m3: 10 x 1.20 = 12.00; 15 x 1.85 = 27.75;
# 6 x 2.60 = 15.60 -> 55.35. Period begins 15 Jun (before 1 Jul) -> old tier-3 rate.
# Twin: period begins 15 Jul -> tier 3 = 2.90 -> 6 x 2.90 = 17.40 -> 57.15.
C("fe01", "What volumetric charge should appear on this water bill?",
"""
Ashcombe Water — Domestic Metered Tariff 2026/27

Section 1 — Volumetric charge (per billing period)
Block 1: the first 10 m³ at 1.20 per m³
Block 2: the next 15 m³ (above 10 and up to 25 m³) at 1.85 per m³
Block 3: all use above 25 m³ at 2.60 per m³
Each block rate applies only to the water that falls within that block.

Section 2 — Standing charge: 0.31 per day (shown separately on the bill; not part of the volumetric charge).

Tariff notice TN-7 (issued 2 May 2026): for billing periods beginning on or after 1 July 2026, the Block 3 rate is 2.90 per m³. Blocks 1 and 2 are unchanged.

Customer account 7710-44-209 — 19 Gorse Hill, Ashcombe
Billing period: 15 June 2026 to 14 July 2026
Meter reads: 4,412 m³ (start) → 4,443 m³ (end); usage 31 m³
Customer's query: "My neighbour says all of it goes on the top rate once you pass 25. Is my bill going to be over 80?"
""",
[("charge_55_35", "The period began before 1 July, so Block 3 is 2.60: 10 × 1.20 + 15 × 1.85 + 6 × 2.60."),
 ("charge_57_15", "The period began on or after 1 July, so Block 3 is 2.90: 10 × 1.20 + 15 × 1.85 + 6 × 2.90."),
 ("charge_80_60", "Once use passes 25 m³ every cubic metre is charged at the Block 3 rate: 31 × 2.60."),
 ("charge_50_85", "The first 10 m³ are at 1.20 and everything above is Block 2: 10 × 1.20 + 21 × 1.85.")],
"charge_55_35", 2,
twin=T([("Billing period: 15 June 2026 to 14 July 2026", "Billing period: 15 July 2026 to 13 August 2026")], "charge_57_15")),

# ------------------------------------------------------------------ fe02
# why: membership months start on the 1st; a month counts as used once any day of it
# has begun. Start 1 Feb 2026; cancel 10 Jun -> Feb-Jun = 5 used -> 7 unused x $40
# (480/12) = 280 - 30 admin = 250. Twin: cancel 31 May -> 4 used -> 8 x 40 = 320 - 30 = 290.
C("fe02", "What refund is due on this cancelled annual membership?",
"""
Pellham Leisure Trust — Membership Conditions (from 1 January 2026)

M4. Annual membership costs $480, paid in advance, for 12 membership months. A membership month runs from the 1st to the last day of a calendar month.
M5. On cancellation, the member is refunded $40 for each unused membership month, minus a $30 administration fee.
M6. A membership month counts as used once any day of it has begun, whether or not the member visited.
M7. Freezes and transfers are covered in M9–M12.

Old website FAQ (archived 2024, still indexed by search engines): "No refunds after 90 days of membership."

Member record PLT-11-8804
Name: Harriet Caulfield
Membership start: 1 February 2026 (annual, paid $480)
Cancellation received: 10 June 2026 (in person, signed form)
Visits since April: 0
Member's note: "I haven't been since March, so I've really only used two months."
""",
[("refund_250", "Five membership months, February to June, had begun by the cancellation date, leaving 7 unused: 7 × $40 − $30."),
 ("refund_290", "Four membership months, February to May, had begun by the cancellation date, leaving 8 unused: 8 × $40 − $30."),
 ("refund_280", "Seven months are unused at $40 each, and no other amount is taken off."),
 ("refund_none", "The membership is more than 90 days old, so no refund is due.")],
"refund_250", 2,
twin=T([("Cancellation received: 10 June 2026", "Cancellation received: 31 May 2026")], "refund_290")),

# ------------------------------------------------------------------ fe03
# why: interest 8%/yr simple, daily, 365-day basis on 18,250 = 4.00/day, from the day
# after due date to payment date inclusive: 1 May-15 Jun = 31 + 15 = 46 days -> 184.00;
# plus fixed recovery charge 70 (debt 10,000-99,999.99) -> 254.00.
# Twin: paid 14 Jun -> 45 days -> 180 + 70 = 250.00.
C("fe03", "What late-payment amount should credit control claim on this invoice?",
"""
Garrow & Finch Timber — Standard Terms of Sale, clause 14 (Late payment)

14.1 Interest on overdue sums runs at 8% per year, simple, calculated daily on a 365-day year.
14.2 Interest runs from the day after the due date up to and including the date payment is received.
14.3 In addition, a fixed recovery charge is claimed once per invoice:
     debt under 1,000.00: 40; debt 1,000.00 to 9,999.99: 55; debt 10,000.00 to 99,999.99: 70; debt of 100,000.00 or more: 100.
14.4 Partial payments reduce the balance on the day they are received.

Invoice GF-26-03117 — customer: Wendlebury Joinery Co.
Invoice amount: 18,250.00
Due date: 30 April 2026
Partial payments: none
Payment received in full: 15 June 2026

Credit controller's draft: "Overdue 45 days, 4.00 a day = 180.00. Customer is a long-standing account; I'd skip the recovery charge."
(No clause lets staff waive the recovery charge.)
""",
[("claim_254_00", "Interest runs 1 May to 15 June inclusive, 46 days at 4.00 a day, plus the 70 recovery charge."),
 ("claim_250_00", "Interest runs 1 May to 14 June inclusive, 45 days at 4.00 a day, plus the 70 recovery charge."),
 ("claim_184_00", "Interest is 46 days at 4.00 a day, and the recovery charge can be left out for a long-standing account."),
 ("claim_258_00", "Interest runs from the due date itself to the payment date, 47 days at 4.00 a day, plus the 70 recovery charge.")],
"claim_254_00", 2,
twin=T([("Payment received in full: 15 June 2026", "Payment received in full: 14 June 2026")], "claim_250_00")),

# ------------------------------------------------------------------ fe04
# why: stay > 30 min -> charged from entry at 2.00 per started hour. 08:50-14:05 =
# 5 h 15 min -> 6 started hours -> 12.00 (below 14 daily max).
# Twin: exit 13:45 -> 4 h 55 min -> 5 started hours -> 10.00.
C("fe04", "What should the pay station charge for this stay?",
"""
Tyneside Quay Car Parks — Tariff Board, Level 2 (short stay)

T1. Stays of 30 minutes or less are free.
T2. Longer stays are charged from the time of entry at 2.00 for each hour or part of an hour. The free 30 minutes are not deducted from a longer stay.
T3. The charge for any single calendar day is capped at 14.00.
T4. Blue-badge holders park free on production of a valid badge at the office.
T5. Lost tickets are charged the daily maximum.

Pay station log, bay reader 2-A
Plate: LQ26 FNE
Entry: 08:50
Exit barrier request: 14:05, same day
Blue badge: none presented
Driver at intercom: "I was only charged for five hours last week for about the same stay — take off the free half hour."
""",
[("charge_12_00", "The stay was 5 h 15 min, which is 6 started hours at 2.00, and the free 30 minutes are not deducted."),
 ("charge_10_00", "The stay was 4 h 55 min, which is 5 started hours at 2.00."),
 ("charge_8_00", "After taking off the free 30 minutes, only full hours are charged: 4 hours at 2.00."),
 ("charge_14_00", "The stay passed 5 hours, so the daily maximum applies.")],
"charge_12_00", 1,
twin=T([("Exit barrier request: 14:05, same day", "Exit barrier request: 13:45, same day")], "charge_10_00")),

# ------------------------------------------------------------------ fe05
# why: 730/seat/yr on a 365-day term = 2.00/seat/day, charged from the add date
# inclusive to 31 Dec. Added 14 Sep: Sep 14-30 = 17, Oct 31, Nov 30, Dec 31 = 109 days
# -> 109 x 2 x 12 = 2,616. Twin: added 15 Sep -> 108 days -> 2,592.
C("fe05", "How much should the mid-term invoice for the extra seats be?",
"""
Lumen Desk — Order Form LD-2026-0418 and Master Subscription Terms (extract)

Order form
Customer: Orrin & Sable Architects
Term: 1 January 2026 to 31 December 2026 (365 days)
Price: $730 per seat per year
Seats at start: 40

Terms, clause 5 (Adding seats)
5.1 Seats added during the term are charged pro rata at the per-seat annual price divided by 365, for each day from the day the seats are added (that day included) to the last day of the term.
5.2 Seats cannot be removed during a term.
5.3 Proration is by day, not by month. Part months are not rounded up.

Admin console log
Seats added: 12, on 14 September 2026
Added by: Priya Venkataraman (customer admin)

Account manager's draft invoice note: "Let's call it 3.5 months: 12 × 730 × 3.5/12 = 2,555."
""",
[("invoice_2616", "Seats were added on 14 September; 109 days run from that day to 31 December inclusive, at $2.00 per seat per day for 12 seats."),
 ("invoice_2592", "Seats were added on 15 September; 108 days run from that day to 31 December inclusive, at $2.00 per seat per day for 12 seats."),
 ("invoice_2555", "The remaining term is about three and a half months: 12 × $730 × 3.5 / 12."),
 ("invoice_2920", "Part months are rounded up, so four months are charged: 12 × $730 × 4 / 12.")],
"invoice_2616", 2,
twin=T([("Seats added: 12, on 14 September 2026", "Seats added: 12, on 15 September 2026")], "invoice_2592")),

# ------------------------------------------------------------------ fe06
# why: event Sat 12 Dec 2026; cancellation Sun 13 Sep -> 90 days before -> ">= 90 days"
# band -> forfeit 10% of 8,400 = 840. Twin: cancelled 14 Sep -> 89 days -> 30-89 band ->
# 50% = 4,200. Email day counts as received (rule), weekend irrelevant.
C("fe06", "What cancellation charge applies to this venue booking?",
"""
Oriel Hall — Hire Agreement, Schedule 3 (Cancellation by the hirer)

3.1 The number of days' notice is the event date minus the date the cancellation is received.
3.2 Charges:
     90 days' notice or more: 10% of the hire fee
     30 to 89 days' notice: 50% of the hire fee
     fewer than 30 days' notice: 100% of the hire fee
3.3 A cancellation sent by email is received on the day it is sent, including weekends.
3.4 Deposits already paid are credited against the charge.

Booking OH-2026-1212
Hirer: Kellerman–Oduya wedding party
Event date: Saturday 12 December 2026
Hire fee: 8,400
Deposit paid: 500
Cancellation email sent: Sunday 13 September 2026, 21:47

Events manager's note: "Sent on a Sunday, so it only counts from Monday — that's 89 days. Half the fee."
""",
[("charge_840", "The cancellation came 90 days before the event, which is in the 90-days-or-more band: 10% of 8,400."),
 ("charge_4200", "The cancellation came 89 days before the event, which is in the 30 to 89 day band: 50% of 8,400."),
 ("charge_340", "10% of 8,400 is 840, and after the 500 deposit is credited only 340 remains, which is the charge."),
 ("charge_8400", "The cancellation came after the deposit deadline, so the full hire fee is payable.")],
"charge_840", 2,
twin=T([("Cancellation email sent: Sunday 13 September 2026, 21:47", "Cancellation email sent: Monday 14 September 2026, 21:47"),
        ("Sent on a Sunday, so it only counts from Monday — that's 89 days.", "Sent on the Monday, which is 89 days out.")], "charge_4200")),

# ------------------------------------------------------------------ fe07
# why: per diem 64. Travel days (departure and return) at 75% = 48; full days 64.
# Mon dep, Tue full, Wed full, Thu return -> 48 + 64 + 64 + 48 = 224. Lunch provided
# on Tue -> deduct 20% of 64 = 12.80 -> 211.20.
# Twin: no meals provided -> 224.00.
C("fe07", "What subsistence allowance should payroll pay for this trip?",
"""
Corvane Freight — Travel Subsistence Rules (UK staff), revised March 2026

P1. The daily subsistence rate is £64.
P2. The day of departure and the day of return are travel days, paid at 75% of the daily rate. Other days away are paid at 100%.
P3. If a meal is provided free (by the company, a client or a conference), deduct 20% of the daily rate for each lunch and 30% for each dinner.
P4. Breakfast included in a hotel rate is not deducted.
P5. Claims must be submitted within 30 days of return.

Claim TS-8821
Employee: Leonie Graftworth, depot audit team
Trip: Stanbury depot audit
Departure: Monday 9 March 2026, 09:00
Return: Thursday 12 March 2026, 18:00
Meals provided: lunch on Tuesday 10 March (client-provided, recorded in the visit log)
Hotel: bed and breakfast
Submitted: 16 March 2026

Claimant's calculation: "4 days × £64 = £256."
""",
[("pay_211_20", "Two travel days at £48 and two full days at £64 make £224, less £12.80 for the provided lunch."),
 ("pay_224_00", "Two travel days at £48 and two full days at £64 make £224, and no provided meals are recorded."),
 ("pay_256_00", "The trip lasted four days, each paid at the full £64 rate."),
 ("pay_243_20", "Four days at £64 make £256, less £12.80 for the provided lunch.")],
"pay_211_20", 2,
twin=T([("Meals provided: lunch on Tuesday 10 March (client-provided, recorded in the visit log)", "Meals provided: none recorded in the visit log")], "pay_224_00")),

# ------------------------------------------------------------------ fe08
# why: commission on NET sales (returns processed in the same quarter deducted).
# 134,000 - 6,000 = 128,000 -> 3% x 50,000 = 1,500; 5% x 70,000 = 3,500; 7% x 8,000 = 560
# -> 5,560. Twin: returns processed 3 Jul (next quarter) -> not deducted this quarter ->
# 134,000 -> 1,500 + 3,500 + 7% x 14,000 = 980 -> 5,980.
C("fe08", "What Q2 commission should be paid to this sales rep?",
"""
Brisa Kitchens — Sales Commission Plan 2026

C1. Commission is paid quarterly on net sales. Net sales = gross invoiced sales in the quarter, minus returns processed in the same quarter.
C2. Returns processed in a later quarter are deducted in the quarter they are processed.
C3. Rates are marginal:
    3% on net sales up to 50,000
    5% on net sales above 50,000 and up to 120,000
    7% on net sales above 120,000
C4. Q2 runs from 1 April to 30 June.

Rep: Dariusz Wennerholm, Northern region
Q2 gross invoiced sales: 134,000
Returns: one return of 6,000 (order BK-4471), processed 22 June 2026
Rep's message: "My gross puts me well into the 7% band — shouldn't all of it be at 7%?"
""",
[("pay_5560", "Net sales are 128,000 after the June return: 1,500 on the first 50,000, 3,500 on the next 70,000 and 560 on the last 8,000."),
 ("pay_5980", "The return falls in a later quarter, so net sales are 134,000: 1,500 + 3,500 + 980 on the 14,000 above 120,000."),
 ("pay_8960", "Net sales of 128,000 are above 120,000, so all of it is paid at 7%."),
 ("pay_5400", "Net sales are 128,000: 3% on the first 50,000 and 5% on the remaining 78,000.")],
"pay_5560", 2,
twin=T([("processed 22 June 2026", "processed 3 July 2026")], "pay_5980")),

# ------------------------------------------------------------------ fe09
# why: late cancellation = LESS than 12 hours before start. Class Tue 07:00; cancelled
# Mon 19:10 -> 11 h 50 min -> late -> 5.00. Twin: 18:55 -> 12 h 05 min -> no fee.
# Only 1 prior no-show in 30 days, so no booking ban.
C("fe09", "What should the booking system do about this cancellation?",
"""
Kinmoor Studios — Class Booking Rules

B1. Members may cancel a class booking free of charge up to 12 hours before the class starts.
B2. A cancellation made less than 12 hours before the start is a late cancellation: fee £5.
B3. Not attending without cancelling is a no-show: fee £8.
B4. A third no-show within 30 days triggers a 7-day booking ban. Late cancellations do not count towards the ban.
B5. All times are studio local time.

Booking KS-0331-7
Member: Gwendolyn Asare
Class: Tuesday 07:00 Reformer Pilates (24 March 2026)
Cancellation made in app: Monday 23 March 2026, 19:10
No-shows in the last 30 days: 1 (5 March)

Front desk note: "She's cancelled late before. Should this be a no-show so we can move toward a ban?"
""",
[("no_fee", "The cancellation came 12 hours or more before the 07:00 class, so it is free."),
 ("late_cancel_fee_5", "The cancellation came 11 h 50 min before the class, less than 12 hours, so it is a late cancellation."),
 ("no_show_fee_8", "She has a record of cancelling late, so this is logged as a no-show."),
 ("booking_ban", "This is her second problem booking within 30 days, which triggers the 7-day ban.")],
"late_cancel_fee_5", 1,
twin=T([("Monday 23 March 2026, 19:10", "Monday 23 March 2026, 18:55")], "no_fee")),

# ------------------------------------------------------------------ fe10
# why: 2.50 per person per night; children UNDER 12 exempt; max 7 nights taxed.
# 2 adults + child aged 12 (not under 12) = 3 people x 7 nights x 2.50 = 52.50.
# Twin: child aged 11 -> exempt -> 2 x 7 x 2.50 = 35.00.
C("fe10", "How much tourist tax should the front desk collect?",
"""
Municipality of Verrano Lido — Tourist Tax Regulation (in force from 1 April 2026)

Art. 3. The tax is 2.50 per person per night.
Art. 4. Exempt: children under 12 years old on the day of arrival; guests staying for medical treatment with a certificate; bus drivers and tour leaders on duty.
Art. 5. No more than 7 consecutive nights per stay are taxed.
Art. 6. The hotel collects the tax at check-out and shows it separately on the bill.

Hotel Scogliera Azzurra — guest folio 26-8830
Guests: Mr and Mrs Halloran, and their daughter Maeve, aged 12 on the day of arrival
Arrival: 2 August 2026; departure: 11 August 2026 (9 nights)
Room rate: 138 per night (not relevant to the tax)
Medical certificates: none

Night auditor's note: "Nine nights × three guests × 2.50 = 67.50, unless the girl is exempt."
""",
[("tax_52_50", "Maeve is not under 12, so three guests are taxed, for no more than 7 nights: 3 × 7 × 2.50."),
 ("tax_35_00", "Maeve is under 12 and exempt, and only 7 of the 9 nights are taxed: 2 × 7 × 2.50."),
 ("tax_67_50", "All three guests are taxed for all 9 nights: 3 × 9 × 2.50."),
 ("tax_45_00", "Only the two adults pay, for all 9 nights: 2 × 9 × 2.50.")],
"tax_52_50", 2,
twin=T([("their daughter Maeve, aged 12 on the day of arrival", "their daughter Maeve, aged 11 on the day of arrival")], "tax_35_00")),

# ------------------------------------------------------------------ fe11
# why: chargeable weight = max(actual, L x W x H / 5000). 60x50x40 = 120,000 / 5000 =
# 24 kg > 18 actual -> 24 kg -> band "over 20 up to 30" -> 52.
# Twin: 50x40x40 = 80,000 / 5000 = 16 < 18 -> 18 kg -> band "up to 20" -> 38.
C("fe11", "Which freight charge applies to this parcel?",
"""
Corvane Freight — Domestic Parcel Rate Card 2026

R1. Chargeable weight is the greater of the actual weight and the volumetric weight.
R2. Volumetric weight (kg) = length × width × height in cm ÷ 5,000.
R3. Rate bands by chargeable weight:
    up to 20 kg (inclusive): 38.00
    over 20 kg and up to 30 kg (inclusive): 52.00
    over 30 kg: 52.00 plus 2.10 for each kg or part kg over 30
R4. Fuel surcharge is billed monthly and is not part of the rate card charge.

Consignment CF-DP-661902
Shipper: Harlow Ceramics Studio
Declared contents: packed pottery (fragile)
Actual weight: 18.0 kg
Carton dimensions: 60 cm × 50 cm × 40 cm
Shipper's booking note: "Scale says 18 kilos, so it's the under-20 band."
""",
[("rate_52_00", "The volumetric weight of 24 kg is greater than the 18 kg actual weight, which puts the parcel in the over-20-to-30 band."),
 ("rate_38_00", "The actual weight of 18 kg is greater than the 16 kg volumetric weight, which puts the parcel in the up-to-20 band."),
 ("rate_60_40", "The volumetric weight is 24 kg, and every kg over 20 adds 2.10 to the 52.00 band rate."),
 ("rate_38_00_actual_only", "The parcel's actual weight on the scale is what decides the band, and 18 kg is under 20.")],
"rate_52_00", 2,
twin=T([("Carton dimensions: 60 cm × 50 cm × 40 cm", "Carton dimensions: 50 cm × 40 cm × 40 cm")], "rate_38_00")),

# ------------------------------------------------------------------ fe12
# why: fee 6 per day when end-of-day balance is overdrawn by MORE than 25.00; cap 5
# days per statement month. Days: -12.40 (no), -25.00 (no, not more than 25), -61.10
# (yes), -140.00 (yes), -88.25 (yes), -25.01 (yes), +14.00 (no), -40.00 (yes) = 5 -> 30.
# Twin: -61.10 -> +3.50 -> 4 days -> 24.
C("fe12", "What overdraft fee should the September statement show?",
"""
Harthill Building Society — Everyday Account Fees (from 1 July 2026)

F1. An unarranged overdraft fee of 6.00 is charged for each day on which the end-of-day balance is overdrawn by more than 25.00.
F2. A day on which the balance is overdrawn by 25.00 or less is free (the "buffer").
F3. No more than 5 days are charged in any statement month.
F4. Returned-payment fees are shown separately (none this month).

Account 40-18-77 / 91142058 — end-of-day balances, September 2026 (only days below zero or recovering are listed; all other days were above zero)
03 Sep: −12.40
04 Sep: −25.00
07 Sep: −61.10
08 Sep: −140.00
09 Sep: −88.25
10 Sep: −25.01
11 Sep: +14.00
22 Sep: −40.00

Customer's message: "I was only in the red for about a week, and some of those days were tiny amounts."
""",
[("fee_30", "Five days were overdrawn by more than 25.00 (7, 8, 9, 10 and 22 September), which is also the monthly cap."),
 ("fee_24", "Four days were overdrawn by more than 25.00 (8, 9, 10 and 22 September)."),
 ("fee_36", "Six days were overdrawn by 25.00 or more, including 4 September."),
 ("fee_42", "Seven days were overdrawn in September at 6.00 each.")],
"fee_30", 2,
twin=T([("07 Sep: −61.10", "07 Sep: +3.50")], "fee_24")),

# ------------------------------------------------------------------ fe13
# why: account created 2025 -> first 50 GB free. 820 GB: 50 free; next 450 at 0.020 =
# 9.00; remaining 320 at 0.015 = 4.80 -> 13.80.
# Twin: account created 2 Mar 2026 (on/after 1 Mar) -> first 500 at 0.020 = 10.00 +
# 320 x 0.015 = 4.80 -> 14.80.
C("fe13", "What storage charge should this month's invoice show?",
"""
Nimbrel Object Storage — Price List, Standard class

N1. Monthly storage is billed on average GB stored over the month, in marginal tiers:
    first 50 GB: free
    next 450 GB (above 50 up to 500 GB): 0.020 per GB
    above 500 GB: 0.015 per GB
N2. Request and egress charges are billed separately.

Pricing update PU-12 (effective 1 March 2026): for accounts created on or after 1 March 2026, there is no free tier. The first 500 GB are charged at 0.020 per GB; usage above 500 GB stays at 0.015 per GB. Accounts created before 1 March 2026 keep the free tier.

Account: Sallow Creek Surveying (acct NB-00-71392)
Account created: 18 November 2025
Average storage for August 2026: 820 GB
Finance query from the customer: "Last month your support bot said it's a flat 0.015 once you're over 500 — so shouldn't it be 12.30?"
""",
[("charge_13_80", "The account keeps the free tier: 450 GB at 0.020 is 9.00, and the 320 GB above 500 at 0.015 is 4.80."),
 ("charge_14_80", "The account has no free tier: 500 GB at 0.020 is 10.00, and the 320 GB above 500 at 0.015 is 4.80."),
 ("charge_12_30", "Above 500 GB the whole volume is charged at the flat 0.015 rate: 820 × 0.015."),
 ("charge_15_40", "After the free 50 GB, the remaining 770 GB are charged at 0.020.")],
"charge_13_80", 2,
twin=T([("Account created: 18 November 2025", "Account created: 2 March 2026")], "charge_14_80")),

# ------------------------------------------------------------------ fe14
# why: time measured in pickup-depot time. Pickup Mon 10:00 (UTC+1); return 11:45 at
# Tessaly depot (UTC+2) = 10:45 UTC+1 on Thu -> 3 x 24 h + 45 min -> within 59-min grace
# -> 3 days x 42 = 126. Twin: return 12:05 UTC+2 = 11:05 UTC+1 -> 3 days + 65 min ->
# beyond grace -> 4 days -> 168.
C("fe14", "How many rental days should this one-way hire be billed for?",
"""
Rollo Car Hire — Rental Terms, section 4 (Charging)

4.1 A rental day is each 24-hour period starting at the pickup time, or any part of one.
4.2 Grace: if the car is returned no more than 59 minutes after the end of a 24-hour period, no further day is charged.
4.3 Pickup and return times are compared in the pickup depot's time zone.
4.4 The daily rate for group C is 42.00.
4.5 One-way fee (charged separately): 35.00.

Rental agreement RCH-44-09123
Pickup: Marlow Airport depot (UTC+1), Monday 6 July 2026, 10:00
Return: Tessaly Central depot (UTC+2), Thursday 9 July 2026, 11:45 Tessaly time
Group: C
Counter agent note: "Came back 1 hour 45 late — that's a fourth day."
""",
[("bill_3_days_126", "In Marlow time the car came back at 10:45, 45 minutes into the fourth period and inside the 59-minute grace: 3 × 42.00."),
 ("bill_4_days_168", "In Marlow time the car came back at 11:05, 65 minutes past three full periods and beyond the grace: 4 × 42.00."),
 ("bill_3_5_days_147", "The late return adds half a day: 3.5 × 42.00."),
 ("bill_4_days_plus_oneway_203", "Mon to Thu counts as four calendar days, and the one-way fee is part of the day charge: 4 × 42.00 + 35.00.")],
"bill_3_days_126", 3,
twin=T([("Thursday 9 July 2026, 11:45 Tessaly time", "Thursday 9 July 2026, 12:05 Tessaly time"),
        ("Came back 1 hour 45 late", "Came back 2 hours 5 late")], "bill_4_days_168")),

# ------------------------------------------------------------------ fe15
# why: de minimis: consignment value (goods + shipping) of 150.00 or less is duty-free;
# above 150.00, duty 8% of the WHOLE value. 138.00 + 14.00 = 152.00 -> duty 12.16.
# Twin: shipping 12.00 -> 150.00 -> duty-free (inclusive).
C("fe15", "What import duty should be charged on this parcel?",
"""
Isles of Carnach Customs — Notice 22: Low-value imports

22.1 The value of a consignment is the price of the goods plus the shipping and insurance charged to the buyer.
22.2 Consignments with a value of 150.00 or less are free of duty.
22.3 Consignments with a value above 150.00 pay duty at 8% of the whole value, not just the part above 150.00.
22.4 Duty is rounded to the nearest cent.
22.5 Handling fees charged by the carrier are not part of the value.

Postal declaration PD-9981-CA
Recipient: Ines Callaghan, Port Varra
Goods: hiking boots, price 138.00
Shipping charged to the buyer: 14.00
Insurance: none
Carrier handling fee: 6.50
Recipient's note: "The boots are under 150. No duty, surely."
""",
[("duty_12_16", "Goods plus shipping come to 152.00, above 150.00, so duty is 8% of the whole 152.00."),
 ("duty_free", "Goods plus shipping come to 150.00 or less, so the parcel is duty-free."),
 ("duty_0_16", "Only the 2.00 above the 150.00 threshold is dutiable, at 8%."),
 ("duty_12_68", "Goods, shipping and the carrier handling fee make 158.50, and 8% of that is duty.")],
"duty_12_16", 2,
twin=T([("Shipping charged to the buyer: 14.00", "Shipping charged to the buyer: 12.00")], "duty_free")),

# ------------------------------------------------------------------ fe16
# why: ERC 2% if repaid before the 2nd anniversary of drawdown; 1% from the 2nd to
# before the 3rd; none after. Drawdown 15 Mar 2024; repaid 20 Mar 2026 (after 15 Mar
# 2026) -> 1% of 42,000 repaid = 420. Twin: repaid 10 Mar 2026 -> 2% -> 840.
C("fe16", "What early repayment charge applies to this partial repayment?",
"""
Fellgate Business Finance — Term Loan Agreement, clause 8 (Voluntary prepayment)

8.1 The borrower may repay all or part of the loan early on 10 business days' notice.
8.2 Early repayment charge (ERC), calculated on the amount repaid (not on the original loan):
    repaid before the second anniversary of drawdown: 2%
    repaid on or after the second anniversary but before the third: 1%
    repaid on or after the third anniversary: none
8.3 ERC is payable on the repayment date.

Loan FBF-TL-2024-0381 — Dunhollow Farm Supplies Ltd
Original loan: 60,000; drawdown date: 15 March 2024
Notice of prepayment given: 3 March 2026 (more than 10 business days before repayment)
Amount repaid early: 42,000
Repayment date: 20 March 2026

Borrower's email: "We're past two years now, so I assume no charge?"
""",
[("erc_420", "The repayment came after the second anniversary on 15 March 2026 and before the third, so 1% of the 42,000 repaid applies."),
 ("erc_840", "The repayment came before the second anniversary on 15 March 2026, so 2% of the 42,000 repaid applies."),
 ("erc_none", "More than two years have passed since drawdown, so no charge applies."),
 ("erc_600", "The 1% charge is worked out on the original loan of 60,000.")],
"erc_420", 2,
twin=T([("Repayment date: 20 March 2026", "Repayment date: 10 March 2026"),
        ("Notice of prepayment given: 3 March 2026", "Notice of prepayment given: 20 February 2026")], "erc_840")),

# ------------------------------------------------------------------ fe17
# why: daily rate = monthly x 12 / 365 = 1,460 x 12 / 365 = 48.00. Move-in day
# included. 20-30 Sep = 11 days -> 528.00. Twin: 21 Sep -> 10 days -> 480.00.
C("fe17", "What first-month rent should be charged for this move-in?",
"""
Calloway Residential — Tenancy Schedule, part B (Rent)

B1. Monthly rent: 1,460.00, due on the 1st of each month.
B2. For a part month at the start of the tenancy, rent is charged by the day. The daily rate is the monthly rent × 12 ÷ 365.
B3. The move-in date is the first day charged. The last day charged is the last day of that calendar month.
B4. The security deposit (one month's rent) is taken separately and is not rent.

Tenancy CR-2026-7718 — Apt 5C, Birchfield Court
Tenant: Anatole Ferreira
Move-in date: 20 September 2026 (keys collected 09:30)
Letting agent's draft statement: "Pro rata = 1,460 ÷ 30 × 11 = 535.33."
""",
[("rent_528_00", "The daily rate is 1,460 × 12 ÷ 365 = 48.00, and 20 to 30 September inclusive is 11 days."),
 ("rent_480_00", "The daily rate is 1,460 × 12 ÷ 365 = 48.00, and 21 to 30 September inclusive is 10 days."),
 ("rent_535_33", "The daily rate is 1,460 ÷ 30, charged for 11 days."),
 ("rent_1460_00", "Rent is due in full on the 1st, so the whole month is charged.")],
"rent_528_00", 1,
twin=T([("Move-in date: 20 September 2026", "Move-in date: 21 September 2026"), ("× 11 = 535.33", "× 10 = 486.67")], "rent_480_00")),

# ------------------------------------------------------------------ fe18
# why: postponed event: face value refundable if requested within 14 days after the
# announcement (announcement day = day 0). Announced 2 Sep; request 16 Sep = day 14 ->
# in window. Booking fee refunded only for cancellation -> refund 85.00.
# Twin: request 17 Sep = day 15 -> no refund; ticket valid for new date.
C("fe18", "What should the box office do with this refund request?",
"""
Quaymarket Arena — Ticket Terms, section 7 (Changes to events)

7.1 Cancelled events: the ticket price and the booking fee are refunded automatically.
7.2 Postponed events: tickets are valid for the new date. A ticket holder who cannot attend may request a refund of the ticket price within 14 days after the postponement is announced. The announcement day is day 0.
7.3 Booking fees are refunded only under 7.1.
7.4 Requests outside the 7.2 window are declined; the ticket stays valid for the new date.
7.5 No administration fee is charged on refunds.

Event: Halcyon Drift — live, originally 26 September 2026
Status: postponed to 6 February 2027; postponement announced 2 September 2026

Refund request QA-R-55107
Customer: Bartholomew Ng
Ticket: 1 × standing, price 85.00, booking fee 7.50
Request received: 16 September 2026
Customer: "The show was called off, so I want everything back, fee included."
""",
[("refund_85_00", "The request came on day 14 after the announcement, inside the window, and booking fees are not refunded for postponements."),
 ("refund_92_50", "The event was called off, so the ticket price and the booking fee are both refunded."),
 ("decline_keep_ticket", "The request came after day 14 from the announcement, so it is declined and the ticket stays valid for 6 February."),
 ("refund_77_50", "The ticket price is refunded less the booking fee as an administration charge.")],
"refund_85_00", 2,
twin=T([("Request received: 16 September 2026", "Request received: 17 September 2026")], "decline_keep_ticket")),

# ------------------------------------------------------------------ fe19
# why: each full 7 days at weekly rate 90; remaining days at 18/day capped at 90.
# 3 Aug 08:00 -> 12 Aug 08:00 = 9 days -> 90 + 2 x 18 = 126.
# Twin: return 13 Aug 08:00 -> 10 days -> 90 + 3 x 18 = 144.
C("fe19", "What hire charge should the depot invoice for this scaffold tower?",
"""
Brackenfield Plant Hire — Rates and Conditions

H1. Hire is charged in 24-hour days from the time the equipment leaves the depot to the time it is returned.
H2. Rates for a 6 m aluminium scaffold tower: daily 18.00; weekly 90.00.
H3. For each full 7 days of hire, the weekly rate is charged. Remaining days are charged at the daily rate, but never more than the weekly rate in total.
H4. Damage and cleaning charges are assessed on return (none recorded).
H5. Delivery and collection are quoted separately.

Hire docket BPH-26-3310
Customer: Tamsin Ellery (self-build)
Equipment left depot: Monday 3 August 2026, 08:00
Returned: Wednesday 12 August 2026, 08:00
Customer's remark: "Nine days at eighteen, or does the weekly price help me?"
""",
[("charge_126", "Nine days of hire: one full week at 90.00 plus 2 days at 18.00."),
 ("charge_144", "Ten days of hire: one full week at 90.00 plus 3 days at 18.00."),
 ("charge_162", "Nine days of hire at the 18.00 daily rate."),
 ("charge_180", "Any part of a second week is charged at the weekly rate, so two weeks at 90.00.")],
"charge_126", 1,
twin=T([("Returned: Wednesday 12 August 2026, 08:00", "Returned: Thursday 13 August 2026, 08:00"),
        ("Nine days at eighteen", "Ten days at eighteen")], "charge_144")),

# ------------------------------------------------------------------ fe20
# why: Trip 1 Mon 4 May 08:15 = listed public holiday -> weekend rate 2.20.
# Trip 2 Tue 5 May 09:30 -> AM peak is 07:00 up to but not including 09:30 -> off-peak 2.60.
# Trip 3 Tue 5 May 17:05 -> PM peak 16:30-19:00 (start included, end excluded) -> 4.80.
# Total 9.60. Twin: Trip 2 at 09:29 -> peak 4.80 -> 11.80.
C("fe20", "What total should this toll account be charged for the week?",
"""
Orwell Crossing Toll — Tariff for cars (2026)

1. Peak: 4.80 — entries from 07:00 up to but not including 09:30, and from 16:30 up to but not including 19:00, Monday to Friday.
2. Off-peak: 2.60 — all other entries Monday to Friday.
3. Weekends and public holidays: 2.20 flat, at any time.
4. Public holidays 2026: 1 Jan, 3 Apr, 6 Apr, 4 May, 25 May, 31 Aug, 25 Dec, 28 Dec.
5. The entry time recorded by the gantry decides the rate.

Account OC-771-20094 — gantry log, week of 4 May 2026
Trip 1: Monday 4 May, entry 08:15
Trip 2: Tuesday 5 May, entry 09:30
Trip 3: Tuesday 5 May, entry 17:05

Customer query: "Two morning rush-hour trips and one evening one — I'm expecting to pay the peak price three times."
""",
[("charge_9_60", "Trip 1 is on a public holiday (2.20), Trip 2 is at 09:30, when the morning peak has ended (2.60), and Trip 3 is peak (4.80)."),
 ("charge_11_80", "Trip 1 is on a public holiday (2.20), and Trips 2 and 3 both fall inside peak windows (4.80 each)."),
 ("charge_14_40", "All three trips were made in rush hour, so each is charged at the peak rate of 4.80."),
 ("charge_12_20", "Trips 1 and 3 are peak (4.80 each), and Trip 2 at 09:30 is off-peak (2.60).")],
"charge_9_60", 2,
twin=T([("Trip 2: Tuesday 5 May, entry 09:30", "Trip 2: Tuesday 5 May, entry 09:29")], "charge_11_80")),

# ------------------------------------------------------------------ fe21
# why: claim amount = principal + interest claimed (filing fee excluded). 4,860 + 180 =
# 5,040 > 5,000 -> fee 5% x 5,040 = 252.00. Twin: interest 130 -> 4,990 -> band
# 1,000.01-5,000 -> 115.00.
C("fe21", "What filing fee should the court office collect for this small claim?",
"""
Tarrant County Civil Court — Small Claims Fee Table (from 1 January 2026)

Claim amount (principal plus any interest claimed; the filing fee itself is not included)
    up to 300.00: 35.00
    300.01 to 1,000.00: 70.00
    1,000.01 to 5,000.00: 115.00
    over 5,000.00: 5% of the claim amount
Fee remissions require form FR-2 with evidence of income (not submitted).
Hearing fees (payable later, if the claim is defended and listed): 27.00 to 346.00 depending on the claim amount — not collected at filing.
Counter staff must not advise on the merits of a claim.

Claim form SC-26-10457
Claimant: Wren & Oakes Decorators
Defendant: Lysander Pike
Principal claimed (unpaid invoice): 4,860.00
Interest claimed to date of filing: 180.00
Total claimed: 5,040.00
Claimant's cover note: "Our debt is under five thousand, so the fee should be 115."
""",
[("fee_252_00", "Principal and interest make 5,040.00, above 5,000.00, so the fee is 5% of 5,040.00."),
 ("fee_115_00", "Principal and interest make 5,000.00 or less, so the claim is in the 1,000.01 to 5,000.00 band."),
 ("fee_243_00", "The fee is 5% of the principal of 4,860.00 only."),
 ("fee_2_00", "Only the 40.00 above 5,000.00 is charged at 5%.")],
"fee_252_00", 2,
twin=T([("Interest claimed to date of filing: 180.00\nTotal claimed: 5,040.00", "Interest claimed to date of filing: 130.00\nTotal claimed: 4,990.00")], "fee_115_00")),

# ------------------------------------------------------------------ fe22
# why: daily deduction = monthly salary x 12 / 261 = 5,220 x 12 / 261 = 240.00.
# Unpaid leave Thu 1 Oct - Tue 6 Oct: working days Thu 1, Fri 2, Tue 6 (Mon 5 Oct is a
# listed holiday; Sat/Sun not working days) = 3 -> 720.00.
# Twin: holiday list has 12 Oct instead of 5 Oct -> Mon 5 is working -> 4 days -> 960.00.
C("fe22", "What unpaid-leave deduction should October payroll make?",
"""
Soltree Housing Association — Payroll Procedures, PP-6 (Unpaid leave)

6.1 Unpaid leave is deducted by working day. The daily rate is monthly salary × 12 ÷ 261.
6.2 Working days are Monday to Friday, excluding the public holidays in the Annex. Weekends and holidays inside a period of unpaid leave are not deducted.
6.3 Deductions are made in the payroll month in which the leave is taken.

Annex — public holidays, second half of 2026: 31 August; 5 October (Harvest Holiday); 25 December; 28 December.

Payroll adjustment form PA-2210
Employee: Mireille Oyelowo, housing officer
Monthly salary: 5,220.00
Unpaid leave approved: Thursday 1 October to Tuesday 6 October 2026 (inclusive)
Line manager's note: "Six days of unpaid leave — please deduct six days."
""",
[("deduct_720", "Only Thursday 1, Friday 2 and Tuesday 6 October are working days in the period, at 240.00 a day."),
 ("deduct_960", "Four working days fall in the period (1, 2, 5 and 6 October), at 240.00 a day."),
 ("deduct_1440", "The manager approved six days of unpaid leave, at 240.00 a day."),
 ("deduct_522", "The daily rate is monthly salary ÷ 30, which is 174.00, over 3 days.")],
"deduct_720", 2,
twin=T([("5 October (Harvest Holiday)", "12 October (Harvest Holiday)")], "deduct_960")),
]
