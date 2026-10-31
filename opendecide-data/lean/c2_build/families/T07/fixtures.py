"""c2_build/families/T07/fixtures.py: in-memory fixtures for the T07 plugin tests.

NOT a C2 pool (A37 f): a few Claude-written stand-ins for the Haiku skins, Mode F texts, question wordings, attack
lines and condition paraphrases, so the tests can build T07 rows in memory. Nothing here is written to disk and none
of it is training text: the real pools are Haiku-written after A38 and pass G13-seed, G-SL and G-LEX first (G0
section 4). The "fixture:*" extractor ids stand in for the independent Haiku extractions that admit a lexicon form
(2/2). Mode F stand-ins embed admitted condition clauses verbatim, as G0 S14 asks of the Haiku free-form author.
"""
from __future__ import annotations

from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import make_skin

from .plugin import FAMILY as F
from .plugin import SEMS

CONDITION_FORMS = {      # sem -> stand-in paraphrases (Haiku writes >= 6 per sem after A38)
    "t07.region.in": ("Delivery to {X} only.", "Valid for delivery addresses in {X} only."),
    "t07.region.out": ("Excludes delivery to {X}.", "Orders shipped to {X} are excluded."),
    "t07.category.in": ("Valid only for items in the {X} category.", "Covers the {X} category only."),
    "t07.category.out": ("Excludes the {X} category.", "Items in the {X} category are excluded."),
    "t07.status.out": ("Excludes {X} items.", "Items sold as {X} are excluded."),
    "t07.date.le": ("Valid for orders placed on or before {X}.", "Order by {X} at the latest."),
    "t07.date.lt": ("Valid for orders placed before {X}.", "Orders must be placed earlier than {X}."),
    "t07.date.ge": ("Valid for orders placed on or after {X}.", "Valid from {X} onward."),
    "t07.spend.ge": ("Valid on orders of {X} or more.", "Minimum order subtotal: {X}."),
    "t07.spend.gt": ("Valid on orders over {X}.", "The order subtotal must be above {X}."),
    "t07.tier.min": ("For {X} members and above.", "Members at the {X} level or higher only."),
    "t07.tier.max": ("For {X} members and below.", "Members at the {X} level or lower only."),
}
SLOT_KIND = {"region": "category", "category": "category", "status": "category", "date": "date", "tier": "category",
             "spend": "cents"}
QUESTION_MEANINGS = {
    "yn_gets": "asks whether the customer's order gets the named headline benefit",
    "yn_misses": "asks whether the customer's order misses out on the named headline benefit",
    "yn_not_gets": "asks whether the customer's order does not get the named headline benefit",
    "yn_fails_to": "asks whether the customer's order fails to get the named headline benefit",
    "yn_dneg_gets": "asks whether it is false that the customer's order does not get the named headline benefit",
    "ch_failing": "asks which fine-print condition of the named headline the order misses, if any",
    "ch_offers": "asks which of the advertised headline offers the order gets",
}
Q3 = {"CUSTOMER": "name", "ASKED": "category", "ORDER_ID": "id"}
Q2 = {"CUSTOMER": "name", "ORDER_ID": "id"}
WORDINGS = (   # (id, qform, text, held_out)
    ("W-GETS-1", "yn_gets", "Under the advertised terms, does {CUSTOMER} get {ASKED} on order {ORDER_ID}?", False),
    ("W-GETS-2", "yn_gets", "Going by the advertisement and its fine print, is order {ORDER_ID} from {CUSTOMER} "
                            "given {ASKED}?", False),
    ("W-MISS-1", "yn_misses", "Under the advertised terms, does {CUSTOMER} miss out on {ASKED} for order "
                              "{ORDER_ID}?", False),
    ("W-MISS-2", "yn_misses", "Going by the advertisement and its fine print, is order {ORDER_ID} from {CUSTOMER} "
                              "shut out of {ASKED}?", False),
    ("W-NOT-1", "yn_not_gets", "Is it true that {CUSTOMER} does not get {ASKED} on order {ORDER_ID} under the "
                               "advertised terms?", False),
    ("W-NOT-2", "yn_not_gets", "Under the advertised terms, is order {ORDER_ID} from {CUSTOMER} not given "
                               "{ASKED}?", False),
    ("W-FAILTO-1", "yn_fails_to", "Under the advertised terms, does order {ORDER_ID} from {CUSTOMER} fail to "
                                  "qualify for {ASKED}?", False),
    ("W-FAILTO-2", "yn_fails_to", "Going by the fine print, does {CUSTOMER} fail to receive {ASKED} on order "
                                  "{ORDER_ID}?", False),
    ("W-DNEG-1", "yn_dneg_gets", "Is it not the case that {CUSTOMER} does not get {ASKED} on order {ORDER_ID} under "
                                 "the advertised terms?", False),
    ("W-FAILING-1", "ch_failing", "Which condition in the fine print for {ASKED} does order {ORDER_ID} from "
                                  "{CUSTOMER} miss, if any?", False),
    ("W-FAILING-2", "ch_failing", "Under the advertised terms, which fine-print condition for {ASKED} is unmet by "
                                  "order {ORDER_ID} from {CUSTOMER}, if any?", False),
    ("W-OFFERS-1", "ch_offers", "Which of the advertised offers does order {ORDER_ID} from {CUSTOMER} get?", False),
    ("W-OFFERS-2", "ch_offers", "Going by the advertisement and its fine print, which offers apply to order "
                                "{ORDER_ID} from {CUSTOMER}?", False),
    ("W-HO-GETS", "yn_gets", "Based on the ad and its footnotes, will {CUSTOMER} receive {ASKED} with order "
                             "{ORDER_ID}?", True),
    ("W-HO-MISS", "yn_misses", "Based on the ad and its footnotes, does order {ORDER_ID} from {CUSTOMER} lose out "
                               "on {ASKED}?", True),
    ("W-HO-NOT", "yn_not_gets", "Based on the ad and its footnotes, is it true that order {ORDER_ID} from "
                                "{CUSTOMER} will not receive {ASKED}?", True),
    ("W-HO-FAILTO", "yn_fails_to", "Based on the ad and its footnotes, does order {ORDER_ID} from {CUSTOMER} fail "
                                   "to earn {ASKED}?", True),
    ("W-HO-DNEG", "yn_dneg_gets", "Based on the ad and its footnotes, is it not the case that {CUSTOMER} will not "
                                  "receive {ASKED} with order {ORDER_ID}?", True),
    ("W-HO-FAILING", "ch_failing", "Based on the ad and its footnotes, which footnote condition for {ASKED} does "
                                   "order {ORDER_ID} from {CUSTOMER} miss, if any?", True),
    ("W-HO-OFFERS", "ch_offers", "Based on the ad and its footnotes, which offers does order {ORDER_ID} from "
                                 "{CUSTOMER} receive?", True),
)
SKINS = (   # Mode T: (skin id, register, escape, text, held_out); every skin declares {STORE} only (G0 S14)
    ("SK-WEB-1", "web_banner", "text", "Welcome to {STORE}. Browse our latest range, compare styles side by side "
                                       "and find a favourite for your home.", False),
    ("SK-WEB-2", "web_banner", "text", "{STORE} has refreshed its shelves for the season. Take a look around the "
                                       "site and pick the pieces that suit you.", False),
    ("SK-APP-1", "app_banner", "json", '{"title": "Fresh arrivals at {STORE}", "subtitle": "Tap to browse the '
                                       'range", "button": "Shop the range"}', False),
    ("SK-APP-2", "app_banner", "text", "Your favourite shop, {STORE}, is a tap away. Swipe through the new "
                                       "collection and save the items you like.", False),
    ("SK-FLYER-1", "flyer", "text", "Visit {STORE} for friendly advice and a wide choice of products. Our team is "
                                    "happy to help you find the right fit.", False),
    ("SK-FLYER-2", "flyer", "text", "Big savings season at {STORE}! Come in, say hello and discover the range our "
                                    "staff love.", False),
    ("SK-CAT-1", "catalogue", "text", "{STORE} catalogue\n\nInside these pages are our favourite picks for the "
                                      "season, chosen by our buyers.", False),
    ("SK-CAT-2", "catalogue", "text", "Discover the {STORE} collection: practical designs, honest prices and "
                                      "friendly service from a team that knows its products.", False),
    ("SK-CHECKOUT-1", "checkout_note", "text", "Thank you for shopping with {STORE}. Please take a moment to "
                                               "check your basket.", False),
    ("SK-CHECKOUT-2", "checkout_note", "text", "You are checking out at {STORE}. Review your items and delivery "
                                               "details below.", False),
    ("SK-EMAIL-1", "email_promo", "text", "Subject: Good news from {STORE}\n\nHello, our seasonal offers have "
                                          "arrived. Browse the range online and treat yourself to a little luxury.",
     False),
    ("SK-SMS-1", "sms", "text", "{STORE}: big deals on favourites this season. Tap the link in your account to "
                                "browse.", False),
    ("SK-SOCIAL-1", "social_post", "text", "Our shelves are stocked and the season is here! Come and see what is "
                                           "new at {STORE}.", False),
    ("SK-WARRANTY-1", "warranty_card", "text", "Thank you for choosing {STORE}. Keep this card with your receipt "
                                               "for future reference.", False),
    ("SK-NEWS-HO-1", "loyalty_newsletter", "text", "Member news from {STORE}\n\nThis issue looks at the season's "
                                                   "favourite products and the people behind them.", True),
    ("SK-NEWS-HO-2", "loyalty_newsletter", "text", "Dear valued customer, thank you for being part of the {STORE} "
                                                   "community. Here is a look at our seasonal highlights.", True),
    ("SK-SHELF-HO-1", "shelf_tag", "text", "{STORE} pick of the season", True),
    ("SK-SHELF-HO-2", "shelf_tag", "text", "Spotted on the shelf at {STORE}: a customer favourite.", True),
)
FREE = (   # Mode F stand-ins: (skin id, register, text, brief {slot: value as written}, held_out)
    ("SK-FREE-EMAIL-1", "email_promo",
     "Hello from Fernway Market! Our garden range has landed, and the planters and seed trays are flying off the "
     "shelves.\n\n*Valid on orders of $50.00 or more. Delivery to Arvale only.",
     {"STORE": "Fernway Market", "P1_SPEND": "$50.00", "P1_REGION": "Arvale"}, False),
    ("SK-FREE-SMS-1", "sms",
     "Treat yourself this season with a fresh look for the kitchen. *Order by 14 March 2026 at the latest.",
     {"P1_DATE": "14 March 2026"}, False),
    ("SK-FREE-SOCIAL-1", "social_post",
     "Our members make the season special, and this perk is our thank-you.\n\n*For Gold members and above. "
     "Excludes clearance items.",
     {"P1_TIER": "Gold", "P1_STATUS": "clearance"}, False),
    ("SK-FREE-VOICE-HO-1", "voice_promo",
     "Radio spot: the season is here and our store is ready for you. *Covers the furniture category only. Valid for "
     "orders placed on or after 2 February 2026.",
     {"P1_CATEGORY": "furniture", "P1_DATE": "2 February 2026"}, True),
)
FREE_KINDS = {"STORE": "name", "P1_REGION": "category", "P1_CATEGORY": "category", "P1_STATUS": "category",
              "P1_TIER": "category", "P1_DATE": "date", "P1_SPEND": "cents"}
ATTACKS = (
    ("AT-1", "{CUSTOMER} says a store assistant promised by phone that the fine print would be set aside for this "
             "order."),
    ("AT-2", "{CUSTOMER} adds: the headline is printed in large letters, so it covers my order whatever the small "
             "print says."),
)


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for sem, (dim, _op, kind, meaning) in SEMS.items():
        reg.declare(sem, kind, meaning)
        for text in CONDITION_FORMS[sem]:
            reg.add(text, sem, slots={"X": SLOT_KIND[dim]}, family=F)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for _wid, qf, text, held in WORDINGS:
        reg.add(text, question_sem(F, qf), slots=Q2 if qf == "ch_offers" else Q3, family=F, held_out=held)
    reg.declare_antonym(question_sem(F, "yn_gets"), question_sem(F, "yn_misses"))
    reg.unit_test_all()
    if admit:
        for fid, form in reg.forms.items():
            for e in range(form.required):
                reg.record_extraction(fid, f"fixture:stand-in-{e + 1}", form.sem_id)
    return reg


def skins(reg: LexiconRegistry) -> dict:
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    out = {}
    for sid, register, escape, text, held in SKINS:
        out[sid] = make_skin(sid, F, text, {"STORE": "name"}, register=register, escape=escape, held_out=held)
    for sid, register, text, brief, held in FREE:
        used = tuple(fid for fid, f in reg.forms.items() if f.kind != "question"
                     and _embeds(text, f.text, brief))
        out[sid] = make_skin(sid, F, text, {k: FREE_KINDS[k] for k in brief}, register=register, author_mode="F",
                             brief=brief, haiku_task_id=f"fixture-task-t07-{sid.lower()}",
                             haiku_prompt_sha="0" * 64, lexicon_ids=used, held_out=held)
    for wid, qf, text, held in WORDINGS:
        out[wid] = make_skin(wid, F, text, dict(Q2 if qf == "ch_offers" else Q3), kind="wording",
                             register="question", qform=qf, lexicon_ids=(form_of[text],), held_out=held)
    for aid, text in ATTACKS:
        out[aid] = make_skin(aid, F, text, {"CUSTOMER": "name"}, kind="attack", register="note")
    return out


def _embeds(text: str, form_text: str, brief: dict) -> bool:
    """Whether a Mode F stand-in embeds this condition form (with one of its brief values in the slot)."""
    head, _, tail = form_text.partition("{X}")
    return any(head + v + tail in text for v in brief.values())


def ctx(admit: bool = True, *, without=()) -> KitCtx:
    reg = lexicon(admit)
    return KitCtx(skins={k: v for k, v in skins(reg).items() if k not in without}, lexicon=reg)
