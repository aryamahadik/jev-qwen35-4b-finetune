"""nli_c / public notices and bulletins (recalls, pay awards, school letters, building
works, bin collections, police appeals). Larger option sets of confusable statements."""
from _lib import C, Y, T

NONE = ("none of these", "The notice establishes none of the statements above.")

ITEMS = [
# ------------------------------------------------------------------ nt01
# why: recalled = 340 g smooth jars, best-before 01/2027-04/2027, EXCEPT batch codes ending -K.
#      02/2027 + code ending -M -> recalled (only true option). -K excepted; 05/2027 outside range;
#      crunchy not affected; no receipt needed; "no injuries reported" does not establish that none
#      occurred; "reports of glass" are reports. Twin: exception becomes -M -> the -K jar is recalled.
C("nt01", "Which one of these statements does the recall notice establish?",
"""
PRODUCT RECALL — Harbrook Foods Ltd
Issued 21 September 2026

Harbrook Smooth Peanut Butter, 340 g glass jar

Harbrook Foods is recalling Harbrook Smooth Peanut Butter in 340 g jars with best-before dates from 01/2027 to 04/2027 inclusive, except jars whose batch code ends in -K, because some jars may contain small pieces of glass. The batch code is printed on the lid next to the best-before date.

No other Harbrook products are affected, including Harbrook Crunchy Peanut Butter and the 1 kg catering tubs.

What to do: do not eat the product. Return it to any store that sells Harbrook products for a full refund. You do not need a receipt.

Harbrook has received two customer reports of glass in jars. No injuries have been reported to the company to date.

This recall has been agreed with the Food Standards Unit. For questions, call the Harbrook careline on 0800 555 0172 (09:00–17:00, Monday to Friday).
""",
[("-K jar recalled", "A 340 g smooth jar with best-before 02/2027 and a batch code ending in -K is recalled."),
 ("-M jar recalled", "A 340 g smooth jar with best-before 02/2027 and a batch code ending in -M is recalled."),
 ("05/2027 jar recalled", "A 340 g smooth jar with best-before 05/2027 is recalled."),
 ("crunchy recalled", "Harbrook Crunchy Peanut Butter is recalled."),
 ("receipt needed", "Customers need a receipt to get a refund."),
 ("nobody was injured", "Nobody has been injured by glass in a Harbrook jar."),
 ("glass was found", "Glass has been found in at least one Harbrook jar."),
 ("catering tubs recalled", "The 1 kg catering tubs are recalled."),
 ("refund only at purchase store", "Refunds are available only at the store where the jar was bought."),
 NONE],
"-M jar recalled", 3,
twin=T([("except jars whose batch code ends in -K,", "except jars whose batch code ends in -M,")], "-K jar recalled")),

# ------------------------------------------------------------------ nt02
# why: grades 1-4 get 4.0%, 5-6 get 3.0%, 7+ "at most 2.0%" set in November; staff still on
#      probation on 1 Oct get it when probation ends. Eamon: grade 2, probation ended 15 Sept ->
#      4% from 1 Oct (only true option). Bruno on probation to 30 Nov (delayed); Chen grade 7 ->
#      at most 2%, exact not set; Dalia grade 6 -> 3%. Twin: Eamon's probation ends 15 Oct ->
#      "Eamon's award is delayed".
C("nt02", "Which one of these statements does the pay bulletin establish?",
"""
STAFF BULLETIN — Pay award 2026
Calderbrook Housing Trust — People Team, 24 September

The board has approved this year's pay award, effective from 1 October 2026:

• Grades 1–4: 4.0% increase.
• Grades 5–6: 3.0% increase.
• Grade 7 and above: an increase of at most 2.0%, to be set individually by the remuneration committee at its November meeting and backdated to 1 October.

Staff who are still in their probation period on 1 October will receive the award from the day after their probation ends.

Examples from the Lettings team (shared with the individuals' permission):
– Amaka Obi, grade 3, joined 2019.
– Bruno Sala, grade 5, probation ends 30 November.
– Chen Wei, grade 7, joined 2016.
– Dalia Nour, grade 6, joined 2021.
– Eamon Keogh, grade 2, probation ended 15 September.

Payslips for October will show the new rates, except where the remuneration committee has not yet decided.
""",
[("Bruno gets 3% from 1 October", "Bruno Sala's 3.0% increase applies from 1 October."),
 ("Chen gets exactly 2%", "Chen Wei's increase is exactly 2.0%."),
 ("Chen gets more than 2%", "Chen Wei's increase is more than 2.0%."),
 ("Dalia gets 4%", "Dalia Nour receives a 4.0% increase."),
 ("Eamon gets 4% from 1 October", "Eamon Keogh's 4.0% increase applies from 1 October."),
 ("Eamon's award is delayed", "Eamon Keogh's increase starts later than 1 October."),
 ("every grade gets at least 2%", "Every member of staff receives an increase of at least 2.0%."),
 ("grade 7 set in October", "Increases for grade 7 and above are set at an October meeting."),
 ("Bruno gets nothing this year", "Bruno Sala receives no increase from this award."),
 NONE],
"Eamon gets 4% from 1 October", 3,
twin=T([("– Eamon Keogh, grade 2, probation ended 15 September.", "– Eamon Keogh, grade 2, probation ends 15 October.")], "Eamon's award is delayed")),

# ------------------------------------------------------------------ nt03
# why: 52 of 58 forms returned -> 6 outstanding -> "fewer than ten outstanding" (only true).
#      "only if" makes a form necessary, not sufficient -> "all 52 will go" not established;
#      contribution is voluntary; trip on Thursday. Twin: 46 of 58 -> 12 outstanding ->
#      "more than ten forms outstanding".
C("nt03", "Which one of these statements does the newsletter establish?",
"""
Fellbrook Primary School — Friday Newsletter, 25 September

Year 5 trip to the Marshgate Wetland Centre

Year 5 will visit the Marshgate Wetland Centre on Thursday 8 October as part of their science topic on habitats. The coach leaves school at 09:15 and returns by 15:10.

Pupils may go on the trip only if a signed consent form has been returned to the school office by Friday 2 October. So far, 52 of the 58 pupils in Year 5 have returned their forms. Thank you to everyone who has already sent them back.

We ask for a voluntary contribution of £6 towards the cost of the coach. No child will be left out because a contribution has not been made.

Children will need a packed lunch (or can order one from the kitchen by Tuesday), wellies and a waterproof coat. Please do not send glass bottles or nut products.

Other dates: harvest assembly on Friday 16 October, 09:00, in the hall — all families welcome.
""",
[("every form returned", "Every Year 5 pupil has returned a consent form."),
 ("more than ten forms outstanding", "More than ten Year 5 pupils have not yet returned a consent form."),
 ("fewer than ten forms outstanding", "Fewer than ten Year 5 pupils have not yet returned a consent form."),
 ("contribution is compulsory", "Pupils must pay £6 to go on the trip."),
 ("a pupil without a form may go", "A pupil whose consent form is not returned by 2 October may still go on the trip."),
 ("the trip is on a Friday", "The Wetland Centre trip takes place on a Friday."),
 ("all 52 will go", "Every pupil who has returned a form will go on the trip."),
 ("lunch is provided free", "Every pupil receives a free lunch on the trip."),
 NONE],
"fewer than ten forms outstanding", 2,
twin=T([("So far, 52 of the 58 pupils in Year 5", "So far, 46 of the 58 pupils in Year 5")], "more than ten forms outstanding")),

# ------------------------------------------------------------------ nt04
# why: floors 1-3 off Tue 09:00-12:00, floors 4-6 off Tue 13:00-16:00, floors 7-8 off Wed
#      09:00-11:00. Flat 5B (floor 5) has water at 10:00 Tue (only true). 2A off at 10:00; lifts
#      are off only during the Wed 09-11 shutdown, so nothing is said about Wed 12:00.
#      Twin: floors 4-6 move to 09:30-12:30 -> 5B dry at 10:00, wet at 14:00.
C("nt04", "Which one of these statements does the building notice establish?",
"""
NOTICE TO RESIDENTS — Quayside Heights (floors 1–8)
From: Estates Office, Tidemark Residential Management
Posted: Friday 2 October

Planned water shut-off for riser valve replacement

To replace the corroded valves on the main water riser, the cold and hot water supply will be switched off floor by floor as follows:

• Floors 1–3: Tuesday 6 October, 09:00–12:00
• Floors 4–6: Tuesday 6 October, 13:00–16:00
• Floors 7–8: Wednesday 7 October, 09:00–11:00

The lifts will not operate during the floors 7–8 shutdown, because the lift motor room shares the upper riser.

Please fill a kettle and a few bottles before your shut-off starts and avoid using washing machines or dishwashers during it. When the water comes back on, run the cold tap for two minutes.

Flat numbers begin with the floor number (for example, flat 5B is on floor 5).

If anyone in your household relies on water for medical equipment, please contact the Estates Office on extension 200 so we can make arrangements.
""",
[("5B has water Tue 10:00", "Flat 5B has a water supply at 10:00 on Tuesday 6 October."),
 ("5B has water Tue 14:00", "Flat 5B has a water supply at 14:00 on Tuesday 6 October."),
 ("2A has water Tue 10:00", "Flat 2A has a water supply at 10:00 on Tuesday 6 October."),
 ("7C has water Wed 10:30", "Flat 7C has a water supply at 10:30 on Wednesday 7 October."),
 ("lifts off Wed 12:00", "The lifts are not operating at 12:00 on Wednesday 7 October."),
 ("whole building off at once", "At some point every floor is without water at the same time."),
 ("work ends Tuesday", "All the shut-offs are finished by the end of Tuesday 6 October."),
 ("only cold water affected", "The hot water supply is not affected by the works."),
 ("lifts off on Tuesday", "The lifts are not operating during the Tuesday shut-offs."),
 NONE],
"5B has water Tue 10:00", 3,
twin=T([("• Floors 4–6: Tuesday 6 October, 13:00–16:00", "• Floors 4–6: Tuesday 6 October, 09:30–12:30")], "5B has water Tue 14:00")),

# ------------------------------------------------------------------ nt05
# why: week of Mon 21 Dec: one day later except Monday (unchanged). Wed 23 -> Thu 24 (true).
#      Mon 21 unchanged (not 22); Fri 25 -> Sat 26 (not 25); Thu 24 -> Fri 25 (not 26). Week of
#      Mon 28 Dec: two days later: Mon 28 -> Wed 30 (not 29); Wed 30 -> Fri 1 Jan (not 30).
#      Garden waste suspended. Twin: exception is Wednesday -> Wed stays 23; Mon 21 -> Tue 22.
C("nt05", "Which one of these statements does the collection notice establish?",
"""
Wendlebury District Council — Waste & Recycling
Christmas and New Year collection changes

In the week beginning Monday 21 December, all bin collections will take place one day later than usual, except Monday collections, which are unchanged.

In the week beginning Monday 28 December, all bin collections will take place two days later than usual, with no exceptions.

Normal collection days resume from Monday 4 January.

Garden waste collections are suspended from 21 December to 8 January inclusive. Real Christmas trees can be left next to your garden waste bin on your first garden waste collection after 8 January; please remove all decorations and the stand.

Please have your bins out by 06:30 on the day of collection, as crews may start earlier than usual during the holiday period. Extra recycling can be left next to your recycling bin in a clear bag or a cardboard box.

Household recycling centres will close at 13:00 on Christmas Eve and New Year's Eve and will be closed on Christmas Day, Boxing Day and New Year's Day.
""",
[("Monday bins on 22 December", "Households whose usual day is Monday are collected on Tuesday 22 December."),
 ("Wednesday bins on 24 December", "Households whose usual day is Wednesday are collected on Thursday 24 December."),
 ("Friday bins on 25 December", "Households whose usual day is Friday are collected on Friday 25 December."),
 ("Thursday bins on 26 December", "Households whose usual day is Thursday are collected on Saturday 26 December."),
 ("Monday bins on 29 December", "Households whose usual day is Monday are collected on Tuesday 29 December."),
 ("Wednesday bins on 30 December", "Households whose usual day is Wednesday are collected on Wednesday 30 December."),
 ("garden waste on 23 December", "Garden waste is collected on Wednesday 23 December."),
 ("centres open Christmas Day", "Household recycling centres are open on Christmas Day."),
 NONE],
"Wednesday bins on 24 December", 3,
twin=T([("except Monday collections, which are unchanged.", "except Wednesday collections, which are unchanged.")], "Monday bins on 22 December")),

# ------------------------------------------------------------------ nt06
# why: police voice: taken to hospital with a broken wrist; CCTV shows him leaving at 23:52 ->
#      "left before midnight" (only true). Pushing and "three men" are what witnesses say; arrest
#      is on suspicion; he was released; the incident was on Saturday night.
#      Twin: CCTV shows 00:07 -> "left after midnight".
C("nt06", "Which one of these statements does the police appeal establish?",
"""
POLICE APPEAL — Eastmoor Neighbourhood Policing Team
Published Monday 28 September

Appeal for witnesses: Crown & Anchor, Quay Street

A 19-year-old man was taken to hospital with a broken wrist following an incident outside the Crown & Anchor on Quay Street, Eastmoor, late on Saturday 26 September.

Witnesses say the man was pushed to the ground by one of a group of three men who then walked off towards the harbour. CCTV from the pub shows the injured man leaving the premises at 23:52.

A 23-year-old man from Eastmoor was arrested on Sunday on suspicion of assault causing actual bodily harm. He has been released under investigation while enquiries continue.

Officers would like to speak to anyone who was on Quay Street between 23:30 and 00:30, and to anyone with phone or doorbell footage from the area. Please quote reference EM-26-40991.
""",
[("the man was pushed", "The injured man was pushed to the ground."),
 ("three men were involved", "A group of three men was involved in the incident."),
 ("arrested man is the attacker", "The arrested 23-year-old caused the injury."),
 ("arrested man is in custody", "The arrested man is still being held by police."),
 ("left before midnight", "The injured man left the pub before midnight."),
 ("left after midnight", "The injured man left the pub after midnight."),
 ("incident on Sunday", "The incident happened on Sunday 27 September."),
 ("injured man is 23", "The injured man is 23 years old."),
 ("charged with assault", "Someone has been charged with assault."),
 NONE],
"left before midnight", 3,
twin=T([("shows the injured man leaving the premises at 23:52.", "shows the injured man leaving the premises at 00:07.")], "left after midnight")),
]
