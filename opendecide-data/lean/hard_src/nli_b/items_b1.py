"""Part B1: conditionals (if, only if, unless, in case, even if, whether or not, chains, contraposition)."""
from _h import it, L3, L3CARD, FOLLOW, RULED, E, C, U, NONE

ITEMS = [

it("B1", "noul",
   "Can the statement be concluded from the claim file alone?",
   """CLAIM FILE - Harbrook Mutual Insurance, Household Division
Claim no.: HM-26-118804
Policyholder: Ms. Delphine Arkwright, 14 Sorrel Mews
Peril: escape of water (burst pipe under kitchen sink)

Handling rules in force (Claims Manual, section 5.2):
(a) If a claim is filed more than 60 days after the incident, it is referred to the Review Team before any payment is made.
(b) Claims with a reserve above 20,000 pounds are also referred to the Review Team.
(c) Referral does not by itself mean a claim will be declined.

Claim history:
- Loss adjuster Kiran Sethi attended on the Thursday after notification and set a reserve of 24,500 pounds (kitchen units, flooring, drying equipment).
- Claim referred to the Review Team on 9 June.
- Policyholder has asked for an interim payment for alternative cooking facilities; this is on hold until the Review Team has seen the file.

Handler's note: the policyholder was polite but frustrated about the delay; please call her before Friday.

Statement: Claim HM-26-118804 was filed more than 60 days after the incident.""",
   0, card=FOLLOW, diff=2),

it("B2", "choice",
   "How does the returns policy bear on the statement?",
   """Brindle & Loom - Online Returns Policy (excerpt), followed by a customer service case note

Section 3. Refunds
3.1 A refund is issued only if the item is returned within 30 days of delivery.
3.2 Customers pay the return postage unless the item is faulty.
3.3 Refunds go back to the original payment method.

Case note, ticket BL-44871:
Customer Farida Oyelowo returned a wool overcoat (order 7713-QZ). Delivery confirmed on 2 October; parcel received at our returns centre on 14 October. The customer paid her own return postage and did not report a fault. The refund screen for the order has not been updated yet, and the customer is asking when her money will arrive.

Statement: Under the policy, a refund is issued for the overcoat in order 7713-QZ.""",
   U, opts=L3[3], card=L3CARD, diff=2,
   twin=[("3.1 A refund is issued only if the item is returned within 30 days of delivery.",
          "3.1 A refund is issued if the item is returned within 30 days of delivery.")],
   twin_gold=E),

it("B3", "noul",
   "Given the monitoring record, must the statement be true?",
   """Kitchen Food Safety Record - St Brannoc's Care Home, Main Kitchen
Walk-in cold room CR-1: door alarm

Equipment note (from the installer's handover sheet): the CR-1 door alarm sounds unless the door is closed within 90 seconds of being opened. The alarm is wired to the nurse call panel as well as the local sounder, and every activation is logged automatically with a timestamp.

Tuesday 3 March, night shift (20:00 - 08:00):
- Door openings logged: 7 (night cook restocking and one delivery at 05:40).
- Alarm activations logged: none. The alarm did not sound at any point during the night shift.
- Temperatures: 2.8 degC at 22:00, 3.1 degC at 02:00, 3.4 degC at 06:00.
- Night cook: Wendell Achebe.

Day shift manager's comment: the delivery at 05:40 was the new dairy supplier; the driver left the pallet outside the door, and Wendell brought it in.

Statement: On the Tuesday night shift, the CR-1 door was closed within 90 seconds every time it was opened.""",
   1, card=FOLLOW, diff=2),

it("B4", "noul",
   "If everything in the sailing instructions and the notice is true, does it follow that the statement is true?",
   """Wexcombe Sailing Club - Autumn Series, Race 6
Sailing Instructions (extract)

SI 9.2 If the forecast wind at 08:00 on race day exceeds 40 knots in the club's forecast service, the race is cancelled and no race will be rescheduled.
SI 9.3 The Race Officer's decisions under the Racing Rules are final.
SI 14 Boats must sign out at the dinghy park before launching.

Notice posted on the club board at 08:20, Sunday 19 October:
"The 08:00 forecast shows a mean wind of 22 knots, gusting 32, from the south-west, veering west by midday. Launching opens at 09:30. Race briefing in the clubhouse at 09:45. Please take extra care with the slipway, which is slippery at low water. - D. Mallory, Race Officer"

Statement: Race 6 of the Autumn Series was not cancelled.""",
   0, card=FOLLOW, diff=2),

it("B5", "choice",
   "Which label fits the statement, judged against the lease excerpt and the letter?",
   """TENANCY AGREEMENT - 4 Quayside Terrace, Flat 2 (excerpt)

Clause 5. Rent
5.1 The rent is 1,150 pounds per calendar month.
5.2 Rent for each month is due on the 1st day of that month even if the landlord's invoice for that month arrives late or not at all.
5.3 Late payment attracts interest at 3% above base rate from the 15th day after the due date.

Letter from the tenant, Mr. Ravi Castellano, to the managing agent, dated 9 March:
"Dear Hollow Oak Lettings, your invoice for March only reached me on 5 March, four days after the start of the month. As I had nothing to pay against, I assume March rent was not due until your invoice arrived. I have paid it today. Please confirm that no interest will be applied."

Agent's handwritten note on the letter: "Paid 9 March - no interest either way. Reply by Friday."

Statement: Rent for March was not due on 1 March.""",
   C, opts=L3[4], card=L3CARD, diff=2),

it("B6", "noul",
   "Taking the message thread as accurate, is the statement guaranteed?",
   """Messages - Hollow Oak Lettings, property team channel, Wednesday

Maddie (09:12): Rhodri, when you go to the Burrow Lane unit at 10 for the boiler engineer, take the spare key in case the tenant is out. She said she might be at the gym.
Rhodri (09:14): Will do.
Maddie (09:15): The key is in the grey key safe, tag BL-7. Sign it out in the book please.
Rhodri (11:02): Back. The tenant was in when I got there, so the engineer went straight in. Boiler needs a new diverter valve, part ordered, second visit next Tuesday.
Maddie (11:04): Great. Did you do everything I asked?
Rhodri (11:05): Yes, everything, as asked. Book's signed.
Maddie (11:06): Thanks.

Statement: Rhodri took the spare key with him to the Burrow Lane unit.""",
   1, card=FOLLOW, diff=3),

it("B7", "choice",
   "Given only the freight tracker notes, what is the status of the statement?",
   """Veldhoven Logistics - Freight tracker, consignment VL-88-2041 (machine parts, Rotterdam to Graz)

Planning notes (dispatcher, Monday 1 September):
- If the consignment clears customs by Thursday, it goes on Friday's truck to Austria.
- If it goes on Friday's truck, it arrives in Graz by Monday 8 September; that route has never missed its Monday slot.
- If it misses customs on Thursday, it waits for the Tuesday truck.

Event log:
- Tue 2 Sep 14:10 - documents submitted to customs broker.
- Wed 3 Sep 09:30 - broker requested an extra commercial invoice; supplied 11:15.
- Mon 8 Sep 18:00 - customer reports consignment not received in Graz. Tracking confirms: not arrived.
- Tue 9 Sep 07:40 - consignment loaded in Rotterdam.

Customer account manager asked for an explanation to be sent to the client by Wednesday.

Statement: Consignment VL-88-2041 cleared customs by Thursday 4 September.""",
   C, opts=L3[5], card=L3CARD, diff=2),

it("B8", "noul",
   "Does the statement follow from the clinic's policy and the appointment record?",
   """Sandgate Physiotherapy Clinic - Missed Appointment Policy (displayed at reception and on the booking site)

1. A fee of 35 pounds applies to every booked appointment slot.
2. The fee is waived if the appointment is cancelled more than 24 hours in advance.
3. Otherwise, the fee is charged whether or not the patient attends the booked slot.

Appointment record:
Patient: Mr. Leopold Farrant
Booked slot: Thursday 12 June, 14:30, with physiotherapist Anneke Voss
Cancellation: by phone, Thursday 12 June, 08:15 (reason: car trouble)
Later the same day: Mr. Farrant arrived at 16:00 hoping for a walk-in slot; Anneke saw him for 20 minutes between patients.

Receptionist note: patient was very apologetic about the cancellation.

Statement: Mr. Farrant was not charged the 35-pound fee for the 14:30 slot.""",
   0, card=FOLLOW, diff=3),

it("B9", "choice",
   "Which of these volunteers is it certain the rules permit to lead a walk?",
   """Highcross Ramblers - Volunteer handbook, section 4 (walk leaders), and the autumn rota query

4.1 A volunteer may lead a walk only if they hold a current first-aid certificate.
4.2 Any volunteer who holds a current first-aid certificate and has completed at least two walks as a back-marker may lead a walk.
4.3 Back-marker walks count from any year.

Rota query from the walks secretary, 2 September:
"Before I fill the autumn rota, here is what I know about the people who have offered to lead:
- Bronwen Tate: current first-aid certificate; back-marker on two walks this spring.
- Kofi Mensah: current first-aid certificate; back-marker once, in 2023.
- Siobhan Rourke: no first-aid certificate; back-marker on five walks and very experienced.
- Emrys Pugh: current first-aid certificate; I haven't found his back-marker record.
- Hilde Sandvik: led three walks last year, but her first-aid certificate lapsed in July.
Please shout if I have any of this wrong."
""",
   "Bronwen Tate",
   opts=["Bronwen Tate", "Kofi Mensah", "Siobhan Rourke", "Emrys Pugh", "Hilde Sandvik", NONE],
   card="- Bronwen Tate: the volunteer listed first in the rota query\n"
        "- Kofi Mensah: the volunteer who was back-marker once, in 2023\n"
        "- Siobhan Rourke: the volunteer with five back-marker walks\n"
        "- Emrys Pugh: the volunteer whose back-marker record was not found\n"
        "- Hilde Sandvik: the volunteer who led three walks last year\n"
        "- none of these: the handbook and the query do not make it certain that any listed volunteer may lead",
   diff=2, twin=[("- Bronwen Tate: current first-aid certificate; back-marker on two walks this spring.",
                  "- Bronwen Tate: current first-aid certificate; back-marker on one walk this spring.")],
   twin_gold=NONE),

it("B10", "choice",
   "Classify the statement relative to the CI log.",
   """Pipeline run #4471 - repo: ledgerline/payments-api - branch: release/2.14
Triggered by: merge of PR #902 ("retry idempotency keys")

Pipeline rules (from .ci/README):
- If every test in the regression suite passes, the build is deployed to staging automatically.
- Deployment to production always needs a manual approval, whatever the test results.

Run summary:
- Lint: passed
- Unit tests: 1,204 run
- Regression suite: 318 tests; summary panel failed to render (known dashboard bug, see INFRA-77)
- Build artefact: payments-api:2.14.0-rc3 (published to registry)
- Deploy to staging: NOT TRIGGERED
- Duration: 14m 22s

Comment from on-call engineer, Yusra Qadri: "Staging still on rc2. Someone needs to open the raw test report."

Statement: No test in the regression suite passed on run #4471.""",
   U, opts=L3[0], card=L3CARD, diff=2),

it("B11", "noul",
   "Is the statement guaranteed by the fulfilment FAQ and the order history?",
   """Tidewell Home - Fulfilment FAQ (internal version for support agents)

Where do orders ship from? We ship from three warehouses: Leeds, Bristol and Derby. The customer cannot choose the warehouse; the system picks the one with stock.
How long does delivery take? Every order that ships from the Leeds warehouse arrives in two working days. Orders from Bristol and Derby usually arrive in two to four working days, depending on the courier.
Can a customer track their parcel? Yes, from the moment the label is printed.

Order history, order 5512 (customer: Mr. Stellan Hjort):
- Placed Monday 09:40, paid by card.
- Label printed Monday 16:05.
- Delivered Friday 11:20 (four working days after dispatch).
- Customer rating: 3 stars, comment "slower than last time".

Statement: Order 5512 shipped from the Bristol warehouse.""",
   0, card=FOLLOW, diff=2,
   twin=[("We ship from three warehouses: Leeds, Bristol and Derby.", "We ship from two warehouses: Leeds and Bristol."), ("Orders from Bristol and Derby usually arrive", "Orders from Bristol usually arrive")], twin_gold=1),

it("B12", "choice",
   "Taking the laboratory protocol and the result sheet as true, how should the statement be labelled?",
   """Ashgrove Regional Laboratory - Protocol P-17: Referral of serology samples

1. All samples are run on the first-line assay within 24 hours of receipt.
2. Samples are sent to the national reference laboratory only if the first-line assay result is inconclusive (optical density ratio between 0.9 and 1.1).
3. Conclusive results (ratio below 0.9 or above 1.1) are reported directly to the requesting clinician.
4. The requesting clinician may ask for a repeat on a fresh sample at any time.

Result sheet, batch 26-0415:
- Sample S-41: ratio 1.04 - inconclusive.
- Sample S-42: ratio 2.87 - positive, reported.
- Sample S-43: ratio 0.95 - inconclusive.
- Sample S-44: ratio 0.21 - negative, reported. Clinician Dr. Ellery phoned to say she was surprised and would consider a repeat.
- Sample S-45: ratio 0.33 - negative, reported.

Statement: Sample S-44 was sent to the national reference laboratory.""",
   C, opts=L3[1], card=L3CARD, diff=1),

it("B13", "noul",
   "Would a reader who accepts the lettings procedure and the file note be forced to accept the statement?",
   """Brightmoor Lettings - Pre-let inspection procedure (extract)

Step 6. The inspector checks every room for damp and for mould and records each separately (present / absent) on form PL-2.
Step 7. If the inspector finds both damp and mould in the same property, the property is taken off the market until a damp specialist has reported.
Step 8. Minor condensation marks on window frames are not recorded as damp.

File note - Flat 3, 27 Hawthorn Rise, inspection on 6 May by Josie Marchbank:
"Inspection complete, PL-2 uploaded. Tenants moving out left the flat clean. Bathroom extractor fan is noisy, maintenance request raised. Property stays listed on the portal and viewings can continue from Thursday."

Branch manager: "Good - we have three viewings booked already."

Statement: The inspector found no mould in Flat 3, 27 Hawthorn Rise.""",
   0, card=FOLLOW, diff=3,
   twin=[("Step 7. If the inspector finds both damp and mould in the same property,",
          "Step 7. If the inspector finds damp or mould in a property,")], twin_gold=1),

]
