"""nli_c / news briefs (city, courts, business, transport, weather, elections)."""
from _lib import C, Y, T, NLI3, REL5, ESTABLISH, FACTIVE, PRESUP, IMPLICATIVE, QUANT, EXCEPT, MODAL, COND, REPORTED

ITEMS = [
# ------------------------------------------------------------------ nw01
# why: "Not every bus route will run" = some routes will not run -> entailment.
#      Twin: "Every bus route will run" -> the hypothesis is false -> contradiction.
C("nw01", 'Hypothesis: "Some bus routes will not run on the new Sunday timetable." What is the relation between the passage and this hypothesis?',
"""
BRENHOLT CITY BRIEF — Wednesday 9 September

Council approves weekend timetable overhaul

Brenholt City Council voted 7–2 on Tuesday evening to adopt the revised weekend timetable proposed by Brenholt Transit, ending a four-month consultation that drew more than 3,100 written responses. The new timetable takes effect on Sunday 4 October.

Under the plan, Saturday frequencies on the six busiest corridors rise from every 20 minutes to every 12 minutes, funded by moving drivers away from lightly used evening services. Not every bus route will run on the new Sunday timetable; routes whose average Sunday boarding fell below 40 passengers per trip last year are being paired with an on-demand minibus zone.

Councillor Hesper Ilunga, one of the two votes against, said the minibus zones "will leave older riders stranded" and asked for a six-month review. The authority's director, Tomas Vey, said a review would be published in April regardless of the council's decision.

Fares are unchanged. Printed timetables will be available at all city libraries from 25 September, and a journey planner goes live online the same day.
""",
NLI3, "entailment", 2,
twin=T([("Not every bus route will run on the new Sunday timetable;", "Every bus route will run on the new Sunday timetable;")], "contradiction")),

# ------------------------------------------------------------------ nw02
# why: "investigators now know that" is factive -> the writer commits to the alarm
#      being switched off at 01:12, forty minutes before the fence was cut -> yes.
#      Twin: "are working on the theory that" is non-factive -> not established.
Y("nw02", "Does the article establish that the depot's alarm was switched off before the fence was cut?",
"""
HARWELL VALLEY GAZETTE — Police & Courts

Break-in at Orrin Street depot under review

Thieves removed roughly £60,000 worth of copper cable from the Kelloway Utilities depot on Orrin Street in the early hours of Saturday, Harwell Valley Police said on Monday. Officers were called at 05:40 by a site supervisor who found a section of the perimeter fence cut.

Detective Sergeant Maren Oduya told reporters that investigators now know that the depot's alarm system had been switched off from inside the control room at 01:12, about forty minutes before the fence was cut. She declined to say who had access to the control room that night. Kelloway said that seven employees hold control-room keycards and that all of them are cooperating.

A 34-year-old man from Delby was arrested on Sunday on suspicion of handling stolen goods after a quantity of cable was found at a scrap yard. He has been released on bail pending further enquiries. Police are appealing for dashcam footage from drivers who used the Orrin Street bypass between midnight and 06:00.
""",
[ESTABLISH, FACTIVE], 1, 2,
twin=T([("investigators now know that", "investigators are working on the theory that")], 0)),

# ------------------------------------------------------------------ nw03
# why: revenue 412.6 vs 381.0 (+8.3%, not >10%); operating profit 31.2 < 34.9 (fell);
#      dividend held; margin recovery only expected by the CEO; "at most two plants could be
#      affected" settles no closure. Only "profit fell while sales rose" is established.
#      Twin: profit 36.4 up from 34.9 -> "operating profit rose" is established instead.
C("nw03", "Which one of the following statements does the report establish?",
"""
MARKETS DESK — Nordvik Business Wire, 14 August

Tarrow Foods posts higher sales, holds dividend

Tarrow Foods, the Nordvik-based maker of chilled ready meals, reported half-year revenue of 412.6 million crowns on Thursday, compared with 381.0 million in the same period last year, an increase of 8.3%. Operating profit was 31.2 million crowns, down from 34.9 million. The board held the interim dividend at 1.10 crowns per share, the same as last year.

Chief executive Ylva Brandt said input costs for dairy and packaging had "stabilised at a high level" and that she expected margins to recover in the second half as price increases agreed with two supermarket chains take effect. Analysts at Oresund Capital called the recovery "plausible but not yet visible in the numbers".

Brandt also confirmed a review of the group's manufacturing footprint, saying that at most two of the company's five plants could be affected. She would not name the sites and said no decision would be taken before November.

Tarrow shares closed 2.1% higher on the day.
""",
[("revenue grew by more than 10%", "Tarrow's half-year revenue was more than 10% higher than in the same period last year."),
 ("operating profit rose", "Tarrow's half-year operating profit was higher than in the same period last year."),
 ("profit fell while sales rose", "Tarrow's half-year operating profit was lower, and its revenue higher, than in the same period last year."),
 ("dividend increased", "The interim dividend per share is higher than last year's."),
 ("margins will recover", "Tarrow's margins will recover in the second half."),
 ("a plant will close", "At least one of Tarrow's five plants will close."),
 ("none of these", "The report establishes none of the statements above.")],
"profit fell while sales rose", 2,
twin=T([("Operating profit was 31.2 million crowns, down from 34.9 million.", "Operating profit was 36.4 million crowns, up from 34.9 million.")], "operating profit rose")),

# ------------------------------------------------------------------ nw04
# why: the falsification appears only as what prosecutors allege; the writer never
#      endorses it -> attributed only. Twin: prosecutors allege a different act
#      (failure to supervise); nobody asserts or attributes falsification -> not settled.
C("nw04", 'How does the court report relate to the hypothesis "Oren Kade falsified the Lintmoor footbridge inspection records"?',
"""
COURT REPORT — Calvern Crown Court, Day 3

Engineer's trial hears from site staff

The trial of Oren Kade, 52, former principal engineer at Brasswick Structures, continued on Wednesday with evidence from two members of the site team that maintained the Lintmoor footbridge before its partial collapse in February, in which three pedestrians were injured.

Prosecutors allege that Mr Kade falsified the inspection records for the Lintmoor footbridge in the eighteen months before the collapse. Mr Kade denies two counts under the Health and Safety at Work Act.

Site supervisor Gemma Rusk told the jury that she had raised concerns about corrosion on the eastern bearing in an email in October 2024. Under cross-examination she agreed that she had not personally seen the inspection sheets that were filed with the county. A second witness, apprentice technician Luka Farrant, said visits to the bridge were "short and irregular" but could not give dates.

The court was shown photographs of the bearing taken by county engineers after the collapse. The trial, expected to last three weeks, continues on Thursday, when a metallurgist instructed by the defence is due to give evidence.
""",
REL5, "attributed only", 3,
twin=T([("Prosecutors allege that Mr Kade falsified the inspection records for the Lintmoor footbridge", "Prosecutors allege that Mr Kade failed to supervise the engineers who inspected the Lintmoor footbridge")], "not settled")),

# ------------------------------------------------------------------ nw05
# why: "closed again" presupposes an earlier closure, so the notice does establish
#      it -> "leave unestablished?" = no. Twin drops "again" and nothing else mentions a
#      previous closure -> unestablished -> yes.
Y("nw05", "Does the traffic notice leave it unestablished that Kessel Bridge had been closed to traffic at some earlier time?",
"""
TRAFFIC & TRAVEL — Lowmarsh Evening Echo

Kessel Bridge closed again from Monday

Kessel Bridge, the single-lane crossing between Lowmarsh and Tedbury, will be closed to all motor traffic from 07:00 on Monday 21 September until further notice, Lowmarsh District Council announced this afternoon. Pedestrians and cyclists will still be able to cross using the protected walkway on the downstream side.

The council said engineers had found movement in two of the bridge's timber deck beams during a routine inspection last week and that the closure was a precaution while a load assessment is carried out. A council spokesperson said it was "too early to say" how long the work would take.

Drivers are advised to use the A418 via Hurst Common, which adds about 11 kilometres to the journey. The number 62 bus will divert the same way and will not serve the stops on Bridge Lane during the closure.

Residents of Bridge Lane will receive a letter explaining parking arrangements for delivery vehicles.
""",
[ESTABLISH, PRESUP], 0, 2, role="neg",
twin=T([("Kessel Bridge closed again from Monday", "Kessel Bridge to close from Monday")], 1)),

# ------------------------------------------------------------------ nw06
# why: "all nine branches except Coldwater and Pym Street" excludes Pym Street, which is
#      one of the branches -> it will not open -> contradiction.
#      Twin: only Coldwater is excepted -> Pym Street opens -> entailment.
C("nw06", 'Given the passage, how should the hypothesis "The Pym Street branch will be open on Saturday 3 October" be classified?',
"""
CULTURE NOTES — Ashby Weekly

Libraries go to seven-day opening

Ashby's library service will open on Saturdays for the first time since 2019, the county's culture committee confirmed this week. From Saturday 3 October, all nine branches except Coldwater and Pym Street will open from 10:00 to 16:00 on Saturdays; the two exceptions are both scheduled for roof repairs this autumn.

The Saturday hours are being paid for from a one-off grant of £410,000 from the Ashby Community Trust, which covers two years of extra staffing. The committee chair, Rukhsana Pell, said she hoped that usage figures would persuade the county to keep the hours when the grant ends.

The Pym Street branch, which houses the county's local history archive, has seen visitor numbers rise by 22% since it began hosting a weekly family-research clinic in January. The archive's online catalogue remains available around the clock.

Opening hours from Monday to Friday are unchanged. The mobile library van will continue to visit villages on its existing fortnightly rota.
""",
NLI3, "contradiction", 2,
twin=T([("all nine branches except Coldwater and Pym Street will open from 10:00 to 16:00 on Saturdays; the two exceptions are both scheduled for roof repairs this autumn.",
         "all nine branches except Coldwater will open from 10:00 to 16:00 on Saturdays; the exception is scheduled for roof repairs this autumn.")], "entailment")),

# ------------------------------------------------------------------ nw07
# why: the reopening is stated only under the unresolved condition of grant approval
#      -> conditional only. Twin: "Now that the grant has been approved" presupposes approval,
#      and the writer states the reopening -> entailed.
C("nw07", 'Hypothesis: "The Halloran Museum will reopen its east wing in the spring." Choose the description that fits.',
"""
ARTS BRIEFING — Tessford Courier

Museum east wing: a timeline at last

The Halloran Museum of Industry has published its plan for the east wing, which has been shut since water damage in 2024 forced the removal of the textile and printing galleries.

If the regional heritage grant is approved at the November panel, the museum will reopen its east wing in the spring with a new permanent gallery on the town's printing trade. The museum has applied for £1.2 million, covering roughly two thirds of the estimated cost; the rest would come from reserves and a public appeal launched last month, which has so far raised £84,000.

The textile collection, currently in storage in Wexley, will not return to the east wing in any case. The museum's board decided in June to lend it long-term to the National Weaving Centre, which has more suitable humidity control.

Director Anouk Petrie described the plan as "achievable and exciting". The west wing, café and learning centre remain open daily except Mondays. The museum's annual print fair will take place in the courtyard on 17 October.
""",
REL5, "conditional only", 2,
twin=T([("If the regional heritage grant is approved at the November panel, the museum will reopen",
         "Now that the regional heritage grant has been approved by the November panel, the museum will reopen")], "entailed")),

# ------------------------------------------------------------------ nw08
# why: 41.2% was exactly 3.0 points lower than last time -> previous = 44.2% > 44% -> yes.
#      Twin: "higher" -> previous = 38.2% -> not over 44% -> no.
Y("nw08", "Does the report establish that turnout at the previous council election was above 44%?",
"""
ELECTION DESK — Merrow Vale Observer, Friday

Lower turnout as independents gain ground

Turnout in Thursday's Merrow Vale District Council election was 41.2%, exactly 3.0 percentage points lower than at the previous council election, according to figures published by the returning officer at 04:30 this morning.

Independent candidates won 14 of the council's 39 seats, up from nine, making them the largest single group. The Civic Alliance, which has run the council since 2018, fell from 17 seats to 12. The remaining 13 seats are split between the Rural Party (8) and the Greens (5). No group has an overall majority, which requires 20 seats.

Returning officer Delphine Achebe said 312 ballot papers were rejected, most because voters had marked more than one candidate in single-member wards. Postal votes made up 38% of all ballots cast.

The leader of the independent group, Farid Olsen, said talks with "all parties willing to put the district first" would begin on Monday. The Civic Alliance group will meet on Saturday to choose a new leader after the defeat of its previous leader in the Harrowgate ward.
""",
[ESTABLISH, ("Percentage point", "the arithmetic difference between two percentages; 41.2% is 3.0 points lower than 44.2%.")], 1, 2,
twin=T([("exactly 3.0 percentage points lower than", "exactly 3.0 percentage points higher than")], 0)),

# ------------------------------------------------------------------ nw09
# why: timeline: smoke detected 02:48; evacuation 02:55; brigade arrived 03:07; power cut 03:20;
#      fire under control 04:40. Power was cut AFTER the brigade arrived -> "brigade before power cut".
#      Twin: power cut at 03:01 -> before brigade (03:07) -> "power cut before brigade".
C("nw09", "According to the report, which statement about the order of events is correct?",
"""
REGIONAL NEWS — Stellby Morning Post

Fire at Ravensmoor recycling plant contained overnight

A fire at the Ravensmoor Materials Recovery Facility was brought under control at 04:40 on Tuesday after firefighters spent almost two hours tackling burning bales of mixed plastics, Stellby Fire and Rescue Service said.

According to the plant's operator, Glenholm Waste Services, smoke was picked up by the thermal cameras in the baling hall at 02:48. The four night-shift workers were evacuated by 02:55 and the fire service was called at the same time. The first crews arrived at 03:07. Glenholm's duty manager cut the power to the whole site at 03:20, after firefighters asked for the conveyor lines to be isolated.

Nobody was hurt. Residents in the Ravensmoor Park estate were asked to keep windows closed until mid-morning. The operator said the baling hall would remain closed while the damage is assessed, and that collections from households would not be affected because material would be diverted to the company's Oxley site.
""",
[("power cut before evacuation", "The site's power was cut before the night-shift workers had been evacuated."),
 ("power cut before brigade", "The site's power was cut before the first fire crews arrived."),
 ("brigade before power cut", "The first fire crews arrived before the site's power was cut."),
 ("brigade before evacuation", "The first fire crews arrived before the night-shift workers had been evacuated."),
 ("control before power cut", "The fire was brought under control before the site's power was cut."),
 ("none of these", "The report establishes none of the statements above.")],
"brigade before power cut", 3,
twin=T([("Glenholm's duty manager cut the power to the whole site at 03:20, after firefighters asked for the conveyor lines to be isolated.",
         "Glenholm's duty manager cut the power to the whole site at 03:01, on the advice of the fire control room.")], "power cut before brigade")),

# ------------------------------------------------------------------ nw10
# why: "has opened an inquiry and might issue a fine" leaves the outcome open -> neutral.
#      Twin: inquiry closed without a fine -> "will end with a fine" is false -> contradiction.
C("nw10", 'Classify the hypothesis "The Maritime Safety Office inquiry into the Sula Star will end with a fine" against the article.',
"""
COAST & SEA — Harrowport Gazette

Ferry overloading: regulator steps in

The Maritime Safety Office has opened an inquiry and might issue a fine once it concludes, after passenger counts showed the Sula Star ferry carried 412 people on a sailing on 29 August when its certificate allows 380. The vessel's operator, Western Isles Link, said a ticketing fault meant that walk-on passengers bought at the harbour kiosk were not counted against the online bookings.

The Sula Star operates four return sailings a day between Harrowport and Inchmory. Islanders' groups have complained about crowding on summer weekends for several years, and the local councillor, Isla Brodie, has asked for a second vessel to be deployed in July and August.

Western Isles Link said it had installed a software patch on 1 September and would now station a member of staff at the gangway with a hand counter on busy sailings. The company said it had "cooperated fully" with the regulator.

No injuries were reported on the 29 August sailing, which crossed in calm conditions.
""",
NLI3, "neutral", 2,
twin=T([("has opened an inquiry and might issue a fine once it concludes,", "closed its inquiry on Friday without issuing a fine,")], "contradiction")),

# ------------------------------------------------------------------ nw11
# why: "Holt succeeded Varga as chair; the latter now leads the audit committee" ->
#      the latter = Varga -> Varga leads audit -> "not established?" = no.
#      Twin: "the former" = Holt leads audit; nothing says Varga does -> yes.
Y("nw11", "Is it not established by the brief that Petra Varga leads the audit committee?",
"""
BUSINESS IN BRIEF — Colbeck Chronicle

Board changes at Hollis Mutual

Hollis Mutual, the Colbeck-based building society, announced changes to its board on Thursday. Anders Holt succeeded Petra Varga as chair at the society's annual meeting on 18 September; the latter now leads the audit committee, a role previously held by Kwame Asante, who is retiring after nine years on the board.

The society also appointed Selin Marwood, a former regional director at the Colbeck Savings Bank, as a non-executive director. Her appointment is subject to regulatory approval, which the society expects before the end of the year.

Hollis Mutual has 61,000 members and 14 branches across the county. Its annual results, published in July, showed mortgage lending up 6% and a small fall in savings balances. At the annual meeting members approved all resolutions, including a change to the rules on electronic voting, with more than 90% support in each case.

The society said its branch network would remain unchanged in 2027.
""",
[ESTABLISH, ("Former / latter", "'the former' refers to the first-mentioned of two people, 'the latter' to the second-mentioned.")], 0, 2, role="neg",
twin=T([("the latter now leads the audit committee", "the former now leads the audit committee")], 1)),

# ------------------------------------------------------------------ nw12
# why: "Contrary to earlier claims, the Varnley Ground will not host the final" is the
#      writer's own assertion -> hypothesis contradicted. Twin: the denial is only the club
#      secretary's insistence -> attributed only.
C("nw12", 'Hypothesis: "The Varnley Ground will host the county cup final." Which description fits the passage?',
"""
SPORT — Halsey & District Advertiser

Cup final venue row rumbles on

Contrary to earlier claims, the Varnley Ground will not host the county cup final on 9 May. The 4,000-capacity stadium, home of Halsey Rovers, had been widely expected to stage the match after the county association's usual venue in Pendry failed a safety inspection in August.

The county association has not yet named an alternative. Its board meets on 12 October, and a shortlist of three grounds is understood to be under consideration. Halsey Rovers chairman Neil Oduro said the club was "disappointed but not surprised", pointing to the cost of the temporary seating the association would have required.

Supporters' groups have started a petition asking for the final to be played at a ground within the county boundary. It had 1,850 signatures by Monday evening.

The cup's semi-finals, scheduled for March, will be played at the grounds of the higher-ranked sides as in previous seasons.
""",
REL5, "contradicted", 2,
twin=T([("Contrary to earlier claims, the Varnley Ground will not host", "Club secretary Dov Harrow insists that the Varnley Ground will not host")], "attributed only")),

# ------------------------------------------------------------------ nw13
# why: "No candidate on the Green list won more than 5%" and Bory is on that list -> Bory
#      won at most 5% -> below 6% -> yes. Twin: "Every candidate ... won more than 5%"
#      gives only a lower bound -> below 6% not established -> no.
Y("nw13", "Does the report establish that Ines Bory received less than 6% of the vote in her ward?",
"""
LOCAL ELECTIONS — Dunmere Standard

Greens fail to break through

The Dunmere Green list fielded candidates in all eleven wards in Sunday's municipal election but will not have a seat on the new council. No candidate on the Green list won more than 5% of the vote in their ward, according to the final count published on Monday.

The list's lead candidate, Ines Bory, a primary-school teacher who stood in the Old Harbour ward, said the party had "planted seeds" and would contest every ward again in four years. The Old Harbour seat was won by Social Forum candidate Mattias Lind with 48% of the vote.

Across the town, the Social Forum won six seats, the Liberal Union four and an independent one. Turnout was 57%, broadly in line with the previous election.

The new council will elect a mayor at its first sitting on 1 October. The Social Forum and the Liberal Union have said they will not govern together, leaving the independent member, Karin Aas, in a pivotal position.
""",
[ESTABLISH, QUANT], 1, 3,
twin=T([("No candidate on the Green list won more than 5% of the vote", "Every candidate on the Green list won more than 5% of the vote")], 0)),

# ------------------------------------------------------------------ nw14
# why: counterfactual "Had the levee been raised in 2019 ... would have" takes for granted
#      the levee was NOT raised in 2019 -> contradiction. Twin: "Because the levee was raised
#      in 2019" asserts it -> entailment.
C("nw14", 'What is the relation between the passage and the hypothesis "The Fenwick levee was raised in 2019"?',
"""
FLOOD REVIEW — Lower Tamsey Journal

Independent review published

The independent review of last winter's flooding in Lower Tamsey was published on Tuesday. It examined the storm of 11–12 January, when the River Tamsey reached its highest level since records began in 1952.

Had the Fenwick levee been raised in 2019, as the drainage board first proposed, the water would have stayed out of the lower town on the night of 11 January. The review's authors, a panel of three engineers from outside the county, found that the storm itself was "exceptional but not unforeseeable" and that forecasts issued on 9 January were broadly accurate.

The review makes 17 recommendations, including new flood gates on Mill Street, a text-alert system for residents of the lower town and a quarterly exercise between the drainage board and the fire service. The drainage board said it accepted all of them and would publish a costed plan by March.

About 140 homes and 30 businesses in Lower Tamsey were affected by the January storm. Most families have now returned home.
""",
NLI3, "contradiction", 3,
twin=T([("Had the Fenwick levee been raised in 2019, as the drainage board first proposed, the water would have stayed out of the lower town on the night of 11 January.",
         "Because the Fenwick levee was raised in 2019, as the drainage board first proposed, the water stayed out of the lower town on the night of 11 January.")], "entailment")),

# ------------------------------------------------------------------ nw15
# why: "did not manage to agree ... before the deadline" -> no deal before the deadline,
#      so the brief fails to establish one -> yes. Twin: "managed to agree" -> established -> no.
Y("nw15", "Does the brief fail to establish that a pay deal was agreed before the midnight deadline?",
"""
WORKPLACE — Brackley Valley News

Bin strike to go ahead after talks end

Negotiators for Brackley Valley Council and the refuse workers' union did not manage to agree a pay deal before the midnight deadline on Sunday, after nine hours of talks at the council's offices in Harn Street.

The union had asked for a flat increase of £1,900 a year for all grades, while the council's final offer was 3.5% for the lowest two grades and 2.5% for the rest. A council spokesperson said the gap between the two positions was "around £410,000 a year" across the workforce of about 180.

The union's regional organiser, Callum Deane, said members would decide at a meeting on Tuesday whether to accept the outcome. Residents have been told to put bins out as normal on Monday. The council said garden-waste collections would be suspended for two weeks in any case while two lorries are repaired.

Recycling centres at Ottery Lane and Fenby will keep their usual opening hours.
""",
[ESTABLISH, IMPLICATIVE], 1, 2, role="neg",
twin=T([("did not manage to agree a pay deal before the midnight deadline on Sunday", "managed to agree a pay deal before the midnight deadline on Sunday")], 0)),

# ------------------------------------------------------------------ nw16
# why: 1,204 respondents. Fewer than half (47%) support; 53% do not -> "a majority do not
#      support". "Not all" drivers oppose. "At most a quarter" would switch. Only the
#      majority-not-support statement follows. Twin: support 52% -> "a majority support".
C("nw16", "Which one of these statements is established by the survey report?",
"""
TRANSPORT — Kelvedon Herald

Congestion charge: survey shows divided town

A survey of 1,204 Kelvedon residents commissioned by the town council found that 47% support the proposed £4 daily charge for driving into the old town between 07:00 and 19:00. The survey was carried out by the independent research firm Colwyn Insight between 1 and 14 September.

Among respondents who drive into the old town at least three times a week, support was lower, at 31%, though not all regular drivers opposed the scheme. At most a quarter of all respondents said they would switch to the bus if the charge were introduced, according to the firm's summary.

Shopkeepers in the Market Square trade group have said they fear a drop in footfall. The council's transport lead, Hanne Doyle, said the survey was "one input among several" and that a formal consultation would open in January.

If introduced, the charge would raise an estimated £2.3 million a year, which the council says would be spent on bus services and cycle lanes.
""",
[("a majority support the charge", "More than half of the survey's respondents support the proposed charge."),
 ("a majority do not support the charge", "More than half of the survey's respondents do not support the proposed charge."),
 ("every regular driver opposes", "All respondents who drive into the old town at least three times a week oppose the charge."),
 ("a quarter would switch", "At least 25% of respondents said they would switch to the bus."),
 ("the charge will be introduced", "The council will introduce the £4 charge."),
 ("shops will lose footfall", "Footfall in the Market Square will fall if the charge is introduced."),
 ("none of these", "The report establishes none of the statements above.")],
"a majority do not support the charge", 3,
twin=T([("found that 47% support the proposed", "found that 52% support the proposed")], "a majority support the charge")),

# ------------------------------------------------------------------ nw17
# why: "tried to block" settles nothing about success -> neutral.
#      Twin: "succeeded in blocking" -> the sale was blocked -> entailment.
C("nw17", 'Hypothesis: "Mayor Linnea Crane blocked the sale of the Eastgate car park." Classify it against the article.',
"""
PLANNING — Oldcastle Times

Eastgate car park sale debated at cabinet

Mayor Linnea Crane tried to block the sale of the Eastgate car park to developer Harbourline Homes at Wednesday's cabinet meeting, arguing that the £3.4 million price undervalued a site in the middle of the town's regeneration zone.

Harbourline plans 96 flats on the site, 20% of them for social rent, above a ground floor of shops. The company has said that 150 public parking spaces would be provided in a new underground car park, compared with 210 today.

The council's finance director, Solomon Achterberg, told the meeting that an independent valuation carried out in April had put the site's value between £3.1 million and £3.6 million. Opposition councillors said the sale should be delayed until the town's new local plan is adopted next year.

Harbourline has said it would submit a planning application within three months of any completed sale. Traders on Eastgate have asked for a guarantee that parking would remain available if construction goes ahead.
""",
NLI3, "neutral", 2,
twin=T([("Mayor Linnea Crane tried to block the sale", "Mayor Linnea Crane succeeded in blocking the sale")], "entailment")),
]
