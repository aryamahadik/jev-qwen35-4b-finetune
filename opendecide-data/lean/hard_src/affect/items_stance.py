"""Affect hard items, batch stance: favor / against / neither toward an explicitly named target."""
from common import S, T

ITEMS = [
# S1 negativity aimed at the mayor, support for the lane; twin retargets to the mayor -> against
S("st_bike_lane_mayor",
"""Letters, The Harlow Courier, 22 September

Sir,

Mayor Tessaly's handling of the Harlow Street works has been a shambles from start to finish: no consultation with the shops, cones left out for six weeks after the paint was dry, and a press release that managed to get the name of the street wrong. I voted for her last time. I won't be making that mistake again.

But let's not throw the lane out with the mayor. Since it opened I have cycled my daughter to Harlow Primary on it every morning, and for the first time in years I am not holding my breath at the Mill Road junction. The number of parents doing the same has gone from two or three to a small peloton. The traffic survey the council published last week shows journey times for cars on the street are within a minute of what they were before.

Yours,
Nia Castellano, Mill Road""",
"the Harlow Street bike lane", "favor", 2,
twin=T([], "against", x="Mayor Tessaly")),

# S2 conditional support with unmet condition -> against; twin meets condition -> favor
S("st_library_levy",
"""Brennan County Community Board > Elections > "Prop 12 - library levy, how are people voting?"

Reply from marguerite_h:

I've volunteered at the Brennan Falls branch every Tuesday for twelve years. I run the toddler story hour. I know better than most what the branches need: the roof over the children's section has leaked for three winters and the computers are older than some of the teenagers using them.

I'd vote yes on 12 in a heartbeat if it had a sunset clause, because I won't put my name to a permanent tax with no review, however much I love those branches. Read section 4 of the measure yourselves: there isn't one; the levy runs indefinitely with no review.

The county's voter guide has the full text on page 31, and the League's forum is on the 9th at the Grange Hall if you want to ask the sponsors directly.""",
"Proposition 12 (the Brennan County library levy)", "against", 2,
twin=T([("there isn't one; the levy runs indefinitely with no review.",
         "there is one; the levy expires after ten years unless voters renew it.")], "favor")),

# S3 reports neighbours' views, asks questions -> neither; twin endorses -> against
S("st_wind_farm_neighbours",
"""Gull Bay Residents (community page) - post by Sunita Rahman

Quick question for anyone who follows planning stuff. My neighbours on Gull Lane are up in arms about the wind farm. Marion at number 6 says it'll wreck the view from the headland, and Dev across the road thinks the noise will carry over the bay at night because sound travels over water.

Does anyone know when the planning hearing is, and whether you can speak at it without registering beforehand? I've also heard the developer is running a drop-in session at the sailing club on the 14th. Is that open to everyone or only to club members? And is there anywhere online to see the photomontages?

Thanks in advance. Also, whoever left a blue child's bike by the slipway, it's now in the porch of the sailing club.""",
"the proposed Kestrel Point wind farm", "neither", 2,
twin=T([("Marion at number 6 says it'll wreck the view from the headland,",
         "Marion at number 6 says it'll wreck the view from the headland, and having seen the developer's own mock-ups I'm afraid she's right,")],
       "against")),

# S4 sarcasm -> against
S("st_stadium_subsidy",
"""Posted to the Riverside Civic Forum, thread "Council budget 2027 - first look", by user eastgate_mum

Oh, marvellous. The council has found £40 million for a "world-class" stadium subsidy, while the Eastgate library still can't open on Sundays and the Hythe Road pool has been shut for two years "pending funding". Truly visionary priorities. I'm sure the Thunder's owners, who reported a £12 million profit last season, will be deeply moved by our generosity.

For anyone who wants to check the numbers themselves: the subsidy is on page 14 of the budget papers, the library and pool lines are on page 22, and the consultation closes on 31 October. You can respond online or in writing to the Town Hall.""",
"the Riverside stadium subsidy", "against", 1),

# S5 favor by knocking down critics' argument (no explicit "support")
S("st_pedestrianisation",
"""Comment on the Fenwick Gazette article "Traders warn pedestrian zone will be 'final nail' for Fenwick Street"

Comment by h.okonjo:

Everyone claiming pedestrianisation will kill the shops on Fenwick Street should read the council's own trial data from the Corn Market last summer, which is linked at the bottom of this article and which the article somehow doesn't mention. Footfall was up 18% on the same months the year before. Card takings at the participating shops were up 11%. Two empty units were let during the trial period.

The "nobody will come if they can't park outside the door" argument was made about the Corn Market too, word for word, by some of the same people quoted here. It was wrong then. The car park on Tanner's Lane is three minutes' walk from the far end of Fenwick Street.""",
"the Fenwick Street pedestrianisation", "favor", 2),

# S6 supporting the only rival -> against; twin makes the race different -> neither
S("st_ward3_byelection",
"""Neighbourhood newsletter, Ashby Rise - "Your vote on 16 October"

The Ward 3 by-election is on Thursday 16 October. The Ward 3 race is between Deng Hollis and Ines Varga.

Personal note from your newsletter editor, Carys Whitfield: I'm voting for Deng. He turned up to the flooding meeting at St Aidan's in March, which his opponent did not, he stayed until the last question, and he has promised in writing to push the drainage survey through before winter. That matters to those of us on the lower end of Ashby Rise, where four houses flooded last year.

Whoever you vote for, please vote. Turnout at the last by-election was 19%. Polling station: St Aidan's church hall, 7 AM to 10 PM. Postal votes must arrive by 5 PM on the day.""",
"Ines Varga", "against", 3,
twin=T([("The Ward 3 race is between Deng Hollis and Ines Varga.",
         "Ines Varga is standing unopposed in Ward 5; the Ward 3 race is between Deng Hollis and Aled Price.")],
       "neither")),

# S7 explicit undecided -> neither
S("st_four_day_week",
"""Linwood Unified Parents' Forum - thread "Four-day week proposal: thoughts?"

Post by Oyelaran family:

The board's proposal would move all schools to a four-day week from next August, Monday to Thursday, with each day 70 minutes longer.

Pros for us: our eldest could join the Friday apprenticeship programme at the college, which currently clashes with school. The district says it would help recruit teachers, and we've lost three good ones in two years.

Cons: I work Fridays and childcare for the younger two would be about £60 a day. Our youngest is already exhausted by 3 PM; I can't picture him lasting until 4:10.

Teachers I've spoken to are split down the middle. I honestly haven't made up my mind, and I'd really like to hear from anyone whose district has actually tried it before the board meeting on the 20th.""",
"the four-day school week proposal", "neither", 1),

# S8 mocking faint praise -> against
S("st_town_logo",
"""Comments under the Cranmere Town Council post: "Introducing our new town identity!"

Comment by Pippa Lowndes:

Well. It's certainly... a logo. It has letters in it, and some of them are blue. I'm sure the £9,000 consultancy fee was money well spent on those letters.

My seven-year-old asked me why the heron looks like a hairdryer, and I genuinely didn't have an answer for her. We then spent a pleasant ten minutes trying to decide whether the wavy line underneath is the river or the hairdryer's cable.

The council says it will appear on bins, vans and the new welcome signs from January. I look forward to explaining it to visitors.""",
"the new Cranmere town logo", "against", 1),

# S9 endorsed quote -> against; twin rebuts the quote -> favor
S("st_millbank_rezoning",
"""Planning committee hearing, Millbank rezoning (application MB/26/114) - written submission from a resident, Ahmed Qureshi, read into the record

Gloria Tan said it best at the first hearing: "This rezoning is a giveaway to developers dressed up as housing policy." I couldn't have put it better. Four-storey blocks where the local plan promised family homes, and not one affordable unit guaranteed in writing.

I have lived on Canal Row for thirty-one years. I have seen the Millbank site go from a dye works to a car park to a fenced-off field, and I want something built there as much as anyone. I have attended both consultation events and read the officers' report in full.

I would ask the committee to note that the traffic assessment was carried out during the school holidays.""",
"the Millbank rezoning", "against", 2,
twin=T([("I couldn't have put it better. Four-storey blocks where the local plan promised family homes, and not one affordable unit guaranteed in writing.",
         "With respect, she's wrong: this is the first time in twenty years the borough has zoned for family homes at all, and 30% affordable is written into the conditions.")],
       "favor")),

# S10 anger at the company, favor toward the product
S("st_tern4_reader",
"""Customer review - Tern 4 e-reader (Veldt Devices) - rating: 3 of 5
Title: "One star for Veldt, five for the Tern"

The three stars are an average, so let me split them. Veldt Devices' support is dreadful. My unit arrived without a charger, it took them three weeks to reply, and the reply was a template telling me to "check the box again".

The Tern 4 itself, though, is the best e-reader I have owned, and I've had four. The screen is the crispest I've seen on any e-ink device, the battery went five weeks on one charge, page turns are instant, and the warm-light slider actually goes warm enough to read in bed without keeping me up. I have already bought one for my mother, which tells you something.

Get the charger separately if you order one.""",
"the Tern 4 e-reader", "favor", 2),

# S11 glad it was scrapped (double negative) -> against the curfew
S("st_youth_curfew",
"""Opinion column, Harrowgate Weekly, "From the rec ground" by Delroy Mensah, youth football coach

I can't pretend I'm not glad the council has finally scrapped the youth curfew. For three years, anyone under 16 on the rec ground after 9 PM was moved on by the wardens, including my under-15s walking home from training in their kit.

The council's own figures, published last month, show antisocial-behaviour reports in the zone went up, not down, over the three years. The lads I coach stopped using the floodlit pitch in the evenings and started hanging round the multi-storey instead, which is darker, further from home and nobody's idea of an improvement.

The pitch is booked again from 7 to 9 on Tuesdays and Thursdays. New players welcome; bring boots and a water bottle.""",
"the Harrowgate youth curfew", "against", 2),

# S12 both sides, decision deferred -> neither
S("st_hospital_merger",
"""Post in a private staff group, Teal Harbor Hospital nurses, by Charge Nurse Imani Okafor

A few people have messaged asking how I'm voting in the staff ballot on the merger, which closes Friday.

Here's where I am. The union has recommended a no vote because of the proposed rota changes, and having read the rota pack, those changes would hurt, especially for anyone with school-age kids. Management says joining Crestline is the only way to keep the cardiac unit open, and having worked in cardiac for nine years I know what losing it would mean for patients in this town.

I'm going to the Q&A on Wednesday and I'll decide after that. I genuinely don't know yet, so please don't take anything I've said as a recommendation either way. The Q&A is in the education centre at 12:30 and 18:30.""",
"the merger between Teal Harbor Hospital and Crestline Health", "neither", 2),

# S13 negative words but favor
S("st_sunday_opening",
"""Letter to the Friends of Eastgate Library newsletter

It is absurd that the one day most working parents can bring their children to the library is the one day it is locked. Every Sunday this month I have watched families walk up to the door, read the opening-hours sign and turn round. One father had come on two buses.

The council keeps telling us there is no budget. The Friends have now offered to staff the front desk on Sundays with trained volunteers, as they do in Morrow and Hythe, so the only real cost is heating and a duty librarian. When I asked the ward councillor about it she said it was "under review". It has been under review since 2023.

Rafaella Duarte, Eastgate""",
"Sunday opening at the Eastgate library", "favor", 2),

# S14 personal loss but accepts and supports the ban
S("st_beach_dog_ban",
"""Hollins Bay Dog Walkers (group page) - post by Martin Okeke

Some of you have asked why I haven't signed the petition against the seasonal dog ban on the beach.

Biscuit and I walked Hollins Beach every morning for nine years, so believe me, I'm not happy about losing it from March to July. But the ringed plovers nest right on the strandline, and the warden's count shows two chicks fledged last year, against eleven the year before dogs were allowed on in spring. Rules like this exist for a reason, and five months isn't forever.

We walk round the reservoir now. It's flatter, which Biscuit's hips appreciate, and there's a van that does decent coffee at the north car park. The petition is on the town noticeboard if you do want to sign it.""",
"the seasonal ban on dogs at Hollins Beach", "favor", 2),

# S15 rhetorical sarcasm -> against
S("st_quay_meters",
"""Quay Street Traders' WhatsApp, message from Bernadette (Bernie's Books), Monday 08:50

Because what Quay Street's half-empty shops really need is to charge their customers £2 an hour for the privilege of visiting them. Brilliant. Next, perhaps a toll on the door handles.

For those who weren't at Thursday's meeting: the council's proposal is meters on both sides of Quay Street, 8 AM to 6 PM, six days a week, from January. The consultation leaflet says it will "improve turnover of spaces". There are currently eleven empty units on the street.

I've printed the consultation form and left copies on my counter. Deadline is 14 November.""",
"the proposed parking meters on Quay Street", "against", 1),

# S16 disagrees on specific policies but favors the person; twin -> against
S("st_headteacher_brook",
"""Speech by a parent governor, Owen Radley, at the leaving assembly for Headteacher Anneliese Brook (transcript supplied by the school office)

I'll be honest, because Ms Brook always was. I've disagreed with almost every decision she has made on uniforms and phones, and I said so at governors' meetings, sometimes louder than I should have.

But she has been a superb head for this school: results up, exclusions down, and she knows the name of every one of the six hundred children who walk through that gate. I'm sorry to see her go.

On behalf of the governing body, the leaving gift will be presented by the head boy and head girl. Parents are invited for tea in the hall afterwards; please use the Mill Lane entrance, as the car park is closed for resurfacing.""",
"Headteacher Anneliese Brook", "favor", 2,
twin=T([("But she has been a superb head for this school: results up, exclusions down, and she knows the name of every one of the six hundred children who walk through that gate. I'm sorry to see her go.",
         "And the rest of her record has been no better: results flat, exclusions up, and staff turnover the highest in the county. I won't pretend I'm sorry to see her go.")],
       "against")),

# S17 reporter summarising both sides -> neither
S("st_solar_farm_report",
"""Aldermoor Messenger - Parish council meeting report, 3 September, by our correspondent

About eighty residents crowded into the village hall on Tuesday for the first public discussion of the proposed Aldermoor solar farm, which would cover 94 acres of Hill Farm.

Ruth Gale, whose family has farmed Hill Farm for four generations, said the lease income would "secure the farm's future for my children". Kenji Ward, of Lower Aldermoor, said it would cover the best grazing land in the parish and that the glare study had been done in winter. Several residents asked about construction traffic on School Lane; the developer's representative said deliveries would avoid school hours.

The parish council will give its formal view on 1 October. The district council makes the final decision. Next week: the bypass consultation.""",
"the Aldermoor solar farm", "neither", 1),

# S18 internal memo with caveats -> favor
S("st_remote_first",
"""To: Leadership team, Corvane Systems
From: Asha Patel, Staff Engineer, Platform
Re: Remote-first pilot - results and recommendation

The twelve-month remote-first pilot ends in November. The numbers for the platform team: deploy frequency up 14%, incident response times unchanged, and voluntary attrition down from 11% to 6%. Two concerns are worth taking seriously. Onboarding for graduates has been slower, and cross-team design reviews take longer to schedule.

Both look fixable with a quarterly in-person week and a buddy scheme for new starters, which the infrastructure team has already trialled. I would ask that the decision on 30 October make the remote-first arrangement permanent, with those two changes attached.

Happy to walk anyone through the raw data before the meeting.""",
"permanent remote-first working at Corvane Systems", "favor", 1),

# S20 hates the interface, recommends the app -> favor
S("st_kestrel_app",
"""Forum: Budget Phones & Plans > Kestrel Mobile > "Is the Kestrel app worth installing?"

Reply by tomas_v:

The Kestrel app has one of the ugliest interfaces I've used in years. Dark mode turns half the text invisible, the menu is hidden behind an icon that looks like a sandwich, and it logs you out every time there's an update.

Still, it's the only one of the three providers' apps I've tried that shows live data usage per day, and since I started checking it my bill has dropped by about £12 a month because I stopped blowing through my allowance by the 20th. If you're on Kestrel, install it. Just turn dark mode off.""",
"the Kestrel Mobile app", "favor", 2),

# S21 opposing one of three candidates -> neither toward Quell; twin two-candidate race -> favor
S("st_rowing_president",
"""Harbourside Rowing Club - members' email list
From: Gwen Aldous
Subject: AGM Saturday - please read before you vote

There are three candidates for president this year: Rob Tanaka, Marta Quell and Idris Ferris.

Whatever you do, please don't vote for Rob. He's the one who proposed selling the second boathouse last year to cover the clubhouse roof, and he has said at two committee meetings since that he would bring it back. Without that boathouse the juniors have nowhere to store their boats.

Practicalities: proxy forms have to be with the secretary by Thursday at 6 PM. The AGM starts at 10 on Saturday in the clubhouse, with coffee from 9:30. The accounts are attached as a PDF.""",
"Marta Quell", "neither", 3,
twin=T([("There are three candidates for president this year: Rob Tanaka, Marta Quell and Idris Ferris.",
         "There are two candidates for president this year: Rob Tanaka and Marta Quell.")],
       "favor")),

# S22 "I support campus safety" framing -> against the proposal
S("st_arm_security",
"""The Ferrow Lantern (student newspaper) - Opinion
"Safer campus, not more guns" by Priyanka Venkat, Students' Union welfare officer

I support campus safety wholeheartedly, which is exactly why I'm writing this. On 12 November the trustees will vote on the proposal to issue firearms to all forty campus security officers.

These are the same officers who currently deal with lockouts, noise complaints and students who have had too much to drink on a Friday. The two universities in the region that armed their officers in 2023 recorded no drop in serious incidents, but both saw use-of-force complaints more than double. The £1.2 million budgeted for weapons and training would fund two years of the late-night safe-walk service that the trustees cut last spring.

Write to your faculty trustee before the 12th. Their addresses are on the Union website.""",
"the proposal to arm campus security officers", "against", 2),

# S23 criticises the process, explicitly no view on the person -> neither
S("st_voss_appointment",
"""Message posted in the staff-side channel of the Joint Consultative Committee, St Brannoc's Hospital, by Kwame Asante (Unison rep)

Several people have asked me whether staff side "has a position" on Dr Helena Voss. For clarity: I have never worked with Dr Voss and I have no view on her one way or the other; I'm told she was well regarded at her last trust, and she may turn out to be excellent.

What I do have a view on is the way the chief medical officer appointment was handled. There was no interview panel, no shortlist was published, and staff side were not consulted at any stage, which is contrary to the agreed recruitment policy (section 7.3). That is what I'll be raising at Thursday's JCC, and that is the only thing I'll be raising.""",
"Dr Helena Voss", "neither", 3),

# S24 complaint about costs, then "worth it" -> favor; twin "not worth it" -> against
S("st_cup_ban",
"""Ferrow Students' Union forum - thread "Single-use cup ban: one month in"

Post by jas_k:

So the campus cafés banned single-use cups in September. The "free" reusable cup they handed out ran out in the first week, and now it's £4 for one, which is steep when you're living on a loan. I've forgotten mine three times and gone without coffee before a 9 AM lecture, which nobody should have to experience.

Honestly? Worth it for the state of the bins alone. Last year the bins outside the library were overflowing with cups by eleven every morning and the wind blew them all over the lawn.

If anyone has a spare reusable cup, the Union shop is taking donations to give away to first-years.""",
"the ban on single-use cups at the Ferrow campus cafés", "favor", 2,
twin=T([("Honestly? Worth it for the state of the bins alone.",
         "Honestly? Not worth it, whatever the bins used to look like.")], "against")),

# S25 view only on opening hours, indifferent to location -> neither
S("st_market_move",
"""Comment on the council's consultation page: "Proposed relocation of the Saturday farmers' market"

Comment by Hollie Brennan:

The council wants to move the Saturday farmers' market from the ring-road lay-by to the Old Quay car park. Honestly, I don't mind where it goes: lay-by, car park, top of the cathedral tower. What I care about is the time. The consultation document mentions "reviewing trading hours". If the market starts at 10 instead of 8, I will never get there before my shift at the care home, and neither will half the people I work with.

Please keep the 8 AM start, wherever the stalls end up. And please keep the cheese man.""",
"moving the farmers' market to the Old Quay car park", "neither", 3),

# S26 "against road closures in general" but favors this one
S("st_wickham_road",
"""Letter to the editor, Southmead Post

I am against closing roads in general. I drive for a living, I think most "low-traffic" schemes simply push the traffic onto the next street, and I have written to this paper saying so more than once.

Wickham Road is the exception. Since the satnav apps discovered it, it has become a rat run of 900 cars an hour at school-run time, past the gates of Wickham Road Primary, on a street with no crossing and pavements you can't fit a pushchair on. My granddaughter goes to that school. The council's plan to close it to through traffic at the junction with Beech Avenue is the first sensible thing I have seen from the highways department in years.

Alan Pritchard, Southmead""",
"the plan to close Wickham Road to through traffic", "favor", 2),

# S27 backing the rival in a two-person election -> against
S("st_branch_secretary",
"""Email to members, Riverside branch, Allied Transport Workers
From: Colette Nwosu, shop steward, Depot B
Subject: Branch secretary ballot

The ballot for branch secretary opens on Monday. There are two nominations: Aurora Sato, the sitting secretary, and Deshawn Price, currently health and safety rep at Depot A.

Aurora has done a decent job, and I want to say that clearly because this isn't personal. But I believe no one should hold a branch office for more than two terms, and this would be Aurora's fourth. I'll be backing Deshawn.

Ballot papers go out by post. If yours hasn't arrived by Wednesday, contact the regional office on the number on your membership card.""",
"Aurora Sato", "against", 2),

# S28 defends the ban against "nanny-state" critics -> favor
S("st_reservoir_ban",
"""Comment by a volunteer lifeguard, Glenmoor Water Safety Group, under the article "Swimmers defy reservoir ban as heatwave continues"

Every summer our volunteers pull someone out of Glenmoor. The surface feels warm on a hot day, but two metres down the water is nine degrees, and there are intake pipes and old fencing under the surface near the dam. Cold-water shock doesn't care how strong a swimmer you are.

People in these comments are calling the ban nanny-state nonsense. They've never done CPR on a sixteen-year-old on the dam wall while waiting for the air ambulance. I have, twice.

If you want to swim, the lido at Harlow Park is open until 8 PM through the heatwave and has lifeguards on duty.""",
"the swimming ban at Glenmoor Reservoir", "favor", 1),

# S29 explicitly neutral question -> neither; twin adds a verdict -> against
S("st_tunnel_bond",
"""Harbourside Voters' Forum - new thread by user r_achterberg
Title: "Harbour Tunnel bond - what does it actually pay for?"

Can someone explain what the Harbour Tunnel bond on next month's ballot actually pays for? I've seen leaflets saying it's £300 million and others saying £500 million once interest is included. One says it covers the approach roads and the other says the approach roads are a separate scheme.

I'd also like to know what happens to the ferry subsidy if it passes, because I use the 07:15 ferry every day.

Not taking sides, just want the facts before I fill in my postal vote. Links to the official documents would be ideal.""",
"the Harbour Tunnel bond", "neither", 1,
twin=T([("Not taking sides, just want the facts before I fill in my postal vote.",
         "Either way, I'm not signing my grandchildren up for £500 million of debt, but I'd like the facts before I fill in my postal vote.")],
       "against")),

# S30 sarcasm aimed at the target's critics -> favor
S("st_tram_timetable",
"""Parkside Commuters (group chat), Monday 07:48

Message from Lotte Baptiste:

Can't believe I now have to wait a whole FOUR minutes for a tram at peak time. What an outrage. Somebody alert the newspapers.

The people in this chat complaining about the new timetable have clearly forgotten waiting twenty-five minutes in the rain at Carrow Street for the old one, only for two trams to turn up together, both full.

Yes, the last tram is now 23:20 instead of 23:45, and yes, that's a pain after the theatre. There's a night bus, the N4, from outside the Grand at 23:50.""",
"the new Parkside tram timetable", "favor", 2),

# S31 named speaker in a hearing transcript: abstains -> neither
S("st_skatepark_hearing",
"""Clearwater Borough Council - Parks Committee, 14 October - extract from the verbatim record
Item 5: Proposed skatepark, Clearwater Park (north field)

Mrs Janet Hollis (resident, Park Terrace): I've lived opposite that field for twenty-six years. A concrete bowl with lights until 9 PM will mean noise every evening from March to October. I'm asking the committee to refuse it.

Mr Tunde Bakare (youth worker, Clearwater Youth Project): Our young people have been asking for this for five years. Right now they skate in the multi-storey car park. This would give them somewhere safe and visible.

Councillor Bram Olsen: I've listened carefully tonight and both sides have real merit. I'll be abstaining on this vote, and I'd ask officers to come back to the next meeting with a proper noise study before any decision is taken.

Chair: Thank you. We will now move to the vote.""",
"the Clearwater Park skatepark", "neither", 2, t="Councillor Olsen"),
]
