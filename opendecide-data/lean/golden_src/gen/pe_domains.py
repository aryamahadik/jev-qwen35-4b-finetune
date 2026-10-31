"""Domain libraries for gen_policy_exceptions: ten realistic policy domains (returns, ticket refunds, home-insurance
claims, HR leave, school coursework extensions, community grants, travel expenses, pharmacy dispensing, building
access control, content moderation).

Each domain lists
  * facts (what case notes can state) and predicates (conditions a policy can test), all Claude-written;
  * seeds: prerequisites (conditions an approval needs), grounds (conditions that lead to refusal or to another
    outcome code), modifiers, approve-type and deny-type overrides;
  * exceptions: for a literal ("final_sale+" = the item was sold as final sale) the literals that can serve as an
    exception to it; exceptions of exceptions are looked up the same way, so chains such as
    "refused if final sale, unless faulty, but the fault exception is lost if the fault was caused by misuse" arise;
  * defined terms (multi-hop), outcome codes with definitions, question templates, noise lines, evidence sources.

Literal notation: "pred+" means the predicate holds, "pred-" means it does not; "a+ & b-" is a conjunction.
No third-party text; no model calls.
"""
from fractions import Fraction as Fr

from pe_atoms import (BoolFact, BoolPred, CatFact, InPred, NumFact, NumPred, PairFact, PairPred, RatioFact, RatioPred,
                      TableFact, TablePred, TimeFact, TimePred)


class Domain:
    def __init__(self, name):
        self.name = name
        self.facts, self.preds = {}, {}
        self.prereq, self.grounds, self.mods, self.ovr_yes, self.ovr_no = [], [], [], [], []
        self.exc, self.terms, self.noise = {}, [], []
        self.nocombine, self.mutex = [], []
        self.extra_ctx = {}
        self.sources = None

    def fact(self, F):
        assert F.id not in self.facts, F.id
        F.order = len(self.facts)
        self.facts[F.id] = F
        return F

    def pred(self, P):
        assert P.id not in self.preds, P.id
        assert P.fact in self.facts, (P.id, P.fact)
        if isinstance(P, InPred):
            P._facts_gof = self.facts[P.fact].gof
            P._facts_groups = self.facts[P.fact].groups
        self.preds[P.id] = P
        return P

    def B(self, id, pos, neg, t, f, q=None, hide=True, req=None, guard=None, ev=None, unk=None, tags=()):
        self.fact(BoolFact(id, t, f, q=q, hide=hide and (q is not None or unk is not None), req=req, ev=ev, unk=unk))
        self.pred(BoolPred(id, id, pos, neg, tags=tags, guard=guard))

    def check(self):
        """Static checks of the library (run at import)."""
        from pe_atoms import lit, seed_lits
        for s in self.prereq:
            assert lit(s)[0] in self.preds, (self.name, s)
        for group in (self.grounds, self.mods, self.ovr_yes, self.ovr_no):
            for s, codes in group:
                for l in seed_lits(s):
                    assert l[0] in self.preds, (self.name, s)
                for c in codes:
                    assert c in self.codes, (self.name, c)
        for k, xs in self.exc.items():
            for l in seed_lits(k):
                assert l[0] in self.preds, (self.name, k)
            for x in xs:
                assert lit(x)[0] in self.preds, (self.name, x)
        for T in self.terms:
            for x in T["pool"]:
                assert lit(x)[0] in self.preds, (self.name, x)
        for c in self.codes:
            assert c in self.code_clause and c in self.code_def, (self.name, c)
        assert self.deny_code in self.codes and self.best in self.codes


# ======================================================================================================== returns
def returns():
    D = Domain("returns")
    D.orgs = ["Northwind Home Goods", "Brightside Outfitters", "Harbor & Pine", "Kestrel Electronics",
              "Maple Street Department Store", "Tallis Sports", "Juniper Kitchen Co.", "Cobalt Tech Store",
              "Wren & Ash Clothing", "Summit Outdoor Supply", "Fernhill Books & Games", "Larkspur Living"]
    D.titles = ["{org} - Returns Policy", "Returns and Exchanges at {org}", "{org}: Returns Rules for Store Staff",
                "Store Policy RT-{num}: Returns ({org})", "{org} Customer Returns Policy"]
    D.intro = ["{n} brought {a_item} back to {org} and asked to return it.", "{n} wants to return {a_item} to {org}.",
               "At the {org} service desk, {n} asked to return {a_item}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "return", "returns", "a return", "returns"
    D.wr = "{n}'s return"
    D.appr = dict(pas="accepted", noun="acceptance", clause=["the return is accepted", "the store accepts the return"])
    D.deny = dict(pas="refused", noun="refusal", clause=["the return is refused", "the store refuses the return"])
    D.q_appr = ["Under the policy, is {n}'s return accepted?", "Does the returns policy allow the store to accept {n}'s return?",
                "Should the store accept {n}'s return under this policy?"]
    D.q_deny = ["Under the policy, must the store refuse {n}'s return?", "Is {n}'s return refused under this policy?",
                "Does this policy require the store to turn down {n}'s return?"]
    D.codes = ["full refund", "store credit only", "exchange only", "return refused"]
    D.code_clause = {"full refund": ["the customer gets a full refund", "a full refund is given"],
                     "store credit only": ["the customer gets store credit instead of a refund", "only store credit is given"],
                     "exchange only": ["the item may only be exchanged for another item", "the store offers an exchange but no refund or credit"],
                     "return refused": ["the return is refused", "the store refuses the return"]}
    D.code_def = {"full refund": "The policy, applied with its exceptions and its stated precedence, gives the customer all their money back.",
                  "store credit only": "The return is taken back, but the policy gives store credit rather than money.",
                  "exchange only": "The policy lets the customer swap the item for another one but gives no refund and no credit.",
                  "return refused": "The policy does not take the item back at all: no refund, credit or exchange."}
    D.deny_code, D.best = "return refused", "full refund"
    D.fact(CatFact("category", {
        "swimwear": ["swimsuit", "pair of swim shorts"], "underwear": ["pack of cotton briefs", "set of boxer shorts"],
        "pierced earrings": ["pair of silver stud earrings", "pair of hoop earrings"],
        "cosmetics": ["lipstick set", "jar of face cream"], "electronics": ["bluetooth speaker", "pair of wireless headphones", "e-reader"],
        "kitchenware": ["cast-iron frying pan", "set of kitchen knives", "ceramic casserole dish"], "outerwear": ["wool coat", "rain jacket"],
        "toys and games": ["board game", "jigsaw puzzle"], "footwear": ["pair of running shoes", "pair of hiking boots"],
        "bedding": ["set of bed sheets", "duvet"]}, None, binds="item", hide=False))
    D.pred(InPred("restricted", "category", ["the item is {list_or}", "the item falls into one of these categories: {list}"],
                  ["the item is none of the following: {list}", "the item is not in any of these categories: {list}"],
                  restrict=["swimwear", "underwear", "pierced earrings", "cosmetics", "bedding"], k=(2, 3),
                  show={"pierced earrings": "earrings for pierced ears"}, sched=("Schedule A", "categories that cannot be returned"),
                  spos=["the item is in a category listed in Schedule A"], sneg=["the item is not in any category listed in Schedule A"],
                  tags=("implicit",)))
    D.pred(InPred("is_elec", "category", ["the item is an electronic device"], ["the item is not an electronic device"],
                  fixed={"electronics"}, tags=("implicit",)))
    D.fact(NumFact("days", ["{n} returned the {item} {vu} after it was bought.", "The {item} was brought back {vu} after the purchase date."],
                   zero=["The {item} was brought back on the same day it was bought."],
                   dates=["The {item} was bought on {d1} and brought back on {d2}.", "The purchase date on record is {d1}; the {item} came back on {d2}."],
                   q="how many days after purchase the {item} was returned"))
    D.pred(NumPred("days", "days", "le", [14, 28, 30, 45, 60, 90],
                   ["the item is returned no more than {tu} after purchase", "the item is returned within {tu} of purchase (day {t} still counts)"],
                   ["the item is returned more than {tu} after purchase"]))
    D.B("receipt", ["the customer has a receipt or order confirmation for the item", "a receipt or order confirmation is shown"],
        ["the customer has no receipt or order confirmation for the item", "no receipt or order confirmation is shown"],
        ["{n} had the original receipt.", "{n} showed the order confirmation email."],
        ["{n} had no receipt and could not find the order confirmation.", "{n} had lost the receipt and had no order confirmation."],
        q="whether {n} had a receipt or order confirmation")
    D.B("packaging", ["the item is in its original packaging"], ["the item is not in its original packaging"],
        ["The {item} was still in its original packaging.", "{n} brought the {item} back in the original box."],
        ["{n} had thrown away the original packaging.", "The {item} came back without its original packaging."],
        q="whether the {item} came back in its original packaging")
    D.B("used", ["the item has been used", "the item shows signs of use"], ["the item has not been used", "the item is unused"],
        ["{n} had used the {item} several times.", "The {item} had clearly been used."],
        ["The {item} had never been used.", "{n} had not used the {item} at all."], q="whether the {item} had been used",
        ev=("the {item} had been used", "the {item} had never been used"))
    D.B("final_sale", ["the item was sold as final sale", "the item was marked \"final sale\" when it was bought"],
        ["the item was not sold as final sale"],
        ["The {item} was sold as final sale; its tag says \"Final sale\".", "The {item} came from the clearance rack, where everything is sold as final sale."],
        ["The {item} was bought at the regular price, not as final sale.", "The {item} was not a final-sale item."],
        q="whether the {item} was sold as final sale", ev=("the {item} was sold as final sale", "the {item} was not sold as final sale"))
    D.B("faulty", ["the item is faulty", "the item has a fault"], ["the item is not faulty", "the item has no fault"],
        ["A store inspector examined the {item} and confirmed that it is faulty.", "Inspection found a fault in the {item}."],
        ["A store inspector examined the {item} and found no fault.", "Inspection found no fault in the {item}."],
        q="whether the {item} is faulty")
    D.B("misuse", ["the fault was caused by the customer's misuse"], ["the fault was not caused by the customer's misuse"],
        ["The inspector found that the fault was caused by the {item} being mistreated.", "The inspector concluded that misuse by the customer caused the fault."],
        ["The inspector found no sign that misuse caused the fault.", "The inspector ruled out misuse as the cause of the fault."],
        q="whether misuse caused the fault", req=("faulty", True), guard=("faulty", True))
    D.B("damaged", ["the item was damaged when the customer first unpacked it"], ["the item was undamaged when the customer first unpacked it"],
        ["The {item} already had dents and scratches when {n} first unpacked it."],
        ["The {item} was in perfect condition when {n} first unpacked it."], q="whether the {item} was damaged when it was unpacked")
    D.B("late_report", ["the damage is reported more than 48 hours after the customer received the item"],
        ["the damage is reported within 48 hours of the customer receiving the item"],
        ["{n} only reported the damage five days after receiving the {item}.", "{n} waited a week before reporting the damage."],
        ["{n} reported the damage on the day the {item} was received.", "{n} reported the damage the morning after receiving the {item}."],
        q="when {n} reported the damage", req=("damaged", True), guard=("damaged", True))
    D.B("recalled", ["the item is subject to a manufacturer recall"], ["the item is not subject to a manufacturer recall"],
        ["The manufacturer has recalled the product line that the {item} belongs to."], ["The {item} is not covered by any recall."],
        q="whether the {item} is covered by a recall")
    D.B("seal", ["the item's factory seal has been broken"], ["the item's factory seal is still intact"],
        ["{n} had broken the factory seal on the {item}.", "The factory seal on the {item} had been opened."],
        ["The factory seal on the {item} was still intact."], q="whether the factory seal on the {item} was intact")
    D.B("tags", ["the original tags are still attached"], ["the original tags have been removed"],
        ["The original tags were still attached."], ["{n} had cut off the original tags."], q="whether the original tags were still attached")
    D.B("gold", ["the customer is a Gold member of the loyalty programme"], ["the customer is not a Gold member of the loyalty programme"],
        ["{n} has been a Gold member of the loyalty programme for three years.", "{n} holds Gold status in the store's loyalty programme."],
        ["{n} is not in the loyalty programme.", "{n} is a Silver member of the loyalty programme, not a Gold member."],
        q="whether {n} is a Gold loyalty member")
    D.B("gift", ["the customer received the item as a gift"], ["the customer did not receive the item as a gift"],
        ["The {item} was a birthday present to {n} from a friend.", "{n} had received the {item} as a gift."],
        ["{n} had bought the {item} for {refl}."], q="whether the {item} was a gift")
    D.fact(NumFact("price", ["The {item} cost {vm}.", "The price paid for the {item} was {vm}."], money=True, lo=5, q="what the {item} cost"))
    D.pred(NumPred("price", "price", "gt", [50, 100, 150, 200, 500], ["the item cost more than {tm}"], ["the item cost {tm} or less"], money=True))
    D.fact(NumFact("returns12", ["Before this visit, {n} had returned {vu} to the store in the past 12 months."], unit=("item", "items"),
                   zero=["{n} had not returned anything in the 12 months before this visit."],
                   one=["Before this visit, {n} had returned one item to the store in the past 12 months."],
                   q="how many items {n} had returned in the past 12 months"))
    D.pred(NumPred("returns12", "returns12", "ge", [4, 5, 6, 8, 10],
                   ["the customer has already returned {t} or more items in the past 12 months (not counting this return)"],
                   ["the customer has returned fewer than {t} items in the past 12 months (not counting this return)"], unit=("item", "items")))
    D.B("account", ["the purchase is recorded in the customer's loyalty account"], ["the purchase is not recorded in the customer's loyalty account"],
        ["The purchase is recorded in {n}'s loyalty account history."], ["The purchase does not appear in any loyalty account."],
        q="whether the purchase is recorded in a loyalty account")
    D.prereq = ["days+", "receipt+", "packaging+", "tags+"]
    D.grounds = [("final_sale+", ["exchange only", "return refused"]), ("used+", ["return refused", "store credit only"]),
                 ("restricted+", ["return refused"]), ("seal+", ["return refused", "exchange only"]),
                 ("is_elec+ & seal+", ["store credit only", "return refused"]), ("returns12+", ["return refused"]),
                 ("days-", ["return refused"]), ("tags-", ["exchange only", "return refused"]),
                 ("price+ & receipt-", ["return refused"])]
    D.mods = [("receipt-", ["store credit only"]), ("packaging-", ["store credit only", "exchange only"]),
              ("gift+", ["store credit only"]), ("used+", ["store credit only"])]
    D.ovr_yes = [("recalled+", ["full refund"]), ("faulty+", ["full refund"])]
    D.ovr_no = [("returns12+", ["return refused"])]
    D.exc = {"days-": ["faulty+", "gold+", "gift+"], "receipt-": ["account+", "gold+"], "packaging-": ["faulty+", "damaged+"],
             "used+": ["faulty+"], "final_sale+": ["faulty+", "damaged+", "recalled+"], "restricted+": ["seal-", "faulty+"],
             "seal+": ["faulty+"], "is_elec+ & seal+": ["faulty+"], "tags-": ["faulty+"], "returns12+": ["faulty+", "recalled+"],
             "price+ & receipt-": ["account+"], "gift+": ["receipt+"], "faulty+": ["misuse+"], "damaged+": ["late_report+"],
             "gold+": ["final_sale+"], "seal-": ["used+"], "account+": ["returns12+"]}
    D.terms = [dict(id="T_std", name="standard return", pool=["days+", "receipt+", "packaging+", "tags+"], modes=["all"], role="prereq",
                    defs=['A return counts as a "{name}" if {cond}.', 'In this policy, a "{name}" is a return where {cond}.'],
                    pos=['the return is a "{name}"', 'the return counts as a "{name}"'], neg=['the return is not a "{name}"']),
               dict(id="T_dmg", name="damage case", pool=["faulty+", "damaged+", "recalled+"], modes=["any"], role="exc",
                    for_=["days-", "packaging-", "final_sale+", "used+", "tags-", "seal+", "restricted+", "returns12+"],
                    defs=['A return is a "{name}" if {cond}.', 'In this policy, a "{name}" means a return where {cond}.'],
                    pos=['the return is a "{name}"'], neg=['the return is not a "{name}"'])]
    D.noise = ["Refunds are made to the original payment method within ten working days.",
               "Exchanges depend on stock being available.", "Staff should explain the outcome to the customer politely."]
    D.sources = ("the customer", "the store's records")
    return D


# ======================================================================================================== refunds
def refunds():
    D = Domain("refunds")
    D.orgs = ["Riverside Arena", "Beacon Theatre Company", "Northfield Concert Hall", "Lakeside Festival Ltd.",
              "Summit Sports Stadium", "Grand Oak Playhouse", "Harborfront Events", "Pinecrest Comedy Club"]
    D.titles = ["{org} Ticket Refund Policy", "Refunds for Tickets Bought from {org}", "{org} - Terms for Ticket Refunds",
                "Box Office Policy BO-{num}: Refunds ({org})"]
    D.extra_ctx = {"event": ["a concert", "a play", "a football match", "a comedy show", "a ballet", "an opera"]}
    D.intro = ["{n} bought a ticket to {event} at {org} and has asked for a refund.",
               "{n} contacted the {org} box office asking for {pos} money back for a ticket to {event}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "refund request", "refund requests", "a refund request", "refund requests"
    D.wr = "{n}'s refund request"
    D.appr = dict(pas="approved", noun="approval", clause=["the refund is approved", "the buyer gets a refund"])
    D.deny = dict(pas="refused", noun="refusal", clause=["the refund is refused", "no refund is given"])
    D.q_appr = ["Under the policy, is {n}'s refund request approved?", "Does {n} get a refund under this policy?",
                "Should the box office approve {n}'s refund?"]
    D.q_deny = ["Under the policy, must {n}'s refund request be refused?", "Is {n} denied a refund under this policy?"]
    D.codes = ["full refund", "refund minus the booking fee", "credit voucher", "no refund"]
    D.code_clause = {"full refund": ["the buyer gets a full refund", "the full ticket price is refunded"],
                     "refund minus the booking fee": ["the buyer is refunded the ticket price minus the booking fee", "the refund excludes the booking fee"],
                     "credit voucher": ["the buyer gets a credit voucher instead of a refund", "only a credit voucher is offered"],
                     "no refund": ["no refund is given", "the refund request is refused"]}
    D.code_def = {"full refund": "The policy, applied with its exceptions and precedence, returns everything the buyer paid.",
                  "refund minus the booking fee": "The buyer gets money back, but the policy keeps the booking fee.",
                  "credit voucher": "The policy gives a voucher for future bookings instead of money.",
                  "no refund": "The policy gives nothing back: no money and no voucher."}
    D.deny_code, D.best = "no refund", "full refund"
    D.fact(NumFact("dbefore", ["{n} asked for the refund {vu} before the event.", "The refund request reached the box office {vu} before the event date."],
                   zero=["{n} asked for the refund on the day of the event."],
                   dates=["The event was scheduled for {d2}; {n} asked for the refund on {d1}."],
                   q="how many days before the event the refund was requested"))
    D.pred(NumPred("dbefore", "dbefore", "ge", [2, 3, 7, 10, 14, 30],
                   ["the refund is requested at least {tu} before the event", "the request is made {tu} or more before the event date"],
                   ["the refund is requested fewer than {tu} before the event", "the request is made less than {tu} before the event date"]))
    D.B("cancelled", ["the event has been cancelled by the organiser"], ["the event has not been cancelled"],
        ["The organiser has cancelled the event.", "The event has been called off by the organiser."], ["The event has not been cancelled."],
        q="whether the event has been cancelled")
    D.B("postponed", ["the event has been moved to a new date"], ["the event has not been moved to a new date"],
        ["The organiser has moved the event to a date three months later."], ["The event date has not changed."],
        q="whether the event date has changed")
    D.B("resale", ["the ticket was bought from a resale website rather than from us"], ["the ticket was bought directly from us"],
        ["{n} bought the ticket second-hand on a resale website.", "{n} got the ticket from a resale site, not from {org}."],
        ["{n} bought the ticket directly from {org}.", "{n} bought the ticket from the {org} box office."],
        q="where {n} bought the ticket", ev=("the ticket came from a resale website", "the ticket was bought directly from {org}"))
    D.B("protect", ["the buyer added refund protection at checkout"], ["the buyer did not add refund protection at checkout"],
        ["{n} paid for refund protection when buying the ticket."], ["{n} did not add refund protection when buying the ticket."],
        q="whether {n} added refund protection")
    D.B("doctor", ["the buyer provides a doctor's note saying they cannot attend because of illness"], ["the buyer provides no doctor's note"],
        ["{n} has sent a doctor's note confirming that {sub} will be in hospital on the day of the event."],
        ["{n} has not provided a doctor's note."], hide=False)
    D.B("promo", ["the ticket was bought with a promotional discount code"], ["the ticket was bought without a promotional discount code"],
        ["{n} used a 30% promotional discount code when buying the ticket."], ["{n} paid the full price, with no discount code."],
        q="whether a discount code was used", ev=("a discount code was used for the ticket", "no discount code was used for the ticket"))
    D.B("season", ["the buyer is a season-ticket holder"], ["the buyer is not a season-ticket holder"],
        ["{n} is a season-ticket holder at {org}."], ["{n} does not have a season ticket."], q="whether {n} holds a season ticket")
    D.B("transfer", ["the buyer has transferred the ticket into another person's name"], ["the buyer has not transferred the ticket into another person's name"],
        ["{n} had transferred the ticket into a friend's name before asking for the refund."], ["{n} has not transferred the ticket to anyone else."],
        q="whether {n} has transferred the ticket to someone else")
    D.B("moved", ["the event has been moved to a venue in a different city"], ["the event is still taking place in the original city"],
        ["The event has been moved to a venue in another city."], ["The event has not been moved to another city."],
        q="whether the venue has changed")
    D.fact(NumFact("price", ["The ticket cost {vm}.", "{n} paid {vm} for the ticket."], money=True, lo=5, q="what the ticket cost"))
    D.pred(NumPred("price", "price", "gt", [40, 60, 100, 150], ["the ticket cost more than {tm}"], ["the ticket cost {tm} or less"], money=True))
    D.mutex = [("cancelled", "postponed"), ("cancelled", "moved")]
    D.prereq = ["dbefore+", "resale-", "transfer-"]
    D.grounds = [("dbefore-", ["no refund", "credit voucher"]), ("resale+", ["no refund"]), ("transfer+", ["no refund"]),
                 ("promo+", ["credit voucher", "refund minus the booking fee"])]
    D.mods = [("postponed+", ["credit voucher"]), ("promo+", ["refund minus the booking fee"]), ("price+", ["refund minus the booking fee"])]
    D.ovr_yes = [("cancelled+", ["full refund"]), ("moved+", ["full refund"])]
    D.ovr_no = [("transfer+", ["no refund"])]
    D.exc = {"dbefore-": ["protect+", "doctor+", "season+"], "resale+": ["cancelled+"], "promo+": ["cancelled+"],
             "protect+": ["promo+"], "season+": ["resale+"], "postponed+": ["protect+"], "transfer+": ["cancelled+"],
             "cancelled+": ["resale+"], "moved+": ["transfer+"], "price+": ["cancelled+"], "doctor+": ["transfer+"]}
    D.terms = [dict(id="T_prot", name="protected booking", pool=["protect+", "promo-", "resale-"], modes=["all"], role="exc",
                    for_=["dbefore-", "postponed+"], defs=['A booking counts as a "{name}" if {cond}.', 'In this policy, a "{name}" is a booking where {cond}.'],
                    pos=['the booking is a "{name}"'], neg=['the booking is not a "{name}"']),
               dict(id="T_direct", name="direct booking", pool=["resale-", "transfer-"], modes=["all"], role="prereq",
                    defs=['A booking is a "{name}" if {cond}.'], pos=['the booking is a "{name}"'], neg=['the booking is not a "{name}"'])]
    D.noise = ["Refunds are paid to the card used for the purchase within 14 days.", "Booking fees are shown separately at checkout."]
    D.sources = ("the buyer", "the ticketing system")
    return D


# ======================================================================================================== insurance
def insurance():
    D = Domain("insurance")
    D.orgs = ["Evergreen Mutual", "Harbor Shield Insurance", "Crestline Home Insurance", "Northstar Assurance",
              "Bluewater Insurance Co.", "Oakwell Mutual", "Pillar Home Cover"]
    D.titles = ["{org} Home Policy - Claims Rules", "{org}: When We Pay a Claim", "Claims Handling Guide ({org}), Part {num}",
                "{org} Home and Contents Cover - Claim Decisions"]
    D.intro = ["{n} has made a claim under {pos} {org} home policy.", "{org} has received a home-insurance claim from {n}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "claim", "claims", "a claim", "claims"
    D.wr = "{n}'s claim"
    D.appr = dict(pas="paid", noun="payment", clause=["the claim is paid", "we pay the claim"])
    D.deny = dict(pas="denied", noun="denial", clause=["the claim is denied", "we decline the claim"])
    D.q_appr = ["Under the policy, is {n}'s claim paid?", "Should the insurer pay {n}'s claim under these rules?",
                "Do these claim rules allow {n}'s claim to be paid?"]
    D.q_deny = ["Under the policy, must {n}'s claim be denied?", "Is {n}'s claim denied under these rules?"]
    D.codes = ["pay the claim", "hold for documents", "refer to a senior adjuster", "deny the claim"]
    D.code_clause = {"pay the claim": ["the claim is paid", "we pay the claim"],
                     "hold for documents": ["the claim is put on hold until the missing documents arrive"],
                     "refer to a senior adjuster": ["the claim is referred to a senior adjuster", "a senior adjuster must review the claim"],
                     "deny the claim": ["the claim is denied", "we decline the claim"]}
    D.code_def = {"pay the claim": "The rules, applied with their exceptions and precedence, lead to payment.",
                  "hold for documents": "The rules say to pause the claim until missing documents are provided.",
                  "refer to a senior adjuster": "The rules send the claim to a senior adjuster instead of deciding it now.",
                  "deny the claim": "The rules lead to refusing the claim."}
    D.deny_code, D.best = "deny the claim", "pay the claim"
    D.fact(CatFact("cause", {"flood": ["river flood"], "storm": ["windstorm"], "theft": ["burglary"], "fire": ["kitchen fire"],
                             "burst": ["burst pipe"], "leak": ["slow leak"]},
                   {"flood": ["The damage was caused by flood water after a nearby river burst its banks."],
                    "storm": ["A windstorm brought down a large tree, which crushed the garage roof."],
                    "theft": ["Jewellery and a laptop were stolen from the home in a burglary."],
                    "fire": ["A kitchen fire caused smoke and fire damage."],
                    "burst": ["A water pipe burst suddenly and soaked the kitchen ceiling."],
                    "leak": ["A pipe under the bathroom floor had been leaking slowly for many months before the damage was noticed."]},
                   unk=["The loss adjuster has not yet established what caused the loss."]))
    D.pred(InPred("c_flood", "cause", ["the damage is caused by flooding", "the loss results from flood water"],
                  ["the damage is not caused by flooding"], fixed={"flood"}))
    D.pred(InPred("c_theft", "cause", ["the loss is caused by theft"], ["the loss is not caused by theft"], fixed={"theft"}))
    D.pred(InPred("c_gradual", "cause", ["the damage results from a gradual leak or other slow deterioration"],
                  ["the damage does not result from a gradual leak or other slow deterioration"], fixed={"leak"}, tags=("implicit",)))
    D.pred(InPred("c_water", "cause", ["the damage is caused by water of any kind"], ["the damage is not caused by water"],
                  fixed={"flood", "burst", "leak"}, tags=("implicit",)))
    D.pred(InPred("c_fire", "cause", ["the damage is caused by fire"], ["the damage is not caused by fire"], fixed={"fire"}))
    D.B("active", ["the policy was in force on the date of the loss"], ["the policy was not in force on the date of the loss"],
        ["{n}'s policy was in force on the date of the loss."], ["{n} never paid the premium for this policy, so it was not in force on the date of the loss."],
        q="whether the policy was in force on the date of the loss")
    D.fact(NumFact("report", ["{n} reported the loss to {org} {vu} after it happened."], zero=["{n} reported the loss to {org} on the day it happened."],
                   dates=["The loss happened on {d1}; {n} reported it to {org} on {d2}."], q="when the loss was reported to {org}"))
    D.pred(NumPred("rep", "report", "le", [14, 30, 45, 60],
                   ["the loss is reported to us within {tu} of the day it happened (day {t} included)", "the loss is reported to us no later than {tu} after it happened"],
                   ["the loss is reported to us more than {tu} after it happened"]))
    D.fact(NumFact("police", ["{n} reported the burglary to the police {vu} after discovering it."], unit=("hour", "hours"), hours=True,
                   zero=["{n} reported the burglary to the police as soon as it was discovered."], req=("c_theft", True),
                   q="when the burglary was reported to the police"))
    D.pred(NumPred("pol_ok", "police", "le", [24, 48, 72], ["the theft is reported to the police no more than {tu} after being discovered"],
                   ["the theft is reported to the police more than {tu} after being discovered"], unit=("hour", "hours"), hours=True,
                   guard=("c_theft", True), tags=("units",)))
    D.B("fcover", ["the policyholder bought the optional flood cover"], ["the policyholder did not buy the optional flood cover"],
        ["{n} had added the optional flood cover to the policy."], ["{n} had not added the optional flood cover."],
        q="whether {n} had bought the optional flood cover")
    D.fact(NumFact("fcdays", ["{n} added the flood cover {vu} before the loss."], lo=1, req=("fcover", True), q="when the flood cover was added"))
    D.pred(NumPred("fc_new", "fcdays", "lt", [14, 21, 30], ["the flood cover was added fewer than {tu} before the loss"],
                   ["the flood cover was added at least {tu} before the loss"], guard=("fcover", True)))
    D.fact(NumFact("vacant", ["The home had been empty for {vu} in a row when the loss happened."],
                   zero=["{n} was living in the home when the loss happened."], q="how long the home had been empty before the loss"))
    D.pred(NumPred("vac", "vacant", "gt", [30, 45, 60], ["the home had been unoccupied for more than {tu} in a row when the loss happened"],
                   ["the home had not been unoccupied for more than {tu} in a row when the loss happened"]))
    D.B("vnotice", ["the policyholder told us about the vacancy in advance"], ["the policyholder did not tell us about the vacancy in advance"],
        ["{n} had told {org} in advance that the home would be empty."], ["{n} had not told {org} that the home would be empty."],
        q="whether {n} told {org} about the empty home in advance", req=("vac", True), guard=("vac", True))
    D.B("deliberate", ["the damage was caused deliberately by the policyholder"], ["the damage was not caused deliberately by the policyholder"],
        ["The loss adjuster found that {n} caused the damage deliberately."], ["The loss adjuster found no sign that the damage was deliberate."],
        q="whether the damage was deliberate", ev=("the damage was deliberate", "the damage was accidental"))
    D.fact(NumFact("amount", ["The claim is for {vm}.", "{n} is claiming {vm}."], money=True, lo=50, q="how much is being claimed"))
    D.pred(NumPred("amt_big", "amount", "gt", [5000, 10000, 25000], ["the claim is for more than {tm}"], ["the claim is for {tm} or less"], money=True))
    D.pred(NumPred("amt_small", "amount", "le", [250, 500, 1000], ["the amount claimed is no more than the {tm} excess"],
                   ["the amount claimed is more than the {tm} excess"], money=True))
    D.fact(NumFact("prior", ["{n} has made {vu} in the past three years."], unit=("other claim", "other claims"),
                   zero=["{n} has made no other claims in the past three years."], q="how many other claims {n} has made recently"))
    D.pred(NumPred("many", "prior", "ge", [2, 3, 4], ["the policyholder has made {t} or more other claims in the past three years"],
                   ["the policyholder has made fewer than {t} other claims in the past three years"]))
    D.B("business", ["the damaged property is used for a business"], ["the damaged property is not used for a business"],
        ["{n} runs a small bakery business from the damaged part of the home."], ["The damaged part of the home is used only as a private home."],
        q="whether the damaged property is used for business",
        ev=("the damaged rooms are used for a business", "the damaged rooms are used only as a private home"))
    D.B("bcover", ["the policy includes the home-business endorsement"], ["the policy does not include the home-business endorsement"],
        ["{n}'s policy includes the home-business endorsement."], ["{n}'s policy has no home-business endorsement."],
        q="whether the policy has the home-business endorsement")
    D.B("fraud", ["our fraud team has flagged the claim"], ["our fraud team has not flagged the claim"],
        ["The fraud team has flagged the claim for inconsistencies."], ["The fraud team has not raised any concern about the claim."],
        q="whether the fraud team has reviewed the claim")
    D.B("hospital", ["the policyholder was admitted to hospital during the period allowed for reporting the loss"],
        ["the policyholder was not admitted to hospital during the period allowed for reporting the loss"],
        ["{n} was admitted to hospital two days after the loss and stayed there for several weeks."],
        ["{n} was not in hospital at any point after the loss."], q="whether {n} was in hospital after the loss")
    D.fact(NumFact("start", ["The loss happened {vu} after the policy started."], dates=["The policy started on {d1} and the loss happened on {d2}."],
                   lo=1, q="how long after the policy started the loss happened"))
    D.pred(NumPred("newpol", "start", "lt", [14, 30], ["the loss happens fewer than {tu} after the policy start date"],
                   ["the loss happens {tu} or more after the policy start date"]))
    D.B("renewal", ["the policy renewed an earlier policy with us with no gap in cover"], ["the policy did not renew an earlier policy with us"],
        ["The policy renewed {n}'s earlier {org} policy with no break in cover."], ["This is {n}'s first policy with {org}."],
        q="whether the policy renewed an earlier {org} policy")
    D.B("proof", ["proof of ownership is provided for the items claimed"], ["no proof of ownership is provided for the items claimed"],
        ["{n} has sent receipts for all the items claimed."], ["{n} has no receipts or other proof of ownership for the items claimed."], hide=False)
    D.prereq = ["active+", "rep+", "proof+"]
    D.grounds = [("c_flood+", ["deny the claim"]), ("c_gradual+", ["deny the claim"]), ("deliberate+", ["deny the claim"]),
                 ("vac+", ["deny the claim"]), ("business+", ["deny the claim"]), ("newpol+", ["deny the claim"]),
                 ("rep-", ["deny the claim"]), ("amt_small+", ["deny the claim"]),
                 ("c_theft+ & pol_ok-", ["deny the claim", "hold for documents"])]
    D.mods = [("proof-", ["hold for documents"]), ("amt_big+", ["refer to a senior adjuster"]), ("many+", ["refer to a senior adjuster"]),
              ("fraud+", ["refer to a senior adjuster"])]
    D.ovr_yes = [("c_fire+", ["pay the claim"])]
    D.ovr_no = [("fraud+", ["deny the claim", "refer to a senior adjuster"]), ("deliberate+", ["deny the claim"])]
    D.exc = {"c_flood+": ["fcover+"], "fcover+": ["fc_new+"], "vac+": ["vnotice+"], "rep-": ["hospital+"], "newpol+": ["renewal+"],
             "business+": ["bcover+"], "proof-": ["c_fire+"], "c_fire+": ["deliberate+"], "c_theft+ & pol_ok-": ["hospital+"],
             "amt_small+": ["c_fire+"], "vnotice+": ["c_water+"], "hospital+": ["fraud+"]}
    D.terms = [dict(id="T_cov", name="covered cause", pool=["c_flood-", "c_gradual-", "deliberate-"], modes=["all"], role="prereq",
                    defs=['A loss has a "{name}" if {cond}.', 'In this policy, a loss has a "{name}" when {cond}.'],
                    pos=['the loss has a "{name}"'], neg=['the loss does not have a "{name}"']),
               dict(id="T_time", name="timely claim", pool=["rep+", "active+"], modes=["all"], role="prereq",
                    defs=['A claim is a "{name}" if {cond}.'], pos=['the claim is a "{name}"'], neg=['the claim is not a "{name}"'])]
    D.noise = ["Claims are acknowledged within two working days.", "Payments are made by bank transfer."]
    D.sources = ("the policyholder", "the loss adjuster's report")
    return D


# ======================================================================================================== HR leave
def hr_leave():
    D = Domain("hr_leave")
    D.orgs = ["Alder & Finch LLP", "Crescent Logistics", "Mapleton City Council", "Brightwave Software", "Harlow Manufacturing",
              "Northgate Hospital Trust", "Sable Retail Group", "Quarry Lane Engineering"]
    D.titles = ["{org} - Annual Leave Policy", "{org} Staff Handbook: Leave Requests", "HR Policy HR-{num}: Time Off ({org})",
                "{org}: Rules for Approving Leave"]
    D.intro = ["{n}, who works at {org}, has asked for time off.", "{n} has submitted a leave request to {pos} manager at {org}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "leave request", "leave requests", "a leave request", "leave requests"
    D.wr = "{n}'s leave request"
    D.appr = dict(pas="approved", noun="approval", clause=["the leave is approved", "the request is approved"])
    D.deny = dict(pas="refused", noun="refusal", clause=["the request is refused", "the leave is refused"])
    D.q_appr = ["Under the policy, is {n}'s leave request approved?", "Should {n}'s manager approve the leave under this policy?",
                "Does the policy allow {n} to take the requested leave?"]
    D.q_deny = ["Under the policy, must {n}'s leave request be refused?", "Is {n}'s leave refused under this policy?"]
    D.codes = ["approved as paid leave", "approved as unpaid leave", "referred to HR", "refused"]
    D.code_clause = {"approved as paid leave": ["the leave is approved as paid leave"],
                     "approved as unpaid leave": ["the leave is approved, but as unpaid leave"],
                     "referred to HR": ["the request is referred to HR for a decision", "HR decides the request instead of the manager"],
                     "refused": ["the request is refused", "the leave is refused"]}
    D.code_def = {"approved as paid leave": "The policy, applied with its exceptions and precedence, grants the leave with pay.",
                  "approved as unpaid leave": "The policy grants the time off but without pay.",
                  "referred to HR": "The policy sends the request to HR instead of letting the manager decide it.",
                  "refused": "The policy does not allow the leave."}
    D.deny_code, D.best = "refused", "approved as paid leave"
    D.fact(NumFact("tenure", ["{n} started working at {org} {vu} ago.", "{n} has worked at {org} for {vu}."], unit=("month", "months"),
                   zero=["{n} started at {org} less than a month ago."], q="how long {n} has worked at {org}"))
    D.pred(NumPred("ten", "tenure", "ge", [3, 6, 12], ["the employee has at least {tu} of service", "the employee has worked here for {tu} or more"],
                   ["the employee has fewer than {tu} of service"], unit=("month", "months")))
    D.fact(NumFact("notice", ["{n} submitted the request {vu} before the first day of leave."],
                   zero=["{n} submitted the request on the first day of the leave."],
                   dates=["{n} submitted the request on {d1}; the leave would start on {d2}."], q="how far in advance the request was submitted"))
    D.pred(NumPred("note", "notice", "ge", [7, 10, 14, 28], ["the request is submitted at least {tu} before the leave starts"],
                   ["the request is submitted fewer than {tu} before the leave starts"]))
    D.fact(PairFact("balance", ["{n} is asking for {x} days and has {y} days of leave left this year.",
                                "The request is for {x} days; {n}'s remaining leave balance is {y} days."],
                    xs=[2, 3, 4, 5, 8, 10], ds=[-3, -1, 0, 1, 5], hide=False))
    D.pred(PairPred("bal", "balance", ["the days requested do not exceed the employee's remaining leave balance"],
                    ["the days requested exceed the employee's remaining leave balance"], tags=("numeric",)))
    D.B("probation", ["the employee is still in the probationary period"], ["the employee has completed the probationary period"],
        ["{n} is still in {pos} probationary period."], ["{n} has completed {pos} probationary period."],
        q="whether {n} has completed the probationary period")
    D.B("stocktake", ["any of the requested days falls in the annual stocktake week"], ["none of the requested days falls in the annual stocktake week"],
        ["One of the requested days falls in the annual stocktake week."], ["None of the requested days falls in the annual stocktake week."],
        q="whether the requested days overlap the stocktake week")
    D.fact(NumFact("others", ["{v} other members of {n}'s team already have approved leave on at least one of the requested days."],
                   unit=("colleague", "colleagues"), zero=["No one else on {n}'s team has approved leave on any of the requested days."],
                   one=["One other member of {n}'s team already has approved leave on at least one of the requested days."],
                   q="how many teammates already have leave on those days"))
    D.pred(NumPred("staff", "others", "ge", [1, 2, 3], ["{t} or more other team members already have approved leave on any of the requested days"],
                   ["fewer than {t} other team members already have approved leave on any of the requested days"]))
    D.fact(CatFact("reason", {"holiday": ["holiday"], "emergency": ["family emergency"], "fun_parent": ["funeral (parent)"],
                              "fun_sibling": ["funeral (sibling)"], "fun_partner": ["funeral (partner)"], "fun_grand": ["funeral (grandparent)"],
                              "fun_cousin": ["funeral (cousin)"], "jury": ["jury service"], "moving": ["moving house"]},
                   {"holiday": ["{n} wants the time off for a holiday abroad."],
                    "emergency": ["{n} needs the time off to look after {pos} young son, who has been admitted to hospital after an accident."],
                    "fun_parent": ["{n} needs the time off to attend {pos} mother's funeral."],
                    "fun_sibling": ["{n} needs the time off to attend {pos} brother's funeral."],
                    "fun_partner": ["{n} needs the time off to attend {pos} partner's funeral."],
                    "fun_grand": ["{n} needs the time off to attend {pos} grandmother's funeral."],
                    "fun_cousin": ["{n} needs the time off to attend {pos} cousin's funeral."],
                    "jury": ["{n} has been summoned by the court for jury service on those days."],
                    "moving": ["{n} is moving house and needs the days off."]}, q="why {n} wants the time off"))
    D.pred(InPred("r_emerg", "reason", ["the leave is needed to care for a close family member who has been taken ill or injured"],
                  ["the leave is not needed to care for a close family member who has been taken ill or injured"],
                  fixed={"emergency"}, tags=("implicit",)))
    D.pred(InPred("r_funeral", "reason",
                  ["the leave is to attend the funeral of an immediate family member (a spouse or partner, child, parent or sibling)"],
                  ["the leave is not to attend the funeral of an immediate family member (a spouse or partner, child, parent or sibling)"],
                  fixed={"fun_parent", "fun_sibling", "fun_partner"}, tags=("implicit",)))
    D.pred(InPred("r_jury", "reason", ["the leave is for jury service required by a court summons"], ["the leave is not for jury service"],
                  fixed={"jury"}))
    D.B("manager", ["the employee's line manager has approved the request in writing"],
        ["the employee's line manager has not approved the request in writing"],
        ["{n}'s line manager has approved the request in writing."], ["{n}'s line manager has not approved the request."], hide=False)
    D.fact(NumFact("hours", ["{n} is contracted to work {v} hours a week."], lo=4, q="how many hours a week {n} is contracted for"))
    D.pred(NumPred("hrs", "hours", "ge", [16, 20, 24, 30], ["the employee is contracted for at least {t} hours a week"],
                   ["the employee is contracted for fewer than {t} hours a week"]))
    D.B("warning", ["the employee has an active written warning for attendance"], ["the employee has no active written warning for attendance"],
        ["{n} has an active written warning for attendance."], ["{n} has no warnings on file."], q="whether {n} has any active warnings",
        ev=("{n} has an active attendance warning", "{n} has no active attendance warning"))
    D.nocombine = [("tenure", "probation")]
    D.prereq = ["ten+", "note+", "manager+", "bal+", "hrs+"]
    D.grounds = [("probation+", ["refused"]), ("stocktake+", ["refused", "referred to HR"]), ("staff+", ["refused", "referred to HR"]),
                 ("warning+", ["referred to HR", "refused"]), ("note-", ["refused"]), ("ten-", ["refused", "approved as unpaid leave"]),
                 ("bal-", ["refused"])]
    D.mods = [("bal-", ["approved as unpaid leave"]), ("hrs-", ["approved as unpaid leave"]), ("ten-", ["approved as unpaid leave"])]
    D.ovr_yes = [("r_jury+", ["approved as paid leave"]), ("r_funeral+", ["approved as paid leave"])]
    D.ovr_no = [("warning+", ["referred to HR"])]
    D.exc = {"note-": ["r_emerg+", "r_funeral+"], "stocktake+": ["r_emerg+", "r_funeral+"], "staff+": ["r_emerg+", "r_funeral+"],
             "probation+": ["r_jury+", "r_funeral+"], "ten-": ["r_jury+"], "bal-": ["r_funeral+"], "manager-": ["r_emerg+"],
             "r_emerg+": ["warning+"], "r_funeral+": ["probation+"], "warning+": ["r_funeral+"], "r_jury+": ["warning+"]}
    D.terms = [dict(id="T_qual", name="qualifying employee", pool=["ten+", "hrs+", "probation-"], modes=["all"], role="prereq",
                    defs=['An employee is a "{name}" if {cond}.', 'In this policy, a "{name}" is an employee where {cond}.'],
                    pos=['the employee is a "{name}"'], neg=['the employee is not a "{name}"']),
               dict(id="T_urg", name="urgent reason", pool=["r_emerg+", "r_funeral+", "r_jury+"], modes=["any"], role="exc",
                    for_=["note-", "stocktake+", "staff+", "manager-"], defs=['A request has an "{name}" if {cond}.'],
                    pos=['the request has an "{name}"'], neg=['the request does not have an "{name}"'])]
    D.noise = ["Managers record approved leave in the HR system.", "Up to five unused days may be carried over to next year."]
    D.sources = ("the line manager", "the HR system")
    return D


# ======================================================================================================== school
def school():
    D = Domain("school")
    D.orgs = ["Westbrook High School", "Riverside Academy", "St. Brendan's College", "Lakeview Secondary School", "Hillcrest School",
              "Oakmont Sixth Form College", "Kingsley International School"]
    D.titles = ["{org} - Coursework Extension Policy", "{org} Student Handbook: Deadlines and Extensions",
                "Assessment Policy AP-{num}: Extensions ({org})", "{org}: How Extension Requests Are Decided"]
    D.extra_ctx = {"subj": ["history", "biology", "English", "geography", "chemistry", "art"], "task": ["essay", "lab report", "project", "portfolio"]}
    D.intro = ["{n}, a Year {yr} student at {org}, has asked for an extension on {pos} {subj} {task}.",
               "{n} (Year {yr}) at {org} wants more time for {a_subjtask}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "extension request", "extension requests", "an extension request", "extension requests"
    D.wr = "{n}'s extension request"
    D.appr = dict(pas="granted", noun="granting the extension", clause=["the extension is granted"])
    D.deny = dict(pas="refused", noun="refusal", clause=["the extension is refused", "the request is refused"])
    D.q_appr = ["Under the policy, is {n}'s extension request granted?", "Should the teacher grant {n} the extension under this policy?",
                "Does the policy allow {n} the extension?"]
    D.q_deny = ["Under the policy, must {n}'s extension request be refused?", "Is {n} refused the extension under this policy?"]
    D.codes = ["extension granted", "two-day extension only", "referred to the head of year", "extension refused"]
    D.code_clause = {"extension granted": ["the extension is granted", "the full extension is granted"],
                     "two-day extension only": ["only a two-day extension is allowed", "the student gets a two-day extension instead of the time asked for"],
                     "referred to the head of year": ["the request is referred to the head of year", "the head of year decides the request"],
                     "extension refused": ["the extension is refused", "the request is refused"]}
    D.code_def = {"extension granted": "The policy, applied with its exceptions and precedence, gives the full extension asked for.",
                  "two-day extension only": "The policy allows a two-day extension, not the full time asked for.",
                  "referred to the head of year": "The policy passes the request to the head of year instead of the teacher deciding it.",
                  "extension refused": "The policy gives no extension."}
    D.deny_code, D.best = "extension refused", "extension granted"
    D.fact(CatFact("year", {"9": ["9"], "10": ["10"], "11": ["11"], "12": ["12"], "13": ["13"]}, None, binds="yr", hide=False))
    D.pred(InPred("senior", "year", ["the student is in Year 12 or Year 13"], ["the student is in Year 9, 10 or 11"], fixed={"12", "13"}))
    D.fact(NumFact("ask", ["{n} asked for the extension {vu} before the deadline."], zero=["{n} asked for the extension on the day of the deadline."],
                   negt=["{n} asked for the extension {au} after the deadline had passed."], lo=-3, q="when {n} asked for the extension"))
    D.pred(NumPred("ask", "ask", "ge", [2, 3, 5], ["the extension is requested at least {tu} before the deadline"],
                   ["the extension is requested fewer than {tu} before the deadline, or after it"]))
    D.fact(NumFact("length", ["{n} is asking for {vu} of extra time."], unit=("school day", "school days"), lo=1, q="how much extra time {n} wants"))
    D.pred(NumPred("len", "length", "le", [3, 5, 7, 10], ["the extension asked for is no longer than {tu}"],
                   ["the extension asked for is longer than {tu}"], unit=("school day", "school days")))
    D.fact(NumFact("prior", ["{n} has already had {vu} this term."], unit=("extension", "extensions"),
                   zero=["This would be {n}'s first extension this term."], q="how many extensions {n} has had this term"))
    D.pred(NumPred("prior", "prior", "lt", [2, 3], ["the student has had fewer than {t} extensions this term"],
                   ["the student has already had {t} or more extensions this term"]))
    D.B("note", ["the request comes with a note from a doctor or a parent"], ["the request comes with no note from a doctor or a parent"],
        ["{n}'s parent sent a signed note explaining the reason."], ["No note from a doctor or parent came with the request."], hide=False)
    D.B("plan", ["the student has a learning support plan that allows extra time"],
        ["the student does not have a learning support plan that allows extra time"],
        ["{n} has a learning support plan that allows extra time on coursework."], ["{n} does not have a learning support plan."],
        q="whether {n} has a learning support plan")
    D.B("capstone", ["the assignment is the final capstone project"], ["the assignment is not the final capstone project"],
        ["The assignment is {n}'s final capstone project."], ["The assignment is ordinary coursework, not the capstone project."],
        q="whether the assignment is the capstone project")
    D.B("board", ["the assignment is marked by the external exam board"], ["the assignment is marked within the school"],
        ["The assignment will be sent to the external exam board for marking."], ["The assignment is marked by {n}'s own teacher."],
        q="who marks the assignment")
    D.B("group", ["the assignment is group work"], ["the assignment is individual work"],
        ["It is a group assignment shared with three classmates."], ["It is an individual assignment."], q="whether the assignment is group work")
    D.B("teamok", ["every other member of the group agrees to the new date"], ["not every other member of the group agrees to the new date"],
        ["All three of {n}'s groupmates have agreed to the new date."], ["One of {n}'s groupmates has not agreed to the new date."],
        q="whether all of {n}'s groupmates agree to the new date", req=("group", True), guard=("group", True))
    D.B("event", ["the student was away representing the school at an official event"],
        ["the student was not away representing the school at an official event"],
        ["{n} spent the week before the deadline representing the school at the regional debate championship."],
        ["{n} was not away on any school event before the deadline."], q="whether {n} was away on a school event",
        ev=("{n} was away at an official school event", "{n} was not away at any school event"))
    D.fact(NumFact("sick", ["{n} was off sick for {vu} in the two weeks before the deadline."], unit=("school day", "school days"),
                   zero=["{n} did not miss any school through illness in the two weeks before the deadline."], q="how many days {n} was off sick"))
    D.pred(NumPred("sick", "sick", "ge", [2, 3, 5], ["the student was absent through illness for at least {tu} in the two weeks before the deadline"],
                   ["the student was absent through illness for fewer than {tu} in the two weeks before the deadline"],
                   unit=("school day", "school days")))
    D.fact(RatioFact("attend", ["{n} has attended {a} of the {b} school days so far this term."], wholes=[40, 60, 80, 100], money=False,
                     q="what {n}'s attendance is this term"))
    D.pred(RatioPred("att", "attend", "ge", [85, 90, 95], ["the student's attendance this term is at least {t}%"],
                     ["the student's attendance this term is below {t}%"], tags=("numeric", "implicit")))
    D.prereq = ["ask+", "len+", "prior+", "note+", "att+"]
    D.grounds = [("capstone+", ["extension refused", "referred to the head of year"]), ("board+", ["referred to the head of year", "extension refused"]),
                 ("prior-", ["extension refused", "referred to the head of year"]), ("ask-", ["extension refused", "two-day extension only"]),
                 ("att-", ["extension refused"]), ("group+", ["extension refused"])]
    D.mods = [("len-", ["two-day extension only"]), ("senior+ & len-", ["two-day extension only"])]
    D.ovr_yes = [("plan+", ["extension granted"]), ("event+", ["extension granted"])]
    D.ovr_no = [("board+", ["referred to the head of year"])]
    D.exc = {"ask-": ["sick+", "event+"], "len-": ["plan+"], "prior-": ["plan+", "sick+"], "note-": ["event+"], "capstone+": ["plan+", "sick+"],
             "group+": ["teamok+"], "att-": ["sick+", "event+"], "plan+": ["board+"], "event+": ["capstone+"], "sick+": ["note-"],
             "senior+ & len-": ["plan+"], "teamok+": ["capstone+"]}
    D.terms = [dict(id="T_sup", name="supported student", pool=["plan+", "event+", "sick+"], modes=["any", "k2"], role="exc",
                    for_=["ask-", "prior-", "att-", "capstone+", "len-"], defs=['A student is a "{name}" if {cond}.'],
                    pos=['the student is a "{name}"'], neg=['the student is not a "{name}"']),
               dict(id="T_std", name="standard request", pool=["ask+", "len+", "prior+"], modes=["all"], role="prereq",
                    defs=['An extension request is a "{name}" if {cond}.'], pos=['the request is a "{name}"'], neg=['the request is not a "{name}"'])]
    D.noise = ["Extensions are recorded on the school portal.", "Teachers confirm new deadlines by email."]
    D.sources = ("the student", "the school's records")
    return D


# ======================================================================================================== grants
def grants():
    D = Domain("grants")
    D.orgs = ["Fairview Community Foundation", "Millbrook Arts Council", "The Rosedale Trust", "Clearwater Neighbourhood Fund",
              "Thornbury Heritage Fund", "Bayside Youth Grants Programme", "Evergreen Green Spaces Fund"]
    D.titles = ["{org} - Small Grants: Eligibility and Decisions", "{org} Grant Guidelines", "How {org} Decides Grant Applications",
                "Funding Rules ({org}), Round {num}"]
    D.extra_ctx = {"g": ["the Oakside Tenants' Association", "Riverside Youth Football Club", "the Green Lane Allotment Society",
                         "Hope Street Food Bank", "the Northfield Community Choir", "Cedar Valley Wildlife Volunteers",
                         "the Millbrook Men's Shed", "Harbour Road Youth Theatre"],
                   "project": ["a summer holiday club", "free coding workshops for teenagers", "a local history exhibition",
                               "a riverside litter clean-up", "weekly lunch clubs for older residents", "a community garden"]}
    D.intro = ["{G} has applied to {org} for a grant to fund {project}.", "{n}, secretary of {g}, has sent {org} a grant application for {project}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "application", "applications", "an application", "applications"
    D.wr = "{g}'s application"
    D.appr = dict(pas="approved", noun="approval", clause=["the application is approved", "the grant is awarded"])
    D.deny = dict(pas="declined", noun="declining the application", clause=["the application is declined"])
    D.q_appr = ["Under these rules, is {g}'s application approved?", "Does {g} get the grant under these rules?"]
    D.q_deny = ["Under these rules, must {g}'s application be declined?", "Is {g}'s application declined under these rules?"]
    D.codes = ["fund in full", "fund at a reduced amount", "refer to the full panel", "decline"]
    D.code_clause = {"fund in full": ["the grant is awarded in full"], "fund at a reduced amount": ["the grant is awarded at a reduced amount"],
                     "refer to the full panel": ["the application is referred to the full panel"], "decline": ["the application is declined"]}
    D.code_def = {"fund in full": "The rules, applied with their exceptions and precedence, award the whole amount requested.",
                  "fund at a reduced amount": "The rules award a grant, but less than the amount requested.",
                  "refer to the full panel": "The rules send the application to the full panel instead of deciding it now.",
                  "decline": "The rules lead to no grant."}
    D.deny_code, D.best = "decline", "fund in full"
    D.B("charity", ["the applicant is a registered charity or non-profit"], ["the applicant is not a registered charity or non-profit"],
        ["{G} is a registered charity."], ["{G} is an informal group that is not registered as a charity or non-profit."],
        q="whether {g} is a registered charity", ev=("{g} is a registered charity", "{g} is not registered as a charity"))
    D.B("local", ["the project takes place within the county"], ["the project takes place outside the county"],
        ["All of the activities will take place within the county."], ["The activities will take place in a neighbouring county."],
        q="where the activities will take place")
    D.fact(NumFact("amount", ["{G} is asking for {vm}.", "The application requests {vm}."], money=True, lo=100, q="how much {g} is asking for"))
    D.pred(NumPred("amt_ok", "amount", "le", [5000, 10000, 15000], ["the amount requested is no more than {tm}"],
                   ["the amount requested is more than {tm}"], money=True))
    D.pred(NumPred("amt_big", "amount", "gt", [2000, 2500, 4000], ["the amount requested is more than {tm}"],
                   ["the amount requested is {tm} or less"], money=True))
    D.fact(NumFact("late", ["{G} submitted the application {vu} after the deadline."], zero=["{G} submitted the application on the deadline day."],
                   negt=["{G} submitted the application {au} before the deadline."], lo=-12, extra=(-10, -7, 3, 6),
                   dates=["The deadline was {d1}; the application arrived on {d2}."], q="when the application arrived"))
    D.pred(NumPred("ontime", "late", "le", [0], ["the application arrives by the deadline (the deadline day itself counts)"],
                   ["the application arrives after the deadline"]))
    D.fact(RatioFact("match", ["The project will cost {b} in total, and {g} will pay {a} of that from its own funds."],
                     wholes=[2000, 4000, 8000, 10000, 20000], q="how much of the cost {g} will pay itself"))
    D.pred(RatioPred("match", "match", "ge", [10, 20, 25], ["the applicant pays at least {t}% of the total project cost from its own funds"],
                     ["the applicant pays less than {t}% of the total project cost from its own funds"], tags=("numeric", "implicit")))
    D.fact(NumFact("years", ["{G} was founded {vu} ago."], unit=("year", "years"), zero=["{G} was founded earlier this year."],
                   q="how long {g} has existed"))
    D.pred(NumPred("est", "years", "ge", [1, 2, 3], ["the applicant has been operating for at least {tu}"],
                   ["the applicant has been operating for less than {tu}"], unit=("year", "years")))
    D.B("political", ["the project involves party-political campaigning"], ["the project involves no party-political campaigning"],
        ["Part of the project is campaigning for a candidate in the local election."], ["The project involves no political campaigning."],
        q="whether the project involves political campaigning")
    D.B("religious", ["the applicant is a religious organisation"], ["the applicant is not a religious organisation"],
        ["{G} is run by a local church."], ["{G} has no religious affiliation."], q="whether {g} is a religious organisation")
    D.B("openall", ["the project is open to everyone and includes no worship"], ["the project is not open to everyone or includes worship"],
        ["The project is open to everyone and includes no worship."], ["The project includes a weekly prayer session for participants."],
        q="whether the project includes worship", req=("religious", True), guard=("religious", True))
    D.B("overdue", ["the applicant has an earlier grant from us whose final report is overdue"],
        ["the applicant has no overdue final report on an earlier grant from us"],
        ["{G}'s final report on an earlier {org} grant is two months overdue."], ["{G} has no overdue reports with {org}."],
        q="whether {g} has any overdue reports with {org}")
    D.B("capital", ["the grant would pay for building work or vehicles"], ["the grant would not pay for building work or vehicles"],
        ["Most of the grant would pay for building work."], ["The grant would pay only for running costs such as staff time and materials."],
        q="what the grant would pay for")
    D.B("access", ["the building work is needed to make a building accessible to disabled people"],
        ["the building work is not needed to make a building accessible to disabled people"],
        ["The building work is a wheelchair ramp and an accessible toilet."], ["The building work is a new kitchen."],
        q="what the building work is for", req=("capital", True), guard=("capital", True))
    D.B("rural", ["the project serves a rural community"], ["the project does not serve a rural community"],
        ["The project serves a small rural village."], ["The project serves a town-centre neighbourhood."], q="what kind of community the project serves")
    D.fact(NumFact("income", ["{G}'s income last year was {vm}."], money=True, lo=500, q="what {g}'s annual income is"))
    D.pred(NumPred("small", "income", "lt", [25000, 50000, 100000], ["the applicant's annual income is under {tm}"],
                   ["the applicant's annual income is {tm} or more"], money=True))
    D.B("partner", ["the project is run jointly with a local school"], ["the project is not run jointly with a local school"],
        ["The project is run jointly with Hillside Primary School."], ["No school is involved in the project."], q="whether a school is involved")
    D.fact(NumFact("past", ["{G} has received {vu} from {org} in the past five years."], unit=("grant", "grants"),
                   zero=["{G} has not received any grant from {org} in the past five years."], one=["{G} has received one grant from {org} in the past five years."],
                   q="how many grants {g} has received before"))
    D.pred(NumPred("repeat", "past", "ge", [2, 3], ["the applicant has received {t} or more of our grants in the past five years"],
                   ["the applicant has received fewer than {t} of our grants in the past five years"]))
    D.prereq = ["charity+", "local+", "ontime+", "amt_ok+", "match+", "est+"]
    D.grounds = [("political+", ["decline"]), ("religious+", ["decline"]), ("overdue+", ["decline", "refer to the full panel"]),
                 ("capital+", ["decline", "fund at a reduced amount"]), ("repeat+", ["fund at a reduced amount", "decline"]),
                 ("match-", ["fund at a reduced amount", "decline"]), ("est-", ["decline"]),
                 ("amt_ok-", ["fund at a reduced amount", "refer to the full panel"]), ("ontime-", ["decline"])]
    D.mods = [("amt_big+", ["refer to the full panel"])]
    D.ovr_no = [("overdue+", ["decline"]), ("political+", ["decline"])]
    D.exc = {"match-": ["rural+", "small+"], "est-": ["partner+"], "religious+": ["openall+"], "capital+": ["access+"], "repeat+": ["small+"],
             "charity-": ["partner+"], "rural+": ["political+"], "small+": ["overdue+"], "partner+": ["local-"], "amt_ok-": ["rural+"],
             "local-": ["partner+"], "access+": ["amt_ok-"]}
    D.terms = [dict(id="T_elig", name="eligible applicant", pool=["charity+", "est+", "overdue-"], modes=["all"], role="prereq",
                    defs=['An applicant is an "{name}" if {cond}.'], pos=['the applicant is an "{name}"'], neg=['the applicant is not an "{name}"']),
               dict(id="T_prio", name="priority project", pool=["rural+", "partner+", "small+"], modes=["any", "k2"], role="exc",
                    for_=["match-", "repeat+", "est-"], defs=['A project is a "{name}" if {cond}.'],
                    pos=['the project is a "{name}"'], neg=['the project is not a "{name}"'])]
    D.noise = ["Decisions are announced within eight weeks of the deadline.", "Successful applicants send a short final report when the project ends."]
    D.sources = ("the application form", "the charity register")
    return D


# ======================================================================================================== travel
def travel():
    D = Domain("travel")
    D.orgs = ["Halcyon Consulting", "Vantage Biotech", "Meridian Engineering", "Castlegate University", "Parkside Health Services",
              "Orion Analytics", "Silverline Media"]
    D.titles = ["{org} Travel and Expenses Policy", "{org} - Business Travel: What We Reimburse", "Finance Policy FIN-{num}: Travel Claims ({org})"]
    D.intro = ["{n} has submitted an expense claim to {org} for a business trip to {city}.",
               "{n} is claiming back the costs of a work trip to {city} from {org}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "expense claim", "expense claims", "an expense claim", "expense claims"
    D.wr = "{n}'s expense claim"
    D.appr = dict(pas="reimbursed", noun="reimbursement", clause=["the claim is reimbursed", "the claim is paid"])
    D.deny = dict(pas="rejected", noun="rejection", clause=["the claim is rejected"])
    D.q_appr = ["Under the policy, is {n}'s expense claim reimbursed?", "Should finance pay {n}'s expense claim under this policy?"]
    D.q_deny = ["Under the policy, must {n}'s expense claim be rejected?", "Is {n}'s claim rejected under this policy?"]
    D.codes = ["reimburse in full", "reimburse up to the policy limits", "refer to the finance director", "reject the claim"]
    D.code_clause = {"reimburse in full": ["the claim is reimbursed in full"],
                     "reimburse up to the policy limits": ["the claim is reimbursed only up to the policy limits"],
                     "refer to the finance director": ["the claim is referred to the finance director"],
                     "reject the claim": ["the claim is rejected"]}
    D.code_def = {"reimburse in full": "The policy, applied with its exceptions and precedence, pays back everything claimed.",
                  "reimburse up to the policy limits": "The policy pays the claim only up to its limits, so part of it is not paid.",
                  "refer to the finance director": "The policy sends the claim to the finance director instead of deciding it now.",
                  "reject the claim": "The policy pays nothing for the claim."}
    D.deny_code, D.best = "reject the claim", "reimburse in full"
    D.fact(TableFact("hotel", ["{n}'s hotel in {k} cost {xm} per night.", "The hotel in {k} charged {xm} a night."],
                     keys=["London", "New York", "Paris", "Tokyo", "Chicago", "Berlin", "Singapore", "Toronto", "Madrid", "Sydney", "Dublin", "Boston"],
                     binds="city", hide=False))
    D.pred(TablePred("hotel_ok", "hotel", "le", ["the nightly hotel rate is no more than the limit for that city in Table 1"],
                     ["the nightly hotel rate is above the limit for that city in Table 1"],
                     keys=["London", "New York", "Paris", "Tokyo", "Chicago", "Berlin", "Singapore", "Toronto", "Madrid", "Sydney", "Dublin", "Boston"],
                     lims=[150, 180, 200, 220, 250, 275, 300], step=1, far=25, title="Table 1 - Nightly hotel limits",
                     cols=("City", "Limit per night"), star="Any other city", money=True, tags=("table", "numeric")))
    D.B("preappr", ["the trip was approved in advance by the budget holder"], ["the trip was not approved in advance by the budget holder"],
        ["{n}'s budget holder approved the trip in writing before it was booked."], ["{n} booked the trip without getting approval first."],
        q="whether the trip was approved in advance")
    D.B("receipts", ["itemised receipts are attached for every expense"], ["at least one itemised receipt is missing"],
        ["Itemised receipts are attached for every expense."], ["The receipt for one of the meals is missing from the claim."], hide=False)
    D.fact(NumFact("submit", ["{n} submitted the claim {vu} after getting back from the trip."],
                   zero=["{n} submitted the claim on the day {sub} got back."],
                   dates=["{n} got back from the trip on {d1} and submitted the claim on {d2}."], q="when the claim was submitted"))
    D.pred(NumPred("sub_ok", "submit", "le", [30, 45, 60, 90],
                   ["the claim is submitted within {tu} of the end of the trip (day {t} included)", "the claim is submitted no more than {tu} after the trip ends"],
                   ["the claim is submitted more than {tu} after the trip ends"]))
    D.fact(CatFact("cls", {"economy": ["economy"], "premium": ["premium economy"], "business": ["business class"]},
                   {"economy": ["{n} flew economy."], "premium": ["{n} flew premium economy."], "business": ["{n} flew business class."]},
                   q="which class {n} flew in"))
    D.pred(InPred("biz", "cls", ["the flight was booked in business class"], ["the flight was not booked in business class"], fixed={"business"}))
    D.pred(InPred("above_econ", "cls", ["the flight was booked in any class above economy"], ["the flight was booked in economy"],
                  fixed={"premium", "business"}))
    D.fact(NumFact("dur", ["The flight took {vu}.", "The flight time was {vu}."], minutes=True, lo=60, conv=Fr(1, 60), q="how long the flight took"))
    D.pred(NumPred("long", "dur", "gt", [6, 8, 10], ["the flight lasts more than {t} hours"], ["the flight lasts {t} hours or less"],
                   conv=Fr(1, 60), btol=Fr(1, 30), tags=("units",)))
    D.fact(NumFact("miles", ["{n} drove {vu} in total for the trip."], unit=("mile", "miles"), lo=1, conv=Fr(1609344, 1000000),
                   q="how far {n} drove"))
    D.pred(NumPred("far", "miles", "gt", [50, 80, 100, 160], ["the total distance driven is more than {t} km"],
                   ["the total distance driven is {t} km or less"], conv=Fr(1609344, 1000000), btol=Fr(2), tags=("units",)))
    D.B("alcohol", ["the claim includes alcohol"], ["the claim includes no alcohol"], ["The claim includes {cur}38 for wine with dinner."],
        ["The claim includes no alcohol."], q="whether the claim includes alcohol")
    D.B("client", ["the meal was with a client"], ["the meal was not with a client"], ["The dinner was with two people from a client company."],
        ["{n} ate dinner alone."], q="who the dinner was with")
    D.B("personal", ["personal holiday days were added to the trip"], ["no personal holiday days were added to the trip"],
        ["{n} added two days of personal holiday at the end of the trip."], ["The trip included no personal days."],
        q="whether the trip included personal days", ev=("personal days were added to the trip", "no personal days were added to the trip"))
    D.B("spouse", ["the claim includes costs for a spouse or partner"], ["the claim includes no costs for a spouse or partner"],
        ["The claim includes the cost of {n}'s partner's train ticket."], ["The claim covers only {n}'s own costs."],
        q="whether the claim includes a partner's costs")
    D.B("taxi", ["the claim includes a taxi fare"], ["the claim includes no taxi fare"], ["The claim includes a taxi fare back to the hotel."],
        ["The claim includes no taxi fares."], q="whether the claim includes a taxi fare")
    D.fact(TimeFact("taxitime", ["The taxi was taken at {tm}."], req=("taxi", True), q="what time the taxi was taken"))
    D.pred(TimePred("night", "taxitime", [(1320, 360), (1350, 330), (1260, 300)], ["the taxi was taken between {s} and {e} (both times included)"],
                    ["the taxi was not taken between {s} and {e}"], guard=("taxi", True), tags=("temporal",)))
    D.B("urgent", ["the trip was an emergency call-out"], ["the trip was not an emergency call-out"],
        ["The trip was an emergency call-out to fix a client's system."], ["The trip was a planned visit."], q="whether the trip was an emergency call-out")
    D.fact(NumFact("total", ["The claim totals {vm}."], money=True, lo=50, q="what the claim totals"))
    D.pred(NumPred("big", "total", "gt", [1000, 2500, 5000], ["the claim totals more than {tm}"], ["the claim totals {tm} or less"], money=True))
    D.B("confhotel", ["the hotel was booked by the organisation the employee was visiting"], ["the hotel was not booked by the organisation the employee was visiting"],
        ["The organisation {n} was visiting booked the hotel for {obj}."], ["{n} booked the hotel {refl}."], q="who booked the hotel")
    D.B("sickleave", ["the employee was on sick leave at some point during the period allowed for submitting the claim"],
        ["the employee was not on sick leave at any point during the period allowed for submitting the claim"],
        ["{n} went on sick leave the day after the trip and was off for three weeks."], ["{n} was not on sick leave at any point after the trip."],
        q="whether {n} was on sick leave after the trip")
    D.prereq = ["preappr+", "receipts+", "sub_ok+"]
    D.grounds = [("alcohol+", ["reimburse up to the policy limits"]), ("hotel_ok-", ["reimburse up to the policy limits", "reject the claim"]),
                 ("biz+", ["reimburse up to the policy limits", "reject the claim"]), ("above_econ+", ["reimburse up to the policy limits"]),
                 ("personal+", ["reimburse up to the policy limits"]), ("spouse+", ["reject the claim", "reimburse up to the policy limits"]),
                 ("sub_ok-", ["reject the claim"]), ("preappr-", ["reject the claim", "refer to the finance director"]),
                 ("far-", ["reject the claim"]), ("taxi+", ["reimburse up to the policy limits"])]
    D.mods = [("big+", ["refer to the finance director"])]
    D.exc = {"alcohol+": ["client+"], "biz+": ["long+"], "above_econ+": ["long+"], "hotel_ok-": ["confhotel+"], "sub_ok-": ["sickleave+"],
             "preappr-": ["urgent+"], "taxi+": ["night+"], "long+": ["personal+"], "urgent+": ["big+"], "client+": ["spouse+"],
             "night+": ["alcohol+"], "confhotel+": ["personal+"]}
    D.terms = [dict(id="T_long", name="long-haul flight", pool=["long+"], modes=["all"], role="exc", for_=["biz+", "above_econ+"],
                    defs=['In this policy, a flight counts as a "{name}" if {cond}.'], pos=['the flight is a "{name}"'], neg=['the flight is not a "{name}"']),
               dict(id="T_comp", name="compliant claim", pool=["receipts+", "sub_ok+", "preappr+"], modes=["all"], role="prereq",
                    defs=['A claim is a "{name}" if {cond}.'], pos=['the claim is a "{name}"'], neg=['the claim is not a "{name}"'])]
    D.noise = ["Approved claims are paid with the next monthly salary.", "Foreign-currency amounts are converted at the rate on the day of purchase."]
    D.sources = ("the employee's claim form", "the travel booking system")
    return D


# ======================================================================================================== pharmacy
CONTROLLED = ["oxycodone", "morphine sulfate", "lorazepam", "diazepam", "methylphenidate", "tramadol", "codeine phosphate"]
ORDINARY = ["amoxicillin", "metformin", "lisinopril", "atorvastatin", "omeprazole", "sertraline", "levothyroxine", "salbutamol (inhaler)"]


def pharmacy():
    D = Domain("pharmacy")
    D.orgs = ["Greenleaf Pharmacy", "CityCare Chemists", "Riverside Community Pharmacy", "Well Street Pharmacy", "Harbour Health Pharmacy",
              "Parkway Drug Store"]
    D.titles = ["{org} Dispensing Policy", "{org} - Standard Operating Procedure: Dispensing", "SOP D-{num}: Prescription Checks ({org})"]
    D.intro = ["{n} has brought a prescription for {drug} to {org}.", "At {org}, {n} has handed in a prescription for {drug}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "prescription", "prescriptions", "a prescription", "prescriptions"
    D.wr = "the prescription {n} brought in"
    D.appr = dict(pas="dispensed", noun="dispensing", clause=["the prescription is dispensed", "the medicine is dispensed"])
    D.deny = dict(pas="refused", noun="refusal", clause=["the prescription is not dispensed", "the pharmacist refuses to dispense it"])
    D.q_appr = ["Under the policy, should the pharmacy dispense the prescription {n} brought in?",
                "Does this policy allow the pharmacist to dispense the medicine to {n}?"]
    D.q_deny = ["Under the policy, must the pharmacist refuse to dispense the medicine to {n}?",
                "Is the prescription {n} brought in refused under this policy?"]
    D.codes = ["dispense", "dispense after a pharmacist consultation", "contact the prescriber first", "do not dispense"]
    D.code_clause = {"dispense": ["the prescription is dispensed", "the medicine is dispensed"],
                     "dispense after a pharmacist consultation": ["the medicine is dispensed only after a consultation with the pharmacist"],
                     "contact the prescriber first": ["the pharmacist must contact the prescriber before anything is dispensed"],
                     "do not dispense": ["the prescription is not dispensed", "the pharmacy refuses to dispense the prescription"]}
    D.code_def = {"dispense": "The policy, applied with its exceptions and precedence, lets the medicine be handed over as normal.",
                  "dispense after a pharmacist consultation": "The medicine may be handed over, but only after the pharmacist has a consultation with the patient.",
                  "contact the prescriber first": "Nothing is handed over until the pharmacist has contacted the prescriber.",
                  "do not dispense": "The policy does not allow the medicine to be handed over."}
    D.deny_code, D.best = "do not dispense", "dispense"
    D.fact(CatFact("drug", {d: [d] for d in CONTROLLED + ORDINARY}, None, binds="drug", hide=False, neutral=ORDINARY))
    D.pred(InPred("sched", "drug", ["the medicine is {list_or}"], ["the medicine is none of the following: {list}"], restrict=CONTROLLED, k=(3, 5),
                  sched=("Schedule C", "medicines with extra checks"), spos=["the medicine is listed in Schedule C"],
                  sneg=["the medicine is not listed in Schedule C"], tags=("multi_hop",)))
    D.fact(NumFact("rxage", ["The prescription was written {vu} ago."], zero=["The prescription was written today."],
                   dates=["The prescription is dated {d1}; {n} brought it in on {d2}."], q="when the prescription was written"))
    D.pred(NumPred("fresh", "rxage", "le", [28, 30, 90, 180], ["the prescription was written no more than {tu} before it is presented"],
                   ["the prescription was written more than {tu} before it is presented"]))
    D.B("signed", ["the prescription is signed by the prescriber"], ["the prescription is not signed by the prescriber"],
        ["The prescription carries the prescriber's signature."], ["The prescription has not been signed."], hide=False)
    D.B("photoid", ["the person collecting shows photo ID"], ["the person collecting shows no photo ID"], ["{n} showed a passport as photo ID."],
        ["{n} had no photo ID."], hide=False)
    D.fact(CatFact("collector", {"patient": ["patient"], "rep": ["named representative"], "family": ["unnamed relative"], "friend": ["neighbour"]},
                   {"patient": ["{n} is the patient and is collecting the medicine in person."],
                    "rep": ["{n} is collecting the medicine for a relative, who named {n} on the prescription as their representative."],
                    "family": ["{n} is collecting the medicine for a relative and is not named anywhere on the prescription."],
                    "friend": ["{n} is collecting the medicine for a neighbour and is not named on the prescription."]},
                   q="who the medicine is for"))
    D.pred(InPred("self", "collector", ["the medicine is collected by the patient in person"], ["the medicine is not collected by the patient in person"],
                  fixed={"patient"}))
    D.pred(InPred("authcol", "collector", ["the person collecting is the patient or the patient's named representative"],
                  ["the person collecting is neither the patient nor the patient's named representative"], fixed={"patient", "rep"}))
    D.fact(NumFact("lastfill", ["The previous 30-day supply of the same medicine was dispensed {vu} ago."], lo=1, q="when the previous supply was dispensed"))
    D.pred(NumPred("early", "lastfill", "lt", [21, 24, 25, 27], ["the previous supply was dispensed fewer than {tu} ago"],
                   ["the previous supply was dispensed at least {tu} ago"]))
    D.B("interact", ["the pharmacy system shows an interaction alert with the patient's other medicines"], ["the pharmacy system shows no interaction alert"],
        ["The pharmacy system shows an interaction alert with another medicine on the patient's record."], ["The pharmacy system shows no interaction alerts."],
        q="whether the system shows an interaction alert")
    D.B("confirmed", ["the prescriber has confirmed the prescription by phone"], ["the prescriber has not confirmed the prescription by phone"],
        ["The pharmacist phoned the prescriber, who confirmed the prescription."], ["The pharmacist could not reach the prescriber."],
        q="whether the prescriber has confirmed the prescription")
    D.fact(NumFact("age", ["The patient is {vu} old."], unit=("year", "years"), lo=1, hi=99, q="how old the patient is"))
    D.pred(NumPred("minor", "age", "lt", [12, 16, 18], ["the patient is under {t}"], ["the patient is {t} or older"]))
    D.B("runout", ["the patient has no doses of the medicine left"],
        ["the patient still has doses of the medicine left"],
        ["The patient has no doses of the medicine left at home."], ["The patient still has a week's supply at home."],
        q="how much of the medicine the patient has left")
    D.B("altered", ["the prescription shows signs of alteration"], ["the prescription shows no signs of alteration"],
        ["The quantity on the prescription has been written over in different ink."], ["The prescription shows no signs of alteration."],
        q="whether the prescription has been altered", ev=("the prescription had been altered", "the prescription had not been altered"))
    D.B("lost", ["the patient's previous supply was reported lost or stolen"], ["the patient's previous supply was not reported lost or stolen"],
        ["The patient reported the previous supply stolen and has a police reference number."],
        ["There is no report that the previous supply was lost or stolen."], q="whether the previous supply was reported lost")
    D.prereq = ["signed+", "fresh+", "photoid+"]
    D.grounds = [("altered+", ["do not dispense"]), ("fresh-", ["do not dispense", "contact the prescriber first"]),
                 ("early+", ["do not dispense", "contact the prescriber first"]), ("sched+ & authcol-", ["do not dispense"]),
                 ("sched+ & photoid-", ["do not dispense"]), ("signed-", ["do not dispense", "contact the prescriber first"]),
                 ("interact+", ["dispense after a pharmacist consultation", "contact the prescriber first"]),
                 ("minor+", ["dispense after a pharmacist consultation"])]
    D.mods = [("interact+", ["dispense after a pharmacist consultation"]), ("self- & minor+", ["contact the prescriber first"])]
    D.ovr_yes = [("runout+", ["dispense"])]
    D.ovr_no = [("altered+", ["do not dispense"])]
    D.exc = {"fresh-": ["runout+"], "early+": ["lost+"], "signed-": ["confirmed+"], "interact+": ["confirmed+"], "runout+": ["sched+"],
             "confirmed+": ["altered+"], "lost+": ["sched+"], "altered+": ["confirmed+"], "minor+": ["self-"]}
    D.terms = [dict(id="T_valid", name="valid prescription", pool=["signed+", "fresh+", "altered-"], modes=["all"], role="prereq",
                    defs=['A prescription is a "{name}" if {cond}.', 'In this procedure, a "{name}" is one where {cond}.'],
                    pos=['the prescription is a "{name}"'], neg=['the prescription is not a "{name}"'])]
    D.noise = ["Every dispensed medicine is labelled with the patient's name and directions.", "Patients may ask the pharmacist for advice at any time."]
    D.sources = ("the patient", "the pharmacy's records")
    return D


# ======================================================================================================== access
ZONES = ["main lobby", "open-plan office", "records room", "chemistry lab", "server room", "clean room", "archive vault", "loading dock", "plant room"]


def access():
    D = Domain("access")
    D.orgs = ["Helix Research Labs", "Northbridge Data Centre", "Atlas Manufacturing Plant", "Crown Street Offices", "Kepler Space Systems",
              "Pioneer Biobank"]
    D.titles = ["{org} - Physical Access Control Policy", "{org} Security Standard SEC-{num}: Door Access", "Who May Enter What at {org}"]
    D.intro = ["{n} swiped {pos} badge at the door to the {zone} at {org}.", "{n} asked the {org} security desk to be let into the {zone}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "access request", "access requests", "an access request", "access requests"
    D.wr = "{n}'s request to enter the {zone}"
    D.appr = dict(pas="granted", noun="granting access", clause=["access is granted", "the door is opened for the person"])
    D.deny = dict(pas="denied", noun="denying access", clause=["access is denied"])
    D.q_appr = ["Under the policy, should {n} be let into the {zone}?", "Does the policy allow {n} to enter the {zone}?"]
    D.q_deny = ["Under the policy, must {n} be refused entry to the {zone}?", "Is {n} denied access to the {zone} under this policy?"]
    D.codes = ["grant access", "grant access with an escort only", "deny access", "deny access and alert security"]
    D.code_clause = {"grant access": ["access is granted", "the door is opened for the person"],
                     "grant access with an escort only": ["access is granted only with an escort"],
                     "deny access": ["access is denied"], "deny access and alert security": ["access is denied and security is alerted"]}
    D.code_def = {"grant access": "The policy, applied with its exceptions and precedence, lets the person in without conditions.",
                  "grant access with an escort only": "The policy lets the person in only if someone cleared for the area escorts them.",
                  "deny access": "The policy keeps the person out, with no alert.",
                  "deny access and alert security": "The policy keeps the person out and requires security to be alerted."}
    D.deny_code, D.best = "deny access", "grant access"
    D.fact(TableFact("badge", ["{n} holds a level {x} security badge.", "{n}'s badge is cleared to level {x}."], keys=ZONES, binds="zone", hide=False))
    D.pred(TablePred("clr", "badge", "ge", ["the person's badge level is at least the minimum level listed for that area in Table 1"],
                     ["the person's badge level is below the minimum level listed for that area in Table 1"], keys=ZONES, lims=[1, 2, 3, 4, 5],
                     step=1, far=2, title="Table 1 - Minimum badge level by area", cols=("Area", "Minimum badge level"),
                     star="All other areas", lo=0, tags=("table", "numeric")))
    D.fact(TimeFact("time", ["It was {tm} when {n} tried to get in."], q="what time {n} tried to get in"))
    D.pred(TimePred("hours", "time", [(420, 1140), (390, 1200), (480, 1080)], ["the entry is between {s} and {e} (both times included)"],
                    ["the entry is before {s} or after {e}"], tags=("temporal",)))
    D.B("escort", ["the person is escorted by an employee cleared for that area"], ["the person is not escorted by an employee cleared for that area"],
        ["{n} was accompanied by a staff member who is cleared for the area."], ["{n} was on {pos} own."], q="whether anyone was escorting {n}",
        ev=("{n} was escorted by a cleared staff member", "{n} was on {pos} own"))
    D.fact(CatFact("status", {"employee": ["employee"], "contractor": ["contractor"], "visitor": ["visitor"]},
                   {"employee": ["{n} is a permanent employee."], "contractor": ["{n} is a contractor from an outside maintenance firm."],
                    "visitor": ["{n} is a visitor from a partner company."]}, q="whether {n} is an employee, a contractor or a visitor"))
    D.pred(InPred("is_con", "status", ["the person is a contractor"], ["the person is not a contractor"], fixed={"contractor"}))
    D.pred(InPred("is_vis", "status", ["the person is a visitor"], ["the person is not a visitor"], fixed={"visitor"}))
    D.fact(NumFact("contract", ["{n}'s contract runs for another {vu}."], zero=["{n}'s contract ends today."], negt=["{n}'s contract ended {au} ago."],
                   lo=-10, extra=(-5, 20, 60), req=("is_con", True), q="when {n}'s contract ends"))
    D.pred(NumPred("cont_ok", "contract", "ge", [0], ["the contractor's contract has not yet ended (its last day still counts)"],
                   ["the contractor's contract has already ended"], guard=("is_con", True)))
    D.fact(NumFact("training", ["{n} last completed the annual security training {vu} ago."], lo=1, q="when {n} last completed the security training"))
    D.pred(NumPred("trained", "training", "le", [90, 180, 365], ["the person last completed the security training no more than {tu} ago"],
                   ["the person last completed the security training more than {tu} ago"]))
    D.B("alarm", ["a fire alarm or other declared emergency is in progress"], ["no fire alarm or declared emergency is in progress"],
        ["A fire alarm was sounding in the building at the time."], ["No alarm or emergency was in progress."], q="whether an alarm was sounding")
    D.B("responder", ["the person is a member of the emergency response team"], ["the person is not a member of the emergency response team"],
        ["{n} is on the site emergency response team."], ["{n} is not on the emergency response team."], q="whether {n} is on the emergency response team")
    D.B("suspended", ["the person's badge has been suspended"], ["the person's badge has not been suspended"],
        ["{n}'s badge was suspended yesterday pending an investigation."], ["{n}'s badge is in good standing."], q="whether {n}'s badge is in good standing")
    D.B("induction", ["the person has completed the lab safety induction"], ["the person has not completed the lab safety induction"],
        ["{n} completed the lab safety induction last year."], ["{n} has never done the lab safety induction."], q="whether {n} has done the lab safety induction")
    D.fact(CatFact("day", {d: [d] for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
                   ["It was a {v}."], q="what day of the week it was"))
    D.pred(InPred("weekend", "day", ["the entry is on a Saturday or Sunday"], ["the entry is on a weekday (Monday to Friday)"],
                  fixed={"Saturday", "Sunday"}, tags=("temporal",)))
    D.prereq = ["clr+", "trained+", "hours+"]
    D.grounds = [("suspended+", ["deny access and alert security", "deny access"]), ("hours-", ["deny access", "grant access with an escort only"]),
                 ("clr-", ["deny access", "grant access with an escort only"]), ("is_vis+ & escort-", ["deny access"]),
                 ("is_con+ & cont_ok-", ["deny access and alert security", "deny access"]),
                 ("trained-", ["deny access", "grant access with an escort only"]), ("weekend+", ["deny access", "grant access with an escort only"]),
                 ("induction-", ["deny access"])]
    D.ovr_yes = [("alarm+ & responder+", ["grant access"])]
    D.ovr_no = [("suspended+", ["deny access and alert security"])]
    D.exc = {"clr-": ["escort+"], "hours-": ["responder+", "escort+"], "weekend+": ["responder+", "escort+"], "trained-": ["escort+"],
             "escort+": ["is_vis+"], "responder+": ["suspended+"], "alarm+ & responder+": ["suspended+"], "induction-": ["escort+"],
             "is_vis+ & escort-": ["alarm+"], "suspended+": ["alarm+"]}
    D.terms = [dict(id="T_auth", name="authorised person", pool=["clr+", "trained+", "suspended-"], modes=["all"], role="prereq",
                    defs=['A person is an "{name}" for an area if {cond}.'], pos=['the person is an "{name}" for that area'],
                    neg=['the person is not an "{name}" for that area']),
               dict(id="T_ooh", name="out-of-hours entry", pool=["hours-", "weekend+"], modes=["any"], role="ground",
                    defs=['An entry is an "{name}" if {cond}.'], pos=['the entry is an "{name}"'], neg=['the entry is not an "{name}"'])]
    D.noise = ["Badges must be worn where they can be seen.", "Lost badges must be reported to security at once."]
    D.sources = ("the badge system", "the guard's logbook")
    return D


# ======================================================================================================== content
def content():
    D = Domain("content")
    D.orgs = ["Chatterbox", "Pinboard Social", "LocalLoop", "StreamSquare", "Threadly", "Neighbourly Forum"]
    D.titles = ["{org} Community Rules: What Stays Up", "{org} Moderation Guidelines, Part {num}", "{org} - Content Policy for Posts"]
    D.intro = ["{n} published a post on {org}, and it has been flagged for review.", "A moderator at {org} is reviewing a post by {n}."]
    D.req, D.req_pl, D.subj, D.subj_pl = "post", "posts", "a post", "posts"
    D.wr = "{n}'s post"
    D.appr = dict(pas="allowed to stay up", noun="leaving the post up", clause=["the post stays up", "the post is left up"])
    D.deny = dict(pas="removed", noun="removal", clause=["the post is removed", "moderators remove the post"])
    D.q_appr = ["Under these rules, may {n}'s post stay up?", "Is {n}'s post allowed to stay up under the policy?"]
    D.q_deny = ["Under these rules, must {n}'s post be removed?", "Does the policy require moderators to remove {n}'s post?"]
    D.codes = ["leave up", "leave up with a warning label", "restrict to adults", "remove"]
    D.code_clause = {"leave up": ["the post stays up", "the post is left up"],
                     "leave up with a warning label": ["the post stays up with a warning label", "the post is labelled but left up"],
                     "restrict to adults": ["the post is restricted to adult users"], "remove": ["the post is removed"]}
    D.code_def = {"leave up": "The rules, applied with their exceptions and precedence, leave the post visible with no label or restriction.",
                  "leave up with a warning label": "The post stays visible but must carry a warning label.",
                  "restrict to adults": "The post stays up but only adult users may see it.",
                  "remove": "The rules require the post to be taken down."}
    D.deny_code, D.best = "remove", "leave up"
    D.B("graphic", ["the post contains graphic images of violence or serious injury"], ["the post contains no graphic images of violence or serious injury"],
        ["The post includes a graphic photo of injuries from a car crash."], ["The post contains no graphic images."],
        q="whether the post contains graphic images", ev=("the post contains graphic injury images", "the post contains no graphic images"))
    D.fact(CatFact("acct", {"news": ["verified news outlet"], "individual": ["private individual"], "business": ["local business"],
                            "gov": ["government agency"]},
                   {"news": ["The account is a verified news account; it belongs to a local news outlet, and {n} runs it."],
                    "individual": ["The account is {n}'s personal account."],
                    "business": ["The account is a business account for a bakery that {n} runs."],
                    "gov": ["The account is an official government account, and {n} runs it."]}, q="who runs the account"))
    D.pred(InPred("is_news", "acct", ["the account is a verified news account"], ["the account is not a verified news account"],
                  fixed={"news"}))
    D.pred(InPred("is_biz", "acct", ["the account is a business account"], ["the account is not a business account"], fixed={"business"}))
    D.B("warned", ["the post carries a sensitive-content warning screen"], ["the post carries no sensitive-content warning screen"],
        ["{n} added a sensitive-content warning screen to the post."], ["The post has no content warning."], q="whether the post has a content warning")
    D.B("doxx", ["the post shares a private person's home address or phone number"], ["the post shares no private person's home address or phone number"],
        ["The post includes a neighbour's home address and phone number."], ["The post contains no one's personal contact details."],
        q="whether the post contains personal contact details")
    D.B("consent", ["the person whose details are shared has agreed to it"], ["the person whose details are shared has not agreed to it"],
        ["The neighbour had asked {n} to share the details for a lost-dog appeal."], ["The neighbour did not agree to the details being shared."],
        q="whether the neighbour agreed to the post", req=("doxx", True), guard=("doxx", True))
    D.fact(NumFact("links", ["The post contains {vu} to the same outside shopping site."], unit=("link", "links"), zero=["The post contains no links."],
                   one=["The post contains one link to an outside shopping site."], q="how many links the post contains"))
    D.pred(NumPred("spam", "links", "ge", [2, 3, 5], ["the post contains {t} or more links to the same outside website"],
                   ["the post contains fewer than {t} links to the same outside website"]))
    D.fact(NumFact("acctage", ["The account was created {vu} ago."], zero=["The account was created today."], q="how old the account is"))
    D.pred(NumPred("newacct", "acctage", "lt", [7, 14, 30], ["the account is less than {tu} old"], ["the account is at least {tu} old"]))
    D.B("nudity", ["the post contains nudity"], ["the post contains no nudity"], ["The image in the post shows a nude figure."],
        ["The post contains no nudity."], q="whether the post contains nudity")
    D.B("art", ["the nudity is in a painting, a sculpture, or medical or educational material"],
        ["the nudity is in none of the following: a painting, a sculpture, or medical or educational material"],
        ["The image is a photograph of a classical marble sculpture in a museum.", "The image is a diagram from a medical textbook."],
        ["The image is a personal photograph."], q="what kind of image it is", req=("nudity", True), guard=("nudity", True))
    D.B("ad", ["the post is a paid advertisement"], ["the post is not a paid advertisement"], ["The post is a paid advertisement."],
        ["The post is not a paid advertisement."], q="whether the post is a paid advertisement")
    D.B("gambling", ["the post promotes gambling"], ["the post does not promote gambling"], ["The post promotes an online casino."],
        ["The post has nothing to do with gambling."], q="whether the post promotes gambling")
    D.B("licensed", ["the gambling operator holds a licence for the country where the post is shown"],
        ["the gambling operator holds no licence for the country where the post is shown"],
        ["The casino holds a gambling licence for the country where the post is shown."], ["The casino has no licence for the country where the post is shown."],
        q="whether the casino is licensed", req=("gambling", True), guard=("gambling", True))
    D.fact(NumFact("reports", ["{vu} have reported the post."], unit=("user", "users"), zero=["No one has reported the post."],
                   one=["One user has reported the post."], q="how many users have reported the post"))
    D.pred(NumPred("reported", "reports", "ge", [5, 10, 25], ["the post has been reported by {t} or more users"],
                   ["the post has been reported by fewer than {t} users"]))
    D.fact(NumFact("strikes", ["{n}'s account has {vu} from the past 90 days."], unit=("strike", "strikes"), zero=["{n}'s account has no strikes."],
                   q="how many strikes the account has"))
    D.pred(NumPred("strikes", "strikes", "ge", [2, 3], ["the account has {t} or more strikes from the past 90 days"],
                   ["the account has fewer than {t} strikes from the past 90 days"]))
    D.B("satire", ["the post is clearly labelled as satire"], ["the post is not labelled as satire"], ["The post is clearly labelled as satire."],
        ["The post is not labelled as satire."], q="whether the post is labelled as satire")
    D.B("falsehealth", ["the post repeats a health claim that our fact-checkers have rated false"],
        ["the post repeats no health claim that our fact-checkers have rated false"],
        ["The post repeats a health claim that {org}'s fact-checkers have rated false."], ["The post makes no claim that the fact-checkers have rated false."],
        q="whether the post repeats a claim rated false")
    D.prereq = []
    D.grounds = [("graphic+", ["remove", "leave up with a warning label", "restrict to adults"]), ("doxx+", ["remove"]), ("spam+", ["remove"]),
                 ("spam+ & newacct+", ["remove"]), ("nudity+", ["restrict to adults", "remove"]), ("gambling+", ["remove", "restrict to adults"]),
                 ("falsehealth+", ["leave up with a warning label", "remove"]), ("ad+ & gambling+", ["remove"]),
                 ("reported+", ["leave up with a warning label"])]
    D.ovr_yes = [("satire+", ["leave up", "leave up with a warning label"])]
    D.ovr_no = [("strikes+", ["remove"])]
    D.exc = {"graphic+": ["is_news+", "warned+"], "doxx+": ["consent+"], "nudity+": ["art+"], "art+": ["ad+"], "gambling+": ["licensed+"],
             "licensed+": ["newacct+"], "falsehealth+": ["satire+"], "satire+": ["falsehealth+"], "warned+": ["ad+"], "is_news+": ["strikes+"],
             "reported+": ["is_news+"], "spam+": ["is_biz+"], "is_biz+": ["newacct+"], "ad+ & gambling+": ["licensed+"]}
    D.terms = [dict(id="T_sens", name="sensitive media", pool=["graphic+", "nudity+"], modes=["any"], role="ground",
                    defs=['A post contains "{name}" if {cond}.'], pos=['the post contains "{name}"'], neg=['the post does not contain "{name}"']),
               dict(id="T_trust", name="trusted account", pool=["newacct-", "strikes-"], modes=["all"], role="exc", for_=["spam+", "reported+"],
                    defs=['An account is a "{name}" if {cond}.'], pos=['the account is a "{name}"'], neg=['the account is not a "{name}"'])]
    D.noise = ["Users can appeal any decision within 14 days.", "Moderators record the reason for every decision."]
    D.sources = ("the reporting user", "the moderator's review")
    return D


DOMAINS = [returns(), refunds(), insurance(), hr_leave(), school(), grants(), travel(), pharmacy(), access(), content()]
for _D in DOMAINS:
    for _a in ("codes", "code_clause", "code_def", "appr", "deny", "q_appr", "q_deny", "intro", "titles", "orgs", "wr"):
        assert hasattr(_D, _a), (_D.name, _a)
    _D.check()
