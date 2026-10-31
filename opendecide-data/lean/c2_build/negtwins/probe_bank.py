"""negtwins/probe_bank.py: a closed bank of neutral probe cores for exactness / G-LEX probes (authored here, no model).

Every pattern needs >= PROBES_PER_PATTERN applicable probe cores whatever the live pools hold, so the exactness check
(A42-D 7.3, 0.9 per pattern) does not depend on which G-block / replay / metadata rows survive. The cores are plain
positive polar questions about invented everyday records; none comes from a training or eval source.
"""
from __future__ import annotations

DO = [
    "Does the notice mention a closing date?", "Does the report name the person who signed it?",
    "Does the memo ask staff to reply by email?", "Does the invoice list a shipping fee?",
    "Does the policy cover damage caused by floods?", "Does the letter confirm the new meeting room?",
    "Does the brochure offer a student discount?", "Does the guide explain how to reset the device?",
    "Does the review recommend the product to families?", "Does the agreement require a written notice?",
    "Does the schedule include a lunch break?", "Does the article cite a government study?",
    "Does the label state the country of origin?", "Does the form request a phone number?",
    "Does the website provide a refund option?", "Does the email announce a change of venue?",
    "Does the manual describe the safety checks?", "Does the contract grant the tenant a parking space?",
    "Does the receipt show the tax amount?", "Does the poster invite visitors to the open day?",
    "Does the lesson plan involve group work?", "Does the menu contain a vegetarian dish?",
    "Does the package include a charger?", "Does the room have a window?",
    "Does the folder contain the signed forms?", "Does the report include a summary table?",
    "Does the kit contain spare batteries?", "Does the plan have a backup route?",
    "Does the offer include free delivery?", "Does the box have a warranty card?",
    "Does the speaker refer to last year's results?", "Does the statement specify the payment date?",
    "Does the sign allow visitors to park here?", "Does the rule permit pets in the building?",
    "Does the update address the login problem?", "Does the card support contactless payment?",
]
COP = [
    "Is the library open on Sundays?", "Is the form required for every applicant?",
    "Is the museum free for children?", "Is the parking lot available to visitors?",
    "Is the report based on a public survey?", "Is the document written in plain language?",
    "Is the meeting scheduled for the morning?", "Is the course limited to adults?",
    "Is the loan approved by the committee?", "Is the trail closed in winter?",
    "Is the pool available after six?", "Is the offer valid for new customers?",
    "Is the guide intended for beginners?", "Is the product shown in the photo?",
    "Is the fee included in the ticket price?", "Is the answer given in the first paragraph?",
    "Is the entrance located on the east side?", "Is the class eligible for the discount?",
    "Is the badge issued to every volunteer?", "Is the sample provided at no cost?",
    "Is the website open to the public?", "Is the room planned for a larger group?",
]
HAVE = [
    "Has the committee approved the budget?", "Has the shop published its opening hours?",
    "Have the tickets been confirmed?", "Has the author named a source?", "Have the results been released?",
    "Has the road reopened to traffic?", "Have the volunteers been told about the change?",
    "Has the school announced a new date?", "Has the vendor provided a receipt?", "Have the files been listed?",
    "Has the council accepted the proposal?", "Have the seats been reserved?",
]
CAN = [
    "Can the member bring a guest?", "Can the visitor use the side entrance?", "Can the customer return the item?",
    "Can the student submit the form online?", "Can the resident park on this street?",
    "Can the guest change the booking?", "Can the reader download the file?", "Can the driver enter the zone?",
    "Can the client pay by card?", "Can the staff member work from home?", "Can the buyer cancel the order?",
    "Can the tenant keep a pet?",
]
THERE = [
    "Is there a phone number in the message?", "Is there a refund policy on the page?",
    "Is there an address in the letter?", "Is there a deadline in the notice?", "Are there prices in the list?",
    "Is there a map in the guide?", "Is there a signature at the bottom?", "Is there a contact name in the email?",
    "Are there rules for guests in the document?", "Is there a discount code in the offer?",
    "Is there a parking area near the venue?", "Is there a summary in the report?",
]
# 8 more cores per LACK verb (have / contain / include), so each verb-specific pattern has >= 10 probes
DO += [
    "Does the pamphlet have a section on safety?", "Does the cabin have a working heater?",
    "Does the clinic have a parking area?", "Does the plan have a named owner?",
    "Does the shop have a returns desk?", "Does the lecture have a recorded version?",
    "Does the trail have a marked entrance?", "Does the bus have a ramp for wheelchairs?",
    "Does the jar contain any nuts?", "Does the file contain a password?", "Does the bag contain a receipt?",
    "Does the cake contain eggs?", "Does the page contain a contact form?", "Does the letter contain an offer?",
    "Does the drawer contain a spare key?", "Does the bottle contain a safety seal?",
    "Does the tour include a guide?", "Does the price include tax?", "Does the ticket include a meal?",
    "Does the course include an exam?", "Does the rent include water?", "Does the bundle include a manual?",
    "Does the kit include gloves?", "Does the fee include insurance?",
]
BANK = {"DO": DO, "COP": COP, "HAVE": HAVE, "MOD": CAN, "THERE": THERE}
ALL = [c for v in BANK.values() for c in v]
