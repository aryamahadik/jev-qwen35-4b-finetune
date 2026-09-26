"""nli_c / meeting minutes (boards, committees, residents' associations, school governors)."""
from _lib import C, Y, T, NLI3, REL5, ESTABLISH, FACTIVE, PRESUP, IMPLICATIVE, QUANT, EXCEPT, MODAL, COND, REPORTED

ITEMS = [
# ------------------------------------------------------------------ mn01
# why: 9 trustees; 5 for, 3 against, 1 abstention -> 5 of 9 is a majority of all trustees
#      -> entailment. Twin: 4 for, 3 against, 2 abstentions -> 4 of 9 is not -> contradiction.
C("mn01", 'Hypothesis: "A majority of all the Trust\'s trustees voted for the motion to sell Brook Cottage." What is the relation between the minutes and the hypothesis?',
"""
MINUTES — Hawkridge Almshouse Trust, Board of Trustees
Meeting of 16 September, 18:30, Trust office, Mill Lane

Present: all nine trustees (Chair: Deborah Anand).
In attendance: Rupert Hale (clerk); Mina Gallo (surveyor, for item 3 only).

1. Apologies: none.

2. Minutes of the previous meeting were approved as a correct record.

3. Brook Cottage. Ms Gallo presented her survey. The cottage needs a new roof and damp treatment, estimated at £138,000, and cannot be let until the work is done. She advised that the property would sell for between £310,000 and £340,000 in its current condition. Ms Gallo left the meeting.

Trustees discussed whether to repair or sell. Two trustees felt the Trust should keep all its properties. The clerk confirmed that the Charity Commission rules would require the proceeds of any sale to be reinvested in housing for the Trust's beneficiaries.

The motion to sell Brook Cottage carried 5–3 with one abstention.

4. Any other business: the Christmas lunch for residents will be held on 12 December.

The meeting closed at 20:10.
""",
NLI3, "entailment", 2,
twin=T([("carried 5–3 with one abstention.", "carried 4–3 with two abstentions.")], "contradiction")),

# ------------------------------------------------------------------ mn02
# why: "Kofi will circulate the draft by Friday" is a future action -> whether it has been
#      circulated is left open -> yes. Twin: "Kofi circulated the draft on Tuesday" -> no.
Y("mn02", "Do the minutes leave open whether the draft volunteer handbook has been circulated to members?",
"""
Riverside Allotment Society — Committee Meeting
Wednesday 23 September, 19:00, the Pavilion

Present: Nadia Ferris (chair), Kofi Mensah (secretary), Elise Warren (treasurer), Bram de Wit, Selma Haq.

1. Treasurer's report. Balance at 31 August: £6,212. The water bill for the summer quarter (£1,048) has been paid. Rent arrears are down to two plots.

2. Volunteer handbook. The working group has finished the draft handbook, which covers work-party dates, tool-shed rules and first aid. Kofi will circulate the draft to all members by Friday for comments, with a four-week deadline. Selma asked that the section on bonfires be checked against the council's rules; Kofi agreed to do this before circulating.

3. Plot inspections. The autumn inspection will take place on Saturday 10 October. Bram and Elise will inspect the lower field; Nadia and Selma the upper field.

4. Date of next meeting: Wednesday 28 October, 19:00.

Meeting closed 20:35.
""",
[ESTABLISH, ("Action item", "a task minuted as something a person will do; it records a plan, not that the task has been done.")], 1, 2, role="neg",
twin=T([("Kofi will circulate the draft to all members by Friday for comments, with a four-week deadline. Selma asked that the section on bonfires be checked against the council's rules; Kofi agreed to do this before circulating.",
         "Kofi circulated the draft to all members on Tuesday for comments, with a four-week deadline. Selma asked that the section on bonfires be checked against the council's rules; Kofi agreed to send members a corrected page if needed.")], 0)),

# ------------------------------------------------------------------ mn03
# why: the £42,300 figure is only what the treasurer stated; the bank statement was not
#      available -> attributed only. Twin: Appendix B bank statement shows it -> entailed.
C("mn03", 'Choose the description that fits the minutes and the hypothesis "The reserve fund stood at £42,300 on 31 August."',
"""
Minutes of the Finance Committee — Greyfield Community Sports Club
Held Monday 14 September, 19:30, clubhouse bar (closed session)

Present: Omar Siddiqui (chair), Paulina Nowak (treasurer), Declan Ross, Marisol Vega.

1. Reserve fund. The treasurer stated that the reserve fund stood at £42,300 on 31 August. The bank statement for August had not arrived by the time of the meeting because of the bank's change of online platform, and the treasurer will circulate it once received.

2. Floodlights. Three quotes have been obtained for replacing the floodlights on pitch 2 with LED units. The lowest is £18,750 from Kestrel Electrical. The committee agreed to recommend the Kestrel quote to the full board, subject to confirmation that the work can be done during the winter break.

3. Membership fees. The committee discussed a proposal to raise adult fees by £15 for next season. Declan Ross said the increase should be delayed until the new floodlights are installed. No decision was reached; the item will return to the October meeting.

4. Any other business. None.

The meeting closed at 20:50.
""",
REL5, "attributed only", 2,
twin=T([("The treasurer stated that the reserve fund stood at £42,300 on 31 August. The bank statement for August had not arrived by the time of the meeting because of the bank's change of online platform, and the treasurer will circulate it once received.",
         "The reserve fund stood at £42,300 on 31 August, as shown on the August bank statement attached as Appendix B, which the treasurer took the committee through.")], "entailed")),

# ------------------------------------------------------------------ mn04
# why: "No member present objected" and Faro is listed as present -> Faro did not object
#      -> yes. Twin: "Only one member present objected" (unnamed) -> not established -> no.
Y("mn04", "Do the minutes establish that Dr Lucia Faro did not object to the change in the visiting policy?",
"""
Ashgrove Care Home — Family Liaison Committee
Minutes of the meeting held on Thursday 10 September, 14:00, Garden Lounge

Present: Hollis Brandt (home manager, chair), Dr Lucia Faro (visiting GP), Mercy Owusu (senior nurse), Jan Kowal (family representative), Ruth Emmerson (family representative).

1. Visiting policy. The home manager proposed that, from 1 October, visitors may come at any time between 09:00 and 20:00 without booking, except during the lunch service from 12:00 to 13:30 in the dining room. Families would still be asked to sign in at reception. No member present objected to the change, and it was agreed.

2. Flu vaccinations. Dr Faro confirmed that the vaccination clinic for residents will be held on 5 October. Consent forms have been sent to next of kin for residents who cannot consent themselves.

3. Garden project. Mr Kowal reported that volunteers have finished the raised beds. A planting day will be held on 26 September, to which families are invited.

4. Next meeting: Thursday 12 November, 14:00.
""",
[ESTABLISH, QUANT], 1, 2,
twin=T([("No member present objected to the change, and it was agreed.", "Only one member present objected to the change, and it was agreed by the others.")], 0)),

# ------------------------------------------------------------------ mn05
# why: 11 governors, quorum 6. 7 at start; Hart and Oyelaran left at 19:50 -> 5 present at the
#      20:05 vote -> not quorate, so the vote was taken while inquorate. The uniform decision is
#      then "not validly made" per the standing order quoted. Established statement:
#      "vote taken while inquorate". Twin: only Hart left -> 6 present -> quorate.
C("mn05", "Which one of these statements do the minutes establish?",
"""
Kingsmead Primary School — Full Governing Board
Minutes, Tuesday 22 September, 18:30, school library

The board has 11 governors. Standing order 4: the quorum is 6 governors present, and a decision taken when fewer than 6 governors are present is not valid and must be ratified at the next quorate meeting.

Present at the start: Anika Rao (chair), Lewis Hart, Grace Oyelaran, Tomasz Bielski, Hollie Price, Ade Coker, Martin Lowe (headteacher). Seven governors.
Apologies: Fenna Dijk, Samir Latif. Absent without apologies: Joy Mercer, Callum Reid.

1. Headteacher's report. Mr Lowe reported 312 pupils on roll, up from 298. Attendance last term was 95.1%.

2. Safeguarding. The safeguarding governor, Ms Price, confirmed that all staff completed their annual training in September.

3. Lewis Hart and Grace Oyelaran left the meeting at 19:50.

4. Uniform. At 20:05 the board voted 4–1 to allow plain black trainers as an alternative to school shoes from January.

5. Date of next meeting: Tuesday 3 November.
""",
[("vote taken while quorate", "The uniform decision was taken while a quorum was present."),
 ("vote taken while inquorate", "The uniform decision was taken while fewer governors than the quorum were present."),
 ("Hart voted on uniform", "Lewis Hart voted on the uniform decision."),
 ("all governors voted", "Every governor present at the start of the meeting voted on the uniform decision."),
 ("uniform change unanimous", "No governor voted against the uniform change."),
 ("fewer pupils than before", "The school has fewer pupils on roll than at the previous count."),
 ("none of these", "The minutes establish none of the statements above.")],
"vote taken while inquorate", 3,
twin=T([("3. Lewis Hart and Grace Oyelaran left the meeting at 19:50.", "3. Lewis Hart left the meeting at 19:50.")], "vote taken while quorate")),

# ------------------------------------------------------------------ mn06
# why: "should be reviewed annually" is an obligation; nothing says whether it was reviewed
#      this year -> neutral. Twin: "last reviewed in March 2024" with minutes in Sept 2026 ->
#      not reviewed in 2026 -> contradiction.
C("mn06", 'Hypothesis: "The lone-working policy was reviewed in 2026." Given the minutes, is it entailed, contradicted or neutral?',
"""
Northgate Tenants' Advice Centre — Management Committee
Minutes of 29 September 2026

Present: Farah Qureshi (chair), Elliot Brandt, Nkechi Obi, Luis Ortega. Staff: Wendy Harlow (centre manager).

1. Policies. The centre manager presented the policy register. The committee noted that the lone-working policy should be reviewed annually, given that advisers visit tenants at home. Ms Harlow will bring the policy to the November meeting with any changes suggested by staff.

2. Funding. The centre has been awarded £24,000 by the Northgate Housing Fund for a second part-time adviser for two years. Recruitment will start in October.

3. Premises. The landlord has agreed to repair the front-door ramp by the end of October. Until then, clients who use wheelchairs will be seen at the library meeting room by appointment.

4. Volunteers. Twelve volunteers attended the September induction. Mr Ortega thanked the volunteer coordinator for organising it.

Next meeting: 24 November 2026.
""",
NLI3, "neutral", 2,
twin=T([("The committee noted that the lone-working policy should be reviewed annually, given that advisers visit tenants at home.",
         "The committee noted that the lone-working policy was last reviewed in March 2024, even though advisers visit tenants at home.")], "contradiction")),

# ------------------------------------------------------------------ mn07
# why: Cllr Rhee left before item 6; the harbour-dues vote was item 6 -> she was absent -> yes.
#      Twin: she left after item 6, before item 7 -> she was present for item 6 -> no.
Y("mn07", "Do the minutes establish that Cllr Joanna Rhee was absent when the harbour-dues motion was voted on?",
"""
Porthallow Town Council — Minutes of the Ordinary Meeting, 17 September

Present: Cllrs M. Tregear (Mayor, in the chair), J. Rhee, A. Lowry, P. Kellow, S. Dunstan, T. Hosking, R. Penrose.
Officers: Town Clerk (Karen Bolitho).

1. Apologies: Cllr Nance.
2. Declarations of interest: Cllr Kellow declared an interest in item 6 as a boat owner and took no part in the vote.
3. Minutes of 20 August approved.
4. Public participation: two residents spoke about parking on Fore Street.
5. Christmas lights. The council agreed to spend up to £4,200 on new lights for the harbour front.

Cllr Rhee left the meeting after item 5, at 20:15.

6. Harbour dues. The council considered the harbourmaster's proposal to raise mooring dues by 6% from April. Resolved (4 in favour, 1 against) to approve the increase.
7. Correspondence: a letter from the lifeboat station thanking the council for its donation was noted.

The meeting closed at 20:55.
""",
[ESTABLISH, ("Order of business", "items in minutes are recorded in the order they were taken, so a person recorded as leaving after item N was present for items up to N and absent for later items.")], 1, 2,
twin=T([("5. Christmas lights. The council agreed to spend up to £4,200 on new lights for the harbour front.\n\nCllr Rhee left the meeting after item 5, at 20:15.\n\n6. Harbour dues. The council considered the harbourmaster's proposal to raise mooring dues by 6% from April. Resolved (4 in favour, 1 against) to approve the increase.",
         "5. Christmas lights. The council agreed to spend up to £4,200 on new lights for the harbour front.\n6. Harbour dues. The council considered the harbourmaster's proposal to raise mooring dues by 6% from April. Resolved (5 in favour, 1 against) to approve the increase.\n\nCllr Rhee left the meeting after item 6, at 20:40.\n")], 0)),

# ------------------------------------------------------------------ mn08
# why: the minutes record that the café lease was renewed for two years (writer's voice) ->
#      "the café lease was not renewed" is contradicted. Twin: renewal deferred; nothing
#      asserted, attributed or conditioned about non-renewal -> not settled.
C("mn08", 'Hypothesis: "The café lease at Tollgate Park was not renewed." Which description fits the minutes?',
"""
Tollgate Park Friends' Group — Committee Minutes
Saturday 19 September, 10:00, Park Lodge

Present: Irene Walsh (chair), Hamid Rahimi, Yvette Colin, Stuart Muir, Zainab Okoro.
In attendance: Gareth Lamb (council parks officer).

1. Café. The council's property committee met on 9 September and renewed the lease of the park café to Hearth & Bean for a further two years from 1 October, on the same terms. Members welcomed the news; several had asked for the café to open earlier at weekends, and Mr Lamb will pass this on to the operator.

2. Tree planting. Forty-five saplings donated by the Rotary Club will be planted on 7 November. Volunteers should bring gloves; spades will be provided.

3. Play area. The council has received two complaints about the zip wire. Mr Lamb said it had been inspected on 1 September and found to be safe, but the seat will be replaced as a precaution.

4. Finances. The group holds £1,380. The committee agreed to spend up to £200 on bulbs for the entrance beds.

Next meeting: Saturday 17 October.
""",
REL5, "contradicted", 3,
twin=T([("met on 9 September and renewed the lease of the park café to Hearth & Bean for a further two years from 1 October, on the same terms. Members welcomed the news;",
         "met on 9 September and deferred its discussion of the park café lease to its December meeting. Members asked to be kept informed;")], "not settled")),

# ------------------------------------------------------------------ mn09
# why: "must complete the fire doors by 30 November" is an obligation; minutes (1 Oct) do not
#      say they are done -> the minutes fail to establish completion -> yes.
#      Twin: "completed the fire-door replacement on 25 September" -> established -> no.
Y("mn09", "Do the minutes fail to establish that the fire-door replacement at Carlow House has been completed?",
"""
Carlow House Residents' Management Company — Directors' Meeting
Thursday 1 October, 18:00, video call

Present: Directors Beatrice Olin (chair), Rashid Karimi, Moira Dowd. Managing agent: Stellan Property Management (Adrian Keane).

1. Fire safety. Mr Keane reported that the fire risk assessment carried out in June identified 14 flat entrance doors that do not meet current standards. The contractor, Fenlow Joinery, must complete the fire-door replacement by 30 November under the terms of its contract; leaseholders will be given at least seven days' notice of the date for their flat. The cost (£19,600) will be met from the reserve fund.

2. Service charge. The budget for next year proposes an increase of 4.5%, mainly because of higher building insurance. Directors asked Mr Keane to obtain one more insurance quote before the budget is sent to leaseholders.

3. Bin store. The new bin-store lock has been fitted. Codes will be sent to residents by post.

4. Next meeting: Thursday 3 December.
""",
[ESTABLISH, MODAL], 1, 2, role="neg",
twin=T([("The contractor, Fenlow Joinery, must complete the fire-door replacement by 30 November under the terms of its contract; leaseholders will be given at least seven days' notice of the date for their flat.",
         "The contractor, Fenlow Joinery, completed the fire-door replacement on 25 September, well ahead of the 30 November contract deadline; all 14 doors have been signed off.")], 0)),

# ------------------------------------------------------------------ mn10
# why: action log. "Of the two, the former" = Ingrid (first of Ingrid/Pavel). Ingrid owns the insurance
#      renewal, due 9 Oct. Pavel owns the website, due after the insurance. Owen's task has
#      no deadline. Established: "Ingrid owns insurance". Twin: "the latter" = Pavel -> "Pavel owns insurance".
C("mn10", "Which one of these statements about the action log do the minutes establish?",
"""
Kestrel Rowing Club — Committee Meeting, 24 September
Minutes (extract): Actions

1. Boat trailer. Owen Blake reported that the trailer's lighting board failed its check. He will get a replacement board fitted before the head races; no date was set.

2. Insurance. The club's insurance renews on 15 October. Ingrid Solberg and Pavel Havel met the club's broker on Monday. Of the two, the former will send the signed renewal form by 9 October, after checking the new boat values with the captain.

3. Website. Pavel Havel will update the membership page with next season's fees once the renewal form has gone off, so that the insurance cost can be included in the fee breakdown.

4. Safety. The committee agreed that no junior crew may go out after sunset from 1 November. The captain will tell coaches.

5. Social. The quiz night on 17 October is fully booked. Owen will collect the prizes from the sponsor.
""",
[("Ingrid owns insurance", "Ingrid Solberg is responsible for sending the signed insurance renewal form."),
 ("Pavel owns insurance", "Pavel Havel is responsible for sending the signed insurance renewal form."),
 ("website before insurance", "The website update is to be done before the insurance renewal form is sent."),
 ("trailer by the head races date", "The replacement lighting board has a set completion date."),
 ("juniors banned from rowing", "Junior crews may not go out on the water at any time from 1 November."),
 ("captain sends the form", "The club captain is responsible for sending the signed insurance renewal form."),
 ("none of these", "The minutes establish none of the statements above.")],
"Ingrid owns insurance", 3,
twin=T([("Of the two, the former will send", "Of the two, the latter will send")], "Pavel owns insurance")),

# ------------------------------------------------------------------ mn11
# why: "All members present except Cllr Dunn voted in favour"; Cllr Mbatha is listed as present
#      -> Mbatha voted in favour -> entailment. Twin: Mbatha moved to apologies (not present),
#      and only members present may vote -> Mbatha did not vote in favour -> contradiction.
C("mn11", 'Given the minutes, classify the hypothesis "Cllr Mbatha voted in favour of the parking scheme."',
"""
Easton Hill Parish Council — Planning & Highways Committee
Minutes of the meeting of Monday 7 September, 19:00, Village Hall

Present: Cllrs Dunn, Mbatha, Price, Ferreira, Holloway.
Apologies: Cllr Okafor.
Standing order 12: only members present at the meeting may vote; there is no proxy or postal voting.

1. Residents' parking scheme for Church Walk. The county council has asked for the parish's view on a residents' permit scheme for Church Walk and Well Lane, which would operate from 08:00 to 18:00 on weekdays. Residents' petition (47 signatures) supporting the scheme was noted. Cllr Dunn spoke against, saying visitors to the church and the surgery would be displaced into neighbouring streets.

Resolved: all members present except Cllr Dunn voted in favour of supporting the scheme. The clerk will write to the county council.

2. Planning application 26/0419 (single-storey rear extension, 3 Orchard Close): no objection.

3. Speed indicator device: the committee agreed to move the device to the Mill Road approach for October.

The meeting closed at 20:20.
""",
NLI3, "entailment", 2,
twin=T([("Present: Cllrs Dunn, Mbatha, Price, Ferreira, Holloway.\nApologies: Cllr Okafor.", "Present: Cllrs Dunn, Price, Ferreira, Holloway.\nApologies: Cllrs Okafor and Mbatha.")], "contradiction")),

# ------------------------------------------------------------------ mn12
# why: "The chair regretted that the survey had not been circulated" is factive -> it had not
#      been circulated -> "had been circulated" not established -> no. Twin: "was pleased that
#      the survey had been circulated" (factive) -> yes.
Y("mn12", "Do the minutes establish that the parents' survey had been circulated before the meeting?",
"""
St Aldric's Pre-School — Parent Committee
Minutes, Wednesday 16 September, 19:30, main room

Present: Chloe Varga (chair), Dominic Ekwueme, Amira Haddad, Lorna Fisk, Sunil Patel. Staff: Mrs Kaye (manager).

1. Parents' survey. The chair regretted that the survey had not been circulated to parents before the meeting, as agreed in July. The survey asks about opening hours, lunch provision and the new outdoor area. Mrs Kaye explained that the school office had been short-staffed during the settling-in weeks.

2. Autumn fair. The fair will be held on Saturday 21 November. Sunil will organise the tombola; Amira and Lorna will run the cake stall. The target is £1,200 towards new outdoor play equipment.

3. Fees. Mrs Kaye confirmed that fees will rise by 3% from January. The committee asked for a letter to parents explaining the reasons.

4. Any other business. Dominic asked whether the pre-school could offer a breakfast club. Mrs Kaye will look into staffing.

Next meeting: Wednesday 14 October.
""",
[ESTABLISH, FACTIVE], 0, 2,
twin=T([("The chair regretted that the survey had not been circulated to parents before the meeting, as agreed in July.",
         "The chair was pleased that the survey had been circulated to parents before the meeting, as agreed in July."),
        ("Mrs Kaye explained that the school office had been short-staffed during the settling-in weeks.",
         "Mrs Kaye said that 31 responses had already come back.")], 1)),

# ------------------------------------------------------------------ mn13
# why: the repainting is stated only if the grant arrives before March, which is unresolved ->
#      conditional only. Twin: "The hall will not be repainted this year, as the grant application
#      was refused" (writer's voice) -> contradicted.
C("mn13", 'Hypothesis: "Bramley Village Hall will be repainted this year." Choose the description that fits the minutes.',
"""
Bramley Village Hall Management Committee
Minutes of the meeting held on Tuesday 8 September 2026

Present: Pamela Ruddock (chair), Idris Morgan (treasurer), Fiona Galt (bookings secretary), Kenji Aoki, Beth Carver.

1. Bookings. Mrs Galt reported that regular bookings are back to pre-2020 levels, with the new Tuesday yoga class taking the hall every week from October.

2. Decoration. The committee discussed the state of the main hall. If the Rural Halls grant of £3,500 arrives before March, the hall will be repainted this year, in the week after the pantomime. The application was submitted in August; the funder's panel meets in January. Mr Morgan noted that the hall's own reserves could not cover the full cost.

3. Heating. The boiler service is booked for 2 October.

4. Fundraising. The quiz night raised £612. Mr Aoki will organise a second quiz in February.

Next meeting: Tuesday 10 November.
""",
REL5, "conditional only", 2,
twin=T([("If the Rural Halls grant of £3,500 arrives before March, the hall will be repainted this year, in the week after the pantomime. The application was submitted in August; the funder's panel meets in January.",
         "The hall will not be repainted this year, because the Rural Halls grant application for £3,500 was refused in August. The committee will apply again next year.")], "contradicted")),

# ------------------------------------------------------------------ mn14
# why: 128 members x £40 = £5,120 < £5,400 hire cost -> fees do NOT cover the hire -> "fail to
#      establish that fees cover the hire?" = yes. Twin: 142 members -> £5,680 >= £5,400 -> no.
Y("mn14", "Do the minutes fail to establish that this season's membership fees cover the pool-hire cost?",
"""
Westmere Masters Swimming Club — AGM Minutes (extract)
Sunday 13 September, 11:00, Westmere Leisure Centre meeting room

Treasurer's report. Luisa Brandt reported that 128 members have paid the adult membership fee of £40 for the season starting 1 October; there are no other membership categories this season. The leisure centre has confirmed the pool-hire cost for the season at £5,400, payable in two instalments in October and February.

The treasurer explained that membership fees are the club's only regular income and that the club holds £2,050 in its reserve account, which the committee would like to keep for emergencies and gala entry fees.

Members discussed whether to raise the fee mid-season, to run a sponsored swim, or to reduce pool time by one session a month. No vote was taken; the committee was asked to bring options to a special meeting in November.

Election of officers. Luisa Brandt (treasurer) and Ravi Sood (secretary) were re-elected unopposed. Holly Nash was elected chair, replacing Graham Tully, who has stood down after six years.
""",
[ESTABLISH, ("Fees cover the hire", "total fee income (members x fee) is at least the pool-hire cost for the season.")], 1, 3, role="neg",
twin=T([("reported that 128 members have paid", "reported that 142 members have paid"),
        ("Members discussed whether to raise the fee mid-season, to run a sponsored swim, or to reduce pool time by one session a month. No vote was taken; the committee was asked to bring options to a special meeting in November.",
         "Members discussed how to use any surplus, such as extra coaching or subsidised gala entries. No vote was taken; the committee was asked to bring options to a special meeting in November.")], 0)),

# ------------------------------------------------------------------ mn15
# why: "It was agreed to consider" moving the market to Saturdays = a plan to consider, not a
#      decision -> neutral. Twin: "It was agreed that the market will move to Saturdays" -> entailment.
C("mn15", 'What is the relation between the minutes and the hypothesis "The farmers\' market will move to Saturdays"?',
"""
Harlow Cross Business Improvement District — Board Meeting
Minutes of 21 September, 08:00, Guildhall committee room

Present: Rosa Delgado (chair), Anil Chaudhry, Bridget Nolan, Stefan Eriksen, Maryam Aziz. BID manager: Clive Oakes.

1. Footfall. Mr Oakes reported that footfall counters on Cross Street recorded 4% more visitors in August than a year earlier, but 9% fewer on Thursdays, the current market day.

2. Farmers' market. Traders have asked for the monthly farmers' market to be held on a weekend day. It was agreed to consider moving the market to Saturdays at the November board, once Mr Oakes has surveyed the 22 regular stallholders and checked the road-closure rules with the highways team.

3. Christmas lights. The switch-on will be on Friday 27 November. The budget is £8,500.

4. Street cleaning. Ms Nolan reported complaints about litter near the bus station. The BID will fund an extra litter-pick on Sunday mornings for a trial period of three months.

Next meeting: 16 November.
""",
NLI3, "neutral", 2,
twin=T([("It was agreed to consider moving the market to Saturdays at the November board, once Mr Oakes has surveyed the 22 regular stallholders and checked the road-closure rules with the highways team.",
         "It was agreed that the market will move to Saturdays from November; Mr Oakes will write to the 22 regular stallholders and arrange the road closure with the highways team.")], "entailment")),

# ------------------------------------------------------------------ mn16
# why: 48 households, "few were represented" -> most were not -> "a majority represented" not
#      established -> no. Twin: "only four were not represented" -> 44 of 48 -> yes.
Y("mn16", "Do the minutes establish that a majority of the estate's households were represented at the meeting?",
"""
Linton Fields Estate Residents' Association
Minutes of the Open Meeting, Thursday 3 September, 19:00, community room

Attendance. Of the 48 households on the estate, few were represented at the meeting. The committee agreed to put a summary through every door.

Chair: Martha Kinsella. Secretary: Ola Adebayo.

1. Play area. The developer, Hollowbrook Homes, has still not handed the play area over to the council. Ms Kinsella will write to the developer and copy in the local councillor.

2. Speeding. Residents raised concerns about speeding on Linton Drive, especially at school times. The secretary will ask the council to consider a 20 mph limit and will request a speed survey.

3. Management charge. The management company has proposed an annual charge of £220 per household for landscaping and street lighting, up from £185. Several residents asked for a breakdown of the costs. The committee will request one before the charge is accepted.

4. Next open meeting: Thursday 3 December, 19:00.
""",
[ESTABLISH, QUANT], 0, 2,
twin=T([("Of the 48 households on the estate, few were represented at the meeting. The committee agreed to put a summary through every door.",
         "Of the 48 households on the estate, only four were not represented at the meeting. The committee agreed to put a summary through their doors.")], 1)),

# ------------------------------------------------------------------ mn17
# why: budget 64,000; spent to date 51,200 (80%); forecast further 9,600 -> total 60,800,
#      under budget by 3,200. Established: "forecast under budget". Twin: further 14,100 ->
#      total 65,300 -> over budget by 1,300 -> "forecast over budget".
C("mn17", "According to the minutes, which statement about the festival budget is established?",
"""
Clearwater Arts Festival — Steering Group
Minutes of 30 September, 18:00, Clearwater Library

Present: Hugo Marchetti (chair), Sadia Rahman (finance), Ellen Voss, Bartek Nowicki.

1. Budget. Ms Rahman reported that the approved budget for this year's festival is £64,000. Spending to date is £51,200, all of it already paid. The remaining invoices expected are for stage hire, the closing-night fireworks and security, and she forecast that these would come to a further £9,600 in total. No other costs are expected.

2. Ticket sales. Sales reached 3,870 tickets, compared with 4,100 last year. Ms Voss noted that the outdoor events had been free this year, which may explain part of the difference.

3. Volunteers. Ninety-two volunteers took part. The group agreed to hold a thank-you evening in November.

4. Next year. Mr Nowicki suggested moving the festival one week later to avoid a clash with the county show. This will be discussed at the January meeting.
""",
[("forecast under budget", "Total forecast spending (paid plus expected) is below the approved budget."),
 ("forecast over budget", "Total forecast spending (paid plus expected) is above the approved budget."),
 ("forecast exactly on budget", "Total forecast spending (paid plus expected) equals the approved budget."),
 ("more tickets than last year", "More tickets were sold this year than last year."),
 ("festival moves next year", "Next year's festival will be held one week later."),
 ("none of these", "The minutes establish none of the statements above.")],
"forecast under budget", 2,
twin=T([("would come to a further £9,600 in total.", "would come to a further £14,100 in total.")], "forecast over budget")),
]
